package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.apache.log4j.Logger;
import org.junit.Ignore;
import org.junit.Test;

import com.hp.hpl.jena.rdf.model.Model;

import es.upm.dit.gsi.semantic.similarity.exceptions.TaxonomyException;
import es.upm.dit.gsi.semantic.similarity.taxonomy.RdfsTaxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.SkosTaxonomy;



public class TaxonomyTest {
	
	private Logger logger = Logger.getLogger(this.getClass());

	static final String ict_service = "dataset/ICT_Service.owl";
	static final String acm_clasification = "dataset/acm-classification.xml";
	static final String gics = "dataset/GICS2010.rdf";
	static final String itSkills = "dataset/it-skills.rdfs";
	static final String NS = "http://gsi.dit.upm.es/gzhu/ontologies/";

	@Ignore
	public void testSkosFormating() {
		Model acm = SemanticRepository.readFromXML(acm_clasification);
		String acm_ns = NS+"ACM#";
		String root = "#10003120";
		SkosTaxonomy taxonomy = new SkosTaxonomy(acm,root,acm_ns);
		Model result = taxonomy.formatModel();
		result.write(System.out);
		
	}
	
	@Test
	public void testRdfsFormating(){
		Model skills = SemanticRepository.readFromXML(itSkills);
		String skill_ns = NS+"IT-SKILL#";
		String root = "http://example.org/it-skills.rdfs#IT_Skills";
		RdfsTaxonomy taxonomy = new RdfsTaxonomy(skills,root,skill_ns);
		Model result = taxonomy.formatModel();
		result.write(System.out);
		int maxDepth = taxonomy.getMaxDepth();
		logger.info(maxDepth);
		try {
			logger.info(taxonomy.getConceptURI("Computer_lauages"));
		} catch (TaxonomyException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
