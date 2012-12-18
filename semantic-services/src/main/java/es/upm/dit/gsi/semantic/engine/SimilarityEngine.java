package es.upm.dit.gsi.semantic.engine;


import net.sf.json.JSONArray;
import net.sf.json.JSONObject;


import es.upm.dit.gsi.semantic.dao.SkosRdfDao;
import es.upm.dit.gsi.semantic.similarity.SemanticSimilarity;
import es.upm.dit.gsi.semantic.similarity.SemanticSimilarity.SimilarityMethod;

public class SimilarityEngine {
	
	public static String pairwiseSimilarity(String concept_1, String concept_2) {
		
		String uri_1 = SkosRdfDao.getConceptURI(concept_1);
		String uri_2 = SkosRdfDao.getConceptURI(concept_2);
		JSONArray array = new JSONArray();

		String[] result = new String[5];

		result[0] = SemanticSimilarity.computeSimilarity(SimilarityMethod.CGM,
				uri_1, uri_2);

		result[1] = SemanticSimilarity.computeSimilarity(
				SimilarityMethod.WuAndPalm, uri_1, uri_2);

		result[2] = SemanticSimilarity.computeSimilarity(SimilarityMethod.Rada,
				uri_1, uri_2);

		result[3] = SemanticSimilarity.computeSimilarity(
				SimilarityMethod.LeacockAndChodorow, uri_1, uri_2);

		result[4] = SemanticSimilarity.computeSimilarity(SimilarityMethod.Li,
				uri_1, uri_2);
		
		for(int i=0;i<5;i++){
			JSONObject o = new JSONObject();
			o.element("value", result[i]);
			array.add(o);
		}
		return array.toString();

	}

}
