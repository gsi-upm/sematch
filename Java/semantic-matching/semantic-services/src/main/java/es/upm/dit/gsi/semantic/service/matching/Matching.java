package es.upm.dit.gsi.semantic.service.matching;

import java.util.List;
import java.util.Map;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import es.upm.dit.gsi.semantic.similarity.SimilarityService;

public class Matching {
	
	private Configuration config = null;
	private Indexing indexing = null;
	private Searching searching = null;
	
	private static Matching matching = null;
	
	//singleton pattern
	public static Matching getMatching(){
		if(matching == null){
			matching = new Matching();
			matching.setConfig(Configuration.getConfiguration());
			matching.initializing();
		}
		return matching;
	}
	
	public Matching(){
	}
	
	public void initializing(){
		
		//indexing initialization
		indexing = new Indexing();
		indexing.createIndexFromLMF();
		
		//searching initialization
		searching = new Searching(indexing.getIndexDirecotry());
		ApplicationContext simContext = new ClassPathXmlApplicationContext(config.getSimConfig());
		SimilarityService simService = simContext.getBean(config.getSimBean(),SimilarityService.class);
		searching.setQueryConfig(config.getQueryConfig());
		searching.setSimService(simService);
		
	}
	
	public List<Map<String,String>> search(Map<String,Object> query){
		return searching.search(query);
	}
	
	public void finalization(){
		searching.close();
		indexing.close();
	}
	
	public Configuration getConfig() {
		return config;
	}

	public void setConfig(Configuration config) {
		this.config = config;
	}
}
