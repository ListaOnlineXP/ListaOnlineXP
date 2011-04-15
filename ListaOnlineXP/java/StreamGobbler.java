import java.io.*;

public class StreamGobbler implements Runnable {
	String name;
	InputStream is;
	Thread thread;
	StringBuilder buffer = new StringBuilder();

	public StreamGobbler(String name, InputStream is) {
		this.name = name;
		this.is = is;
	}

	public void start() {
		thread = new Thread(this);
		thread.start();
	}
	
	public void interrupt() {
		thread.interrupt();
	}

	public void run() {
		try {
			InputStreamReader isr = new InputStreamReader(is);
			BufferedReader br = new BufferedReader(isr);

			while (true) {
				String s = br.readLine();
				if (s == null)
					break;
				//System.out.println("[" + name + "] " + s);
				buffer.append(s + "\n");
			}

			is.close();

		} catch (Exception ex) {
			System.out.println("Problem reading stream " + name + "... :" + ex);
			ex.printStackTrace();
		}
	}

	public String getText() {
		return this.buffer.toString();
	}
}
