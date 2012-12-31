package es.upm.dit.gsi.semantic.similarity.measure;

import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.Similarity;
import es.upm.dit.gsi.semantic.similarity.util.SimilarityUtil;

public class ClusterSimilarity implements Similarity {

	public Logger logger = Logger.getLogger(this.getClass());

	private double weight;

	private String label;

	private List<Similarity> similarityList;

	public void setLabel(String label) {
		this.label = label;
	}

	public List<Similarity> getSimilarityList() {
		return similarityList;
	}

	public void setSimilarityList(List<Similarity> similarityList) {
		this.similarityList = similarityList;
	}

	public void setWeight(double weight) {
		this.weight = weight;
	}

	@Override
	public String getLabel() {
		return label;
	}

	@Override
	public double getWeight() {
		return weight;
	}

	@Override
	public double getSimilarity(Resource query, Resource resource) {
		double similarity = SimilarityUtil.getSimilarity(query, resource,
				getSimilarityList());
		logger.info(label + "	Weight: " + weight
				+ "	Similarity: " + similarity);
		return similarity*getWeight();
	}

}
