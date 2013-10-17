package es.upm.dit.gsi.sematch.service;

import static org.junit.Assert.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.junit.Ignore;
import org.junit.Test;


import es.upm.dit.gsi.sematch.service.Indexing;
import es.upm.dit.gsi.sematch.similarity.Repository;

public class TestIndexingFromLMF {

	@Ignore
	public void testSparql(){
		Indexing index = new Indexing();
		index.createIndexFromLMF();
		
	}


}
