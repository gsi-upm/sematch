package es.upm.dit.gsi.semantic.dao;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.*;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;

public class SkosRdfDao {

	private static Model model = null;
	private static final String rdf = "acm-information-system.rdf";
	public static String queryStringPre = " PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"
			+ "SELECT ?concept WHERE {{?concept skos:prefLabel \"";
	public static String queryStringBac = "\"@en }}";

	public static String getConceptURI(String concept) {
		
		if(model == null){
			model = RDFFileUtil.readRDFFromXML(rdf);
		}
		
		String queryString = queryStringPre+concept+queryStringBac;
		Query query =  QueryFactory.create(queryString);

		Resource uri = SparqlClient.asResource(
				SparqlClient.executeSelectQuery(query, model),
				"concept");
		return uri.getURI();
	}

}
