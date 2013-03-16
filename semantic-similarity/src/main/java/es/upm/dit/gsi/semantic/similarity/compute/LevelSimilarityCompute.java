package es.upm.dit.gsi.semantic.similarity.compute;

import java.util.Map;

import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.type.MatchingMode;

public class LevelSimilarityCompute implements SimilarityCompute {
	
	private Map<Object, Object> levels;
	private MatchingMode mode;
	private MatchingMode direction;
	private double deviation = 0;
	
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
	public double computeSimilarity(RDFNode query, RDFNode resource) {

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
		return similarity;
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
		
		return (1-distance*deviation);
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
	
	double simRelated(int query, int resource){
		
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

}
