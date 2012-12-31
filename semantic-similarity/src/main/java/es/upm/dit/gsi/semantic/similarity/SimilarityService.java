package es.upm.dit.gsi.semantic.similarity;

import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.util.SimilarityUtil;

public class SimilarityService {

	public Logger logger = Logger.getLogger(this.getClass());
	
	private double similarity;
	private List<Similarity> similarityList;

	public List<Similarity> getSimilarityList() {
		return similarityList;
	}

	public void setSimilarityList(List<Similarity> similarityList) {
		this.similarityList = similarityList;
	}
	
	public double getSimilarity(Resource query, Resource resource) {
		logger.info("query: " + query.toString());
		logger.info("resource: " + resource.toString());
		similarity = SimilarityUtil.getSimilarity(query, resource, getSimilarityList());
		logger.info("similarity: "+similarity);
		return similarity;
	}

}
