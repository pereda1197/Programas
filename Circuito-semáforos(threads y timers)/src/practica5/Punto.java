package practica5;

/**
 * Clase que representa un punto del trazado de un circuito
 * @author (J. Javier Gutierrez) 
 * @version (Septiembre 2018)
 */

import fundamentos.*;

public class Punto {
	// Coordenadas (x,y) del punto
	private int x, y; 
	private Semaphore mutex;
	
	/**
	 * Constructor
	 * @param x la coordenada x del punto
	 * @param y la coordenada y del punto
	 */
	public Punto (int x, int y) {
		this.x=x;
		this.y=y;
	}
	
	/**
	 * Devuelve la coordenada x del punto
	 * @return x
	 */
	public int x() {
		return x;
	}
	
	/**
	 * Devuelve la coordenada y del punto
	 * @return y
	 */
	public int y() {
		return y;
	}
	
    /**
     * Pinta el circuito en el objeto de la clase Dibujo que se pasa como parametro
     * No refresca el dibujo
     * 
     * @param  d es el objeto en el que se pinta
     */
    public void pinta(Dibujo d, ColorFig c) 
    {
    	synchronized(d) {
       d.ponColorLapiz(c);
	   d.ponGrosorLapiz(10);
       d.dibujaPunto(x,y);
    	}
    }

    /**
	 * Compara el punto actual con otro que se pasa como parámetro
     * @param  p es el punto con el que se compara
     * @return true si coinciden las dos coordenadas 
	 */
	public boolean equals(Punto p) {
		return p.x() == x && p.y() == y;
	}
	
	public void setSemaforo(Semaphore semaforo) {
		mutex=semaforo;
	}
	
	public Semaphore getSemaforo() {
		return mutex;
	}

}
