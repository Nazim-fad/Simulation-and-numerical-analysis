import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {

    private final int trials;
    private final int n;
    private final double[] thresholds;
    private final double mean;
    private final double stddev;
    private static final double CONFIDENCE_PARAM = 1.96;




    // perform independent trials on an n-by-n grid
    public PercolationStats(int n, int trials) {
        if (n <= 0 || trials <= 0) {
            throw new IllegalArgumentException("n and trials must be > 0");
        }
        this.n = n;
        this.trials = trials;
        thresholds = new double[trials];
        for (int i = 0; i < trials ; i++) {
            Percolation percolation = new Percolation(n);
            while (!(percolation.percolates())) {
                int site = StdRandom.uniformInt(n * n);
                int col = (site % n) + 1;
                int row = (site / n) + 1;
                if (!percolation.isOpen(row, col)) {
                    percolation.open(row, col);
                }
            }
            thresholds[i] = (double) percolation.numberOfOpenSites() / (n*n);
        }
        this.mean = StdStats.mean(thresholds);
        this.stddev = StdStats.stddev(thresholds);
    }

    // sample mean of percolation threshold
    public double mean() {
        return mean;
    }

    // sample standard deviation of percolation threshold
    public double stddev() {
        return stddev;
    }

    // low endpoint of 95% confidence interval
    public double confidenceLo() {
        return mean - CONFIDENCE_PARAM * stddev/ Math.sqrt(trials);
    }

    // high endpoint of 95% confidence interval
    public double confidenceHi() {
        return mean + CONFIDENCE_PARAM * stddev / Math.sqrt(trials);
    }


    // test client (see below)
    public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);

        PercolationStats stats = new PercolationStats(n, trials);

        System.out.println("Mean                    = " + stats.mean());
        System.out.println("Standard Deviation      = " + stats.stddev());
        System.out.println("95% CI = [" + stats.confidenceLo() + ", " + stats.confidenceHi() + "]");
    }
}
