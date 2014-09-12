package es.upm.dit.gsi.sematch.similarity.measure;

import java.util.ArrayList;
import java.util.Map;

import net.sf.json.JSONArray;

import org.apache.log4j.Logger;

import es.upm.dit.gsi.sematch.similarity.Similarity;
import es.upm.dit.gsi.sematch.similarity.SimilarityConfig;

public class JSONMeasure extends SimilarityMeasure {

	public Logger logger = Logger.getLogger(this.getClass());

	private Similarity measure;
	
	public Similarity getMeasure() {
		return measure;
	}

	public void setMeasure(Similarity measure) {
		this.measure = measure;
	}

	@Override
	public double getSimilarity(SimilarityConfig config) {
		
		String query = config.getQuery(label).toString();
		String resource = config.getResource(label).toString();
		JSONArray queryArray = JSONArray.fromObject(query);
		JSONArray resourceArray = JSONArray.fromObject(resource);
		ArrayList<Double> simArray = new ArrayList<Double>();
		for(Object qObject :queryArray.toArray()){
			double sim = 0;
			for(Object rObject : resourceArray.toArray()){
				Map<String,Object> qmap = (Map<String,Object>)qObject;
				Map<String,Object> rmap = (Map<String,Object>)rObject;
				SimilarityConfig conf = new SimilarityConfig();
				conf.setQuery(qmap);
				conf.setResource(rmap);
				double similarity = measure.getSimilarity(conf);
				if(similarity > sim){
					sim = similarity;
				}
			}
			simArray.add(sim);
		}
		
		int simL = simArray.size();
		double sum = 0;
		for(Double sim : simArray){
			sum += sim;
		}
		return sum/simL;
	}


}
