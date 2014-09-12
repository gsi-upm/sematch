package es.upm.dit.gsi.sematch.service;

import static org.junit.Assert.*;

import org.junit.Test;

import es.upm.dit.gsi.sematch.search.Indexing;

public class MatchingTest {

	@Test
	public void test() {
		Configuration config = Configuration.getConfiguration();
		Indexing indexing = new Indexing(config.getIndexConfig());
		indexing.index_from_json_file();
		
	}

}
