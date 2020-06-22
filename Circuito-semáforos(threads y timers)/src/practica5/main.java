package practica5;

public class main {
	public static void main(String[] args) {
		
		//dibujo sobre el que pintamos los circuitos y los vehiculos
	    Dibujo maqueta=new Dibujo("Ejemplo de simulacion de movimiento",800,600);
	    
	    //creo circuitos
	    Circuito c1=new Circuito(300,350,12,7,15);
	    Circuito c2=new Circuito(240,350,20,10,15);
	    Circuito c3=new Circuito(327,230,8,8,15);
	    Circuito c4=new Circuito(270,200,16,10,15);
	    
	    //pinto circuitos
	    c1.pinta(maqueta,ColorFig.azul);
	    c2.pinta(maqueta,ColorFig.azul);
	    c3.pinta(maqueta,ColorFig.azul);
	    c4.pinta(maqueta,ColorFig.azul);
	    
	    //vehiculos practica 1
	    Vehiculo v1=new Vehiculo(c1, "horario",30,450,ColorFig.rosa,ColorFig.azul,maqueta);
	    Vehiculo v2=new Vehiculo(c2, "antihorario",0,900,ColorFig.verde,ColorFig.azul,maqueta);
	    Vehiculo v3=new Vehiculo(c3, "horario",0,1800,ColorFig.blanco,ColorFig.azul,maqueta);
	    Vehiculo v4=new Vehiculo(c4, "antihorario",0,2700,ColorFig.amarillo,ColorFig.azul,maqueta);
	    
	    //vehiculos practica 2
	    Vehiculo v5=new Vehiculo(c1, "antihorario",30,330,ColorFig.grisClaro,ColorFig.azul,maqueta);
	    Vehiculo v6=new Vehiculo(c2, "horario",0,1120,ColorFig.negro,ColorFig.azul,maqueta);
	    Vehiculo v7=new Vehiculo(c3, "antihorario",0,1970,ColorFig.magenta,ColorFig.azul,maqueta);
	    Vehiculo v8=new Vehiculo(c4, "horario",0,3830,ColorFig.naranja,ColorFig.azul,maqueta);
	    
	    //thread para pintar dibujo
	    dibujoPinta dib=new dibujoPinta(maqueta,10);
	    dib.setPriority(10);
	    
	    dib.start();
	    
//	    //semaforos
	    Semaphore semaforo1=new Semaphore(1);
	    Semaphore semaforo2=new Semaphore(2);
	    Semaphore semaforo3=new Semaphore(3);
	    
	    //Circuito 1: abajo pequeño
	    //Circuito 2: abajo grande
	    //Circuito 3: arriba pequeño
	    //Circuito 4: arriba grande
	    
	    c1.punto(0).setSemaforo(semaforo2);
	    c1.punto(12).setSemaforo(semaforo2);
	    c1.punto(2).setSemaforo(semaforo3);
	    c1.punto(10).setSemaforo(semaforo3);
	    
	    c2.punto(2).setSemaforo(semaforo1);
	    c2.punto(18).setSemaforo(semaforo1);
	    c2.punto(4).setSemaforo(semaforo2);
	    c2.punto(16).setSemaforo(semaforo2);
	    c2.punto(6).setSemaforo(semaforo3);
	    c2.punto(14).setSemaforo(semaforo3);
	    
	    c3.punto(16).setSemaforo(semaforo3);
	    c3.punto(24).setSemaforo(semaforo3);
	    
	    c4.punto(26).setSemaforo(semaforo1);
	    c4.punto(42).setSemaforo(semaforo1);
	    c4.punto(28).setSemaforo(semaforo2);
	    c4.punto(40).setSemaforo(semaforo2);
	    c4.punto(38).setSemaforo(semaforo3);
	    c4.punto(30).setSemaforo(semaforo3);
	    
//	    c4.punto(30).pinta(maqueta,ColorFig.negro);
	    
	    //comienzo los threads de los vehiculos
        v1.start();
        v2.start();
        v3.start();
        v4.start();
        v5.start();
        v6.start();
        v7.start();
        v8.start();
        
	}
}
