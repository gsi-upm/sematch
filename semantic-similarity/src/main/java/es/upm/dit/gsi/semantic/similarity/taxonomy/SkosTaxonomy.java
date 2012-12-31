package es.upm.dit.gsi.semantic.similarity.taxonomy;



import com.hp.hpl.jena.rdf.model.Literal;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;
import com.hp.hpl.jena.vocabulary.RDF;

import es.upm.dit.gsi.semantic.similarity.SKOS;

public class SkosTaxonomy extends Taxonomy {

	public SkosTaxonomy(Model model, String rootURI, String NS) {
		super(model, rootURI, NS);
	}

	@Override
	public void pushChildren(Resource source, Resource target) {
		target.addProperty(RDF.type, SKOS.Concept);
		//Literal literal = targetModel.createLiteral(source.getProperty(SKOS.prefLabel).getString(), "en");
		target.addProperty(SKOS.prefLabel,source.getProperty(SKOS.prefLabel).getString());

		StmtIterator iter = source.listProperties(SKOS.narrower);
		int i = 0;
		while (iter.hasNext()) {
			Resource sourceChild = iter.nextStatement().getResource();
			Resource targetChild = targetModel.createResource(target.getURI()+CODE[i++]);
			targetChild.addProperty(SKOS.broader, target);
			target.addProperty(SKOS.narrower, targetChild);
			stack.push(sourceChild);
			targetStack.push(targetChild);
		}

	}

}
