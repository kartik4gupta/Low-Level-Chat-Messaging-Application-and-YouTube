# Message Server README

The `message_server.py` file contains the code for a message server that facilitates communication between users in different groups. Here's a brief overview of the functions and how to use them:

1. **Register Group Functionality**:
    - The `register_group()` function registers a new group with the server.
    - It takes three parameters: `group_name`, `ip_address`, and `port`.
    - To register a group, send a message to the server with the format `"REGISTER_GROUP group_name ip_address port"`.
    - Example usage: `REGISTER_GROUP Group1 127.0.0.1 5555`.

2. **Get Group List Functionality**:
    - The `get_group_list()` function retrieves the list of all registered groups.
    - To request the group list, send a message `"GET_GROUP_LIST"` to the server.
    - Example usage: `GET_GROUP_LIST`.

3. **Generate UUID Functionality**:
    - The `gen_uuid()` function generates a unique identifier for new users.
    - To generate a UUID, send a message `"NEW_USER"` to the server.
    - Example usage: `NEW_USER`.

# Group README

The `group.py` file contains the code for managing user interactions within groups. Here's a brief overview of the functions and how to use them:

1. **Register Functionality**:
    - The `register()` function registers a user with a group server.
    - It takes four parameters: `name`, `ip`, `socket`, and `port`.
    - Example usage: `register(name, ip, socket, port)`.

2. **Handle Join Group Functionality**:
    - The `handle_join_group()` function processes requests from users to join a group.
    - Example usage: `handle_join_group(user_id)`.

3. **Handle Leave Group Functionality**:
    - The `handle_leave_group()` function processes requests from users to leave a group.
    - Example usage: `handle_leave_group(user_id)`.

4. **Handle Get Messages Functionality**:
    - The `handle_get_messages()` function retrieves messages from a group, optionally filtered by timestamp.
    - Example usage: `handle_get_messages(user_id, timestamp)`.

5. **Handle Send Message Functionality**:
    - The `handle_send_message()` function sends a message to a group.
    - Example usage: `handle_send_message(user_id, message_content)`.

6. **Run Functionality**:
    - The `run()` function runs the group server, processing incoming messages from users.
    - Example usage: `run()`.

# User README

The `user.py` file contains the code for user interactions within groups. Here's a brief overview of the functions and how to use them:

1. **Get Group List Functionality**:
    - The `get_grp_list()` function retrieves the list of all available groups.
    - Example usage: `get_grp_list()`.

2. **Get UUID Functionality**:
    - The `get_uuid()` function retrieves a unique identifier for the user.
    - Example usage: `get_uuid()`.

3. **Join Group Functionality**:
    - The `join_group()` function allows the user to join a group.
    - Example usage: `join_group(user_id, grp_name, grp_ip, grp_port)`.

4. **Leave Group Functionality**:
    - The `leave_group()` function allows the user to leave a group.
    - Example usage: `leave_group(user_id, grp_name)`.

5. **Send Message Functionality**:
    - The `send_msg()` function allows the user to send a message to a group.
    - Example usage: `send_msg(user_id, grp_name, msg)`.

6. **Get Message Functionality**:
    - The `get_msg()` function allows the user to retrieve messages from a group.
    - Example usage: `get_msg(user_id, grp_name, time=None)`.

7. **User Interface**:
    - The user interface allows users to perform various actions such as joining/leaving groups, sending/receiving messages, and getting the group list.

Please ensure to follow the provided examples for each functionality to interact with the system effectively.
