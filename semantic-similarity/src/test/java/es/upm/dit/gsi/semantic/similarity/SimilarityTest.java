package es.upm.dit.gsi.semantic.similarity;

import java.util.HashMap;
import java.util.Map;

import org.junit.Ignore;
import org.junit.Test;
import static org.junit.Assert.*;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.SemanticSimilarity.SimilarityMethod;

/**
 * Unit test for similarities.
 */
public class SimilarityTest {

	public static String concept_1 = "http://gsi.dit.upm.es/gzhu/2012/12/Enterprise-Skills#1324";
	public static String concept_2 = "http://gsi.dit.upm.es/gzhu/2012/12/Enterprise-Skills#1332";
	public static String queryStringPre = " PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"
			+ "SELECT ?concept WHERE {{?concept skos:prefLabel \"";
	public static String queryStringBac = "\"@en }}";
	public static String conceptString = null;
	static final String acmInfo = "result/acm-information-system.rdf";

	public static String queryConcept = "Image search";
	public static String[] resourceConcept = { "RAID", "Web services",
			"Expert systems", "Data streams", "Online banking",
			"Ontologies", "Video search", "Image search", "Mashups",
			"Social networks" };

	@Ignore
	public void testConceptResource() {
		Model model = RDFFileUtil.readRDFFromXML(acmInfo);
		System.out.println(queryConcept);
		Query query = QueryFactory.create(queryStringPre + queryConcept
				+ queryStringBac);
		SparqlClient.displayQuery(
				SparqlClient.executeSelectQuery(query, model), query);
		for (int i = 0; i < 10; i++) {
			System.out.println(resourceConcept[i]);
			query = QueryFactory.create(queryStringPre + resourceConcept[i]
					+ queryStringBac);
			SparqlClient.displayQuery(
					SparqlClient.executeSelectQuery(query, model), query);
		}
	}
	

	@Test
	public void testSim() {

		String[] simMileStones = new String[10];
		String[] simWuAndPalmer = new String[10];
		String[] simRada = new String[10];
		String[] simLandC = new String[10];
		String[] simLi = new String[10];
		String[] resourceURI = new String[10];
		String queryURI = null;

		Model model = RDFFileUtil.readRDFFromXML(acmInfo);

		Query query = QueryFactory.create(queryStringPre + queryConcept
				+ queryStringBac);
		Resource uri = SparqlClient.asResource(
				SparqlClient.executeSelectQuery(query, model), "concept");
		queryURI = uri.getURI();
		
		System.out.println("Query concept is : "+queryConcept);
		System.out.println("Resource concepts are: ");
		for (int i = 0; i < 10; i++) {

			query = QueryFactory.create(queryStringPre + resourceConcept[i]
					+ queryStringBac);
			uri = SparqlClient.asResource(
					SparqlClient.executeSelectQuery(query, model), "concept");
			resourceURI[i] = uri.getURI();
			System.out.println(resourceConcept[i]);
		}
		
		
		System.out.println(SimilarityMethod.CGM+"\t"+SimilarityMethod.WuAndPalm
				+"\t"+SimilarityMethod.Rada+"\t"+SimilarityMethod.LeacockAndChodorow+"\t"+SimilarityMethod.Li);

		for (int i = 0; i < 10; i++) {

			simMileStones[i] = SemanticSimilarity.computeSimilarity(
					SimilarityMethod.CGM, queryURI, resourceURI[i]);
			
			simWuAndPalmer[i] = SemanticSimilarity.computeSimilarity(
					SimilarityMethod.WuAndPalm, queryURI, resourceURI[i]);
			
			simRada[i] = SemanticSimilarity.computeSimilarity(
					SimilarityMethod.Rada, queryURI, resourceURI[i]);
			
			simLandC[i] = SemanticSimilarity.computeSimilarity(
					SimilarityMethod.LeacockAndChodorow, queryURI, resourceURI[i]);
			
			simLi[i] = SemanticSimilarity.computeSimilarity(
					SimilarityMethod.Li, queryURI, resourceURI[i]);

			System.out.println(simMileStones[i] + "\t" + simWuAndPalmer[i]
					+"\t\t"+simRada[i]+"\t"+simLandC[i]+"\t\t\t"+simLi[i]);
		}
	}

	@Ignore
	public void testWuAndPalmer() {

		System.out.println(SemanticSimilarity.computeSimilarity(
				SimilarityMethod.WuAndPalm, concept_1, concept_2));
	}

	@Ignore
	public void testSimilarityGanggao() {

		String fragment_1 = SemanticSimilarity.parseURI(concept_1);
		String fragment_2 = SemanticSimilarity.parseURI(concept_2);

		assertEquals("1324", fragment_1);
		assertEquals("1332", fragment_2);

		int depth_1 = SemanticSimilarity.getDepth(concept_1);
		int depth_2 = SemanticSimilarity.getDepth(concept_2);
		int depth_c = SemanticSimilarity.getCommonDepth(concept_1, concept_2);

		assertEquals(4, depth_1);
		assertEquals(4, depth_2);
		assertEquals(2, depth_c);

		double similarity = SemanticSimilarity.computeConceptSimilarity(
				SimilarityMethod.CGM, depth_1, depth_2, depth_c);
		System.out.println("Similarity between 1324 and 1332 is " + similarity);

	}
}
