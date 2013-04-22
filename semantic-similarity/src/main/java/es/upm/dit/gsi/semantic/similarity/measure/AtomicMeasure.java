package es.upm.dit.gsi.semantic.similarity.measure;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.compute.SimCompute;

public class AtomicMeasure extends SimilarityMeasure {

	private Logger logger = Logger.getLogger(this.getClass());

	protected String queryURI;

	protected String resourceURI;

	protected SimCompute simCompute;

	@Override
	public double getSimilarity(Resource query, Resource resource) {

		Property pQ = query.getModel().getProperty(getQueryURI());
		Property pR = resource.getModel().getProperty(getResourceURI());

		RDFNode qNode = query.getRequiredProperty(pQ).getObject();
		RDFNode rNode = resource.getRequiredProperty(pR).getObject();
		
		double similarity = simCompute.compute(qNode, rNode);
		logger.info(label + " Weight: " + weight+ "	Sim: " + similarity);
		
		return similarity*getWeight();
	}
	
	public SimCompute getSimCompute() {
		return simCompute;
	}

	public void setSimCompute(SimCompute simCompute) {
		this.simCompute = simCompute;
	}

	public String getQueryURI() {
		return queryURI;
	}

	public void setQueryURI(String queryURI) {
		this.queryURI = queryURI;
	}

	public String getResourceURI() {
		return resourceURI;
	}

	public void setResourceURI(String resourceURI) {
		this.resourceURI = resourceURI;
	}

}
