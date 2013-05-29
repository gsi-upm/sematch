package es.upm.dit.gsi.semantic.search;

import java.io.IOException;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.Directory;

public class Searcher {

	private IndexSearcher searcher = null;
	private IndexReader reader = null;
	private int resultNumber= 0;

	public IndexSearcher getIndexSearcher(Directory directory) {

		if (searcher == null) {
			try {
				reader = IndexReader.open(directory);
				searcher = new IndexSearcher(reader);
			} catch (CorruptIndexException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return searcher;
	}
	
	public void search(Query query){
		try {
			ScoreDoc[] docs = searcher.search(query, 100).scoreDocs;
			Document hitDoc = null;
			for(int i=0;i<docs.length;i++){
				hitDoc = searcher.doc(docs[i].doc);
				System.out.println(hitDoc.get("resURI")+ ": skill" +
						hitDoc.get("skill") +
						" : level" +hitDoc.get("level") +
						" score= " + docs[i].score);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void closeSemanticSearcher() {
		if (searcher != null) {
			try {
				searcher.close();
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

}
