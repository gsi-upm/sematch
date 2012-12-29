package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.Resource;

public class Engine {
	
	private SimilarityService similarityService;
	private RepositoryService repositoryService;
	
	public Engine(){
	}
	
	public void execute(){
		for(Resource query : repositoryService.getQueryGraph().getResourceList()){
			for(Resource resource : repositoryService.getResourceGraph().getResourceList()){
				compute(query,resource);
			}
		}
	}

	public void compute(Resource query, Resource resource) {
		similarityService.getSimilarity(query, resource);
		similarityService.printResult(query, resource);
	}
	
	public SimilarityService getSimilarityService() {
		return similarityService;
	}

	public void setSimilarityService(SimilarityService similarityService) {
		this.similarityService = similarityService;
	}

	public RepositoryService getRepositoryService() {
		return repositoryService;
	}

	public void setRepositoryService(RepositoryService repositoryService) {
		this.repositoryService = repositoryService;
	}

}
