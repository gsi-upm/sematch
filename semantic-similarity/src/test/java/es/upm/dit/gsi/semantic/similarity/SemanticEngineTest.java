package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SemanticEngineTest {

	@Test
	public void test() {

		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/config.xml");
		Engine engine = context.getBean("Engine", Engine.class);
		engine.execute();
	}

}
