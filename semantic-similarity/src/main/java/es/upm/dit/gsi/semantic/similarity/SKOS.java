package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

/**
 * Simple Knowledge Organization System model is implemented here.
 * @author gzhu
 *
 */

public class SKOS {

	
	/** The RDF model that holds the vocabulary terms. */
	private static Model model = ModelFactory.createDefaultModel();
	
	/** Default Namespace */
	public static final String NS = "http://www.w3.org/2004/02/skos/core#";

	public static String getURI() {return NS;}
	    
	    /** <p>The namespace of the vocabulary as a resource</p> */
	public static final Resource NAMESPACE = model.createResource( NS );
	
	/** Vocabulary concepts */
	public static final Resource ConceptScheme = model.createResource(NS+ "ConceptScheme");
	public static final Resource Concept = model.createResource(NS + "Concept");
	public static final Resource Collection = model.createResource(NS
			+ "Collection");
	public static final Resource OrderedCollection = model.createResource(NS
			+ "OrderedCollection");
	public static final Resource CollectableProperty = model.createResource(NS
			+ "CollectableProperty");

	/** Vocabulary properties */
	public static final Property prefLabel = model.createProperty(NS,
			"prefLabel");
	public static final Property altLabel = model
			.createProperty(NS, "altLabel");
	public static final Property hiddenLabel = model.createProperty(NS,
			"hiddenLabel");

	public static final Property symbol = model.createProperty(NS, "symbol");
	public static final Property prefSymbol = model.createProperty(NS,
			"prefSymbol");
	public static final Property altSymbol = model.createProperty(NS,
			"altSymbol");

	public static final Property note = model.createProperty(NS, "note");
	public static final Property definition = model.createProperty(NS,
			"definition");
	public static final Property example = model.createProperty(NS, "example");

	public static final Property semanticRelation = model.createProperty(NS,
			"semanticRelation");
	public static final Property broader = model.createProperty(NS, "broader");
	public static final Property narrower = model
			.createProperty(NS, "narrower");
	public static final Property related = model.createProperty(NS, "related");

	public static final Property inScheme = model
			.createProperty(NS, "inScheme");
	public static final Property hasTopConcept = model.createProperty(NS,
			"hasTopConcept");
	public static final Property member = model.createProperty(NS, "member");
	public static final Property memberList = model.createProperty(NS,
			"memberList");

	public static final Property subject = model.createProperty(NS, "subject");
	public static final Property primarySubject = model.createProperty(NS,
			"primarySubject");
	public static final Property isSubjectOf = model.createProperty(NS,
			"isSubjectOf");
	public static final Property isPrimarySubjectOf = model.createProperty(NS,
			"isPrimarySubjectOf");
	public static final Property subjectIndicator = model.createProperty(NS,
			"subjectIndicator");

}
