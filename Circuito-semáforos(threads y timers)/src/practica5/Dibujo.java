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

import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Polygon;
import java.io.File;
import java.util.LinkedList;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import java.awt.Image;
import java.awt.Color;

/**  Dibujo     por Michael Gonzalez y Mariano Benito. Version
     3.5. Octubre 2016. <p>


     Es una clase sencilla que ofrece facilidades para hacer dibujos: <p>
     - puntos <p>
     - rectas <p>
     - poligonos abiertos y cerrados <p>
     - circulos y elipses <p>
     - rectangulos <p>
     - arcos circulares <p>
     - texto <p>
     - imagenes <p>

     Interfaz:  <p>
     ********   <p>

     basica
     ------

     new  Dibujo(titulo)             Constructor con tama\no 640*480<p>
     new  Dibujo(titulo,ancho,alto)  Constructor con tama\no definible <p>
     espera()                        Hace el dibujo y espera a que se
                                     pulse aceptar <p>
     pinta()                         Hace el dibujo de manera inmediata,
                                     sin esperar <p>

     atributos del dibujo <p>
     -------------------- <p>
     <p>
     ponColorLapiz(color)    pone el color del lapiz con el que se pinta <p>
     ponGrosorLapiz(ancho)   pone el grosor del lapiz con el que se pinta <p>
     ponRelleno(color)       pone el color del relleno de figuras cerradas <p>
     ponLetra(tamano))       pone el tamano de la letra del texto dibujado <p>
     hazLienzoLimitado()     hace que el lienzo sea de tamano limitado;  
                             si se pinta fuera del lienzo se muestra un mensaje
                             de error; por defecto el lienzo es limitado <p>
     hazLienzoSinLimite()    hace que el lienzo no tenga limite de tamano; los
                             dibujos que esten fuera del lienzo se ignoran <p>
     <p>
     funciones de dibujar <p>
     -------------------- <p>
     Observar que las coordenadas X aumentan hacia la derecha <p>
     y que las coordenadas Y aumentan hacia abajo  en el dibujo <p>
     <p>
     borra() <p>
     borra(color) <p>
     dibujaTexto(texto,xOrigen,yOrigen) <p>
     dibujaPunto(x,y) <p>
     dibujaLinea(xOrigen,yOrigen,xDestino,yDestino) <p>
     dibujaLineas (x[],y[]); <p>
     dibujaRectangulo(x1,y1,x2,y2)  //(x1,y1): sup. izqda. (x2,y2):inf.dcha. <p>
     dibujaElipse(x1,y1,x2,y2)      //(x1,y1): sup. izqda. (x2,y2):inf.dcha. <p>
     dibujaArco(x1,y1,x2,y2,angulo1,angulo2); <p>
     dibujaPoligono(x[],y[]) <p>
     dibujaImagen(xOrigen,yOrigen,nombreFichero) <p>
     <p>
     Los metodos se han hecho sincronizados para poder utilizar los objetos
     de esta clase desde una aplicacion con multiples threads
     <p>
     @author Michael Gonzalez Harbour <mgh at unican dot es>
     @author Mariano Benito Hoz <mbenitohoz at gmail dot com>
     @version 3.4
*/

public class Dibujo extends JFrame implements ActionListener {

    private JButton BtAceptar, BtCerrar;
    private PanelDibujos pDibujo;
    private int ancho, alto;
    private Atributos atributosActuales = new Atributos();
    private LinkedList<Figura> figuras;
    private Graphics2D grafica; 
    private Image imagen;
    private boolean lienzoLimitado=true;

    private class PanelDibujos extends JPanel {

        @Override
        public void paint(Graphics g) {
            // super.paint(g);
            // pinta la imagen donde hemos hecho el dibujo
            g.drawImage(imagen,0,0,null);
        }
    }

    // Define los atributos del dibujo
    private class Atributos {

        ColorFig col = ColorFig.negro;
        ColorFig colRelleno = ColorFig.blanco;
        int grosorLapiz = 1;
        int fontSize = 12;

        Atributos copia() {
            Atributos atr = new Atributos();
            atr.col = col;
            atr.colRelleno = colRelleno;
            atr.grosorLapiz = grosorLapiz;
            atr.fontSize = fontSize;
            return atr;
        }
    }

    // Raiz de la jerarquia de figuras
    private abstract class Figura {

