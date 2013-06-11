package es.upm.dit.gsi.semantic.matching;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.HierarchicalConfiguration;
import org.apache.commons.configuration.XMLConfiguration;

import es.upm.dit.gsi.semantic.search.IndexConfig;
import es.upm.dit.gsi.semantic.search.SearchConfig;

/**
 * Configuration class, used to parse the configuration xml file.
 * @author gzhu
 *
 */
public class Configuration {

	private IndexConfig indexConfig = null;
	private SearchConfig searchConfig = null;
	private XMLConfiguration config = null;

	public Configuration() {
		try {
			config = new XMLConfiguration("system-config.xml");
		} catch (ConfigurationException cex) {
			cex.printStackTrace();
		}
	}

	public IndexConfig getIndexConfig() {

		if (indexConfig == null) {
			List<HierarchicalConfiguration> fields = 
					config.configurationsAt("indexing.fields.field");
			indexConfig = new IndexConfig();
			indexConfig.setLocalFile(config.getString(
					"indexing.respository.local.file"));
			indexConfig.setRemoteUrl(config.getString(
					"indexing.repository.remote.url"));
			indexConfig.setQuery(config.getString(
					"indexing.repository.remote.query"));
			Map<String,String> fieldMap = new HashMap<String,String>();
			for (HierarchicalConfiguration sub : fields) {
				String label = sub.getString("label");
				String resource = sub.getString("resource");
				fieldMap.put(label,resource);
			}
			indexConfig.setFieldMap(fieldMap);
		}
		return indexConfig;
	}

	public void setIndexConfig(IndexConfig indexConfig) {
		this.indexConfig = indexConfig;
	}

	public SearchConfig getSearchConfig() {
		return searchConfig;
	}

	public void setSearchConfig(SearchConfig searchConfig) {
		this.searchConfig = searchConfig;
	}
	
	public String getSimConfig(){
		return config.getString("similarity.config");
	}

	public String getSimBean(){
		return config.getString("similarity.bean");
	}
}
