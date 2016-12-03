#!/usr/bin/python

import socket, urllib2, sys, os, time, json, re
from pymongo import MongoClient
from bs4 import BeautifulSoup

#Colores
class colores:
    HEADER = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    alert = '\033[93m'
    FAIL = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

client = MongoClient()
db = client.test

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def get_target():
	global client, db
	cursor = db.ShoditaCybercamp.find({"bot":"Nobita", "port":"443"})
	for document in cursor:
		scan_heartbleed(document["ip"].replace("\n",""), document["port"])

def scan_heartbleed(target, port):
	url = "https://filippo.io/Heartbleed/#"
	url_complete = url + str(target) + ":" + str(port)
	print url_complete
	html = urllib2.urlopen(url_complete).read()
	soup = BeautifulSoup(html, "html.parser")
	res = soup.findAll("h3",{"class":"bg-danger bleed bleed-vuln"})
	print colores.HEADER + "[TARGET][>] " + target + colores.normal
	print colores.green + "[URL][>] " + url_complete + colores.normal
	print remove_tags(str(res))

def main():
	get_target()

if __name__ == '__main__':
	main()
