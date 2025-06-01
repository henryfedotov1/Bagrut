import socket
import json
from constants import server_ip, server_port, login_action


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket

def send_login_request(client_socket, student_id, password):
    request = {
        "action": login_action,
        "student_id": student_id,
        "password": password
    }
    print(f"Sending login request: {request}")
    client_socket.send(json.dumps(request).encode('utf-8'))

def receive_response(client_socket):
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {response}")
    if response:
        return json.loads(response)
    else:
        return {'status': 'fail', 'message': 'No response from server'}

def main():
    student_id = input("Enter student id: ")
    password = input("Enter password: ")
    client_socket = connect_to_server()
    send_login_request(client_socket, student_id, password)
    response = receive_response(client_socket)
    if response['status'] == 'success':
        print(f"Login successful! Paying Status: {response['paying_status']}")
        if response['picture']:
            print(f"Picture URL: {response['picture']}")
    else:
        print("Login failed. Please check your credentials.")
    client_socket.close()

if __name__ == "__main__":
    main()
