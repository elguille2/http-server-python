import socket

def handle_request(request):
    """Parse the HTTP request and return the aproppiate response"""
    request_line = request.split("\r\n")[0]
    method, path, version = request_line.split(" ")

    if path.startswith("/echo/"):
        message = path[len("/echo/"):]
        response_body = message.encode("utf-8")
        response = (
            b"HTTP/1.1 200 OK\r\n"          # Status Line
            b"Content-Type: text/plain\r\n"                                             # Headers
            b"Content-Length: " + str(len(response_body)).encode("utf-8") + b"\r\n"     # Headers
            b"\r\n" # Empty line
            + response_body                                                   
        )
    elif path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    return response

def start_server(host, port):
    """Start the HTTP server and handle incoming connections"""
    server_socket = socket.create_server((host, port), reuse_port=True)
    print(f"Server started on {host}:{port}")

    while True:
        # Accept a connection
        connection, address = server_socket.accept()
        # Read the request
        request = connection.recv(1024).decode("utf-8")
        print(f"Received request: {request}")

        response = handle_request(request)
        connection.sendall(response)
        connection.close()

def main():
    print("Logs from your program will appear here!")
    start_server("localhost", 4221)
        

if __name__ == "__main__":
    main()
