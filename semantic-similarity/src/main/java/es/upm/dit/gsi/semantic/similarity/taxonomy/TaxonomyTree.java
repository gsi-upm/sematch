package es.upm.dit.gsi.semantic.similarity.taxonomy;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.Stack;

import es.upm.dit.gsi.semantic.similarity.util.SimilarityUtil;

public class TaxonomyTree {
	
	private int maxDepth = 4;
	private Map<String,Node> index = null;
	private Queue<Node> queue = null;
	private Stack<Node> visited = null;
	private double upwards = 0.9;
	private double downwards = 0.9;
	
	
	public TaxonomyTree(){
		this.index = new HashMap<String,Node>();
		queue = new LinkedList<Node>();
		visited = new Stack<Node>();
	}
	
	
	public void travel(Node node){
		int d1 = node.getLabel().length();
		queue.add(node);
		visited.add(node);
		node.setUp(0);
		node.setDown(0);
		node.rank = 1;
		
		while(!queue.isEmpty()){
			
			Node concept = queue.poll();
			//rankNode(concept,node,false);
			
			int d2 = concept.getLabel().length();
			int dc = Taxonomy.getCommon(node.getLabel(), concept.getLabel());
			String result = computeSimilarity(d1,d2,dc);
			System.out.println(concept.getLabel() + "\t\t" + computeSimilarity(concept) + result);
			
			if (!concept.isLeaf()) {
				for (Node child : concept.getChildren()) {
					path(concept, child, downwards);
				}
			}
			if(!concept.isRoot()){
				Node father = concept.getFather();
				path(concept, father, upwards);
			}
			
		}
	}
	
	public double computeSimilarity(Node node){
		double sim = node.rank;
		sim = sim + 1;
		return Math.log(sim)/Math.log(2);
	}
	
	public void path(Node previous, Node current, double factor){
		
		if (!visited.contains(current)) {
			
			current.rank = previous.rank*factor;
			visited.add(current);
			queue.add(current);
			
		}
	}
	
	public String computeSimilarity(int depth_1, int depth_2, int depnt_c){
		
		String simWuPalm = SimilarityUtil.format(SimilarityUtil.simWuAndPalmer(depth_1, depth_2, depnt_c));
		String simLi = SimilarityUtil.format(SimilarityUtil.simLi(depth_1, depth_2, depnt_c));
		String simLC = SimilarityUtil.format(SimilarityUtil.simLeacockandChodorow(depth_1, depth_2, depnt_c, maxDepth));
		String simRada = SimilarityUtil.format(SimilarityUtil.simRada(depth_1, depth_2, depnt_c, maxDepth));
		String simCGM = SimilarityUtil.format(SimilarityUtil.simCGM(depth_1, depth_2, depnt_c));
		String result = "\t"+simWuPalm+"\t"+simLi+"\t"+simLC+"\t"+simRada+"\t"+simCGM+"\n";
		return result;
	}
	
	/**
	 * Build a binary tree breadth-first.
	 * @return
	 */
	public Node buildBinaryTree(){
		
		Node root = new Node();
		root.setRoot(true);
		root.setDepth(1);
		root.setLabel("1");
		index.put(root.getLabel(), root);
		queue.add(root);
		
		while(!queue.isEmpty()){
			
			Node node = queue.poll();
			if(node.getDepth() < maxDepth){
				node.setLeaf(false);
				Node child1 = new Node();
				child1.setLabel(node.getLabel()+"1");
				index.put(child1.getLabel(), child1);
				Node child2 = new Node();
				child2.setLabel(node.getLabel()+"2");
				index.put(child2.getLabel(), child2);
				child1.setDepth(node.getDepth()+1);
				child2.setDepth(node.getDepth()+1);
				child1.setFather(node);
				child2.setFather(node);
				node.getChildren().add(child1);
				node.getChildren().add(child2);
				queue.add(child1);
				queue.add(child2);
			}else{
				node.setLeaf(true);
			}
		}
		
		return root;
	}
	
	public void printTree(Node root){
		
		queue.add(root);
		System.out.println(root.getLabel());
		int count = 1;
		while(!queue.isEmpty()){
			Node node = queue.poll();
			if(node.getDepth()>count){
				System.out.println();
				count++;
			}
			if(!node.isLeaf()){
				for(Node child:node.getChildren()){
					System.out.print(child.getLabel()+"\t");
					queue.add(child);
				}
			}
		}
	}
	
	public Node getNodebyLabel(String label){
		return index.get(label);
	}
	public void printIndex(){
		for(String key : index.keySet()){
			System.out.println(index.get(key).getLabel());
		}
	}
	

}
