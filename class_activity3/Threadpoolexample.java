import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Threadpoolexample {
    public static void main(String[] args) {
        int num = Integer.parseInt(args[0]);

        ExecutorService pool = Executors.newCachedThreadPool();

        for (int i = 0; i < num; i++) {
            pool.execute(new SimpleTask());
        }

        pool.shutdown();
    }
}
