import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {

    private final WeightedQuickUnionUF uf;
    private final int n;
    // our data structure as a list of bool(open/blocked) N^2 - 1 + 2 last fake top and bottom to make answer to "percolate?" easier
    private final boolean[] grid;
    private int numberOfOpenSites;
    private final int top;
    private final int bottom;

    // creates n-by-n grid, with all sites initially blocked
    public Percolation(int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("n must be > 0");
        }
        this.n = n;
        top = n * n;
        bottom = n * n + 1;
        uf = new WeightedQuickUnionUF(n * n + 2);
        grid = new boolean[n*n];

    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) {
            throw new IllegalArgumentException("Check your col or/and row");
        } else {
            // we start from (1x1) but the list starts at 0
            int index = (row - 1) * n + (col - 1);
            if (!grid[index]) {
                grid[(row - 1) * n + (col - 1)] = true;
                numberOfOpenSites ++;
                // Connect to fake top if in the top row
                if (row == 1) {
                    uf.union(index, top);
                }

                // Connect to fake bottom if in the bottom row
                if (row == n ) {
                    uf.union(index, bottom);
                }
                // neighbors check
                if (col > 1 && isOpen(row, col-1)) {
                    uf.union(index, index - 1);
                }
                if (col < n  && isOpen(row, (col+1))) {
                    uf.union(index, index + 1);
                }
                if (row < n  && isOpen((row+1), col)) {
                    uf.union(index, index + n);
                }
                if (row > 1  && isOpen((row-1), col)) {
                    uf.union(index, index - n);
                }

            }
        }

    }

    // is the site (row, col) open?
    public boolean isOpen(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) {
            throw new IllegalArgumentException("Check your col or/and row");
        } else {
            int index = (row - 1) * n + (col - 1);
            return grid[index];
        }

    }


    // is the site (row, col) full?
    public boolean isFull(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) {
            throw new IllegalArgumentException("Check your col or/and row");
        } else {
            int index = (row - 1) * n + (col - 1);
            return isOpen(row, col) && uf.find(index) == uf.find(top);
        }

    }

    // returns the number of open sites
    public int numberOfOpenSites() {
        return numberOfOpenSites;
    }

    // does the system percolate?
    public boolean percolates() {
        return uf.find(top) == uf.find(bottom);

    }

    // test client (optional)
    public static void main(String[] args) {
        Percolation p = new Percolation(10);
        System.out.println("Successfully created a Percolation grid.");
        p.open(2,2);
        p.open(2,2);
        System.out.println("Is (3,1) open? " + p.isOpen(3,1));

        for(int row = 1; row <= 10; row++) {
            p.open(row, 3);
            System.out.println("Opened site (" + row + ", 3)");
        }

        System.out.println("Percolates: " + p.percolates());

        System.out.println("Is (5,3) full? " + p.isFull(5,3));
        System.out.println("Is (2,2) open? " + p.isOpen(2,2));
        System.out.println("Is (2,2) full? " + p.isFull(2,2));
        System.out.println("Is (1,1) open? " + p.isOpen(1,1));
        System.out.println("Is (1,1) full? " + p.isFull(1,1));
    }

}
