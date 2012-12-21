package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Ignore;
import org.junit.Test;

public class RDFUtilTest {

	static final String ict_service = "dataset/ICT_Service.owl";
	static final String acm_clasification = "dataset/acm-classification.xml";
	static final String gics = "dataset/GICS2010.rdf";
	static final String resource = "http://gsi.dit.upm.es/gzhu/ontologies/2012/12/GICS#1";
	static final String leaf = "http://gsi.dit.upm.es/gzhu/ontologies/2012/12/GICS#1111";
	static final String acmInfoRoot = "#10002951";
	static final String ictservice = "http://gsi.dit.upm.es/gzhu/2012/12/Enterprise-Skills#1";
	static final String acmOutFileName = "result/acm-information-system.rdf";
	static final String NS = "http://gsi.dit.upm.es/gzhu/ontologies/2012/12/ACM#";

	@Ignore
	public void testSkosFormating() {
		RDFFileUtil.writeRDFToXML(RDFFileUtil.formatSkosResourceURI(acm_clasification,
				acmInfoRoot, NS), acmOutFileName);
	}

}
