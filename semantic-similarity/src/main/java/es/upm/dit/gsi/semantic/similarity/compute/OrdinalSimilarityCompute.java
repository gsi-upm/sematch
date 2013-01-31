package es.upm.dit.gsi.semantic.similarity.compute;

public class OrdinalSimilarityCompute {

	private double alpha;
	private double[] distribution;
	private int maxLevel;

	public int getMaxLevel() {
		return maxLevel;
	}

	public void setMaxLevel(int maxLevel) {
		this.maxLevel = maxLevel;
	}

	public double getAlpha() {
		return alpha;
	}

	public void setAlpha(double alpha) {
		this.alpha = alpha;
	}

	public double[] getDistribution() {
		return distribution;
	}

	public void setDistribution(double[] distribution) {
		this.distribution = distribution;
	}

	public double computeSemmf(int x, int y) {

		if (x < y) {
			return 1;
		} else {
			double sim = x * 1.0 - y * 1.0;
			sim = alpha * sim;
			return 1 - sim;
		}
	}

	public double computeLin(int x, int y) {

		double common = 0;
		double description = 0;
		
		if (x > y) {
			for (int i = y; i <= x; i++) {
				common = common + distribution[i - 1];
			}
		} else {
			for(int i = x; i <=y; i++){
				common = common + distribution[i - 1];
			}
		}
	
		if (common == 1.0)
			return 0;
		else {
			common = 2 * Math.log(common);

			description = description + Math.log(distribution[x - 1]);
			description = description + Math.log(distribution[y - 1]);

			return common / description;
		}
	}
	
	public double computeGSI(int x, int y){
		
		double sim = y*1.0;
		sim = sim/(x*1.0);
		double normalise = 1.0/getMaxLevel();
		return sim*normalise;
		
	}
	
	public double computeSigmoid(int x, int y){
		
		int distance = x-y;
		double sim = distance*(1.0);
		sim = Math.exp(sim);
		sim = 1 + sim;
		return 1/sim;
		
	}

}