        Atributos atr;

        Figura() {
            this.atr = atributosActuales.copia();
        }

        abstract void dibuja(Graphics2D g);
    }

    // Figura que representa una linea
    private class Linea extends Figura {

        int x1, y1, x2, y2;

        Linea(int x1, int y1, int x2, int y2) {
            super();
            this.x1 = x1;
            this.x2 = x2;
            this.y1 = y1;
            this.y2 = y2;
        }

        @Override
            void dibuja(Graphics2D g) {
            g.setColor(atr.col.colorOf());
            g.setStroke(new BasicStroke(atr.grosorLapiz));
            g.drawLine(x1, y1, x2, y2);
        }
    }

    // Figura rectangular
    private class Rectangulo extends Figura {

        int x1, y1, x2, y2;

        Rectangulo(int x1, int y1, int x2, int y2) {
            super();
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
        }

        void dibuja(Graphics2D g) {
            // borde
            g.setColor(atr.col.colorOf());
            g.fillRect(x1, y1, x2 - x1, y2 - y1);
            // relleno
            g.setColor(atr.colRelleno.colorOf());
            g.fillRect(x1 + atr.grosorLapiz, y1 + atr.grosorLapiz,
                       x2 - x1 - 2 * atr.grosorLapiz, 
                       y2 - y1 - 2 * atr.grosorLapiz);
        }
    }

    // Figura elipsoidal
    private class Elipse extends Figura {

        int x1, y1, x2, y2;

        Elipse(int x1, int y1, int x2, int y2) {
            super();
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
        }

        void dibuja(Graphics2D g) {
            // borde
            g.setColor(atr.col.colorOf());
            g.fillOval(x1, y1, x2 - x1, y2 - y1);
            // relleno
            g.setColor(atr.colRelleno.colorOf());
            g.fillOval(x1 + atr.grosorLapiz, y1 + atr.grosorLapiz,
                       x2 - x1 - 2 * atr.grosorLapiz, 
                       y2 - y1 - 2 * atr.grosorLapiz);
        }
    }

    // Arco de elipse
    private class Arco extends Elipse {

        int angulo1, angulo2; // en grados

        Arco(int x1, int y1, int x2, int y2, int angulo1, int angulo2) {
            super(x1, y1, x2, y2);
            this.angulo1 = angulo1;
            this.angulo2 = angulo2;
        }

        @Override
            void dibuja(Graphics2D g) {
            // borde
            g.setColor(atr.col.colorOf());
            g.fillArc(x1, y1, x2 - x1, y2 - y1, angulo1, angulo2 - angulo1);
            // relleno
            g.setColor(atr.colRelleno.colorOf());
            g.fillArc(x1 + atr.grosorLapiz, y1 + atr.grosorLapiz,
                      x2 - x1 - 2 * atr.grosorLapiz, 
                      y2 - y1 - 2 * atr.grosorLapiz,
                      angulo1, angulo2 - angulo1);
        }
    }

    // Texto que se pinta en el dibujo
    private class Texto extends Figura {

        int x, y;
        String s;

        Texto(String s, int x, int y) {
            super();
            this.x = x;
            this.y = y;
            this.s = s;
        }

        void dibuja(Graphics2D g) {
            g.setFont(g.getFont().deriveFont(Font.PLAIN, atr.fontSize));
            g.setColor(atr.col.colorOf());
            g.drawString(s, x, y);
        }
    }

    // Poligono abierto formado por varias lineas
    private class Lineas extends Figura {

        int x[], y[];

        Lineas(int x[], int y[]) {
            super();
            this.x = new int[x.length];
            this.y = new int[x.length];
            for (int i = 0; i < x.length; i++) {
                this.x[i] = x[i];
                this.y[i] = y[i];
            }
        }

        void dibuja(Graphics2D g) {
            g.setColor(atr.col.colorOf());
            g.setStroke(new BasicStroke(atr.grosorLapiz));

            for (int n = 0; n < x.length - 1; n++) {
                g.drawLine(x[n], y[n], x[n + 1], y[n + 1]);
            }
        }
    }

    //Poligono cerrado
    private class Poligono extends Lineas {

        private Polygon pol;

        Poligono(int x[], int y[]) {
            super(x, y);
            pol=new Polygon(x,y,x.length);
        }
 
