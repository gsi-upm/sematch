package es.upm.dit.gsi.semantic.engine;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import es.upm.dit.gsi.semantic.dao.SkosRdfDao;


public class SimilarityEngine {

	public SkosRdfDao dao = null;

	public SimilarityEngine() {
		dao = new SkosRdfDao();
	}
	
	public SimilarityEngine(String filePath){
		System.out.println(filePath);
		dao = new SkosRdfDao(filePath);
	}
	
	public SimilarityEngine(InputStream in){
		dao = new SkosRdfDao(in);
	}

	public List<SimilarityResult> pairwiseSimilarity(String concept_1, String concept_2) {
		
		
		String uri_1 = dao.getConceptURI(concept_1);
		String uri_2 = dao.getConceptURI(concept_2);
		ArrayList<SimilarityResult> list = new ArrayList<SimilarityResult>();
		String[] result = new String[5];

		/*result[0] = TaxonomySimCompute.computeSimilarity(SimilarityMethod.CGM,
				uri_1, uri_2);

		result[1] = TaxonomySimCompute.computeSimilarity(
				SimilarityMethod.WuAndPalm, uri_1, uri_2);

		result[2] = TaxonomySimCompute.computeSimilarity(SimilarityMethod.Rada,
				uri_1, uri_2);

		result[3] = TaxonomySimCompute.computeSimilarity(
				SimilarityMethod.LeacockAndChodorow, uri_1, uri_2);

		result[4] = TaxonomySimCompute.computeSimilarity(SimilarityMethod.Li,
				uri_1, uri_2);*/

		for (int i = 0; i < 5; i++) {
			SimilarityResult value = new SimilarityResult();
			value.setValue(result[i]);
			list.add(value);
		}
		return list;

	}

}
