import socket, os, sys
from threading import Thread

HOST = os.popen('ifconfig | grep "inet addr" | cut -d: -f2 | cut -d" " -f1 | head -1').read().strip() #socket.gethostname()
print("HOST: %s" % HOST)
PORT = int(input('Enter port: '))
NAME = input("Enter name: ")
BUFSIZE = 1024

ADDR = (HOST, PORT)

RESET = "\033[0;0m"
BOLD  = "\033[;1m"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

client_socket.send(bytes(NAME, "utf-8"))
left = False

stat = True

def rc():
	while True:
		try:
			#print("Running")
			msg = client_socket.recv(BUFSIZE).decode("utf-8")
			'''if msg.startswith("INFO"):
				sys.stdout.write("\r\033[K")
				sys.stdout.write(msg), sys.stdout.flush()
				return'''
			if not left:
				sys.stdout.write("\r\033[K")
				sys.stdout.write(msg), sys.stdout.flush()
				if not msg.startswith("INFO") and not stat:
					sys.stdout.write(BOLD+"{}> ".format(NAME)+RESET); sys.stdout.flush()
					stat = True
			else:
				return
		except:
			break

print("WELCOME {}, You can start to typing messages!".format(NAME))

while True:
	x = Thread(target=rc)
	#x.daemon = True
	x.start()
	sys.stdout.write(BOLD+"{}> ".format(NAME)+RESET); sys.stdout.flush()
	stat = False
	msg = sys.stdin.readline()
	#print("MSG:", msg)
	if msg == "/quit\n":
		left = True
		client_socket.send(bytes("LEFT", "utf-8"))
		client_socket.close()
		#x._stop()
		sys.exit()
		break
	elif msg == "/list\n":
		client_socket.send(bytes("LIST", "utf-8"))
		continue
	client_socket.send(bytes(msg, "utf-8"))
