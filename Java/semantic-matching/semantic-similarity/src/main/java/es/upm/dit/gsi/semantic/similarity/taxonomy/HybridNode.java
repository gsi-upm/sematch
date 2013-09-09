package es.upm.dit.gsi.semantic.similarity.taxonomy;

import java.util.ArrayList;
import java.util.List;

public class HybridNode {
	
	public HybridNode(){}
	
	public static List<Double> generateAlphas(double start, double end, double step){
		List<Double> alphas = new ArrayList<Double>();
		double alpha = start;
		while(alpha<=end){
			alpha = Math.round(alpha*100.0)/100.0;
			alphas.add(alpha);
			alpha = alpha+step;
		}
		return alphas;
	}
	
	public static double weightedSum(double sim1, double sim2, double alpha){
		sim1 = sim1*alpha;
		sim2 = (1-alpha)*sim2;
		return sim1+sim2;
	}
	
	
	public static double weightedProduct(double sim1, double sim2, double alpha){
		sim1 = Math.pow(sim1,alpha);
		sim2 = Math.pow(sim2, 1-alpha);
		return sim1*sim2;
	}
	
	public static double weightedF(double sim1, double sim2, double alpha){
		double up = alpha*alpha;
		double down = up;
		up = 1 + up;
		up = up*sim1*sim2;
		down = down*sim1;
		down = down+sim2;
		return up / down;
	}
	
	
	public static double norm(double v){
		double nv = v+1.0;
		return Math.log(nv)/Math.log(2);
	}
	

}
