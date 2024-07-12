import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        # Accept a connection
        connection, address = server_socket.accept()

        # Read the request
        request = connection.recv(1024).decode("utf-8")
        print(f"Received request: {request}")

        # Analyze the request
        request_line = request.split("\r\n")[0]
        print(f"Request Line: {request_line}")

        # Extract the path
        method, path, version = request_line.split(" ")

        # Responses
        if path == "/index.html":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        # Send the response
        connection.sendall(response)
        connection.close()

    


if __name__ == "__main__":
    main()
