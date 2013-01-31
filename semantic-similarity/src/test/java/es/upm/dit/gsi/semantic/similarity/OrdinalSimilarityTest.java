package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Ignore;
import org.junit.Test;

import es.upm.dit.gsi.semantic.similarity.compute.OrdinalSimilarityCompute;

public class OrdinalSimilarityTest {
	
	OrdinalSimilarityCompute simCompute = new OrdinalSimilarityCompute();

	@Ignore
	public void testSemmf() {
		simCompute.setAlpha(0.25);
		for(int i=1;i<=3;i++){
			for(int j=1;j<=3;j++)
			{
				System.out.print(simCompute.computeSemmf(i, j)+"\t");
			}
			System.out.println();
		}
	}
	
	@Test
	public void testLin(){
		
		double[] distribution = {0.09,0.16,0.28,0.47};
		
		simCompute.setDistribution(distribution);
		
		for(int i=1;i<=distribution.length;i++){
			for(int j=1;j<=distribution.length;j++)
			{
				System.out.print(simCompute.computeLin(i, j)+"\t");
			}
			System.out.println();
		}
	}
	
	@Ignore
	public void testGSI() {
		simCompute.setMaxLevel(3);
		for(int i=1;i<=3;i++){
			for(int j=1;j<=3;j++)
			{
				System.out.print(simCompute.computeGSI(i, j)+"\t");
			}
			System.out.println();
		}
	}
	
	@Ignore
	public void testSigmoid(){
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++)
			{
				System.out.print(simCompute.computeSigmoid(i, j)+"\t");
			}
			System.out.println();
		}
	}

}
