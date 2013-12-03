package es.upm.dit.gsi.sematch.service;

public class Candidate {

	private String uri;
	private String city;
	private String salary;
	private String skill;
	private String level;
	private String sim;

	public String getCity() {
		return city;
	}

	public void setCity(String city) {
		this.city = city;
	}

	public String getSalary() {
		return salary;
	}

	public void setSalary(String salary) {
		this.salary = salary;
	}

	public String getSkill() {
		return skill;
	}

	public void setSkill(String skill) {
		this.skill = skill;
	}

	public String getLevel() {
		return level;
	}

	public void setLevel(String level) {
		this.level = level;
	}

	public String getSim() {
		return sim;
	}

	public void setSim(String sim) {
		this.sim = sim;
	}
	
	public String getUri() {
		return uri;
	}

	public void setUri(String uri) {
		this.uri = uri;
	}

	@Override
	public String toString() {
		return "Candidate [uri=" + uri + ", city=" + city + ", salary="
				+ salary + ", skill=" + skill + ", level=" + level + ", sim="
				+ sim + "]";
	}

}
