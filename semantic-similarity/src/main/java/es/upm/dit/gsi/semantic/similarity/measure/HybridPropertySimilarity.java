package es.upm.dit.gsi.semantic.similarity.measure;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;

import es.upm.dit.gsi.semantic.similarity.Similarity;
import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class HybridPropertySimilarity implements Similarity {

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

	/**
	 * get the max similarity from the property pairs
	 */
	@Override
	public double getSimilarity(Resource query, Resource resource) {

		Property pQuery = query.getModel().getProperty(getQueryPropertyURI());
		Property pResource = resource.getModel().getProperty(
				getResourcePropertyURI());

		StmtIterator stmtIt = query.listProperties(pQuery);
		List<RDFNode> qList = new ArrayList<RDFNode>();

		while (stmtIt.hasNext()) {
			RDFNode node = stmtIt.nextStatement().getObject();
			qList.add(node);
		}

		List<RDFNode> rList = new ArrayList<RDFNode>();
		stmtIt = resource.listProperties(pResource);
		while (stmtIt.hasNext()) {
			RDFNode node = stmtIt.nextStatement().getObject();
			rList.add(node);
		}

		List<Double> simList = new ArrayList<Double>();
		for (RDFNode queryNode : qList) {
			for (RDFNode resourceNode : rList) {
				Double sim = new Double(getSimilarityCompute()
						.computeSimilarity(queryNode, resourceNode));
				simList.add(sim);
			}
		}

		similarity = Collections.max(simList).doubleValue() * getWeight();
		return similarity;
	}

	@Override
	public void printResult() {
		logger.info(label + "	Weight: " + weight
				+ "	Similarity: " + similarity);

	}

}
