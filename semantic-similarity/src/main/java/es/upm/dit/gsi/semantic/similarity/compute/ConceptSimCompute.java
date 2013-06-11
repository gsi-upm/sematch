package es.upm.dit.gsi.semantic.similarity.compute;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.InitializingBean;

import es.upm.dit.gsi.semantic.similarity.exceptions.TaxonomyException;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy.MethodType;

public class ConceptSimCompute implements SimCompute, InitializingBean {

	private Logger logger = Logger.getLogger(this.getClass());

	private MethodType methodType;
	private Taxonomy taxonomy;
	private int maxDepth = 1;

	public ConceptSimCompute() {

	}

	@Override
	public double compute(String query, String resource) {
		
		String q;
		String r;
		
		try {
			q = taxonomy.getConceptURI(query);
			r = taxonomy.getConceptURI(resource);
		} catch (TaxonomyException e) {
			// TODO Auto-generated catch block
			logger.error(query + ":" + resource );
			e.printStackTrace();
			return 1.0;
		}
		
		int depth_1 = Taxonomy.getDepth(q);
		int depth_2 = Taxonomy.getDepth(r);
		int depth_c = Taxonomy.getCommonDepth(q, r);
		
		double similarity = 0;

		switch (methodType) {
		case CGM:
			similarity = Taxonomy.simCGM(depth_1, depth_2, depth_c);
			break;
		case WuAndPalm:
			similarity = Taxonomy.simWuAndPalmer(depth_1, depth_2, depth_c);
			break;
		case Rada:
			similarity = Taxonomy.simRada(depth_1, depth_2, depth_c, maxDepth);
			break;
		case LeacockAndChodorow:
			similarity = Taxonomy.simLeacockandChodorow(depth_1, depth_2,
					depth_c, maxDepth);
			break;
		case Li:
			similarity = Taxonomy.simLi(depth_1, depth_2, depth_c);
			break;
		case GSI:
			break;
		}
		return similarity;
	}

	public int getMaxDepth() {
		return maxDepth;
	}

	public void setMaxDepth(int maxDepth) {
		this.maxDepth = maxDepth;
	}

	public MethodType getMethodType() {
		return methodType;
	}

	public void setMethodType(MethodType methodType) {
		this.methodType = methodType;
	}

	public Taxonomy getTaxonomy() {
		return taxonomy;
	}

	public void setTaxonomy(Taxonomy taxonomy) {
		this.taxonomy = taxonomy;
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		taxonomy.initializing();
		taxonomy.formatModel().write(System.out);
	}

}
