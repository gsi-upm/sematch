package es.upm.dit.gsi.sematch.extraction;

import java.util.HashSet;

import com.hp.hpl.jena.rdf.model.Model;

public abstract class Extractor {
	
	protected Model model;
	protected String[] seeds;
	protected HashSet<String> extractedSet;
	
	protected Extractor(){
		
		this.extractedSet = new HashSet<String>();
		
	}
	
	public abstract void extract();
	

	//to make sure there is no resourse that is same as the ones
	//in the previous seeds.
	
	public void filter(){
		
		for(int i=0; i<seeds.length; i++){
			if(extractedSet.contains(seeds[i])){
				extractedSet.remove(seeds[i]);
			}
		}
		
	}
	
	public String getExtractedSeeds() {
		
		StringBuffer extracted = new StringBuffer();

		for (String str : extractedSet) {
			extracted.append(str);
			extracted.append("\n");
		}
		return extracted.toString();
	}
	
	public Model getModel() {
		return model;
	}

	public void setModel(Model model) {
		this.model = model;
	}

	public String[] getSeeds() {
		return seeds;
	}

	public void setSeeds(String[] seeds) {
		this.seeds = seeds;
	}

	public HashSet<String> getExtractedSet() {
		return extractedSet;
	}

	public void setExtractedSet(HashSet<String> extractedSet) {
		this.extractedSet = extractedSet;
	}

	
}
