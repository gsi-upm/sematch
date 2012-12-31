package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Ignore;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SemanticEngineTest {

	@Test
	public void test() {

		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/config.xml");
		Engine engine = context.getBean("Engine", Engine.class);
		engine.init();
		engine.execute();
		engine.print();
	}
	
	@Ignore
	public void testTaxonomy(){
		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/config.xml");
		SemanticGraph graph = context.getBean("taxonomy",SemanticGraph.class);
		graph.getModelFromLocal().write(System.out);
	}

}
