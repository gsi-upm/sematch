package es.upm.dit.gsi.semantic.similarity.exceptions;

public class TaxonomyException extends Exception {
	
	private static final long serialVersionUID = 1L;
	
	public TaxonomyException() {
		super();
	}
	
	public TaxonomyException(String msg, Throwable cause) {
		super(msg, cause);
	}
	
	public TaxonomyException(String msg) {
		super(msg);
	}
	
	public TaxonomyException(Throwable cause) {
		super(cause);
	}

}