package es.upm.dit.gsi.sematch.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.UriInfo;

import net.sf.json.JSONObject;

import es.upm.dit.gsi.sematch.service.Matching;
import es.upm.dit.gsi.sematch.similarity.taxonomy.Taxonomy;

@Path("/semantic")
public class SemanticSearchService {

	@Context
	ServletContext context;
	
	public SemanticSearchService(){}

	@GET
	@Path("/search")
	@Produces(MediaType.APPLICATION_JSON)
	public List<Candidate> getCandidateJSON(@Context UriInfo info) {
		
		/*String queryString = info.getQueryParameters().getFirst("q");
		JSONObject json = JSONObject.fromObject(queryString);
		Map<String,Object> query = (Map<String,Object>) json;
		
		List<Map<String,String>> results = Matching.getMatching().search(query);
		
		List<Candidate> candidates = new ArrayList<Candidate>();
		
		for(Map<String,String> result : results){
			Candidate candidate = new Candidate();
			candidate.setUri(Taxonomy.parseURI(result.get("uri")));
			candidate.setSim(result.get("sim"));
			candidate.setCity(result.get("city"));
			candidate.setSalary(result.get("salary"));
			candidate.setSkill(result.get("skill"));
			candidate.setLevel(result.get("level"));
			candidates.add(candidate);
		}
		*/
		return null;
	}
	

}
