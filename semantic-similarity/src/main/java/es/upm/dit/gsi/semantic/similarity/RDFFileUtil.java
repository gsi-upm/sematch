package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.util.FileManager;
import com.hp.hpl.jena.vocabulary.RDF;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;
import net.sf.json.JSONObject;

public class RDFFileUtil {

	public static char[] RESOURCE_CODE = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
			'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
			'X', 'Y', 'Z' };

	/**
	 * This method is used to formalize the skos concept resource URI. In our
	 * similarity measurement, the least common ancestor is established by
	 * processing the concept resource URI. Moreover, the depth and the path length
	 * are also calculated from the URI. Thus the URI should be formalized.
	 */
	public static Model formatSkosResourceURI(String skosFileName,
			String rootConcept, String NS) {

		Model sourceModel = readRDFFromXML(skosFileName);
		Model targetModel = ModelFactory.createDefaultModel();
		targetModel.setNsPrefix("skos", SKOS.getURI());

		Resource sourceRoot = sourceModel.getResource(rootConcept);
		Resource targetRoot = targetModel.createResource(NS + RESOURCE_CODE[0]);
		Stack<Resource> srcStack = new Stack<Resource>();
		Stack<Resource> tarStack = new Stack<Resource>();
		pushChildren(srcStack, tarStack, sourceRoot, targetRoot, targetModel);

		while (!srcStack.isEmpty()) {
			Resource sChi = srcStack.pop();
			Resource tChi = tarStack.pop();
			pushChildren(srcStack, tarStack, sChi, tChi, targetModel);
		}

		return targetModel;
	}
	
	public static void writeRDFToXML(Model model, String fileName){
		
		File file = null;
		FileOutputStream out = null;
		try {
			file = new File(fileName);
			out = new FileOutputStream(file);
			if(!file.exists()){
				file.createNewFile();
			}
			model.write(out);
			out.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}

	public static void pushChildren(Stack<Resource> srcStack,
			Stack<Resource> tarStack, Resource source, Resource target,
			Model targetModel) {

		target.addProperty(RDF.type, SKOS.Concept);
		target.addProperty(SKOS.prefLabel, targetModel.createLiteral(source.getProperty(SKOS.prefLabel)
				.getString(), "en"));

		StmtIterator iter = source.listProperties(SKOS.narrower);
		int i = 0;
		while (iter.hasNext()) {
			Resource srcChild = iter.nextStatement().getResource();
			Resource targetChild = targetModel.createResource(target.getURI()
					+ RESOURCE_CODE[i++]);
			targetChild.addProperty(SKOS.broader, target);
			target.addProperty(SKOS.narrower, targetChild);
			srcStack.push(srcChild);
			tarStack.push(targetChild);
		}

	}

	// generate a json file for viewing.
	public static void generateJson(String skosFileName, String rootResource,
			String jsonFileName) {
		Model skosModel = readRDFFromXML(skosFileName);
		Resource rootConcept = skosModel.getResource(rootResource);
		writeJSON(generateMapObject(rootConcept), jsonFileName);
	}

	public static Model readRDFFromXML(String fileName) {
		Model model = ModelFactory.createDefaultModel();
		InputStream in = FileManager.get().open(fileName);
		if (in == null) {
			throw new IllegalArgumentException("File: " + fileName
					+ " not found");
		}
		
		model.read(in, "");
		return model;
	}

	// store the json to persistent file.
	public static void writeJSON(Map<String, Object> map, String jsonFileName) {
		JSONObject json = JSONObject.fromObject(map);
		JSONUtil.write(jsonFileName, json);
	}

	// traverse the skos tree in depth first order.
	public static Map<String, Object> generateMapObject(Resource root) {

		Stack<Resource> mainStack = new Stack<Resource>();
		Map<String, Object> rootMap = new HashMap<String, Object>();
		Stack<Resource> workStack = new Stack<Resource>();
		Stack<Map<String, Object>> mapStack = new Stack<Map<String, Object>>();
		mainStack.push(root);
		pushAllChildren(workStack, mapStack, root, rootMap);
		while (!workStack.isEmpty()) {
			Resource concept = workStack.pop();
			Map<String, Object> mapConcept = mapStack.pop();
			mainStack.push(concept);
			pushAllChildren(workStack, mapStack, concept, mapConcept);
		}
		return rootMap;
	}

	// push all the children of a concept into stack.
	public static void pushAllChildren(Stack<Resource> work,
			Stack<Map<String, Object>> mapStack, Resource concept,
			Map<String, Object> mapConcept) {

		if (!isLeaf(concept)) {
			mapConcept.put("name", concept.getProperty(SKOS.prefLabel)
					.getString());
			ArrayList<Object> children = new ArrayList<Object>();
			mapConcept.put("children", children);
			StmtIterator iter = concept.listProperties(SKOS.narrower);
			while (iter.hasNext()) {

				Resource child = iter.nextStatement().getResource();
				work.push(child);
				Map<String, Object> childMap = new HashMap<String, Object>();
				childMap.put("name", child.getProperty(SKOS.prefLabel)
						.getString());
				mapStack.push(childMap);
				children.add(childMap);
			}
		}
	}

	// check if the concept is a leaf concept
	public static boolean isLeaf(Resource concept) {
		if (concept.getProperty(SKOS.narrower) == null)
			return true;
		else
			return false;
	}

}
