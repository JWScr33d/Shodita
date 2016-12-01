import socket

def banner_grabbing(ip_address,port):
	s=socket.socket()
	s.connect((ip_address,port))
	s.send("GET HTTP/1.1 \r\n")
	banner = s.recv(2048)
	return banner

def main():
	target = str(raw_input("Target: "))
	port = int(raw_input("Port: "))
	print banner_grabbing(target, port)

if __name__ == '__main__':
	main()
