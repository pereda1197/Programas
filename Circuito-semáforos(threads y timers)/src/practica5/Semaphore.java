package practica5;
import java.util.*;

public class Semaphore {
	protected int value;
	
	public Semaphore(int initial) {
		value = initial;
	}

	public synchronized void acquire() throws InterruptedException {
		while (value == 0)
			wait();
		value--;
	}

	public synchronized void release() {
		value++;
		notify();
	}

}