        @Override
            void dibuja(Graphics2D g) {
            // draw the background
            g.setColor(atr.colRelleno.colorOf());
            g.fill(pol);
            //draw the foreground
            g.setStroke(new BasicStroke(atr.grosorLapiz));
            g.setColor(atr.col.colorOf());
            g.draw(pol);
        }

    }

    // Punto sencillo
    private class Punto extends Figura {

        int x, y;

        Punto(int x, int y) {
            super();
            this.x = x;
            this.y = y;
        }

        void dibuja(Graphics2D g) {
            g.setColor(atr.col.colorOf());
            g.setStroke(new BasicStroke(atr.grosorLapiz));
            g.drawLine(x, y, x, y);
        }
    }

    // Imagen procedente de un archivo jpg, gif, o png
    private class Imagen extends Figura {

        int x, y;
        String filename;

        Imagen(int x, int y, String filename) {
            super();
            this.x = x;
            this.y = y;
            this.filename = filename;
            File f = new File(filename);
            if (!f.exists()) {
                msjError("Fichero de imagen " + filename + " no existe");
            }
        }

        void dibuja(Graphics2D g) {
            ImageIcon im = new ImageIcon(filename);
            g.drawImage(im.getImage(), x, y, null);
        }
    }

    /**
     * Constructor simple, que hace la ventana de tamano 640*480.
     * @param titulo Titulo que tendra la ventana.
     */
    public Dibujo(String titulo) {
        this(titulo, 640, 480);
    }

    /**
     * Constructor completo, que pone el titulo y tamano de la ventana.
     * @param titulo Titulo que tendra la ventana.
     * @param ancho Ancho del area de dibujo.
     * @param alto Alto del area de dibujo.
     */
    public Dibujo(String titulo, int ancho, int alto) {
        super(titulo);
        this.ancho = ancho;
        this.alto = alto;
        BtAceptar = new JButton("Aceptar");
        BtCerrar = new JButton("Cerrar aplicacion");
        figuras = new LinkedList<Figura>();
        pDibujo = new PanelDibujos();
        inicializa();
    }

    // Redibuja todas las figuras
    private void redraw() {
	for (Figura fig : figuras) {
	    fig.dibuja(grafica);
	}
	pDibujo.repaint();
    }

    // Finaliza la inicializacion del constructor
    private void inicializa() {
        // Ventana
        pDibujo.setPreferredSize(new Dimension(ancho, alto));

        JPanel inferior = new JPanel(new FlowLayout(
                                                    FlowLayout.CENTER, 2, 0));

        inferior.add(BtAceptar);
        inferior.add(BtCerrar);

        setLayout(new BorderLayout(5, 5));

        add(pDibujo, BorderLayout.CENTER);
        add(inferior, BorderLayout.SOUTH);

        pack();

        Dimension size= pDibujo.getSize();
        imagen = pDibujo.createImage(size.width, size.height);
        grafica= (Graphics2D)imagen.getGraphics();
        grafica.setColor(Color.white);
        grafica.fillRect(0, 0, size.width, size.height);

        // Manejadores
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        BtCerrar.addActionListener(new ActionListener() {

                public void actionPerformed(ActionEvent e) {
                    System.exit(0);
                }
            });
        BtAceptar.addActionListener(this);
    }

    /**
     *  Pone el grosor del lapiz con el que se pinta.
     */
    public synchronized void ponGrosorLapiz(int grosor) {
        atributosActuales.grosorLapiz = grosor;
    }

    /**
     *  Pone el color del lapiz con el que se pinta.
     */
    public synchronized void ponColorLapiz(ColorFig color) {
        atributosActuales.col = color;
    }

    /**
     *  Pone el tamano de la letra del texto dibujado.
     */
    public synchronized void ponLetra(int tamano) {
        atributosActuales.fontSize = tamano;
    }

    /**
     *  Pone el color del relleno de las figuras cerradas.
     */
    public synchronized void ponRelleno(ColorFig color) {
        atributosActuales.colRelleno = color;
    }
    
    
    /**
     * Hace que el lienzo sea de tamano limitado.
     * Si se pinta fuera del lienzo se muestra un mensaje de error.
     * Por defecto el lienzo es limitado.
     */
    public synchronized void  hazLienzoLimitado() {
        lienzoLimitado=true;     
    }
        
    
    /**
     *  Hace que el lienzo no tenga limite de tamano.
     *  Los dibujos que esten fuera del lienzo se ignoran.
     *  Por defecto el lienzo es limitado.
     */
    public synchronized void hazLienzoSinLimite() {
        lienzoLimitado=false;
    }
    

