package practica5;

import java.util.*;

import practica5.ColorFig;
import practica5.Dibujo;

public class Vehiculo extends Thread{

	
	private Circuito c;
	private String sentido;
	private int posicion;
	private int velocidad;
	private ColorFig vehiculo;
	private ColorFig circuito;
	private Dibujo dib;
	
	private LinkedList <Semaphore> listaDeSemaforos = new LinkedList<Semaphore>();
	
	public Vehiculo (Circuito c, String sentido, int posicion, int velocidad, ColorFig vehiculo, ColorFig circuito, Dibujo dib) {
		this.c=c;
		this.sentido=sentido;
		this.posicion=posicion;
		this.velocidad=velocidad;
		this.vehiculo=vehiculo;
		this.circuito=circuito;
		this.dib=dib;
	}
	
	public int velocidad() {
		return velocidad;
	}
	
	public void avanza() {
		c.punto(posicion).pinta(dib,circuito);
		
		if(sentido.equals("horario")) {
			int aux1=posicion+1;
			if(aux1 >= c.longitud()) {
				posicion=0;
			}else {
				posicion++;
			}
			c.punto(posicion).pinta(dib,vehiculo);
		}else if(sentido.equals("antihorario")){
			
			int aux2=posicion-1;
			if(aux2 < 0) {
				posicion=c.longitud()-1;
			}else {
				posicion--;
			}
			c.punto(posicion).pinta(dib,vehiculo);
		}
		
	}
	
	public int siguientePosicion() {
		int siguientePosicion;
		if (sentido.equals("horario")) {
			if (c.longitud() <= posicion + 1) {
				siguientePosicion=0;
			}else {
				siguientePosicion= posicion + 1;
			}
		} else {
			if (posicion == 0) {
				siguientePosicion=c.longitud()-1;
			}else {
				siguientePosicion=posicion-1;
			}
		}
		return siguientePosicion;
	}
		
	public void avanzaSemaforo() throws InterruptedException {
		Semaphore semaforo=c.punto(siguientePosicion()).getSemaforo();
		if(semaforo!=null){
			if (listaDeSemaforos.contains(semaforo)){
				semaforo.release();
				listaDeSemaforos.remove(semaforo);
			} else {
				semaforo.acquire();
				listaDeSemaforos.add(semaforo);
			}
		}

		avanza();
	}
	
		
	public void run() {
	    while(true)
	    {
	        try {
	            Thread.sleep(velocidad);
	            avanzaSemaforo();
	        } catch (InterruptedException e) {}
	        
	    }
	}
}
