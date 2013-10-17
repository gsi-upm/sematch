package es.upm.dit.gsi.sematch.search;

import java.io.IOException;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.LockObtainFailedException;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;

public class Indexer {

	private Directory directory = null;
	private Analyzer analyzer = null;
	private IndexWriter writer = null;
	private IndexWriterConfig config = null;

	public Indexer() {
	}

	public IndexWriter getIndexWriter() {

		if (writer == null) {
			directory = new RAMDirectory();
			analyzer = new StandardAnalyzer(Version.LUCENE_36);
			config = new IndexWriterConfig(Version.LUCENE_36, analyzer);
			try {
				writer = new IndexWriter(directory, config);
			} catch (CorruptIndexException e) {
				e.printStackTrace();
				return null;
			} catch (LockObtainFailedException e) {
				e.printStackTrace();
				return null;
			} catch (IOException e) {
				e.printStackTrace();
				return null;
			}
		}
		return writer;
	}

	public void closeDirectory() {
		if (directory != null) {
			try {
				directory.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public Directory getDirectory() {
		return directory;
	}

	public Analyzer getAnalyzer() {
		return analyzer;
	}

	public void closeIndexWriter() {
		if (writer != null) {
			try {
				writer.close();
			} catch (CorruptIndexException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public void indexDocument(Document doc) {

		try {
			writer.addDocument(doc);
		} catch (CorruptIndexException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