    /**
     *  Borra la imagen poniendola del color de fondo indicado.
     * @param color Color de fondo a establecer.
     */
    public synchronized void borra(ColorFig color) {
        figuras.clear();
        Atributos atr = atributosActuales.copia();
        atributosActuales.colRelleno = color;
        atributosActuales.col = color;
        figuras.add(new Rectangulo(0, 0, ancho, alto));
        atributosActuales.col = atr.col;
        atributosActuales.colRelleno = atr.colRelleno;
    }

    /**
     * Borra la imagen poniendola del color de fondo gris claro.
     */
    public void borra() {
        borra(ColorFig.gris.masClaro());
    }

    /**
     * Dibuja una linea desde el punto (x1,y1) hasta (x2,y2).
     * @param x1 Coordenada x inicial.
     * @param x2 Coordenada x final.
     * @param y1 Coordenada y inicial.
     * @param y2 Coordenada y final.
     */
    public synchronized void dibujaLinea(int x1, int y1, int x2, int y2) {
        if (lienzoLimitado && 
            (x1 < 0 || y1 < 0 || x2 > ancho || y2 > alto))
        {
            msjError("Las medidas de la linea exceden el area "
                     + "de dibujo. La linea no se ha pintado");
        } else {
            figuras.add(new Linea(x1, y1, x2, y2));
        }
    }

    /**
     * Dibuja un rectangulo cuya esquina superior izquierda es el
     * punto (x1,y1) y la esquina inferior derecha es (x2,y2).
     * @param x1 Coordenada x inicial.
     * @param x2 Coordenada x final.
     * @param y1 Coordenada y inicial.
     * @param y2 Coordenada y final.
     */
    public synchronized void dibujaRectangulo(int x1, int y1, int x2, int y2) {
        if (lienzoLimitado && 
            (x1 < 0 || y1 < 0 || x2 > ancho || y2 > alto)) 
        {
            msjError("Las medidas del rectangulo exceden el area "
                     + "de dibujo. El rectangulo no se ha pintado");
        } else {
            figuras.add(new Rectangulo(x1, y1, x2, y2));
        }
    }

    /**
     * Dibuja un ovalo contenido en el rectangulo
     * cuya esquina superior izquierda es el
     * punto (x1,y1) y la esquina inferior derecha es (x2,y2).
     * @param x1 Coordenada x inicial.
     * @param x2 Coordenada x final.
     * @param y1 Coordenada y inicial.
     * @param y2 Coordenada y final.
     */
    public synchronized void dibujaElipse(int x1, int y1, int x2, int y2) {
        if (lienzoLimitado && 
            (x1 < 0 || y1 < 0 || x2 > ancho || y2 > alto)) 
        {
            msjError("Las medidas de la elipse exceden el area "
                     + "de dibujo. La elipse no se ha pintado");
        } else {
            figuras.add(new Elipse(x1, y1, x2, y2));
        }
    }

    /**
     * Dibuja una parte (un arco) de un ovalo.
     * El ovalo completo es el contenido en el rectangulo
     * cuya esquina superior izquierda es el
     * punto (x1,y1) y la esquina inferior derecha es (x2,y2)
     * La parte que se dibuja es la comprendida entre angulo1 y angulo2
     * Los angulos van en grados. El angulo cero es la horizontal hacia
     * la derecha.
     * @param x1 Coordenada x inicial.
     * @param x2 Coordenada x final.
     * @param y1 Coordenada y inicial.
     * @param y2 Coordenada y final.
     */
    public synchronized void dibujaArco(int x1, int y1, int x2, int y2,
                           int angulo1, int angulo2) {
        if (lienzoLimitado && 
            (x1 < 0 || y1 < 0 || x2 > ancho || y2 > alto)) 
        {
            msjError("Las medidas del arco exceden el area "
                     + "de dibujo. El arco no se ha pintado");
        } else {
            figuras.add(new Arco(x1, y1, x2, y2, angulo1, angulo2));
        }
    }

