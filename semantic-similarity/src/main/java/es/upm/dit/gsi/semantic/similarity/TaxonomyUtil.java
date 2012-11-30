package es.upm.dit.gsi.semantic.similarity;

import java.net.URI;
import java.net.URISyntaxException;

/**
 * Several util methods are implemented here to parse the uri, to calculate the
 * depth of the concpets and least common ancestor.
 * 
 * @author gzhu
 * 
 */
public class TaxonomyUtil {

	public TaxonomyUtil(){}
	
	// return the depth of the least common ancestor of two concepts
	public static int getCommonDepth(String URI_1, String URI_2) {
		
		char[] concept_1 = TaxonomyUtil.parseURI(URI_1).toCharArray();
		char[] concept_2 = TaxonomyUtil.parseURI(URI_2).toCharArray();

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
		return TaxonomyUtil.parseURI(uri).length();
	}

	//extract the fragment of a URI
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

}
