package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Test;

import es.upm.dit.gsi.semantic.similarity.compute.LevelSimilarityCompute;
import es.upm.dit.gsi.semantic.similarity.type.MatchingMode;

public class MatchingTest {
	
	LevelSimilarityCompute simCompute = new LevelSimilarityCompute();

	@Test
	public void test() {
		
		simCompute.setDeviation(0.25);
		System.out.println("Exact");
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Exact);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
		
		System.out.println("\n Close");
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Close);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
		
		System.out.println("\n Broad");
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Broad);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
		
		System.out.println("\n Narrow");
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Narrow);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
		
		System.out.println("\n Broad Related");
		simCompute.setDirection(MatchingMode.Broad);
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Related);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
		
		System.out.println("\n Narrow Related");
		simCompute.setDirection(MatchingMode.Narrow);
		for(int i=1;i<=4;i++){
			for(int j=1;j<=4;j++){
				simCompute.setMode(MatchingMode.Related);
				System.out.print(simCompute.computeSimilarity(i, j)+"\t");
			}
			System.out.println();
		}
	}

}
