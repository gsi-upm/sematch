
package es.upm.dit.gsi.semantic.similarity.taxonomy;

import java.net.URI;
import java.net.URISyntaxException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import net.sf.json.JSONObject;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.ResIterator;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;

import es.upm.dit.gsi.semantic.similarity.Repository;
import es.upm.dit.gsi.semantic.similarity.exceptions.TaxonomyException;

public abstract class Taxonomy {

	public static char[] CODE = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
			'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
			'W', 'X', 'Y', 'Z' };
	
	private static final DecimalFormat simFormat = new DecimalFormat("0.0000");

	public static String format(double similarity) {
		return simFormat.format(similarity);
	}
	
	public enum MethodType {
		CGM, WuAndPalm, Rada, LeacockAndChodorow, Li,GSI
	}

	protected Model originModel = null;
	protected Model targetModel = null;
	protected String rootURI = null;
	protected String targetRootURI = null;
	protected String NS = null;
	protected Stack<Resource> stack = null;
	protected Stack<Resource> targetStack = null;
	protected int Max_Depth = 0;
	protected String taxFile = null;
	
	protected Taxonomy(){
		
	}
	
	protected Taxonomy(Model model, String rootURI, String NS) {
		this.originModel = model;
		this.rootURI = rootURI;
		this.NS = NS;
		init();
	}

	protected void init() {
		stack = new Stack<Resource>();
		targetStack = new Stack<Resource>();
		targetModel = ModelFactory.createDefaultModel();
		targetModel.setNsPrefix("skos", SKOS.getURI());
		targetRootURI = NS + CODE[0];
	}
	
	public void initializing(){
		
		this.originModel = Repository.readFromXML(taxFile);
		init();
	}

	public Model formatModel() {
		Resource root = originModel.getResource(rootURI);
		Resource targetRoot = targetModel.createResource(targetRootURI);
		pushChildren(root, targetRoot);
		while (!stack.isEmpty()) {
			Resource source = stack.pop();
			Resource target = targetStack.pop();
			pushChildren(source, target);
		}
		return targetModel;
	}

	public abstract void pushChildren(Resource source, Resource target);

	public int getMaxDepth() {
		if (Max_Depth == 0) {
			Resource root = targetModel.getResource(targetRootURI);
			targetStack.clear();
			computeMaxDepth(root);
			while (!targetStack.isEmpty()) {
				Resource child = targetStack.pop();
				computeMaxDepth(child);
			}
		}
		return this.Max_Depth;
	}

	public void computeMaxDepth(Resource concept) {
		StmtIterator iter = concept.listProperties(SKOS.narrower);
		while (iter.hasNext()) {
			Resource child = iter.nextStatement().getResource();
			String childURI = child.getURI();
			int depth = getDepth(childURI);
			if (depth > this.Max_Depth) {
				this.Max_Depth = depth;
			}
			targetStack.push(child);
		}
	}

	public String getConceptURI(String concept) throws TaxonomyException {

		ResIterator iter = targetModel.listResourcesWithProperty(
				SKOS.prefLabel, concept);
		if (iter.hasNext()) {
			return iter.nextResource().getURI();
		} else
			throw new TaxonomyException("No such concept");
		
	}

	public JSONObject getTaxonomyAsJSON() {
		return getTaxonomyAsJSON(targetModel, targetRootURI);
	}

	public JSONObject getTaxonomyAsJSON(Model taxonomy, String rootConcept) {

		Stack<Resource> stack = new Stack<Resource>();
		Resource root = taxonomy.getResource(rootConcept);
		Map<String, Object> rootJSON = new HashMap<String, Object>();
		Stack<Map<String, Object>> jsonStack = new Stack<Map<String, Object>>();
		rootJSON.put("name", root.getProperty(SKOS.prefLabel).getString());
		pushAllChildren(stack, jsonStack, root, rootJSON);
		while (!stack.isEmpty()) {
			Resource concept = stack.pop();
			Map<String, Object> json = jsonStack.pop();
			pushAllChildren(stack, jsonStack, concept, json);
		}

		return JSONObject.fromObject(rootJSON);
	}

	public void pushAllChildren(Stack<Resource> stack,
			Stack<Map<String, Object>> jsonStack, Resource concept,
			Map<String, Object> json) {

		if (!(concept.getProperty(SKOS.narrower) == null)) {

			ArrayList<Object> children = new ArrayList<Object>();
			json.put("children", children);
			StmtIterator iter = concept.listProperties(SKOS.narrower);
			while (iter.hasNext()) {
				Resource child = iter.nextStatement().getResource();
				Map<String, Object> jsonChild = new HashMap<String, Object>();
				jsonChild.put("name", child.getProperty(SKOS.prefLabel)
						.getString());
				children.add(jsonChild);
				stack.push(child);
				jsonStack.push(jsonChild);
			}
		}
	}

	// return the depth of the least common ancestor of two concepts
	public static int getCommonDepth(String URI_1, String URI_2) {

		return getCommon(parseURI(URI_1),parseURI(URI_2));
	}
	
	public static int getCommon(String s1, String s2){
		
		char[] concept_1 = s1.toCharArray();
		char[] concept_2 = s2.toCharArray();
		
		int depth_1 = concept_1.length;
		int depth_2 = concept_2.length;

		int common = 0;

		if (depth_1 >= depth_2) {
			for (int i = 0; i < depth_2; i++) {
				if (concept_1[i] != concept_2[i]) {
					common = i;
					return common;
				}
			}
			common = depth_2;
		} else {
			for (int i = 0; i < depth_1; i++) {
				if (concept_1[i] != concept_2[i]) {
					common = i;
					return common;
				}
			}
			common = depth_1;
		}

		return common;
	}

	// return the depth of a node in the taxonomy
	public static int getDepth(String uri) {
		return parseURI(uri).length();
	}

	// extract the fragment of a URI
	public static String parseURI(String nURI) {
		String fragment = null;
		try {
			URI uri = new URI(nURI);
			fragment = uri.getFragment();
		} catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return fragment;
	}


	//CGM milestone methods
	public static double simCGM(int depth_1, int depth_2, int depth_common) {

		// information content values
		
		double ic_1 = 0.5/Math.pow(2, depth_1);
		double ic_2 = 0.5/Math.pow(2, depth_2);
		double ic_common = 0.5/Math.pow(2, depth_common);

		double distance_1_c = ic_common - ic_1;
		double distance_2_c = ic_common - ic_2;
		
		double distance = 0;
		distance = distance_1_c + distance_2_c;

		return 1 - distance;
	}

	// Wu & Palm methods
	public static double simWuAndPalmer(int depth_1, int depth_2, int depth_common) {

		double common = 2.0 * depth_common;
		double fraction = depth_1 + depth_2;

		double sim = common/fraction ;

		return sim;
	}

	// Rada & Resnik
	public static double simRada(int depth_1, int depth_2, int depth_common,int maxDepth) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		double distance = path / (2.0 * maxDepth);
		double sim = 1 - distance;

		return sim;
	}

	// Leacock & Chodorow
	// TODO:The similarity value is not located between 0 and 1. Need to be
	public static double simLeacockandChodorow(int depth_1, int depth_2,int depth_common,int maxDepth) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2 + 1;
		double denominator = -Math.log(1 / (2.0 * maxDepth));
		double sim = -Math.log(path / (2.0 * maxDepth));
		return sim/denominator;

	}

	// Li
	public static double simLi(int depth_1, int depth_2, int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		double l = 0.2*path;
		double simpath = Math.exp(-l);
		double D = 0.6*depth_common;
		double simdepth_up = (Math.exp(D) - Math.exp(-D));
		double simdepth_down = (Math.exp(D) + Math.exp(-D));
		double simdepth = simdepth_up / simdepth_down;
		double result = simpath * simdepth;
		return result;
	}
	
	public String getRootURI() {
		return rootURI;
	}

	public void setRootURI(String rootURI) {
		this.rootURI = rootURI;
	}

	public String getTaxFile() {
		return taxFile;
	}

	public void setTaxFile(String taxFile) {
		this.taxFile = taxFile;
	}
	public String getNS() {
		return NS;
	}

	public void setNS(String nS) {
		NS = nS;
	}
	
	public Model getOriginModel() {
		return originModel;
	}

	public void setOriginModel(Model originModel) {
		this.originModel = originModel;
	}

	public Model getTargetModel() {
		return targetModel;
	}

	public void setTargetModel(Model targetModel) {
		this.targetModel = targetModel;
	}
}
