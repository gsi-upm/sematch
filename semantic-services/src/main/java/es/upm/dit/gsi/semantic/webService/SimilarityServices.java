package es.upm.dit.gsi.semantic.webService;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import es.upm.dit.gsi.semantic.engine.SimilarityEngine;

@Path("/similarity")
public class SimilarityServices {
	
	@GET
	@Path("{c1}/{c2}")
	@Produces({ MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML })
	public String similarity(@PathParam("c1") String concept_1,@PathParam("c2") String concept_2 ) {
		return SimilarityEngine.pairwiseSimilarity(concept_1, concept_2);
	}

}
