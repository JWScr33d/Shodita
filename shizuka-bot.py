#!/usr/bin/python

import socket, urllib, sys, os, time, csv, re
from pymongo import MongoClient
from bs4 import BeautifulSoup

file_directory = "data/simotic-port-102.csv"


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

def insert_mongodb(ip, dominio):
	global client, db
	try:
		date_Insert = time.strftime("%H:%M:%S")
		date_Update = ""
		cursor = db.ShoditaCybercamp.insert({"ip":ip, "dominio":dominio, "date_insert": date_Insert, "date_Update": date_Update, "bot": "Shizuka"})
		print colores.blue + "[INFO] INSERT IN DB " + dominio + colores.normal
	except:
		print colores.alert + "[WARNING] ERROR INSERT IN MONGODB" + colores.normal


def check_domain_mongodb(ip, dominio):
	global client, db
	if db.Shodita.find({"ip":ip, "dominio": dominio}).count() >= 1:
		return True
	else:
		return False


def get_domain(target):
	url = "https://www.robtex.net/?dns=" + str(target) + "&rev=1"
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.findAll("td")
	table = remove_tags(str(table))
	data = table.split(",")
	for d in data:
		if len(d) > 10:
			d = d.replace(" ", "")
			d = d.replace("]","")
			if check_domain_mongodb(target, d):
				print "[INFO]" + str(d) + " in " + str(target) + " already insert ..."
			else:
				insert_mongodb(target, d)
				print colores.green + "[INFO]" + str(d) + " in " + str(target) + " insert ..." + colores.normal
		else:
			print colores.green + "[INFO]" + colores.alert + str(target) + " no web domains ..." + colores.normal

def get_target():
	global file_directory
	with open(file_directory) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print row["IP"]
			get_domain(row["IP"])

def main():
	get_target()

if __name__ == '__main__':
	main()
