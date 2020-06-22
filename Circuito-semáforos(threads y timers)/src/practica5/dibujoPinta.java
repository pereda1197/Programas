package practica5;
import practica5.Dibujo;

public class dibujoPinta extends Thread{

	Dibujo dib;
	int tiempo;
	public dibujoPinta(Dibujo dib, int tiempo) {
		this.dib=dib;
		this.tiempo=tiempo;
	}
	
	public void run() {
		while(true)
	    {
	        try {
	            Thread.sleep(tiempo);
	        } catch (InterruptedException e) {}
	        dib.pinta();
	    }
	}
}
