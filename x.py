import requests
import json
import urlparse
import sys
import random
import string
import base64
import time
import argparse
import certifi
from urllib import quote
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as BS

class X:
	def __init__(self):
		self.session = requests.Session()
		self.base_url = "https://vjudge.net"
		self.session.headers.update({"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"})
		self.language = None
		self.runid = []
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		self.sub_url = self.base_url + "/problem/submit"
		self.session.get(self.base_url, verify = False)
		self.ojlanguages = self.get(self.base_url + "/util/ojLanguages").json()

	def get(self, url, data = {}):
#		print "Getting %s ..." % url
		for attempt in range(10):
			try:
				r = self.session.get(url,
						data = data,
						verify = False
						)
			except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
#				print "Retry #%d ..." % attempt
				continue
			else:
#				print "Got"
				return r
		else:
			raise Exception('Failed to get %s TAT' % url)

	def post(self, url, data = {}, referer = None):
#		print "Posting %s ..." % url
		if referer != None:
			self.session.headers.update({"referer" : referer})
#		print data
		for attempt in range(10):
			try:
				r = self.session.post(url,
						data = data,
						verify = False
						)
			except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
#				print "Retry #%d ..." % attempt
				continue
			else:
#				print "Got"
				return r
		else:
			raise Exception('Failed to post %s TAT' % url)

	def login(self, username, password):
		print "Logining ..."
		self.username, self.password = username, password
#		print username, password
		r = self.post(self.base_url + "/user/login", data = {
			"username": username,
			"password": password
			})
		print "Success!"
#		print r.content

	def getsoup(self, resp):
		return BS(resp.content, "html.parser")

	def getlanguage(self):
		soup = self.getsoup(self.get(self.sub_url))
		def is_language_option(tag):
			return tag.name == "option" and tag.parent["name"] == "language"
		options = soup.find_all(option)
		self.languages = []
		for option in options:
			self.languages.append((int(option["value"]), option.string))

	def showlanguage(self):
		if len(self.languages) == 0:
			self.getlanguage
		for language in languages:
			print language[0], language[1]

	def setlanguage(self, language):
		if language.isdigit():
			self.language = int(language)
		else:
			def is_target_language(tag):
				return tag.name == "option" and tag.string == language
			try:
				option_tag = soup.find_all(is_target_language)[0]
				self.language = int(option_tag["value"])
			except:
				raise Exception('No such language as %s !!??' % language)

	def setoj(self, OJ):
		self.OJ = OJ

	def setprob(self, problem):
		self.problem = problem

	def setlang(self, language):
		self.language = language

	def input_language(self, default):
		languages = self.ojlanguages[self.OJ]
		if default != None:
			print "Your default language is [%s]: %s, change? [y/N]" % (default, languages[default])
			resp = raw_input()
			if resp != 'y':
				return default
		while True:
			for key, value in languages.iteritems():
				print "[%s]: %s" % (key, value)
			lang = raw_input("Please input your preferred language in []: ")
			if lang in languages:
				return lang
			else:
				print "???"

	def get_submissions(self):
#		url = "%s/status/#un=%s&OJId=%s&probNum=%s&res=0&orderBy=run_id&language=" % (self.base_url, self.username, self.OJ, self.problem)
#		soup = self.getsoup(self.get(url))
#		def is_id_tr(tag):
#			return tag.name == "tr" and tag.has_attr("class") and tag["class"] == "no odd"
#		print soup.prettify()
#		return soup.find_all(is_id_tr)[0]["id"]
		url = self.base_url + "/status/data/"
		data = dict(urlparse.parse_qsl("draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&un=footoredo&OJId=CodeForces&probNum=592E&res=0&language=&orderBy=run_id"))
		data['un'] = self.username
		data['OJId'] = self.OJ
		data['probNum'] = self.problem
		r = self.post(url, data)
		return json.loads(r.content)[u'data']

	def fetch_runid(self):
		submissions = self.get_submissions()
		self.runid.append(submissions[0][0])
		return self.runid[-1]

	def fetch_status(self, runid = None):
		if runid == None:
			runid = self.runid[-1]
		url = self.base_url + "/solution/data/%s" % runid;
		r = self.get(url)
		return r.json()

	def print_status(self, status):
		print "Status: %s" % status["status"]
		if "additionalInfo" in status:
			print "Info: "
			print status["additionalInfo"]

	def submit(self, source, language = None):
		print "Submitting ..."
		if language != None:
			self.setlanguage(language)
#		print self.language
#		print base64.b64encode(source)
#		return
		r = self.post(self.sub_url, data = {
			"language" : str(self.language),
			"share": str(0),
			"source": base64.b64encode(quote(source)),
			"oj": self.OJ,
			"probNum": self.problem
			}, referer = self.sub_url)
#		print r.status_code
#		print r.content
		print "Submitted!"
		if "error" in r.json():
			print "error: %s" % r.json()["error"]
		else:
			self.runid.append(r.json()["runId"])
			while True:
				status = self.fetch_status()
				self.print_status(status)
				if not status["processing"]:
					break
				time.sleep(0.5)

	def fetch_info(self, runid = None):
		if runid == None:
			runid = self.runid[-1]
		url = self.base_url + "/problem/source/" + str(runid)
		soup = self.getsoup(self.get(url))
		def fetch_item(item_name, tag):
			return tag.name == ""

def rand_code():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))

if __name__ == "__main__":
	x = X()
	x.login('footoredo', '123456')
	x.setenv('CodeForces', '592E', "1")
	x.submit(rand_code())
	while (x.fetch_status()["processing"]):
		time.sleep(0.5)
	print x.fetch_status()
