import zmq
import uuid

def register_group(group_name, ip_address, port):
    groups[group_name] = (ip_address,port)
    print("JOIN REQUEST FROM " + ip_address + ":" + port)
    return "SUCCESS"

def get_group_list():
    print("GROUP LIST REQUEST FROM USER")
    return "\n".join(f"{group} - {details[0]} {details[1]}" for group, details in groups.items())

def gen_uuid():
    return str(uuid.uuid4())

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
groups = {}

while True:
    message = socket.recv_string()
    if message.startswith("REGISTER_GROUP"):
        group_name = message.split(" ")[1]
        ip_address = message.split(" ")[2]
        port = message.split(" ")[3]
        response = register_group(group_name, ip_address, port)
    elif message == "GET_GROUP_LIST":
        response = get_group_list()
    elif message == "NEW_USER":
        response = gen_uuid()
    else:
        response = "Invalid command"

    socket.send_string(response)