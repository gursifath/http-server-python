import socket
import threading

def handle_request(server_socket):
    while True:
        client_socket, _ = server_socket.accept() # wait for client
        request = client_socket.recv(1024).decode()
        success = "HTTP/1.1 200 OK\r\n"
        content_type = "Content-Type: text/plain\r\n"
        path = request.split(" ")

        if "echo" in request.lower():
            body = path[1].split("/")[-1]
            response = f"{success}{content_type}Content-Length: {len(body)}\r\n\r\n{body}"
        elif "user-agent" in request.lower():
            path = request.split("\r\n")
            user_agent = path[2].split(" ")[-1]
            response = f"{success}{content_type}Content-Length: {len(user_agent)}\r\n\r\n{user_agent}"
        else:
            if path[1] != "/":
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                response = f"{success}\r\n"

        client_socket.sendall(response.encode())

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    threading.Thread(target=handle_request, args=[server_socket]).start()
    

if __name__ == "__main__":
    main()
