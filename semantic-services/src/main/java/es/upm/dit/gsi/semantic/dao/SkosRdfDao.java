package es.upm.dit.gsi.semantic.dao;

import java.io.InputStream;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.*;
import es.upm.dit.gsi.semantic.similarity.util.TaxonomyUtil;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;

public class SkosRdfDao {

	private Model model = null;
	private static final String rdf = "acm-information-system.rdf";
	public static String queryStringPre = " PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"
			+ "SELECT ?concept WHERE {{?concept skos:prefLabel \"";
	public static String queryStringBac = "\"@en }}";

	public SkosRdfDao() {
		InputStream in = this.getClass().getClassLoader().getResourceAsStream(rdf);
		//System.out.println(this.getClass().getClassLoader().getResource(rdf));
		model = TaxonomyUtil.readRDFFromXML(in);
	}
	
	public SkosRdfDao(InputStream in){
		model = TaxonomyUtil.readRDFFromXML(in);
	}
	
	public SkosRdfDao(String filePath){
		String file = filePath+"data/"+rdf;
		System.out.println(file);
		model = TaxonomyUtil.readRDFFromXML(file);
	}

	public String getConceptURI(String concept) {

		String queryString = queryStringPre + concept + queryStringBac;
		Query query = QueryFactory.create(queryString);

		Resource uri = SparqlClient.asResource(
				SparqlClient.executeSelectQuery(query, model), "concept");
		return uri.getURI();
	}

}
