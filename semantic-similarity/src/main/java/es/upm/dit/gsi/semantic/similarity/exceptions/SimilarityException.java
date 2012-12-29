package es.upm.dit.gsi.semantic.similarity.exceptions;

public class SimilarityException extends Exception {
	
	private static final long serialVersionUID = 1L;
	
	public SimilarityException() {
		super();
	}
	
	public SimilarityException(String msg, Throwable cause) {
		super(msg, cause);
	}
	
	public SimilarityException(String msg) {
		super(msg);
	}
	
	public SimilarityException(Throwable cause) {
		super(cause);
	}
}