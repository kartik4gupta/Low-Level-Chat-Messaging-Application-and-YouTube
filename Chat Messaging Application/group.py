import zmq
import sys
import threading
import random
from datetime import datetime

messages = []
users = set()

def register(name, ip, socket, port):
    message = "REGISTER_GROUP " + name + " " + ip + " " + port
    socket.send_string(message)
    reply = socket.recv_string()
    print(reply)

def handle_join_group(user_id):
    print("JOIN REQUEST FROM " + user_id)
    users.add(user_id)
    return "SUCCESS"

def handle_leave_group(user_id):
    print("LEAVE REQUEST FROM " + user_id)
    if user_id in users:
        users.remove(user_id)
        return "SUCCESS"
    else:
        return "User not a part of group."

def handle_get_messages(user_id, timestamp=None):
    print("MESSAGE REQUEST FROM "+user_id)
    if timestamp is not None:
        chats = [str(msg[0])+" - "+ msg[1] for msg in messages if msg[0] >= timestamp]
    else:
        chats = [str(msg[0])+" - "+ msg[1] for msg in messages]
    socket_rep.send_string("\n".join(chats))

def handle_send_message(user_id, message_content):
    print("MESSAGE SEND FROM "+user_id)
    if user_id in users:
        messages.append((datetime.now(), message_content))
        socket_rep.send_string("SUCCESS")
    else:
        socket_rep.send_string("FAILED")

def run():
    while True:
        message = socket_rep.recv_string()
        if message.startswith("JOIN_GROUP"):
            user_id = message.split(" ")[1]
            response = handle_join_group(user_id)
            socket_rep.send_string(response)
        elif message.startswith("LEAVE_GROUP"):
            user_id = message.split(" ")[1]
            response = handle_leave_group(user_id)
            socket_rep.send_string(response)
        elif message.startswith("GET_MESSAGES"):
            user_id = message.split(" ")[1]

            if(len(message.split(" ")) > 2):
                timestamp_str = message.split(" ")[2] + " " + message.split(" ")[3]
                time_format = "%Y-%m-%d %H:%M:%S"
                timestamp = datetime.strptime(timestamp_str,time_format)
            else:
                timestamp = None
            
            thread = threading.Thread(target=handle_get_messages, args=(user_id, timestamp))
            thread.start()
            thread.join()
        elif message.startswith("SEND_MESSAGE"):
            user_id = message.split(" ")[1]
            message_content = " ".join(message.split(" ")[2:])
            thread = threading.Thread(target=handle_send_message, args=(user_id, message_content))
            thread.start()
            thread.join()
        else:
            response = "Invalid command"
            socket_rep.send_string(response)

context = zmq.Context()
socket_req = context.socket(zmq.REQ)
socket_req.connect("tcp://localhost:5555")

name = sys.argv[1]
ip = sys.argv[2]
port = str(random.randrange(5000,6000))

register(name, ip, socket_req, port)

socket_rep = context.socket(zmq.REP)
socket_rep.bind("tcp://"+ip+":"+port)

run()