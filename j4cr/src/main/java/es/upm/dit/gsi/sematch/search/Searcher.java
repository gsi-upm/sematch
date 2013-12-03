package es.upm.dit.gsi.sematch.search;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.Directory;

public class Searcher {

	private IndexSearcher searcher = null;
	private IndexReader reader = null;
	private int resultSize = 0;

	public Searcher(Directory directory) {
		try {
			reader = IndexReader.open(directory);
			searcher = new IndexSearcher(reader);
		} catch (CorruptIndexException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public ArrayList<Map<String,String>> search(SemanticQuery query) {
		
		ArrayList<Map<String,String>> results = new ArrayList<Map<String,String>>();
		
		try {
			ScoreDoc[] docs = searcher.search(query, resultSize).scoreDocs;
			Document hitDoc = null;
			for (int i = 0; i < docs.length; i++) {
				
				hitDoc = searcher.doc(docs[i].doc);
				Map<String,String> result = new HashMap<String,String>();
				result.put("uri",hitDoc.get("uri"));
				result.put("sim", ""+docs[i].score);
				
				for(String field: query.getQueryConfig().getFileds()){
					result.put(field, hitDoc.get(field));
				}
				results.add(result);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return results;
	}

	public void close() {
		if (searcher != null) {
			try {
				searcher.close();
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public int getResultSize() {
		return resultSize;
	}

	public void setResultSize(int resultSize) {
		this.resultSize = resultSize;
	}

}
