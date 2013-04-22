package es.upm.dit.gsi.semantic.similarity.measure;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.StmtIterator;

public class HybridMeasure extends AtomicMeasure {

	private Logger logger = Logger.getLogger(this.getClass());

	/**
	 * max average methods.
	 */
	@Override
	public double getSimilarity(Resource query, Resource resource) {

		Property pQ = query.getModel().getProperty(getQueryURI());
		Property pR = resource.getModel().getProperty(getResourceURI());

		StmtIterator stmtIt = query.listProperties(pQ);
		List<RDFNode> qList = new ArrayList<RDFNode>();

		while (stmtIt.hasNext()) {
			RDFNode node = stmtIt.nextStatement().getObject();
			qList.add(node);
		}

		List<RDFNode> rList = new ArrayList<RDFNode>();
		stmtIt = resource.listProperties(pR);
		while (stmtIt.hasNext()) {
			RDFNode node = stmtIt.nextStatement().getObject();
			rList.add(node);
		}

		// choose the max similarity then average
		List<Double> simList = new ArrayList<Double>();
		List<Double> tempList = new ArrayList<Double>();
		
		for (RDFNode queryNode : qList) {
			tempList.clear();
			for (RDFNode resourceNode : rList) {
				Double sim = new Double(getSimCompute().compute(queryNode, resourceNode));
				tempList.add(sim);
			}
			simList.add(Collections.max(tempList).doubleValue());
		}
		int totalNo = simList.size();
		double sumSim = 0;
		for(int i=0;i<totalNo;i++){
			sumSim = sumSim + simList.get(i).doubleValue();
		}
		double similarity = sumSim/totalNo;
		logger.info(label + " Weight: " + weight+ "	Sim: " + similarity);
		return similarity*getWeight();
	}

}
