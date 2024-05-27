import socket
import threading
import os
import re
from sys import argv
# Above line imports the argv variable from the sys module.
# The argv variable is a list in Python, which contains the command-line arguments passed to the script. 
# When you run a Python script, the argv list will have at least one element, argv[0], which is the name of the script. 
# Additional arguments are added to this list, so you can access them inside your script.
# In the context of this server, argv[1] would be --directory and argv[2] would be the actual directory path provided by the user when they start the server.
# This path is used later in the code to open and read files from the specified directory.

directory = ""
if len(argv) > 2:
    _, directory = argv[1:]
    
class HttpRequest():
    def __init__(self, data):
        data_str = data.decode()
        lines = data_str.split("\r\n")
        method, path, version = lines[0].split()
        self.request_method = None
        self.method = method
        self.path = path
        self.version = version
        self.user_agent = re_extract(lines[2], r"User-Agent: (.*)")

class HttpResponse():
    def __init__(self, status_code, data, isFile = False):
        self.isFile = isFile
        self.status_code = status_code
        self.data = data
        self.status_dict = {200: "OK", 404: "Not Found", 201: "Created"}

    def encode(self):
        contentType = "text/plain" if not self.isFile else "application/octet-stream"
        response_str = "HTTP/1.1 {status_code} {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len}\r\n\r\n{body}".format(
            status_code = self.status_code,
            status = self.status_dict[self.status_code],
            content_type = contentType,
            len = len(self.data),
            body = self.data,
        )
        return response_str.encode()

def re_extract(string, pattern):
    search = re.search(pattern, string)
    if search:
        return search.group(1)

def handle_request(server_socket):
    while True:
        client_socket, _ = server_socket.accept() # wait for client
        data = client_socket.recv(1024)
        request = HttpRequest(data)
        try:
            if request.path == "/":
                # response = HttpResponse(200)
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif "user-agent" in request.path:
                response = HttpResponse(200, request.user_agent)
            elif "echo" in request.path:
                arg = re_extract(request.path, r"/echo/(.*)")
                response = HttpResponse(200, arg)
            elif "files" in request.path:
                file_name = request.path.split("/")[-1]
                if request.method == "GET":
                    if file_name in os.listdir(directory):
                        with open(os.path.join(directory, file_name)) as f:
                            s = f.read()
                            response = HttpResponse(200, s, isFile=True)
                            f.close()
                    else:
                        raise Exception("not found")
                elif request.method == "POST":
                    pass
            else:
                raise Exception("not found")
        except Exception:
            # response = HttpResponse(404)
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(response.encode())

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    threading.Thread(target=handle_request, args=[server_socket]).start()

if __name__ == "__main__":
    main()
