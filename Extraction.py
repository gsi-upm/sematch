#Use the multiprocessing to extract the interested rdfs from the raw
#geodata.
from bs4 import BeautifulSoup
import bs4
import urllib2
import json
import re
import csv
import multiprocessing
import re
import gc


#city name scraping from geonames
def extract_cities_from_geonames_web():
	geoname = "http://www.geonames.org"
	path = "/search.html?q=&country=ES"
	count = 1
	cities = []
	while count < 102:
		print str(count) + geoname + path
		page = urllib2.urlopen(geoname+path).read()
		soup = BeautifulSoup(page)
		table = soup.find("table",{"class":"restable"})
		for row in table.findAll("tr"):
			cells = row.findAll("td")
			if len(cells) == 6:
				geoURL = cells[0].a["href"]
				links = cells[1].findAll("a")
				name = links[0].text
				if len(links) == 2:
					wikiURL = links[1]["href"]
				else:
					wikiURL = None
				latitude = cells[1].find("span",{"class":"latitude"}).text
				longitude =  cells[1].find("span",{"class":"longitude"}).text
				hierarchy = cells[2].contents
				if len(hierarchy) == 5:
					automous = hierarchy[1].replace(", ","").encode('utf-8')
					province = hierarchy[3].text.encode('utf-8')
					hierarchy = automous+" > "+province
					hierarchy = hierarchy.decode('utf-8')
				else:
					hierarchy = None
				feature = cells[3].text
				city = {"name":name, "geoURL":geoURL,
				 "wikiURL":wikiURL,"lat":latitude,"lon":longitude,
				 "hierarchy":hierarchy,"feature":feature}
				cities.append(city)
		links = table.next_siblings
		aNull = False
		nextPage = -1
		while not aNull:
			try:
				item = links.next()
				if type(item) is not bs4.element.Tag:
					continue
				else:
					nextPage = item.text.find("next")
				if nextPage >= 0:
					break
			except StopIteration:
				aNull = True
		if nextPage >= 0:
			path = item["href"]
		else:
			break
		count += 1

	with open('cities.txt', 'w') as outfile:
		for city in cities:
			json.dump(city, outfile)
			outfile.write("\n")

def createCityIndex():
	index = []
	pattern = ".org/(\d+)/"
	with open('index.txt', 'r') as f:
		for line in f:
			city = json.loads(line)
			number = re.search(pattern,city['url']).group(1)
			index.append(number)
	with open('ids.txt', 'w') as f:
	    for i in index:
	    	f.write(i)
	    	f.write('\n')

def extractCityInfo():
	print "start extracting.."
	extracted = []
	pattern = ".org/(\d+)/"
	with open('extracted.txt', 'r') as f:
		for line in f:
			number = re.search(pattern,line).group(1)
			extracted.append(number)
	print "Number of extracted cities: ","\t",len(extracted)
	path = "http://sws.geonames.org/%s/about.rdf"
	count = 1
	cities_rdf = ""
	with open('ids.txt', 'r') as f:
		for line in f:
			line = line.strip()
			if line not in extracted:
				url = path % line
				about = urllib2.urlopen(url).read()
				print count, '\t', url
				count += 1
				begin = about.find("<gn:Feature")
				end = about.find("<foaf:Document")
				cities_rdf = cities_rdf + about[begin:end]
		
	with open("cities.rdf", "a") as myfile:
	    myfile.write(cities_rdf)

#save file
def save_file(name, data):
	with open(name,'w') as f:
		for d in data:
			f.write(d)
			f.write('\n')

#read small size file, load into meomery at onece.
def read_file(name):
	with open(name,'r') as f:
		data = [line.strip() for line in f]
	return data

