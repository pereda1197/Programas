#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stddef.h>
#include <assert.h>
#include <poll.h>
#include <errno.h>
#include <time.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <netinet/in.h>

#include "library.h"
#include "global.h"

/*
 * SECTION 1: GLOBAL DATA
 * ----------------------
 * Add your own data fields below this
 *
 */
 char buffer[500];
 int windowsize;
 long timeout;
 int paquetesEnviados=1;
 // packet_t *paquete;
 int16_t numPkt;
 int16_t numTramaPkt;
 int16_t tipo;
 int16_t numAck;


 int16_t numeroTrama=0;
 int timer=0;
 //si es 0 es que esta libre y si es 1 ocupada
 int trama0=0;
 int trama1=0;

/*
 * SECTION 2: CALLBACK FUNCTIONS
 * -----------------------------
 * The following functions are called on the corresponding event
 *
 */


/*
 * Creates a new connection. You should declare any variable needed in the upper section, DO NOT DECLARE
 * ANY VARIABLES HERE. This function should only make initializations as required.
 *
 * You should save the input parameters in some persistant global variable (defined in Section 1) so it can be
 * accessed later
 */
void connection_initialization(int _windowSize, long timeout_in_ns) {
  if(!_windowSize){
    windowsize=1;
  }else{
    windowsize=_windowSize;
  }

  if(!timeout_in_ns){
    timeout=10000000;
  } else{
    timeout=timeout_in_ns;
  }
}

/* This callback is called when a packet pkt of size n is received*/
void receive_callback(packet_t *pkt, size_t n) {

  printf("Comienzo a recibir\n");
  tipo=pkt->type;

  if(tipo==DATA){
    timer=0;
    SET_TIMER(timer,timeout);
    if(VALIDATE_CHECKSUM(pkt)==0){
      printf("El paquete es corrupto\n");
      sleep(timeout);
    }
    printf("Llega Data\n");
    char *data = (char *) malloc (n*sizeof(char));
    data=pkt->data;
    numPkt=pkt->seqno;
    numTramaPkt=pkt->ackno;

    if(numTramaPkt==0){
      trama0=1;
    }else{
      trama1=1;
    }

    int recibidoPkt=ACCEPT_DATA(data,n-10);

    if(recibidoPkt==-1){
      printf("Ha ocurrido un error\n");
      sleep(timeout);
    }else{
      printf("Recibo trama: %d\n",numTramaPkt);
      // printf("Datos: %s\n",data);
      printf("Envio ack\n");
      CLEAR_TIMER(timer);
      SEND_ACK_PACKET(numTramaPkt);
    }
  }else{
    timer=1;
    SET_TIMER(timer,timeout);
    if(VALIDATE_CHECKSUM(pkt)==0){
      printf("El paquete es corrupto\n");
      sleep(timeout);
    }
    printf("Llega ACK\n");
    numAck=pkt->ackno;
    if(numAck==0){
      printf("Trama 0 libre\n");
      trama0=0;
      CLEAR_TIMER(timer);
      RESUME_TRANSMISSION();
    }else if(numAck==1){
      printf("Trama 1 libre\n");
      trama1=0;
      CLEAR_TIMER(timer);
      RESUME_TRANSMISSION();
    }else{
      printf("Error con el ack\n");
    }

  }

  printf("\n");

}

/* Callback called when the application wants to send data to the other end*/
void send_callback() {

  uint16_t bufferlen=READ_DATA_FROM_APP_LAYER(buffer,500);
  if(bufferlen<=0){
    printf("No hay datos\n");
  }
  printf("Envio datos\n");
  printf("Trama: %d\n",numeroTrama);
  if((numeroTrama==0 && trama0==1) || (numeroTrama==1 && trama1==1)){
    printf("Error, esta trama esta ocupada\n");
    exit(0);
  }
  // printf("Datos enviados: %s\n",buffer);
  SEND_DATA_PACKET(DATA,bufferlen+10,numeroTrama,paquetesEnviados,buffer);

  memset(buffer,0,sizeof(buffer));
  printf("Pauso hasta recibir ack\n");

  PAUSE_TRANSMISSION();

  paquetesEnviados++;

  if(numeroTrama==0){
    numeroTrama=1;
  }else{
    numeroTrama=0;
  }

  printf("\n");
}

/*
 * This function gets called when timer with index "timerNumber" expires.
 * The function of this timer depends on the protocol programmer
 */
void timer_callback(int timerNumber) {
  printf("El tiempo del timer %d ha acabado\n",timerNumber);
  if(timerNumber==0){
    printf("Ha fallado el data,reenvialo\n");
    send_callback();
  }else{
    printf("Ha fallado el ack\n");
    SEND_ACK_PACKET(numTramaPkt);
  }
}
