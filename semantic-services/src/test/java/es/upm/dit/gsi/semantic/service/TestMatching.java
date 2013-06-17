package es.upm.dit.gsi.semantic.service;

import static org.junit.Assert.*;

import org.junit.Test;

import es.upm.dit.gsi.semantic.service.matching.Matching;

public class TestMatching {

	@Test
	public void test() {
		
		Matching matching = new Matching();
		matching.initializing();
		//matching.search();
		matching.finalization();
	}

}
