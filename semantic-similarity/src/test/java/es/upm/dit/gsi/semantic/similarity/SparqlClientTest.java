package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import java.io.File;

import org.junit.Ignore;
import org.junit.Test;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.rdf.model.Model;

public class SparqlClientTest {

	static final String acmInfo = "result/acm-information-system.rdf";
	static final String queryFile = "dataset/query/sparql-query";
	static final String sparqlService = "http://dbpedia.org/sparql";
	static final String querySkos = "dataset/query/querySkos";
	
	
	@Ignore
	public void testSelectQuery(){
		File file = new File(querySkos);
		Query query = SparqlClient.getQueryFromFile(file);
		System.out.println(query.toString());
		SparqlClient.displayQuery(SparqlClient.executeSelectQuery(acmInfo,query),query);
	}
	
	@Ignore
	public void testHttpSelectQuery(){
		File file = new File(queryFile);
		Query query = SparqlClient.getQueryFromFile(file);
		SparqlClient.displayQuery(SparqlClient.executeSelectQuery(query, sparqlService),query);
		
	}
	
	
	
	

}
