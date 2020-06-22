///////////////////////////////////////////////////////////////////////
//                       Paquete fundamentos                         //
//  Conjunto de clases para hacer entrada/salida sencilla en Java    //
//                                                                   //
//                     Copyright (C) 2005-2016                       //
//                 Universidad de Cantabria, SPAIN                   //
//                                                                   //
// Authors: Michael Gonzalez   <mgh@unican.es>                       //
//          Mariano Benito Hoz <mbenitohoz at gmail dot com>         //
//                                                                   //
// This program is free software; you can redistribute it and/or     //
// modify it under the terms of the GNU General Public               //
// License as published by the Free Software Foundation; either      //
// version 3 of the License, or (at your option) any later version.  //
//                                                                   //
// This program is distributed in the hope that it will be useful,   //
// but WITHOUT ANY WARRANTY; without even the implied warranty of    //
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU //
// General Public License for more details.                          //
///////////////////////////////////////////////////////////////////////

 package practica5;

import java.awt.Color;

/**
 * ColorFig por Michael Gonzalez y Mariano Benito. 
 * Version 3.5. Octubre 2016. <p>
 * Clase que define algunos colores usados en la clase Dibujo <p>
 *
 * @author Mariano Benito Hoz <mbenitohoz at gmail dot com>
 * @version 3.4
 */
public class ColorFig {

    private Color col;

    // Constructor privado, que obtiene el color
    //   a partir de un objeto de la clase Color
    private ColorFig(Color col) {
        this.col = new Color(col.getRed(), col.getGreen(), col.getBlue());
    }

    // Retorna el color en un objeto de la clase Color
    Color colorOf() {
        return col;
    }

    /**
     * Contructor que crea un color a partir de una combinacion
     * de rojo (r) verde (g) y azul (b). Cada uno de estos datos
     * estara comprendido entre 0 y 255
     */
    public ColorFig(int r, int g, int b) {
        this.col = new Color(r, g, b);
    }

    /** 
     * Constantes estaticas para los colores mas habituales 
     */
    public static final ColorFig negro = new ColorFig(Color.black);
    public static final ColorFig azul = new ColorFig(Color.blue);
    public static final ColorFig grisOscuro = new ColorFig(Color.darkGray);
    public static final ColorFig gris = new ColorFig(Color.gray);
    public static final ColorFig verde = new ColorFig(Color.green);
    public static final ColorFig grisClaro = new ColorFig(Color.lightGray);
    public static final ColorFig magenta = new ColorFig(Color.magenta);
    public static final ColorFig naranja = new ColorFig(Color.orange);
    public static final ColorFig rosa = new ColorFig(Color.pink);
    public static final ColorFig rojo = new ColorFig(Color.red);
    public static final ColorFig blanco = new ColorFig(Color.white);
    public static final ColorFig amarillo = new ColorFig(Color.yellow);

    /**
     *  Retorna un color mas oscuro que el original
     */
    public ColorFig masOscuro() {
        return new ColorFig(col.darker());
    }

    /**
     * Retorna un color mas claro que el original
     */
    public ColorFig masClaro() {
        return new ColorFig(col.brighter());
    }

}
