package es.upm.dit.gsi.semantic.similarity.compute;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;


public class HybridSimCompute implements SimCompute {

	private Logger logger = Logger.getLogger(this.getClass());

	private String queryConcept;
	private String resourceConcept;
	private String queryConceptProperty;
	private String resourceConceptProperty;
	private boolean weighted = false;
	private double conceptWeight;
	private double propertyWeight;
	private ConceptSimCompute conceptSimilarity;
	private SimCompute conceptPropertySimilarity;

	public boolean isWeighted() {
		return weighted;
	}

	public void setWeighted(boolean weighted) {
		this.weighted = weighted;
	}

	public double getConceptWeight() {
		return conceptWeight;
	}

	public void setConceptWeight(double conceptWeight) {
		this.conceptWeight = conceptWeight;
	}

	public double getPropertyWeight() {
		return propertyWeight;
	}

	public void setPropertyWeight(double propertyWeight) {
		this.propertyWeight = propertyWeight;
	}

	public String getQueryConcept() {
		return queryConcept;
	}

	public void setQueryConcept(String queryConcept) {
		this.queryConcept = queryConcept;
	}

	public String getResourceConcept() {
		return resourceConcept;
	}

	public void setResourceConcept(String resourceConcept) {
		this.resourceConcept = resourceConcept;
	}

	public String getQueryConceptProperty() {
		return queryConceptProperty;
	}

	public void setQueryConceptProperty(String queryConceptProperty) {
		this.queryConceptProperty = queryConceptProperty;
	}

	public String getResourceConceptProperty() {
		return resourceConceptProperty;
	}

	public void setResourceConceptProperty(String resourceConceptProperty) {
		this.resourceConceptProperty = resourceConceptProperty;
	}

	public SimCompute getConceptPropertySimilarity() {
		return conceptPropertySimilarity;
	}

	public void setConceptPropertySimilarity(
			SimCompute conceptPropertySimilarity) {
		this.conceptPropertySimilarity = conceptPropertySimilarity;
	}

	public ConceptSimCompute getConceptSimilarity() {
		return conceptSimilarity;
	}

	public void setConceptSimilarity(ConceptSimCompute conceptSimilarity) {
		this.conceptSimilarity = conceptSimilarity;
	}

	@Override
	public double compute(RDFNode query, RDFNode resource) {

		double similarity = 0;
		double propertySim = 0;
		double conceptSim = 0;

		Resource q = (Resource) query;
		Resource r = (Resource) resource;

		// query concept and property
		Property qConcept = q.getModel().getProperty(this.getQueryConcept());
		Property qConceptProperty = q.getModel().getProperty(
				this.getQueryConceptProperty());

		// resource concept and property
		Property rConcept = r.getModel().getProperty(this.getResourceConcept());
		Property rConceptProperty = r.getModel().getProperty(
				this.getResourceConceptProperty());

		RDFNode qConceptNode = q.getRequiredProperty(qConcept).getObject();
		RDFNode qConceptPropertyNode = q.getRequiredProperty(qConceptProperty)
				.getObject();

		//logger.info("Query Concept: " + qConceptNode + " Property: "
			//	+ qConceptPropertyNode);

		RDFNode rConceptNode = r.getRequiredProperty(rConcept).getObject();
		RDFNode rConceptPropertyNode = r.getRequiredProperty(rConceptProperty)
				.getObject();

		//logger.info("Resource Concept: " + rConceptNode + " Property: "
				//+ rConceptPropertyNode);
		
		if (isWeighted()) {
			propertySim = getConceptPropertySimilarity().compute(
					qConceptPropertyNode, rConceptPropertyNode);
			logger.debug("Property sim: "+propertySim);
			conceptSim = getConceptSimilarity().compute(qConceptNode,
					rConceptNode);
			logger.debug("Concept sim: "+conceptSim);
			similarity = getConceptWeight()*conceptSim;
			similarity = getPropertyWeight()*propertySim + similarity;
		} else {
			propertySim = getConceptPropertySimilarity().compute(
					qConceptPropertyNode, rConceptPropertyNode);
			double propertyDistance = 1 - propertySim;
			similarity = getConceptSimilarity().computeSimilarity(qConceptNode, rConceptNode, propertyDistance);
		}

		//logger.info("Similarity: " + similarity);

		return similarity;
	}

}
