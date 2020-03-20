import socket, os, sys
from threading import Thread

HOST = os.popen('ifconfig | grep "inet addr" | cut -d: -f2 | cut -d" " -f1 | head -1').read().strip() #socket.gethostname()

RESET = "\033[0;0m"
BOLD  = "\033[;1m"
RED  = "\033[91m"
GREEN = "\033[92m"

print("Host: {0}".format(HOST))
PORT = input("Port: ")
BUFSIZ = 1024
ADDR = (HOST, int(PORT))

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(1)

#functon that converts a list into a string with separator: ';'
def convert_list(lista):
	string = ""
	for item in lista:
		string += item+";"
	string += "\n"
	l = list(string)
	del l[-2]
	string = ""
	for item in l:
		string += item
	return string

def from_client(client, adress):
	while True:
		try:
			msg = client.recv(BUFSIZ).decode("utf-8")
			#print(msg)
			if msg == "LEFT":
				leftname = people[adress[1]]
				sys.stdout.write(BOLD+RED+people[adress[1]]+" left"+RESET+"\n")
				names.remove(people[adress[1]])
				del people[adress[1]]
				sks.remove(client)
				#print("2", names, people)
				for sock in sks:
					if sock == client:
						continue
					sock.send(bytes("INFO: "+BOLD+RED+leftname+" left"+RESET+"\n", "utf-8"))
				client.sendall(bytes("left", "utf-8"))
				#client.sendall(bytes("left", "utf-8"))
				return
				#continue
			if msg == "LIST":
				client.send(bytes("INFO: "+convert_list(names), "utf-8"))
				continue
			sys.stdout.write(people[adress[1]]+"> "+msg)
			for sock in sks:
				if sock == client:
					continue
				sock.send(bytes(people[adress[1]]+": "+msg, "utf-8"))
		except Exception as e:
			print("While loop exited [{}]".format(e))
			#client.close()
			break

people = {}
names = []
sks = []

print("Waiting for connections...")
while True:
	c, a = SERVER.accept()
	sks.append(c)
	name = c.recv(BUFSIZ).decode("utf-8")
	#print("NAME", name)
	sys.stdout.write(BOLD+GREEN+"Connected "+a[0]+":"+str(a[1])+RESET+"\n")
	people[a[1]] = name
	names.append(name)
	for sock in sks:
		if sock == c:
			continue
		sock.send(bytes("INFO: "+BOLD+GREEN+"Connected "+a[0]+":"+str(a[1])+" ("+"%s" % (name) +")"+RESET+"\n", "utf-8"))
	Thread(target=from_client, args=(c,a)).start()
	#print(names, people)
	#c.send(bytes("Welcome!", "utf-8"))
