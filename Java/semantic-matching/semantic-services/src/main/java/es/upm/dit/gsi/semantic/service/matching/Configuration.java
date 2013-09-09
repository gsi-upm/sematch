package es.upm.dit.gsi.semantic.service.matching;


import java.util.List;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.HierarchicalConfiguration;
import org.apache.commons.configuration.XMLConfiguration;

import es.upm.dit.gsi.semantic.search.QueryConfig;



/**
 * Configuration class, used to parse the configuration xml file.
 * @author gzhu
 *
 */
public class Configuration {

	private QueryConfig queryConfig = null;
	private XMLConfiguration config = null;
	private static Configuration configuration = null;
	
	
	//singleton pattern
	public static Configuration getConfiguration(){
		if(configuration == null){
			System.out.println("init configuration");
			configuration = new Configuration();
		}
		return configuration;
	}

	public Configuration() {
		
		try {
			config = new XMLConfiguration("system-config.xml");
		} catch (ConfigurationException cex) {
			cex.printStackTrace();
		}
		
	}
	
	public QueryConfig getQueryConfig() {

		if (queryConfig == null) {
			queryConfig = new QueryConfig();
			List<HierarchicalConfiguration> fields = 
					config.configurationsAt("matching.query.field");
			queryConfig.setResultSize(config.getInt("matching.results.size"));
	
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
