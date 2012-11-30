package es.upm.dit.gsi.semantic.similarity;

import junit.framework.TestCase;

/**
 * Unit test for simple App.
 */
public class SimilarityTest extends TestCase {
	/**
	 * Create the test case
	 * 
	 * @param testName
	 *            name of the test case
	 */
	public SimilarityTest(String testName) {
		super(testName);
	}

	public void testSimilarityGanggao() {
		
		String concept_1 = "http://gsi.dit.upm.es/gzhu/2012/12/Enterprise-Skills#1324";
		String concept_2 = "http://gsi.dit.upm.es/gzhu/2012/12/Enterprise-Skills#1332";
		
		String fragment_1 = TaxonomyUtil.parseURI(concept_1);
		String fragment_2 = TaxonomyUtil.parseURI(concept_2);
		
		assertEquals("1324",fragment_1);
		assertEquals("1332",fragment_2);
		
		int depth_1 = TaxonomyUtil.getDepth(concept_1);
		int depth_2 = TaxonomyUtil.getDepth(concept_2);
		int depth_c = TaxonomyUtil.getCommonDepth(concept_1, concept_2);
		
		assertEquals(4,depth_1);
		assertEquals(4,depth_2);
		assertEquals(2,depth_c);
		
		double similarity = SemanticSimilarity.simGanggao(depth_1, depth_2, depth_c);
		System.out.println("Similarity between 1324 and 1332 is "+similarity);	
		
	}
}
