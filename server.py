import socket, os, sys
from threading import Thread

try:
	HOST, PORT = sys.argv[1], int(sys.argv[2])
except:
	print("Invalid arguments given:")
	HOST = input("Enter host: ")
	PORT = input("Port: ")

BUFSIZ = 1024
ADDR = (HOST, int(PORT))

RESET = "\033[0;0m"
BOLD  = "\033[;1m"
RED  = "\033[91m"
GREEN = "\033[92m"

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(1)

#functon that converts a list into a string with separator: ';'
#['hi', 'my', 'name', 'is'] becomes hi;my;name;is

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
			if msg == "LEFT":
				leftname = people[adress[1]]
				sys.stdout.write(BOLD+RED+people[adress[1]]+" left"+RESET+"\n")
				names.remove(people[adress[1]])
				del people[adress[1]]
				sks.remove(client)
				for sock in sks:
					if sock == client:
						continue
					sock.send(bytes("INFO: "+BOLD+RED+leftname+" left"+RESET+"\n", "utf-8"))
				client.send(bytes("left", "utf-8"))
				return
			if msg == "LIST":
				client.send(bytes("INFO: "+convert_list(names), "utf-8"))
				continue
			sys.stdout.write(people[adress[1]]+"> "+msg)
			for sock in sks:
				if sock == client:
					continue
				sock.send(bytes(people[adress[1]]+": "+msg, "utf-8"))

		except Exception as e:
			print("While loop exit because of {}".format(e)) #To remove
			client.close()
			break

people = {} #dictionary of PIDs and names
names = []  #list of names
sks = []    #list of sockets

print("#"+"-"*30+"#") #separator

print("Waiting for connections...")
while True:
	c, a = SERVER.accept()
	sks.append(c)
	name = c.recv(BUFSIZ).decode("utf-8")
	sys.stdout.write(BOLD+GREEN+a[0]+":"+str(a[1])+" connected"+RESET+"\n")
	people[a[1]] = name
	names.append(name)
	for sock in sks:
		if sock == c:
			continue
		sock.send(bytes("INFO: "+BOLD+GREEN+a[0]+":"+str(a[1])+" ("+"%s" % (name) +")"+" joined"+RESET+"\n", "utf-8"))
	Thread(target=from_client, args=(c,a)).start()
	#print(names, people)
