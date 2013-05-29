package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;
import org.junit.Ignore;
import org.junit.Test;

import com.hp.hpl.jena.rdf.model.Model;

import es.upm.dit.gsi.semantic.similarity.exceptions.TaxonomyException;
import es.upm.dit.gsi.semantic.similarity.taxonomy.RdfsTaxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.SkosTaxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;
import es.upm.dit.gsi.semantic.similarity.taxonomy.TaxonomyTree;

public class TaxonomyTest {

	private Logger logger = Logger.getLogger(this.getClass());

	static final String ict_service = "dataset/ICT_Service.owl";
	static final String acm_clasification = "dataset/acm-classification.xml";
	static final String gics = "dataset/GICS2010.rdf";
	static final String itSkills = "dataset/it-skills.rdfs";
	static final String NS = "http://gsi.dit.upm.es/gzhu/ontologies/";

	@Ignore
	public void testSkosFormating() {
		Model acm = Repository.readFromXML(acm_clasification);
		String acm_ns = NS + "ACM#";
		String root = "#10003120";
		SkosTaxonomy taxonomy = new SkosTaxonomy(acm, root, acm_ns);
		Model result = taxonomy.formatModel();
		result.write(System.out);

	}

	@Ignore
	public void testRdfsFormating() {
		Model skills = Repository.readFromXML(itSkills);
		String skill_ns = NS + "IT-SKILL#";
		String root = "http://example.org/it-skills.rdfs#IT_Skills";
		RdfsTaxonomy taxonomy = new RdfsTaxonomy(skills, root, skill_ns);
		Model result = taxonomy.formatModel();
		result.write(System.out);
		int maxDepth = taxonomy.getMaxDepth();
		logger.info(maxDepth);
		try {
			logger.info(taxonomy.getConceptURI("Computer_lauages"));
		} catch (TaxonomyException e) {
			e.printStackTrace();
		}
	}

	@Ignore
	public void testWuAndPalm() {

		String[] concepts = { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" };
		Map<String, String> taxonomy = new HashMap<String, String>();
		
		taxonomy.put("a", "1");
		taxonomy.put("b", "11");
		taxonomy.put("c", "12");
		taxonomy.put("d", "13");
		taxonomy.put("e", "121");
		taxonomy.put("f", "122");
		taxonomy.put("g", "131");
		taxonomy.put("h", "132");
		taxonomy.put("i", "1221");
		taxonomy.put("j", "1222");

		/*for (int i = 0; i < 10; i++) {
			for (int j = i; j < 10; j++) {
				String t1 = concepts[i];
				String t2 = concepts[j];
				String c1 = taxonomy.get(t1);
				String c2 = taxonomy.get(t2);
				int d1 = c1.length();
				int d2 = c2.length();
				int dc = Taxonomy.getCommon(c1, c2);
				System.out.print("Sim("
						+ t1
						+ ","
						+ t2
						+ ")= "
						+ Taxonomy.format(Taxonomy.simWuAndPalmer(
								d1, d2, dc)));
				// System.out.print(SimilarityUtil.format(SimilarityUtil.simWuAndPalmer(d1,
				// d2, dc)));
				System.out.print("\t"
						+ Taxonomy.format(Taxonomy
								.simLi(d1, d2, dc)));
				System.out.print("\t"
						+ Taxonomy.format(Taxonomy
								.simLeacockandChodorow(d1, d2, dc, 4)));
				System.out.print("\t"
						+ Taxonomy.format(Taxonomy.simRada(d1, d2,
								dc, 4)));
				System.out.println("\t"
						+ Taxonomy.format(Taxonomy.simCGM(d1, d2,
								dc)));

			}*/
	//	}

	}
	
	@Test public void testTree(){
		
		TaxonomyTree tree = new TaxonomyTree();
		System.out.println("The binary tree");
		tree.printTree(tree.buildBinaryTree());
		System.out.println("\n"+"The results \n"+"concepts"+"\t"+"Rank"+"\t"+
		"W&P"+"\t"+"Li"+"\t"+"L&C"+"\t"+"Rada"+"\t"+"CGM");
		tree.travel(tree.getNodebyLabel("112"));
		
	}
	

	
}
