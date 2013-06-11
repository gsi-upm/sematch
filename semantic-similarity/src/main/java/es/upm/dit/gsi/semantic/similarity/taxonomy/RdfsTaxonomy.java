package es.upm.dit.gsi.semantic.similarity.taxonomy;


import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ResIterator;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.vocabulary.RDF;
import com.hp.hpl.jena.vocabulary.RDFS;


public class RdfsTaxonomy extends Taxonomy{
	
	public RdfsTaxonomy(){
		super();
	}

	public RdfsTaxonomy(Model model, String rootURI, String NS) {
		super(model, rootURI, NS);
	}

	@Override
	public void pushChildren(Resource source, Resource target) {
		
		target.addProperty(RDF.type, SKOS.Concept);
		//Literal literal = targetModel.createLiteral(parseURI(source.toString()), "en");
		target.addProperty(SKOS.prefLabel, parseURI(source.toString()));
		ResIterator iter = originModel.listSubjectsWithProperty(RDFS.subClassOf, source);
		int i = 0;
		while(iter.hasNext()){
			Resource sourceChild = iter.nextResource();
			Resource targetChild = targetModel.createResource(target.getURI()+CODE[i++]);
			targetChild.addProperty(SKOS.broader, target);
			target.addProperty(SKOS.narrower, targetChild);
			stack.push(sourceChild);
			targetStack.push(targetChild);
		}
	}

}
