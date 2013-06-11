package es.upm.dit.gsi.semantic.webService;

import java.util.List;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;

@Path("/similarity")
public class SimilarityServices {

	@Context
	ServletContext context;
	
	public SimilarityServices(){
		
	}

	//@GET
	//@Path("{c1}/{c2}")
	//@Produces({ MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML })
	/*public List<SimilarityResult> similarity(@PathParam("c1") String concept_1,
			@PathParam("c2") String concept_2) {
		
		//System.out.println(context.getRealPath("/"));
		//return engine.pairwiseSimilarity(concept_1, concept_2, context.getRealPath("/"));
		//return null;
		//response.s
		return engine.pairwiseSimilarity(concept_1, concept_2);
	}*/
	

}