    /**
     *  Dibuja el texto indicado a partir del punto (x,y).
     * @param s Texto a escribir.
     * @param x Coordenada x del inicio del texto.
     * @param y Coordenada y del inicio del texto.
     */
    public synchronized void dibujaTexto(String s, int x, int y) {
        if (lienzoLimitado && 
            (x < 0 || y < 0 || x > ancho || y > alto)) 
        {
            msjError("Las medidas del texto exceden el area "
                     + "de dibujo. El texto no se ha pintado");
        } else {
            figuras.add(new Texto(s, x, y));
        }
    }

    /**
     * Dibuja un  poligono abierto cuyas coordenadas x e y estan
     * en los respectivos arrays.
     * @param x Array de coordenadas x de las lineas.
     * @param y Array de coordenadas y de las lineas.
     */
    public synchronized void dibujaLineas(int x[], int y[]) {
        boolean error = false;
        if (x.length!=y.length) {
            msjError("Error: las coordenadas x e y del poligono"+
                     "no tienen el mismo tamano. El poligono no se ha pintado");
            error = true;
        }
        for (int i = 0; i < x.length; i++) {
            if (lienzoLimitado && 
                (x[i] < 0 || y[i] < 0 || x[i] > ancho || y[i] > alto)) 
            {
                msjError("Las medidas de las lineas exceden el area "
                         + "de dibujo. Las lineas no se han pintado.");
                error = true;
                break; // exit loop
            }
        }
        if (!error) {
            figuras.add(new Lineas(x, y));
        }
    }

    /**
     * Dibuja un  poligono cerrado cuyas coordenadas x e y estan
     * en los respectivos arrays.
     * @param x Array de coordenadas x de los puntos del poligono.
     * @param y Array de coordenadas y de los puntos del poligono.
     */
    public synchronized void dibujaPoligono(int x[], int y[]) {
        boolean error = false;
        if (x.length!=y.length) {
            msjError("Error: las coordenadas x e y del poligono"+
                     "no tienen el mismo tamano. El poligono no se a pintado");
            error = true;
        }
        for (int i = 0; i < x.length; i++) {
            if (lienzoLimitado && 
                (x[i] < 0 || y[i] < 0 || x[i] > ancho || y[i] > alto)) 
            {
                msjError("Las medidas del poligono exceden el area "
                         + "de dibujo. El poligono no se ha pintado.");
                error = true;
                break; // exit loop
            }
        }
        if (!error) {
            figuras.add(new Poligono(x, y));
        }
    }

    /**
     * Dibuja un  punto en la posicion (x,y).
     * @param x Coordenada x del punto.
     * @param y Coordenada y del punto.
     */
    public synchronized void dibujaPunto(int x, int y) {
        if (lienzoLimitado && 
            (x < 0 || x > ancho || y < 0 || y > alto)) 
        {
            msjError("La posicion del punto excede el area "
                     + "de dibujo. El punto no se ha pintado");
        } else {
            figuras.add(new Punto(x, y));
        }
    }

    /**
     * Dibuja la imagen contenida en el fichero cuyo nombre se indica,
     * dibujandola desde la posicion (x,y).
     * Si la imagen excede las dimensiones de la pantalla, se redimensiona.
     * @param filename Ruta del archivo.
     * @param x Coordenada x en la que se colocara la imagen.
     * @param y Coordenada y en la que se colocara la imagen.
     */
    public synchronized void dibujaImagen(int x, int y, String filename) {
        if (lienzoLimitado && 
            (x < 0 || x > ancho || y < 0 || y > alto)) 
        {
            msjError("La posicion de la imagen excede el area "
                     + "de dibujo. La imagen no se ha pintado");
        } else {
            figuras.add(new Imagen(x, y, filename));
        }
    }

    /**
     * Hace el dibujo y espera a que se pulse Aceptar
     */
    public synchronized void espera() {
        redraw();
        setVisible(true);
        try {
            wait();
        } catch (InterruptedException e) {
        }
    }

    /**
     * Hace el dibujo de manera inmediata, sin esperar
     */
    public synchronized void pinta() {
        redraw();
        setVisible(true);
    }

    /**
     * No usar este metodo interno.
     */
    public synchronized void actionPerformed(ActionEvent e) {
        notify();
        setVisible(false);
    }

    // Pone un mensaje de error en una ventana
    private void msjError(String mensaje) {
        JOptionPane.showMessageDialog(null, mensaje, "Error",
                                      JOptionPane.ERROR_MESSAGE);
    }
}
