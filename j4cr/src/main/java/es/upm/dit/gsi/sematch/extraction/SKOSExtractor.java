package es.upm.dit.gsi.sematch.extraction;

import com.hp.hpl.jena.rdf.model.ResIterator;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.sematch.similarity.taxonomy.SKOS;

public class SKOSExtractor extends Extractor {
	
	private boolean checkNarrower = false;

	public SKOSExtractor() {
		super();
	}

	@Override
	public void extract() {
		
		for (int i = 0; i < seeds.length; i++) {

			Resource concept = model.getResource(seeds[i]);
			ResIterator iter = model.listResourcesWithProperty(
					SKOS.broader, concept);

			while (iter.hasNext()) {
				Resource narrower = iter.nextResource();
				if (checkNarrower) {
					ResIterator iter2 = model.listResourcesWithProperty(
							SKOS.broader, narrower);
					if (iter2.hasNext()) {
						extractedSet.add(narrower.getURI());
					}
				} else {
					extractedSet.add(narrower.getURI());
				}
			}
		}

	}
	
	public boolean isCheckNarrower() {
		return checkNarrower;
	}

	public void setCheckNarrower(boolean checkNarrower) {
		this.checkNarrower = checkNarrower;
	}

}
