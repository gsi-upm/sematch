package es.upm.dit.gsi.semantic.similarity.compute;

import java.util.Map;

import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.type.LevelSimType;

public class LevelSimilarityCompute implements SimilarityCompute {
	
	private Map<Object, Object> levels;
	private boolean overmatch;
	private LevelSimType simType;

	public LevelSimType getSimType() {
		return simType;
	}

	public void setSimType(LevelSimType simType) {
		this.simType = simType;
	}

	public Map<Object, Object> getLevels() {
		return levels;
	}

	public void setLevels(Map<Object, Object> levels) {
		this.levels = levels;
	}

	public boolean isOvermatch() {
		return overmatch;
	}

	public void setOvermatch(boolean overmatch) {
		this.overmatch = overmatch;
	}

	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {

		double similarity = 0;

		String queryLevel = query.toString();
		String resourceLevel = resource.toString();

		queryLevel = Taxonomy.parseURI(queryLevel);
		resourceLevel = Taxonomy.parseURI(resourceLevel);

		int maxDepth = levels.size();
		int queryValue = Integer.valueOf((String)levels.get(queryLevel));
		int resourceValue = Integer.valueOf((String)levels.get(resourceLevel));
		switch (getSimType()) {
		case Semmf:
			similarity = simSemmf(queryValue, resourceValue, maxDepth);
			break;
		case GSI:
			similarity = simGSI(queryValue, resourceValue, maxDepth);
			break;
		}

		return similarity;
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

	public double simGSI(int queryLevel, int resourceLevel, int maxDepth) {
		
		return 0;
	}

}
