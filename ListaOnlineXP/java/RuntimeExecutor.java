import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeoutException;

/**
* Execute command from the Runtime. This class will make sure the external
* application will not hung the application by specifying a timeout in which
* the application must return. If it does not an InterruptedException will be
* thrown
* 
* @author Aviran Mordo
* 
*/
public class RuntimeExecutor {
    private long timeout = Long.MAX_VALUE;
    private String stdOut = "";
    private String stdErr = "";

    public String getStdOut() {
        return stdOut;
    }

    public String getStdErr() {
        return stdErr;
    }

    /**
    * Default constructor - Timeout set to Long.MAX_VALUE
    */
public RuntimeExecutor() {
    // Do nothing
}

/**
* Constructor
* 
* @param timeout
*            Set the timeout for the external application to run
*/
public RuntimeExecutor(long timeout) {
    this.timeout = timeout;
}

/**
* Execute a Runtime process
* 
* @param command
*            - The command to execute
* @param env
*            - Environment variables to put in the Runtime process
* @return The output from the process
* @throws IOException
* @throws TimeoutException
*             - Process timed out and did not return in the specified
*             amount of time
*/
public String execute(String command, String[] env) throws Exception {
    Process p;

    System.setProperty("file.encoding", "utf-8"); 

    if (env == null) {
        p = Runtime.getRuntime().exec(command, env);
    } else {
        p = Runtime.getRuntime().exec(command);
    }
    StreamGobbler stdin = new StreamGobbler ("stdin", p.getInputStream());
    StreamGobbler stderr = new StreamGobbler ("stderr", p.getErrorStream());
    stdin.start();
    stderr.start();

    // Set a timer to interrupt the process if it does not return within the
    // timeout period
    Timer timer = new Timer();
    timer.schedule(new InterruptScheduler(Thread.currentThread()), this.timeout);

    try {
        p.waitFor();
    } catch (InterruptedException e) {
        // Stop the process from running
        p.destroy();
        Runtime.getRuntime().runFinalization();
        stdin.interrupt();
        stderr.interrupt();
        return "TIMEOUT_ERROR : O programa excedeu o tempo limite de execução ("+ this.timeout + " milisegundos)";
    } finally {
        // Stop the timer
        timer.cancel();
    }

    // Get the output from the external application
    /*
    StringBuilder buffer = new StringBuilder();
    BufferedReader stdInput = new BufferedReader(new 
    InputStreamReader(p.getInputStream()));
    String s = null;
    while ((s = stdInput.readLine()) != null) {
    buffer.append(s + "\n");
    }
    */
        stdOut = stdin.getText();
    stdErr = stderr.getText();

    if (!stdin.getText().equals("")) {
        return stdin.getText();
    } else {
        return stderr.getText();
    }

}

// ///////////////////////////////////////////
private class InterruptScheduler extends TimerTask {
    Thread target = null;

    public InterruptScheduler(Thread target) {
        this.target = target;
    }

    @Override
    public void run() {
        target.interrupt();
    }

}

public static void main(String[] args) {
    // Set timeout to 4 seconds
    RuntimeExecutor r = new RuntimeExecutor(4000);
    try {
        //String saida = r.execute(System.getenv("windir") +"\\system32\\"+"tree.com /A", null);
        String saida = r.execute("java -Dfile.encoding=utf-8 -Djava.security.manager Teste", null);
        //String saida = r.execute("rundll32 url.dll,FileProtocolHandler c:/00291294.pdf", null);
        //String saida = r.execute("cmd /c start excel.exe", null);

        System.out.println(saida);
    } catch (Exception e) {
        e.printStackTrace();
    }

    System.out.println("TIMEOUT_ERROR : STOPPED");
}
}


