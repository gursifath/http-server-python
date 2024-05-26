# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, _ = server_socket.accept() # wait for client

    request = client_socket.recv(1024).decode()
    path = request.split(" ")
    if "echo" not in request.lower():
        if path[1] != "/":
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        body = path[1].split("/")[-1]
        body_len = len(body)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {body_len}\r\n\r\n{body}"

    client_socket.sendall(response.encode())
    client_socket.close

if __name__ == "__main__":
    main()
