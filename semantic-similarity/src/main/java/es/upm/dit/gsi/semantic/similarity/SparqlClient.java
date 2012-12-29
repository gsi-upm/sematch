package es.upm.dit.gsi.semantic.similarity;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.sparql.engine.http.QueryEngineHTTP;

import es.upm.dit.gsi.semantic.similarity.util.TaxonomyUtil;

/**
 * This is a simple client for sparql, note that this class is not thread safe.
 * 
 * @author gzhu
 * 
 */

public class SparqlClient {

	private static QueryExecution qexec = null;
	private static QueryEngineHTTP hqexec = null;

	// execute a select query in a rdf file.
	public static ResultSet executeSelectQuery(String rdfFile, Query query) {
		Model model = TaxonomyUtil.readRDFFromXML(rdfFile);
		return executeSelectQuery(query, model);
	}

	// execute select query inside a model
	public static ResultSet executeSelectQuery(Query query, Model model) {
		closeQuery();
		qexec = QueryExecutionFactory.create(query, model);
		return executeSelectQuery(qexec);
	}
	
	public static Model executeConstructQuery(Query query, Model model){
		closeQuery();
		qexec = QueryExecutionFactory.create(query, model);
		return qexec.execConstruct();
	}

	// execute select query from a remote sparql service.
	public static ResultSet executeSelectQuery(Query query, String sparqlService) {
		closeQuery();
		qexec = QueryExecutionFactory.sparqlService(sparqlService, query);
		return executeSelectQuery(qexec);
	}

	public static ResultSet executeSelectQuery(Query query,
			String sparqlService, Map<String, String> paramMap) {
		closeQuery();
		hqexec = QueryExecutionFactory.createServiceRequest(sparqlService,
				query);
		for (String string : paramMap.keySet()) {
			hqexec.addParam(string, paramMap.get(string));
		}
		ResultSet results = hqexec.execSelect();
		return results;
	}

	// execute select query
	public static ResultSet executeSelectQuery(QueryExecution qexec) {

		ResultSet result = null;
		result = qexec.execSelect();
		return result;
	}

	// read the query string from a file and execute the query in a rdf file
	public static Query getQueryFromFile(File file) {
		return QueryFactory.read(file.getAbsolutePath());
	}

	// display the query result in console.
	public static void displayQuery(ResultSet results, Query query) {
		ResultSetFormatter.out(System.out, results, query);
	}


	//TODO:this is just for experiment
	public static Resource asResource(ResultSet resultSet, String resource) {

		Resource result = null;
		while (resultSet.hasNext()) {
			QuerySolution soln = resultSet.nextSolution();
			result = soln.getResource(resource);
		}
		return result;
	}

	// return the query result as resource list.
	public static List<Resource> asResourceList(ResultSet resultSet, String resource) {

		List<Resource> result = new ArrayList<Resource>();
		while (resultSet.hasNext()) {
			QuerySolution soln = resultSet.nextSolution();
			result.add(soln.getResource(resource));
		}
		return result;
	}
	
	public static void closeQuery() {
		if (qexec != null)
			qexec.close();
		if (hqexec != null)
			hqexec.close();
		qexec = null;
		hqexec = null;
	}

}
