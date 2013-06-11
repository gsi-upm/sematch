package es.upm.dit.gsi.semantic.similarity.taxonomy;

public class HybridNode {
	
	private String label;
	private double conceptSim;
	private double propertySim;
	
	public HybridNode(){}
	
	public String getLabel() {
		return label;
	}
	public void setLabel(String label) {
		this.label = label;
	}
	public double getConceptSim() {
		return norm(conceptSim);
	}
	public void setConceptSim(double conceptSim) {
		this.conceptSim = conceptSim;
	}
	public double getPropertySim() {
		return propertySim;
	}
	public void setPropertySim(double propertySim) {
		this.propertySim = propertySim;
	}
	
	public double combineSimilarity(double alpha){
		double sim1 = getConceptSim();
		double sim2 = getPropertySim();
		sim1 = alpha*sim1;
		sim2 = (1-alpha)*sim2;
		return sim1+sim2;
	}
	
	
	public double average(){
		double sum = this.getConceptSim()+ this.getPropertySim();
		return sum/2;
	}
	
	public double weightedNorm(){
		double c = norm(getConceptSim());
		double p = norm(getPropertySim());
		double sum = 0.8*p+0.2*c;
		return sum;
	}
	
	public double weighted(){
		double c = getConceptSim();
		double p = getPropertySim();
		c = c*0.8;
		p = p*0.2;
		double h = p+c;
		return h;
	}
	
	public double times(){
		double c = conceptSim;
		double p = propertySim;
		
		c = Math.pow(c, 2);
		return p*c;
	}
	
	public double getConceptSimNorm(){
		return norm(conceptSim);
	}
	
	public double getPropertySimNorm(){
		return norm(propertySim);
	}
	
	public double norm(double v){
		double nv = v+1.0;
		return Math.log(nv)/Math.log(2);
	}
	

}
