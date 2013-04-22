package es.upm.dit.gsi.semantic.similarity.compute;

import com.hp.hpl.jena.rdf.model.RDFNode;

public interface SimCompute {
	
	public double compute(RDFNode query, RDFNode resource);
	
}
