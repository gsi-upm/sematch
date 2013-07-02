package es.upm.dit.gsi.semantic.similarity.compute;

import java.util.Map;

public class LevelSimCompute implements SimCompute {
	
	public enum MatchingMode {
		Exact,Close,Broad,Narrow,Related
	}
	
	private Map<Object, Object> levels;
	private boolean mapingLevel = true;
	private MatchingMode matchModel;
	private MatchingMode direction;
	private double deviation = 0;
	private double log2 = Math.log(2);
	
	@Override
	public double compute(String query, String resource) {

		double similarity = 0;
		
		int queryLevel;
		int resourceLevel;
		
		if(isMapingLevel()){
			queryLevel = Integer.valueOf((String)levels.get(query));
			resourceLevel = Integer.valueOf((String)levels.get(resource));
		}else{
			queryLevel = Integer.valueOf(query);
			resourceLevel = Integer.valueOf(resource);
		}

		similarity = computeSimilarity(queryLevel,resourceLevel);
		return norm(similarity);
	}
	
	public double computeSimilarity(int query,int resource){
		double similarity = 0;
		switch(matchModel){
		case Exact:
			similarity = simExact(query,resource);
			break;
		case Close:
			similarity = simClose(query,resource);
			break;
		case Broad:
			similarity = simBroad(query,resource);
			break;
		case Narrow:
			similarity = simNarrow(query,resource);
			break;
		case Related:
			similarity = simRelated(query,resource);
			break;
		}
		return norm(similarity);
	}
	
	double simExact(int query,int resource){
		if(query == resource)
			return 1;
		else return 0;
		
	}
	
	double simClose(int query,int resource){
		
		int distance = 0;
		if(query >= resource)
			distance = query - resource;
		else
			distance = resource - query;
		
		return 1-distance*deviation;
	}
	
	double simBroad(int query, int resource){
	
		if(query <= resource)
			return 1;
		else{
			int distance = query - resource;
			return 1-distance*deviation;
		}
	}
	
	double simNarrow(int query, int resource){
		
		if(query >= resource)
			return 1;
		else{
			int distance = resource - query;
			return 1-distance*deviation;
		}
		
	}
	
	/*double simRelated(int query, int resource){
		
		int distance = 0;
		double similarity = 0;
		switch(direction){
		case Broad:
			if(query>=resource){
				distance = query - resource;
				similarity = 1 - deviation*distance;
			}
			else{
				distance = resource - query;
				similarity = 1 + deviation*distance;
			}
			break;
		case Narrow:
			if(query>=resource){
				distance = query - resource;
				similarity = 1 + deviation*distance;
			}
			else{
				distance = resource - query;
				similarity = 1 - deviation*distance;
			}
			break;
		}
		
		return 0.5*similarity;
	}
	*/
	
	//TODO:add the direction check.
	public double simRelated(int query, int resource){
		return sigmoid(query,resource);
	}
	
	public double sigmoid(int query, int resource){
		
		double sim = deviation * (query - resource);
		sim = Math.exp(sim)+1;
		return 1/sim;
	}
	

	public double simSemmf(int queryLevel, int resourceLevel, int maxDepth) {
		
		double query = queryLevel*1.0;
		double resource = resourceLevel*1.0;
		double distance = 0;
		double similarity = 0;
		
		query = query/maxDepth;
		resource = resource/maxDepth;
		
		query = 1-query;
		resource = 1-resource;
		
		if(queryLevel > resourceLevel){
			distance = resource - query;
			similarity = 1- distance;
		}else{
			similarity = 1.0;
		}	
		return similarity;
	}
	
	public double norm(double v) {
		double nv = v + 1.0;
		return Math.log(nv) / log2;
	}
	
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
	
	public double computeSigmoid(int x, int y){
		
		int distance = x-y;
		double sim = distance*(1.0);
		sim = Math.exp(sim);
		sim = 1 + sim;
		return 1/sim;
		
	}
	
	public boolean isMapingLevel() {
		return mapingLevel;
	}

	public void setMapingLevel(boolean mapingLevel) {
		this.mapingLevel = mapingLevel;
	}

	public MatchingMode getDirection() {
		return direction;
	}

	public void setDirection(MatchingMode direction) {
		this.direction = direction;
	}

	public MatchingMode getMatchModel() {
		return matchModel;
	}

	public void setMatchModel(MatchingMode model) {
		this.matchModel = model;
	}

	public double getDeviation() {
		return deviation;
	}

	public void setDeviation(double deviation) {
		this.deviation = deviation;
	}
	
	public Map<Object, Object> getLevels() {
		return levels;
	}

	public void setLevels(Map<Object, Object> levels) {
		this.levels = levels;
	}

}
