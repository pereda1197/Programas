package practica5;

/**
 * Clase que representa el trazado del circuito.
 * 
 * @author (J. Javier Gutierrez) 
 * @version (Septiembre 2018)
 */

import java.util.*;
import fundamentos.*;

public class Circuito
{
    // Lista de puntos del circuito
    private ArrayList<Punto> lista;
    

    /**
     * Constructor que genera el trazado de un circuito
     * @param x es la coordenada x de la esquina superior izquierda del circuito
     * @param y es la coordenada y de la esquina superior izquierda del circuito
     * @param nPasosX es el numero de puntos a generar en la dirección x
     * @param nPasosY es el numero de puntos a generar en la dirección y
     * @param lPaso es la longitud del paso entre puntos en pixeles
     */
    public Circuito(int x, int y, int nPasosX, int nPasosY, int lPaso)
    {
        lista=new ArrayList<Punto> ();

        for (int i=0; i<nPasosX;i++)
        {
            lista.add(new Punto(x+i*lPaso,y));    
        }
        for (int i=0; i<nPasosY;i++)
        {
            lista.add(new Punto(x+nPasosX*lPaso,y+i*lPaso));    
        }
        for (int i=0; i<nPasosX;i++)
        {
            lista.add(new Punto(x+(nPasosX-i)*lPaso,y+nPasosY*lPaso));    
        }
        for (int i=0; i<nPasosY;i++)
        {
            lista.add(new Punto(x,y+(nPasosY-i)*lPaso));    
        }
        
        
    }

     /**
     * Obtiene el punto de una posición concreta de la lista
     * 
     * @param  posicion es el índice de la lista correspondiente al punto a obtener
     * @return el punto indicado por posicion 
     */
    public Punto punto(int posicion) 
    {
        return lista.get(posicion);
    }

    /**
     * Obtiene la longitud del circuito en número de puntos
     * 
     * @return el número de puntos del circuito 
     */
    public int longitud() 
    {
        return lista.size();
    }
 
	/**
     * Pinta el circuito en el objeto de la clase Dibujo que se pasa como parametro
     * y en el color dado. No refresca el dibujo
     * 
     * @param  d es el objeto en el que se pinta
     * @param  c es el color con el que se pinta
     */
    public void pinta(Dibujo d, ColorFig c) 
    {
       d.ponColorLapiz(c);
	   d.ponGrosorLapiz(15);

       for (int i=0; i<lista.size();i++)
       {
           d.dibujaPunto(lista.get(i).x(),lista.get(i).y());
	   }
    }
	   
}

