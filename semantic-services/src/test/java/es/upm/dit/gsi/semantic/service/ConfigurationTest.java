package es.upm.dit.gsi.semantic.service;

import static org.junit.Assert.*;

import org.junit.Test;

import es.upm.dit.gsi.semantic.matching.Configuration;
import es.upm.dit.gsi.semantic.search.IndexConfig;

public class ConfigurationTest {

	@Test
	public void test() {
		
		Configuration config = new Configuration();
		IndexConfig indexConfig = config.getIndexConfig();
		
		String r1 = "http://www.gsi.dit.upm.es/gzhu/ontology/employment.rdfs#skill";
		String r2 = "http://www.gsi.dit.upm.es/gzhu/ontology/employment.rdfs#level";
		String skill = indexConfig.getFieldURI("skill");
		String level = indexConfig.getFieldURI("level");
		
		assertEquals("resource",r1,skill);
		assertEquals("resource",r2,level);
		
	}

}
