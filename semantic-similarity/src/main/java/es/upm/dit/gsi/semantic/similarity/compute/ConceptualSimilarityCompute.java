package es.upm.dit.gsi.semantic.similarity.compute;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class ConceptualSimilarityCompute implements SimilarityCompute{
	
	private Logger logger = Logger.getLogger(this.getClass());
	
	private String queryConcept;
	private String resourceConcept;
	private String queryConceptProperty;
	private String resourceConceptProperty;
	private SimilarityCompute conceptSimilarity;
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

	public SimilarityCompute getConceptSimilarity() {
		return conceptSimilarity;
	}

	public void setConceptSimilarity(SimilarityCompute conceptSimilarity) {
		this.conceptSimilarity = conceptSimilarity;
	}

	public SimilarityCompute getConceptPropertySimilarity() {
		return conceptPropertySimilarity;
	}

	public void setConceptPropertySimilarity(
			SimilarityCompute conceptPropertySimilarity) {
		this.conceptPropertySimilarity = conceptPropertySimilarity;
	}

	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {
		
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
		
		//logger.info("Concept: "+qConceptNode +" Property: "+ qConceptPropertyNode);
	
		RDFNode rConceptNode = r.getRequiredProperty(rConcept).getObject();
		RDFNode rConceptPropertyNode = r.getRequiredProperty(rConceptProperty).getObject();

		//logger.info("Concept: "+rConceptNode +" Property: "+ rConceptPropertyNode);
		
		getConceptPropertySimilarity().computeSimilarity(qConceptPropertyNode, rConceptPropertyNode);
		return 0;
	}

}
