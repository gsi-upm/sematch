package es.upm.dit.gsi.sematch.service;

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

import net.sf.json.JSONObject;
import es.upm.dit.gsi.sematch.service.Matching;

@Path("/job")
public class JobMatchingService {

	@Context
	ServletContext context;
	
	public JobMatchingService(){}

	@GET
	@Path("/search")
	@Produces(MediaType.APPLICATION_JSON)
	public List<MatchResult> getCandidateJSON(@Context UriInfo info) {
		
		String queryString = info.getQueryParameters().getFirst("q");
		JSONObject json = JSONObject.fromObject(queryString);
		String skills = json.getJSONArray("episteme.search.new_search").getJSONObject(0)
				.getJSONArray("result").getJSONObject(0).getJSONArray("semantic").toString();
		System.out.println(skills);
		Map<String,Object> query = new HashMap<String,Object>();
		query.put("skill", skills);
		
		List<Map<String,String>> results = Matching.getMatching().search(query);
		
		List<MatchResult> matches = new ArrayList<MatchResult>();
		
		for(Map<String,String> result : results){
			MatchResult match = new MatchResult();
			match.setUrl(result.get("uri"));
			match.setSim(result.get("sim"));
			matches.add(match);
		}
		
		return matches;
	}
	

}
