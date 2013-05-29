package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import java.util.ArrayList;

import org.junit.Test;

import es.upm.dit.gsi.semantic.similarity.taxonomy.HybridNode;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;


public class TestHybridNode {

	@Test
	public void test() {
		
		double[] conceptSim = {1.0,0.54,0.2916};
		double[] propertySim = {1.0,0.807,0.585};
		ArrayList<HybridNode> nodeList = new ArrayList<HybridNode>();
		
		int identifier = 1;
		
		for(int i=0;i<3;i++){
			for(int j=0;j<3;j++){
				HybridNode node = new HybridNode();
				node.setLabel(""+identifier++);
				node.setConceptSim(conceptSim[i]);
				node.setPropertySim(propertySim[j]);
				nodeList.add(node);
			}
		}
		
		
		System.out.println("MaxC: " +(1-0.369)+ "MinC: "+(1 - 0.623)+ " "+ (0.623 - 0.369));
		System.out.println((1 - 0.585)+" "+(1-0.807)+ " "+(0.807-0.585));
		double f1 = 0.193/(0.631 + 0.193);
		double f2 = 0.415/(0.415+0.254);
		System.out.println("Lower "+f1);
		System.out.println("Upper "+f2);
		
		System.out.println("Label\t SimC\t SimP\t L\t H\t C");
		for(HybridNode node : nodeList){
			System.out.println(node.getLabel()+
					//"\t"+SimilarityUtil.format(node.getConceptSim())+
					//"\t"+SimilarityUtil.format(node.getPropertySim())+
					"\t"+Taxonomy.format(node.combineSimilarity(0.2))+
					"\t"+Taxonomy.format(node.combineSimilarity(0.4))+
					"\t"+Taxonomy.format(node.combineSimilarity(0.7)));
		}
	}

}
