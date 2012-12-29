package es.upm.dit.gsi.semantic.similarity.measure;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.Similarity;
import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class SinglePropertySimilarity implements Similarity {

	private Logger logger = Logger.getLogger(this.getClass());

	private double weight;

	private double similarity;

	private String label;

	private String queryPropertyURI;

	private String resourcePropertyURI;

	private SimilarityCompute similarityCompute;

	public void setLabel(String label) {
		this.label = label;
	}

	public void setWeight(double weight) {
		this.weight = weight;
	}

	public String getQueryPropertyURI() {
		return queryPropertyURI;
	}

	public void setQueryPropertyURI(String queryPropertyURI) {
		this.queryPropertyURI = queryPropertyURI;
	}

	public String getResourcePropertyURI() {
		return resourcePropertyURI;
	}

	public void setResourcePropertyURI(String resourcePropertyURI) {
		this.resourcePropertyURI = resourcePropertyURI;
	}

	public SimilarityCompute getSimilarityCompute() {
		return similarityCompute;
	}

	public void setSimilarityCompute(SimilarityCompute similarityCompute) {
		this.similarityCompute = similarityCompute;
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

		Property pQuery = query.getModel().getProperty(getQueryPropertyURI());
		Property pResource = resource.getModel().getProperty(
				getResourcePropertyURI());

		RDFNode q = query.getRequiredProperty(pQuery).getObject();
		RDFNode r = resource.getRequiredProperty(pResource).getObject();
		similarity = getSimilarityCompute().computeSimilarity(q, r);

		return similarity;
	}

	@Override
	public void printResult() {
		logger.info(label + "	Weight: " + weight
				+ "	Similarity: " + similarity);

	}
}
