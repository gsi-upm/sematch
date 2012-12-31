package es.upm.dit.gsi.semantic.similarity.compute;


import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class ConceptualSimilarityCompute implements SimilarityCompute{
	
	private Logger logger = Logger.getLogger(this.getClass());
	
	private String queryConcept;
	private String resourceConcept;
	private String queryConceptProperty;
	private String resourceConceptProperty;
	private TaxonomySimilarityCompute conceptSimilarity;
	private SimilarityCompute conceptPropertySimilarity;
	
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


	public SimilarityCompute getConceptPropertySimilarity() {
		return conceptPropertySimilarity;
	}

	public void setConceptPropertySimilarity(
			SimilarityCompute conceptPropertySimilarity) {
		this.conceptPropertySimilarity = conceptPropertySimilarity;
	}
	
	public TaxonomySimilarityCompute getConceptSimilarity() {
		return conceptSimilarity;
	}

	public void setConceptSimilarity(TaxonomySimilarityCompute conceptSimilarity) {
		this.conceptSimilarity = conceptSimilarity;
	}

	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {
		
		double similarity = 0;
		double propSim = 0;
		
		Resource q = (Resource)query;
		Resource r = (Resource)resource;
		
		//query concept and property
		Property qConcept = q.getModel().getProperty(this.getQueryConcept());
		Property qConceptProperty = q.getModel().getProperty(this.getQueryConceptProperty());
	
		//resource concept and property
		Property rConcept = r.getModel().getProperty(this.getResourceConcept());
		Property rConceptProperty = r.getModel().getProperty(this.getResourceConceptProperty());
		
		RDFNode qConceptNode = q.getRequiredProperty(qConcept).getObject();
		RDFNode qConceptPropertyNode = q.getRequiredProperty(qConceptProperty).getObject();
		
		logger.debug("Concept: "+qConceptNode +" Property: "+ qConceptPropertyNode);
	
		RDFNode rConceptNode = r.getRequiredProperty(rConcept).getObject();
		RDFNode rConceptPropertyNode = r.getRequiredProperty(rConceptProperty).getObject();

		logger.debug("Concept: "+rConceptNode +" Property: "+ rConceptPropertyNode);
		
		getConceptPropertySimilarity().computeSimilarity(qConceptPropertyNode, rConceptPropertyNode);
		similarity = getConceptSimilarity().computeSimilarity(qConceptNode, rConceptNode);
		logger.debug("Similarity: "+similarity);
		
		return similarity;
	}

}
