package es.upm.dit.gsi.semantic.service;

import static org.junit.Assert.*;

import org.junit.Test;

import es.upm.dit.gsi.semantic.search.IndexConfig;
import es.upm.dit.gsi.semantic.search.QueryConfig;
import es.upm.dit.gsi.semantic.service.matching.Configuration;

public class ConfigurationTest {

	@Test
	public void test() {
		
		Configuration config = new Configuration();
		IndexConfig indexConfig = config.getIndexConfig();
		QueryConfig queryConfig = config.getQueryConfig();
		
		String r1 = "http://www.gsi.dit.upm.es/gzhu/ontology/employment.rdfs#skill";
		String r2 = "http://www.gsi.dit.upm.es/gzhu/ontology/employment.rdfs#level";
		String skill = indexConfig.getFieldURI("skill");
		String level = indexConfig.getFieldURI("level");
		String type = indexConfig.getType();
		String localFile = indexConfig.getLocalFile();
		String remoteURL = indexConfig.getRemoteUrl();
		String query = indexConfig.getQuery();
		
		
		for(String str : queryConfig.getQueryFileds()){
			System.out.println(str);
		}
		
		assertEquals("size",20,queryConfig.getResultSize());
		assertEquals("type","local",type);
		assertEquals("localfile","dataset/employees.rdf",localFile);
		assertEquals("remoteURL",null,remoteURL);
		assertEquals("query",null,query);
		assertEquals("field",r1,skill);
		assertEquals("rield",r2,level);
		
	}

}
