import zmq
from datetime import datetime

def get_grp_list():
    socket.send_string("GET_GROUP_LIST")
    response = socket.recv_string()
    print(response)

def get_uuid():
    socket.send_string("NEW_USER")
    return socket.recv_string()

def join_group(user_id, grp_name, grp_ip, grp_port):
    new_socket = context.socket(zmq.REQ)
    new_socket.connect("tcp://"+grp_ip+":"+grp_port)

    new_socket.send_string("JOIN_GROUP "+user_id)
    response = new_socket.recv_string()

    if(response=="SUCCESS"):
        groups[grp_name] = new_socket
    print(response)

def leave_group(user_id, grp_name):
    if(grp_name in groups.keys()):
        temp_socket = groups[grp_name]
        temp_socket.send_string("LEAVE_GROUP "+user_id)
        response = temp_socket.recv_string()
        print(response)
    else:
        print("Not a part of "+grp_name)

def send_msg(user_id, grp_name, msg):
    if(grp_name in groups.keys()):
        temp_socket = groups[grp_name]
        temp_socket.send_string("SEND_MESSAGE "+user_id+" "+msg)
        response = temp_socket.recv_string()
        print(response)
    else:
        print("Not a part of "+grp_name)

def get_msg(user_id, grp_name, time=None):
    if(grp_name in groups.keys()):
        temp_socket = groups[grp_name]
        request = "GET_MESSAGES "+user_id+" "+str(time) if(time!=None) else "GET_MESSAGES "+user_id
        temp_socket.send_string(request)
        response = temp_socket.recv_string()
        print(response)
    else:
        print("Not a part of "+grp_name)


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
user_id = get_uuid()

groups = {}

ch = 10

while(ch!=0):
    print('''
        Welcome User {%s}
          
          Press 1 to Join a group
          Press 2 to Leave a group
          Press 3 to Send a message in a group
          Press 4 to Get messages from a group
          Press 5 to Get group list

          Press 0 to Exit

          '''%user_id)
    ch = int(input("Choice: "))
    print()

    if(ch==1):
        grp_name = input("Name of group: ")
        grp_ip = input("IP address of group: ")
        grp_port = input("Port of group: ")
        join_group(user_id, grp_name, grp_ip, grp_port)

    elif(ch==2):
        grp_name = input("Name of group: ")
        leave_group(user_id, grp_name)
    
    elif(ch==3):
        grp_name = input("Name of group: ")
        msg = input("Message: ")
        send_msg(user_id, grp_name, msg)

    elif(ch==4):
        grp_name = input("Name of group: ")

        inp_time = int(input("Enter time? (0-No, 1-Yes): "))
        if(inp_time==1):

            time_str = input("Enter time in hh:mm:ss format: ")
            time_format = "%H:%M:%S"  
            time_obj = datetime.strptime(time_str, time_format)
            current_date = datetime.now().date()
            combined_datetime = datetime.combine(current_date, time_obj.time())

            get_msg(user_id, grp_name, combined_datetime)
        else:
            get_msg(user_id, grp_name)

    elif(ch==5):
        get_grp_list()
    
    elif(ch==0):
        print("Exited.")
    
    else:
        print("Invalid input")
        ch = 0