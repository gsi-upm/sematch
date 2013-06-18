package es.upm.dit.gsi.semantic.webService;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.UriInfo;

import es.upm.dit.gsi.semantic.search.QueryConfig;
import es.upm.dit.gsi.semantic.service.matching.Configuration;
import es.upm.dit.gsi.semantic.service.matching.Matching;
import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;

@Path("/search")
public class SemanticSearchService {

	@Context
	ServletContext context;
	
	public SemanticSearchService(){}

	@GET
	@Path("/query")
	@Produces(MediaType.APPLICATION_JSON)
	public List<Candidate> getCandidateJSON(@Context UriInfo info) {
		
		HashMap<String,String> query = new HashMap<String,String>();
		QueryConfig queryConfig = Configuration.getConfiguration().getQueryConfig();
		
		for(String field : queryConfig.getQueryFileds()){
			query.put(field, info.getQueryParameters().getFirst(field));
		}
		
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
		
		return candidates;
		
	}
	

}
