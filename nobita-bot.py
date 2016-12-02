#!/usr/bin/python

import socket, urllib, sys, os, time, json
from pymongo import MongoClient
portList = [21,22,23,25,53,63,80,90,102,110,143,161,443,500,513,520,559,1434,3306,3389,5000,5050, 5060,8000,8069,8080, 9443,27017, 28017] 
totalPuertos =  len(portList)
ip_root = ""

def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
	try:
		client = MongoClient()
		db = client.test
		cursor = db.ShoditaCybercamp.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
		print "[INFO] INSERT IN DB"
	except:
		print "[WARNING]ERROR INSERT MONGODB"

def geoIp(IP):
	return urllib.urlopen("http://ip-api.com/json/" + str(IP))

'''Grab Banner'''
def banner_grabbing_web(ip_address,port):  
	global portList
	try:  
		s=socket.socket()  
		s.settimeout(5.0)
		s.connect((ip_address,port))
		s.send("GET HTTP/1.1 \r\n")
		banner = s.recv(2048)  
		print "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' '
		return banner
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
		print "[INFO] Connecting to: " + ip_address
		for port in portList:
			porc = str(porcentaje(portList.index(port)))
			print "|----[!] " + str(ip_address) + " -> " + str(port) + " " + porc + "%"
			#Obtenemos el mensaje del servidor en el puerto 
			Banner = banner_grabbing_web(ip_address, port)
			else:
			#Variables obtenidas de la geoIp
				data_geoIP = geoIp(ip_address)
				data_geoIP = json.load(data_geoIP)
				Country = data_geoIP["country"]
				City = data_geoIP["city"]
				regionName = data_geoIP["regionName"]
				ISP = data_geoIP["isp"]
				Latitud = data_geoIP["lat"]
				Longitud = data_geoIP["lon"]
				date_Insert = time.strftime("%H:%M:%S")
				date_Update = "none"
				insert_mongodb(ip_address, Country, City, regionName, ISP, port, Banner, Latitud, Longitud, date_Insert, date_Update)

if __name__ == '__main__':
	main()
