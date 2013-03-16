package es.upm.dit.gsi.semantic.similarity;

import static org.junit.Assert.*;

import org.junit.Ignore;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.hp.hpl.jena.rdf.model.Resource;

public class SemanticEngineTest {

	@Ignore
	public void testSemmfConfig() {

		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/semmf-config.xml");
		Engine engine = context.getBean("Engine", Engine.class);
		engine.init();
		engine.execute();
		engine.print();
	}
	
	@Ignore
	public void testGSIConfig(){
		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/gsi-config.xml");
		Engine engine = context.getBean("Engine", Engine.class);
		engine.init();
		engine.execute();
		engine.print();
	}
	
	@Test
	public void testEmployConfig(){
		ApplicationContext context = new ClassPathXmlApplicationContext(
				"config/employ-config.xml");
		Engine engine = context.getBean("Engine", Engine.class);
		engine.init();
		engine.execute();
		engine.print();
	}

}
