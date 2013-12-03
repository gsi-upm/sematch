package es.upm.dit.gsi.sematch.similarity;

import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.junit.Ignore;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import es.upm.dit.gsi.sematch.similarity.measure.JSONMeasure;

public class TestSimCompute {

	@Ignore
	public void testJSON() {
		
		String query = "[{skill:'Java',level:'Expert'},{skill:'C',level:'Expert'},{skill:'PHP',level:'Expert'}]";
		String resource = "[{skill:'Java',level:'Expert'},{skill:'C',level:'Beginner'},{skill:'PHP',level:'Expert'}]";
		Map<String,Object> mq = new HashMap<String,Object>();
		mq.put("skill", query);
		Map<String,Object> mr = new HashMap<String,Object>();
		mr.put("skill", resource);
		SimilarityConfig config = new SimilarityConfig();
		config.setQuery(mq);
		config.setResource(mr);
		
		ApplicationContext simContext = new ClassPathXmlApplicationContext("similarity-config.xml");
		JSONMeasure jsonMeasure = simContext.getBean("multiSkill",JSONMeasure.class);
		jsonMeasure.getSimilarity(config);

	}

}
