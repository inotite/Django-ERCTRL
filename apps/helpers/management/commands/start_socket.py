from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import json
import requests


class Command(BaseCommand):
    help = 'Start server socket'

    def handle(self, *args, **options):
        import socket
        # get the hostname
        # host = "192.168.2.130"
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        host = socket.gethostbyname('localhost')
        port = 9999  # initiate port no above 1024
        
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(100)
        # import pdb;pdb.set_trace()

        while True:
            conn, address = server_socket.accept()  # accept new connection
            # conn.send(str(test)) #send only takes string
            print("Connection from: " + str(address))
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(2048).decode()

            if data == 'users':
                new_date = requests.get('http://localhost:8000/api/users/')
            elif data == 'rooms':
                new_date = requests.get('http://localhost:8000/api/rooms/')
            elif data == 'userrooms':
                new_date = requests.get('http://localhost:8000/api/users/19/rooms/')
            elif data == 'roomautomations':
                new_date = requests.get('http://localhost:8000/api/rooms/26/automations/')
            elif data == 'roomclues':
                new_date = requests.get('http://localhost:8000/api/rooms/26/clues/')
            elif data == 'roomimages':
                new_date = requests.get('http://localhost:8000/api/rooms/26/images/')
            elif data == 'roomsounds':
                new_date = requests.get('http://localhost:8000/api/rooms/26/sounds/')
            elif data == 'roomvideos':
                new_date = requests.get('http://localhost:8000/api/rooms/26/videos/')
            elif data == 'roompuzzles':
                new_date = requests.get('http://localhost:8000/api/rooms/26/puzzles/')
            elif data == 'timeElapse':
                new_date = requests.get('http://localhost:8000/api/room/5/event/timeElapse')
            elif data == 'timerStart':
                new_date = requests.get('http://localhost:8000/api/room/5/event/timerStart')
            elif data == 'timerStop':
                new_date = requests.get('http://localhost:8000/api/room/5/event/timerStop')
            elif data == 'roomComplet':
                new_date = requests.get('http://localhost:8000/api/room/5/event/roomComplet')
            elif data == 'roomFail':
                new_date = requests.get('http://localhost:8000/api/room/5/event/roomFail')
            elif data == 'roomReset':
                new_date = requests.get('http://localhost:8000/api/room/5/event/roomReset')
            elif data == 'networkPolling':
                new_date = requests.get('http://localhost:8000/api/room/5/event/networkPolling') 
            elif data == 'customButton':
                new_date = requests.get('http://localhost:8000/api/room/5/event/customButton') 
            elif data == 'customEvent':
                new_date = requests.get('http://localhost:8000/api/room/5/event/customEvent')                                      
            else:
                new_date = {}

            reply = new_date.text + data
            # reply = json.dumps((test)) + data
            if not data:
                print("break")
                # if data is not received break
                break
            print("from connected user: " + str(data))
            # if str(data) == 'start':
            #     conn.send(data.encode())
            # else:
            # conn.send("New action")  
            # data = input(' -> ')
            conn.send(reply.encode())  # send data to the client

        conn.close()  # close the connection
