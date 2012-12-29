package es.upm.dit.gsi.semantic.similarity;

import org.apache.log4j.Logger;

public class RepositoryService {

	public Logger logger = Logger.getLogger(this.getClass());
	
	private Graph queryGraph;
	private Graph resourceGraph;
	
	public RepositoryService(){}

	public Graph getQueryGraph() {
		return queryGraph;
	}

	public void setQueryGraph(Graph queryGraph) {
		this.queryGraph = queryGraph;
	}

	public Graph getResourceGraph() {
		return resourceGraph;
	}

	public void setResourceGraph(Graph resourceGraph) {
		this.resourceGraph = resourceGraph;
	}
}
