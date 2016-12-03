#!/usr/bin/python

import socket, urllib, sys, os, time, json, struct
from pymongo import MongoClient
from pymodbus.client.sync import ModbusTcpClient
import snap7
from snap7.util import *
from bs4 import BeautifulSoup

class colores:
    HEADER = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    alert = '\033[93m'
    FAIL = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

portList = [21,22,23,25,53,63,80,90,102,110,143,161,443,500,502,503,513,520,559,1434,3306,3389,5000,5050, 5060,8000,8069,8080,8081,9443,10000,27017, 28017] 
totalPuertos =  len(portList)

def insert_mongodb(IP, Country, City, regionName, ISP, Port, Banner, Latitud, Longitud, date_Insert, date_Update):
	try:
		client = MongoClient()
		db = client.test
		cursor = db.ShoditaCybercamp.insert({"ip":IP, "country": Country, "city": City, "region_name": regionName, "isp": ISP, "port": Port, "banner": Banner, "latitud": Latitud, "longitud": Longitud, "date_insert": date_Insert, "date_Update": date_Update, "bot":"Nobita"})
		print colores.green + "[INFO] INSERT IN DB" + col
	except:
		print colores.alert + "[WARNING]ERROR INSERT MONGODB" + colores.normal

def geoIp(IP):
	return urllib.urlopen("http://ip-api.com/json/" + str(IP))


'''Grab Banner'''
def banner_grabbing(ip_address,port):  
	global portList
	try:
		if port == 502 or port == 503:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(10)
			sock.connect((ip_address, 502))
 			print colores.blue + "[INFO] " + colores.normal + " Starting modbus scan ..."
			try:
				
				unitId = 16
				functionCode = 5

				print colores.green + "CoilID 1" + colores.normal
				coilId = 1
				req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
				sock.send(req)
				print("TX: (%s)" %req)
				rec = sock.recv(BUFFER_SIZE)
				print("RX: (%s)" %rec)
				time.sleep(2)
 
				print colores.green + "CoilID 2" + colores.normal
				coilId = 2
				req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
				sock.send(req)
				print("TX: (%s)" %req)
				rec = sock.recv(BUFFER_SIZE)
				print("RX: (%s)" %rec)
				time.sleep(2)
 
			except:
				print('Closing socket')
				sock.close()

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

		if not port == 102 or port == 502 or port == 503:
			s=socket.socket()
			s.settimeout(5.0)
			s.connect((ip_address,port))
			s.send("GET HTTP/1.1 \r\n")
			banner = s.recv(2048)  
			print colores.blue + "[+]" + ip_address + ' : ' + str(port) + ' -BANNER- ' + banner + time.strftime("%H:%M:%S") + ' ' + colores.normal
			return banner
		else:
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
	f = open("dic/targets2.txt", "r")
	targets = f.readlines()
	for target in targets:

		ip_address = target
		print colores.HEADER + "[INFO] Connecting to: " + ip_address + colores.normal
		for port in portList:
			porc = str(porcentaje(portList.index(port)))
			print colores.green + "|----[!] " + str(ip_address) + " -> " + str(port) + " " + porc + "%" + colores.normal
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
