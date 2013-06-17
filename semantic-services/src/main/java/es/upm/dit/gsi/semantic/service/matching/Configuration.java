package es.upm.dit.gsi.semantic.service.matching;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.HierarchicalConfiguration;
import org.apache.commons.configuration.XMLConfiguration;

import es.upm.dit.gsi.semantic.search.IndexConfig;
import es.upm.dit.gsi.semantic.search.QueryConfig;



/**
 * Configuration class, used to parse the configuration xml file.
 * @author gzhu
 *
 */
public class Configuration {

	private IndexConfig indexConfig = null;
	private QueryConfig queryConfig = null;
	private XMLConfiguration config = null;

	public Configuration() {
		
		try {
			config = new XMLConfiguration("system-config.xml");
		} catch (ConfigurationException cex) {
			cex.printStackTrace();
		}
		
	}

	//configuring the settings of indexing
	public IndexConfig getIndexConfig() {

		if (indexConfig == null) {
			indexConfig = new IndexConfig();
			List<HierarchicalConfiguration> fields = 
					config.configurationsAt("indexing.fields.field");
			indexConfig.setType(config.getString("indexing.repository.type"));
			indexConfig.setLocalFile(config.getString("indexing.repository.local.file"));
			indexConfig.setRemoteUrl(config.getString("indexing.repository.remote.url"));
			indexConfig.setQuery(config.getString("indexing.repository.remote.query"));
			Map<String,String> fieldMap = new HashMap<String,String>();
			ArrayList<String> labels = new ArrayList<String>();
			for (HierarchicalConfiguration sub : fields) {
				String label = sub.getString("label");
				String resource = sub.getString("resource");
				labels.add(label);
				fieldMap.put(label,resource);
			}
			indexConfig.setFieldMap(fieldMap);
			indexConfig.setFields(labels);
		}
		return indexConfig;
	}
	
	public QueryConfig getQueryConfig() {

		if (queryConfig == null) {
			queryConfig = new QueryConfig();
			List<HierarchicalConfiguration> fields = 
					config.configurationsAt("searching.query.field");
			queryConfig.setResultSize(config.getInt("searching.results.size"));
	
			for (HierarchicalConfiguration sub : fields) {
				queryConfig.addField(sub.getString("label"));
			}
		}
		
		return queryConfig;
	}

	public String getSimConfig(){
		return config.getString("similarity.config");
	}

	public String getSimBean(){
		return config.getString("similarity.bean");
	}
	


	
}
