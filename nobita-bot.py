#!/usr/bin/python

import socket, urllib, sys, os, time, json
from pymongo import MongoClient
from pymodbus.client.sync import ModbusTcpClient
import snap7
from snap7.util import *
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
#Lista de puertos que escanea el bot
portList = [21,22,23,25,53,63,80,90,102,110,143,161,443,500,502,503,513,520,559,1434,3306,3389,5000,5050, 5060,8000,8069,8080,8081,9443,10000,27017, 28017] 
totalPuertos =  len(portList)
ip_root = ""

#funcion encargada en insertar en mongoDB
def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
	try:
		client = MongoClient()
		db = client.test
		cursor = db.ShoditaCybercamp.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
		print colores.green + "[INFO] INSERT IN DB" + colores.normal
	except:
		print colores.alert + "[WARNING]ERROR INSERT MONGODB" + colores.normal

#funcion encargada de obtener datos geoIP
def geoIp(IP):
	return urllib.urlopen("http://ip-api.com/json/" + str(IP))

#parser HTML
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

#funcion para detectar heartbleed vuln
def scan_heartbleed(target, port):
	url = "https://filippo.io/Heartbleed/#"
	url_complete = url + target + ":" + port
	html = urllib2.urlopen(url_complete).read()
	soup = BeautifulSoup(html, "html.parser")
	res = soup.findAll("h3",{"class":"bg-danger bleed bleed-vuln"})
	res = str(remove_tags(res))
	print res
	
#funcion que obtiene el banner
def banner_grabbing(ip_address,port):  
	global portList
	try:
		#modbus banner
		if port == 502 or port == 503:
			try:
				client = ModbusTcpClient(ip_address)
				client.write_coil(1, True)
				result = client.read_coils(1,1)
				print result.bits[0]
				client.close()
				banner = "PLC"
				return banner
			except:
				#print "502 error"
				pass
		#simatic banner
		if port == 102:
			try:
				plc = snap7.client.Client()
				if plc.connect(ip_address,0,1):
					banner = "PLC"
				return banner
				plc.disconnect()
			except:
				#print "102 error"
				pass
		#banner socket GET
		if not port == 102 or port == 502 or port == 503:
			s=socket.socket()
			s.settimeout(5.0)
			s.connect((ip_address,port))
			s.send("GET HTTP/1.1 \r\n")
			banner = s.recv(2048)  
			print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' '
			return banner
			scan_heartbleed(ip_address,port)
		else:
			#obtener codigo web
			try:
				url = "http://" + ip_address + ":" + "port"
				html = urllib2.urlopen(url).read()
				print html
			except:
				pass
			try:
				url = "https://" + ip_address + ":" + "port"
				html = urllib2.urlopen(url).read()
				print html
			except:
				pass
	except:
		return "none"

def porcentaje(portID):
	global portList, totalPuertos
	total = portID * 100
	total = total / totalPuertos
	return total

def main():  
	global portList, totalPuertos, ip_address
	f = open("dic/targets.txt", "r")
	targets = f.readlines()
	for target in targets:

		ip_address = target
		print colores.HEADER + "[INFO] Connecting to: " + ip_address + colores.normal
		for port in portList:
			porc = str(porcentaje(portList.index(port)))
			print "|----[!] " + str(ip_address) + " -> " + str(port) + " " + porc + "%"
			#Obtenemos el mensaje del servidor en el puerto 
			Banner = banner_grabbing(ip_address, port)
			#Variables obtenidas de la geoIp
			data_geoIP = geoIp(ip_address)
			data_geoIP = json.load(data_geoIP)
			Country = data_geoIP["country"]
			City = data_geoIP["city"]
			regionName = data_geoIP["regionName"]
			ISP = data_geoIP["isp"]
			Latitud = data_geoIP["lat"]
			Longitud = data_geoIP["lon"]
			date_Insert = time.strftime("%c")
			date_Update = "none"
			if Banner == "none":
				pass
			else:
				insert_mongodb(ip_address, Country, City, regionName, ISP, port, Banner, Latitud, Longitud, date_Insert, date_Update)

if __name__ == '__main__':
	main()
