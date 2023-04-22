import socket
import json

def run_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        first_res = True
        while True:
            if first_res:
                client.sendall(json.dumps({"user_input":"first_res"}).encode('utf-8'))
                data = client.recv(1024)
                response = data.decode('utf-8')

                print(response)
                first_res = False
            else:
                user_input = input("You: ")
               # print(user_input)
                request = {'user_input': user_input}
                client.sendall(json.dumps(request).encode('utf-8'))

                data = client.recv(1024)
                response = data.decode('utf-8')

                print(response)

                if user_input.lower() == "quit":
                    break
            first_res = False
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12354
    run_client(host, port)
