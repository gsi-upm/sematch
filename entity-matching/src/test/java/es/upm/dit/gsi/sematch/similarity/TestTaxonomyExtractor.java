package es.upm.dit.gsi.sematch.similarity;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;


import org.junit.Ignore;
import org.junit.Test;

import com.hp.hpl.jena.rdf.model.Literal;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.ResIterator;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;
import com.hp.hpl.jena.vocabulary.RDF;


import es.upm.dit.gsi.sematch.similarity.taxonomy.SKOS;
import es.upm.dit.gsi.sematch.extraction.Extractor;
import es.upm.dit.gsi.sematch.extraction.SKOSExtractor;
import es.upm.dit.gsi.sematch.extraction.TaxonomyExtraction;

public class TestTaxonomyExtractor {

	@Ignore
	public void test() {
		
		String sampleFile = "dataset/sample-triple.nt";
		String taxFile = "dataset/dbpedia_skos_categories_en.nt";
		String rootURI = "http://dbpedia.org/resource/Category:Programming_languages";
		TaxonomyExtraction extraction = new TaxonomyExtraction();
		
		HashSet<String> resource = new HashSet<String>();
		resource.add(rootURI);
		
		for(int i=1;i<=3;i++){
			String input = Repository.readTextFile("gen"+i+".txt");
			String[] inputs = input.split("\n");
			for(int j=0;j<inputs.length;j++){
				resource.add(inputs[j]);
			}
		}
		StringBuffer buffer = new StringBuffer();
		for(String str : resource){
			buffer.append(str);
			buffer.append("\n");
		}
		extraction.initTaxonomy(taxFile);
		extraction.buildSubTaxonomy(buffer.toString());
		extraction.getNewTaxonomy().write(System.out);
		
		Repository.writeModelFile(extraction.getNewTaxonomy(), "programming-language.rdf");
		
		
	}
	
	@Ignore public void testDepthExtraction(){
		
		String taxFile = "dataset/dbpedia_skos_categories_en.nt";
		
		//String feed = "http://dbpedia.org/resource/Category:Programming_languages";
		
		TaxonomyExtraction extraction = new TaxonomyExtraction();
		SKOSExtractor extractor = new SKOSExtractor();
		extractor.setCheckNarrower(false);
		
		extraction.initTaxonomy(taxFile);
		extraction.setExtractor(extractor);
		
		String feed = Repository.readTextFile("gen3.txt");
		
		ArrayList<String> list = extraction.extract(1, feed);
		Repository.writeTextFile("gen4.txt", list.get(1));
		
	}
}
