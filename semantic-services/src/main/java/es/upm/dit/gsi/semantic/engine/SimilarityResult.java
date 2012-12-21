package es.upm.dit.gsi.semantic.engine;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class SimilarityResult {
	
	String value;

	public String getValue() {
		return value;
	}

	public void setValue(String value) {
		this.value = value;
	}
	
}
