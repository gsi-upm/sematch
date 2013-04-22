package es.upm.dit.gsi.semantic.similarity.compute;

import java.util.Map;

import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.type.MatchingMode;

public class LevelSimCompute implements SimCompute {
	
	private Map<Object, Object> levels;
	private MatchingMode mode;
	private MatchingMode direction;
	private boolean norm = true;

	private double deviation = 0;
	
	public boolean isNorm() {
		return norm;
	}

	public void setNorm(boolean norm) {
		this.norm = norm;
	}
	
	public MatchingMode getDirection() {
		return direction;
	}

	public void setDirection(MatchingMode direction) {
		this.direction = direction;
	}

	public MatchingMode getMode() {
		return mode;
	}

	public void setMode(MatchingMode mode) {
		this.mode = mode;
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

	@Override
	public double compute(RDFNode query, RDFNode resource) {

		double similarity = 0;

		String queryLevel = query.toString();
		String resourceLevel = resource.toString();

		queryLevel = Taxonomy.parseURI(queryLevel);
		resourceLevel = Taxonomy.parseURI(resourceLevel);

		int queryValue = Integer.valueOf((String)levels.get(queryLevel));
		int resourceValue = Integer.valueOf((String)levels.get(resourceLevel));

		similarity = computeSimilarity(queryValue,resourceValue);
		
		return similarity;
	}
	
	public double computeSimilarity(int query,int resource){
		double similarity = 0;
		switch(mode){
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
	
	public double norm(double v){
		if(isNorm()){
			double nv = v+1.0;
			return Math.log(nv)/Math.log(2);
		}else
			return v;
		
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
