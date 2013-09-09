package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import java.util.List;

import org.junit.Ignore;
import org.junit.Test;

import es.upm.dit.gsi.semantic.similarity.taxonomy.HybridNode;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;

public class TestHybridNode {

	@Test
	public void test() {

		double[] conceptSim = { 1.0,0.7,0.48};
		double[] propertySim = {1.0,0.75,0.5};
		List<Double> alphas = HybridNode.generateAlphas(0.01d, 0.99d, 0.01d);
		
		for (int j = 0; j < conceptSim.length; j++) {
			for (int k = 0; k < propertySim.length; k++) {
				for(Double alpha: alphas){
					double simSum = HybridNode.weightedSum(conceptSim[j],
							propertySim[k], alpha);
					System.out.print(Taxonomy.format(simSum)+"\t");
				}
				
				for(Double alpha: alphas){
					double simSum = HybridNode.weightedProduct(conceptSim[j],
							propertySim[k], alpha);
					System.out.print(Taxonomy.format(simSum)+"\t");
				}
				
				for(Double alpha: alphas){
					double simSum = HybridNode.weightedF(conceptSim[j],
							propertySim[k], alpha);
					System.out.print(Taxonomy.format(simSum)+"\t");
				}
				
				System.out.println();
			}
		}

	}

}