class Worker(multiprocessing.Process):

	def __init__(self, task_queue, result_queue, index):
		multiprocessing.Process.__init__(self)
		self.task_queue = task_queue
		self.result_queue = result_queue
		self.index = index

	def test(self):
		rdf = []
		for item in iter(self.task_queue.get, 'STOP'):
			if item in self.index:
				rdf.append(item)
		self.result_queue.put(rdf)

	def run(self):
		proc_name = self.name
		print "Starting %s .." % proc_name
		pattern = re.compile(".org/(\d+)/")
		result = {}
		ids = []
		rdf = []
		for items in iter(self.task_queue.get, 'STOP'):
			for item in items:
				start = item.find("<gn:Feature")
				end = item.find("<rdfs")
				number = re.search(pattern,item[start:end]).group(1)
				if number in self.index:
					ids.append(number)
					rdf.append(item.strip())
			del items[:]
			gc.collect()
		result["index"] = ids
		result["data"] = rdf
		self.result_queue.put(result)
		print "Ending %s ..." % proc_name

	def run_scan_whole_geo_file(self):
		proc_name = self.name
		print "Starting %s .." % proc_name
		pattern = re.compile(".org/(\d+)/")
		rdf = []
		for items in iter(self.task_queue.get, 'STOP'):
			aNull = False
			i = iter(items)
			while not aNull:
				try:
					item = i.next()
					number = re.search(pattern,item).group(1)
					if number in self.index:
						item = i.next()
						rdf.append(item.strip())
					else:
						i.next()
				except StopIteration:
					aNull = True
			del items[:]
			gc.collect()
		self.result_queue.put(rdf)
		print "Ending %s ..." % proc_name

def load_file_lines(name, number, info, queue, start=1, end=0):
	"""
	given a file name, read every number lines and put into queue, and produce line information
	every info lines. only extract the lines between start and end if given the start and end.
	"""
	with open(name,'r') as f:
		count = 1
		line = f.readline()
		data = []
		while line:
			if end == 0:
				if count > start:
					data.append(line)
					if count % number == 0:
						queue.put(data)
						data = []
			else:
				if count >= start and count <= end:
					data.append(line)
					if count % number == 0:
						queue.put(data)
						data = []
			line = f.readline()
			count += 1
			if count % info == 0:
				print count
		if data:
			queue.put(data)

def boss():
	NUMBER_OF_PROCESSES = 2
	results = multiprocessing.Queue(5)
	tasks = multiprocessing.Queue(NUMBER_OF_PROCESSES)
	#index = read_file('geo_index_es.txt')
	index = read_file('city_index_es.txt')
	# used to test index
	# index = range(10000)[::100]
	# index = map(str,index)
	#initial annd start the workers.
	workers = [ Worker(tasks,results,index) for i in range(NUMBER_OF_PROCESSES) ]
	for w in workers:
		w.daemon = True
		w.start()
	# for i in range(10000):
	# 	tasks.put(i)
	#read a specific number of lines from the file into memory and put into the queue.
	#do the whole file scan 
	#load_file_lines("all-geonames-rdf.txt", 300000, 1000000, tasks)
	load_file_lines("es_rdf.txt", 10000, 10000, tasks)
	#Notify the child process to stop.
	for w in workers:
		tasks.put("STOP")
	#collecting the computing results and wait the child processes finish.
	#the calling order matters. The join() should be called after collecting 
	#the result by calling result queue with get(), otherwise, the child process
	#will block.
	# rdf = []
	# for w in workers:
	# 	rdf += results.get()
	# for w in workers:
	# 	w.join()
	#save result and exit
	#save_file('es_rdf.txt',rdf)
	rdf = []
	ids = []
	for w in workers:
		result = results.get()
		ids += result["index"]
		rdf += result["data"]
	for w in workers:
		w.join()
	ids.sort()
	save_file('city_extracted_rdf_index.txt',ids)
	save_file('city_extracted_rdf.txt',rdf)

	print "Finished..."
	print "num active children:", multiprocessing.active_children()

def create_total_city_index():
	filter_class = ["A","P"] #A means country, state, region, and P means city village....
	index = read_file("feature_index.txt")	
	index = [line.split()[0] for line in index if line.split()[1] in filter_class]
	index.sort()
	save_file("city_index_es.txt", index)
	

if __name__ == '__main__':
	boss()