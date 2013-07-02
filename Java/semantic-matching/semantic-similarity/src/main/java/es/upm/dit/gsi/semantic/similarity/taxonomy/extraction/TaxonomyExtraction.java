package es.upm.dit.gsi.semantic.similarity.taxonomy.extraction;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

import com.hp.hpl.jena.rdf.model.Literal;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;
import com.hp.hpl.jena.vocabulary.RDF;

import es.upm.dit.gsi.semantic.similarity.Repository;
import es.upm.dit.gsi.semantic.similarity.taxonomy.SKOS;

public class TaxonomyExtraction {
	
	private Model rawTaxonomy = null;
	private Extractor extractor = null;
	private Model newTaxonomy = null;
	
	public TaxonomyExtraction(){
	}
	
	public void initTaxonomy(String fileName){
		rawTaxonomy = Repository.readModelNTriple(fileName);
		rawTaxonomy.setNsPrefix("skos", SKOS.getURI());
		newTaxonomy = ModelFactory.createDefaultModel();
		newTaxonomy.setNsPrefix("skos", SKOS.getURI());
	}
	
	public ArrayList<String> extract(int maxDepth, String initSeeds){
		
		int depth = 0;
		extractor.setModel(rawTaxonomy);
		ArrayList<String> seedList = new ArrayList<String>();
		seedList.add(initSeeds);
		
		while(depth < maxDepth){
			String[] s = seedList.get(depth).split("\n");
			extractor.setSeeds(s);
			extractor.extract();
			extractor.filter();
			String nSeed = extractor.getExtractedSeeds();
			seedList.add(nSeed);
			depth++;
		}
		
		return seedList;
	}
	
	public void buildSubTaxonomy(String resourseFile){
	
		String[] strList = resourseFile.split("\n");
		
		HashMap<String,Resource> resMap = new HashMap<String,Resource>();
		Resource resource;
		for(int i=0;i<strList.length;i++){
			resource = newTaxonomy.createResource(strList[i]);
			resMap.put(strList[i], resource);
		}
		
		HashSet<String> extraRes = new HashSet<String>();
		
		for(String uri : resMap.keySet()){
			
			Resource target = resMap.get(uri);
			Resource origin = rawTaxonomy.getResource(target.getURI());
			target.addProperty(RDF.type, SKOS.Concept);
			Literal li = newTaxonomy.createLiteral(origin.getProperty(SKOS.prefLabel).getString(), "en");
			target.addProperty(SKOS.prefLabel,li);
			StmtIterator iter = origin.listProperties(SKOS.broader);
			while(iter.hasNext()){
				
				Resource broader = iter.nextStatement().getResource();
				if (resMap.keySet().contains(broader.getURI())) {
					target.addProperty(SKOS.broader,
							resMap.get(broader.getURI()));
				}else{
					extraRes.add(broader.getURI());
				}

			}
		}
		
		for(String res : extraRes){
			System.out.println(res);
		}
		
	}
	
	public Model getNewTaxonomy() {
		return newTaxonomy;
	}

	public void setNewTaxonomy(Model newTaxonomy) {
		this.newTaxonomy = newTaxonomy;
	}

	public Model getRawTaxonomy() {
		return rawTaxonomy;
	}

	public void setRawTaxonomy(Model rawTaxonomy) {
		this.rawTaxonomy = rawTaxonomy;
	}

	public Extractor getExtractor() {
		return extractor;
	}

	public void setExtractor(Extractor extractor) {
		this.extractor = extractor;
	}

}
