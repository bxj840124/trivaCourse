'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
import json
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = int(sys.argv[1]) # Arbitrary non-privileged port
userdata = {}
login_user = []
user_rating = {}
doc_rating = {}

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    # conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        print data
        # reply = 'OK...' + data
        if not data: 
            break
        obj = json.loads(data.decode('utf-8'))

        if 'action' not in obj.keys():
            reply = 'no actions'
# login
        elif obj['action'] == 'login':     
            if obj['username'] in userdata.keys():
                if obj['password'] == userdata[obj['username']]:
                    login_user.append(obj['username'])
                    reply = 'login success'
                else:
                    reply = 'wrong password'
            else:
                reply = 'illegal username'
# register
        elif obj['action'] == 'register':     
            if obj['username'] in userdata.keys():
                reply = 'username already registered'
            else:
                userdata[obj['username']] = obj['password']
                reply = 'register success'
# logout
        elif obj['action'] == 'logout':     
            if obj['username'] in login_user:
                login_user.remove(obj['username'])
                reply = 'logout success'
            else:
                reply = 'user not in login list'
# rating
        elif obj['action'] == 'rating':    
            if obj['username'] in login_user:
                if obj['username'] not in user_rating.keys():
                    user_rating[obj['username']] = []
                if obj['docId'] not in doc_rating.keys():
                    doc_rating[obj['docId']] = [0,0]
                user_rating[obj['username']].append(obj['docId'])
                doc_rating[obj['docId']][int(obj['score'])] += 1
                reply = 'rating success'
            else:
                reply = 'user not in login list'
# get_rating 
        elif obj['action'] == 'get_rating':     
            reply = str(doc_rating[str(obj['docId'])][0]) +','+ str(doc_rating[str(obj['docId'])][1])
        print 'finish action: ',obj['action']

        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()