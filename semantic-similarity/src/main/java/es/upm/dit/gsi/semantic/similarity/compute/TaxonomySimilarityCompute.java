package es.upm.dit.gsi.semantic.similarity.compute;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.InitializingBean;

import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.exceptions.TaxonomyException;
import es.upm.dit.gsi.semantic.similarity.taxonomy.RdfsTaxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.SkosTaxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.type.SimilarityMethod;
import es.upm.dit.gsi.semantic.similarity.type.TaxonomyType;
import es.upm.dit.gsi.semantic.similarity.util.SimilarityUtil;
import es.upm.dit.gsi.semantic.similarity.SemanticGraph;
import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class TaxonomySimilarityCompute implements SimilarityCompute, InitializingBean{
	
	private Logger logger = Logger.getLogger(this.getClass());

	private SimilarityMethod methodType;
	private SemanticGraph taxonomyGraph;
	private String taxonomyNS;
	private String rootURI;
	private TaxonomyType taxonomyType;
	private Taxonomy taxonomy;

	public TaxonomySimilarityCompute() {
	}

	public SimilarityMethod getMethodType() {
		return methodType;
	}

	public void setMethodType(SimilarityMethod methodType) {
		this.methodType = methodType;
	}
	
	public SemanticGraph getTaxonomyGraph() {
		return taxonomyGraph;
	}

	public void setTaxonomyGraph(SemanticGraph taxonomyGraph) {
		this.taxonomyGraph = taxonomyGraph;
	}

	public String getTaxonomyNS() {
		return taxonomyNS;
	}

	public void setTaxonomyNS(String taxonomyNS) {
		this.taxonomyNS = taxonomyNS;
	}

	public String getRootURI() {
		return rootURI;
	}

	public void setRootURI(String rootURI) {
		this.rootURI = rootURI;
	}

	public TaxonomyType getTaxonomyType() {
		return taxonomyType;
	}

	public void setTaxonomyType(TaxonomyType taxonomyType) {
		this.taxonomyType = taxonomyType;
	}


	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {

		return computeSimilarity(query, resource, 0);
	}

	public double computeSimilarity(RDFNode query, RDFNode resource,
			double propertySim) {

		String queryConcept = query.toString();
		String resourceConcept = resource.toString();
		
		queryConcept = taxonomy.parseURI(queryConcept);
		resourceConcept = taxonomy.parseURI(resourceConcept);
		
		try {
			queryConcept = taxonomy.getConceptURI(queryConcept);
			resourceConcept = taxonomy.getConceptURI(resourceConcept);
		} catch (TaxonomyException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		logger.debug(queryConcept);
		logger.debug(resourceConcept);
		
		int depth_1 = Taxonomy.getDepth(queryConcept);
		int depth_2 = Taxonomy.getDepth(resourceConcept);
		int depth_c = Taxonomy.getCommonDepth(queryConcept, resourceConcept);
		
		logger.debug("D1 "+depth_1 +" D2 "+depth_2+" Dc "+depth_c+" P "+propertySim);
		return computeConceptSimilarity(depth_1, depth_2, depth_c, propertySim);
	}

	public double computeConceptSimilarity(int depth_1, int depth_2,
			int depth_common, double propertySim) {

		double similarity = 0;

		switch (methodType) {
		case CGM:
			similarity = SimilarityUtil.simCGM(depth_1, depth_2, depth_common);
			break;
		case WuAndPalm:
			similarity = SimilarityUtil.simWuAndPalmer(depth_1, depth_2,
					depth_common);
			break;
		case Rada:
			similarity = SimilarityUtil.simRada(depth_1, depth_2, depth_common,
					taxonomy.getMaxDepth());
			break;
		case LeacockAndChodorow:
			similarity = SimilarityUtil.simLeacockandChodorow(depth_1, depth_2,
					depth_common, taxonomy.getMaxDepth());
			break;
		case Li:
			similarity = SimilarityUtil.simLi(depth_1, depth_2, depth_common);
			break;
		case GSI:
			similarity = SimilarityUtil.simGSI(depth_1, depth_2, depth_common,
					propertySim);
			break;
		}
		return similarity;
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		
		switch(taxonomyType){
		case SKOS:
			taxonomy = new SkosTaxonomy(taxonomyGraph.getModelFromLocal(),
					rootURI,taxonomyNS);
			break;
		case RDFS:
			taxonomy = new RdfsTaxonomy(taxonomyGraph.getModelFromLocal(),
					rootURI,taxonomyNS);
			break;
		}
		
		taxonomy.formatModel();
		
	}

}
