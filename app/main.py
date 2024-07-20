import socket
import threading
import argparse
import os

def handle_request(request, connection, files_directory):
    """Parse the HTTP request and return the aproppiate response"""
    request_line = request.split("\r\n")[0]
    method, path, version = request_line.split(" ")

    if path.startswith("/echo/"):
        message = path[len("/echo/"):]
        response_body = message.encode("utf-8")
        response = (
            b"HTTP/1.1 200 OK\r\n"          # Status Line
            b"Content-Type: text/plain\r\n"                                             
            b"Content-Length: " + str(len(response_body)).encode("utf-8") + b"\r\n"     
            b"\r\n" # Empty line
            + response_body                                                   
        )
    elif path.startswith("/user-agent"):
        user_agent = request.split("User-Agent: ")[1].split("\r\n")[0]
        response_body = user_agent.encode("utf-8")
        response = (
            b"HTTP/1.1 200 OK\r\n"          # Status Line
            b"Content-Type: text/plain\r\n"                                             
            b"Content-Length: " + str(len(response_body)).encode("utf-8") + b"\r\n"     
            b"\r\n" # Empty line
            + response_body                                                   
        )
    elif path.startswith("/files/"):
        filename = path[len("/files/"):]
        file_path = os.path.join(files_directory, filename) # Build the path to the file

        if method == "POST":
            headers, body = request.split("\r\n\r\n", 1)
            content_length = 0
            for header in headers.split("\r\n")[1:]:
                if header.startswith("Content-Length:"):
                    content_length = int(header.split(":")[1].strip())
                    break

            # Read the body of the request
            while len(body) < content_length:
                body += connection.recv(content_length - len(body)).decode("utf-8")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the body to the file
            with open(file_path, "wb") as file:
                file.write(body.encode("utf-8"))

            response = b"HTTP/1.1 201 Created\r\n\r\n"

        elif method == "GET":

            if os.path.isfile(file_path): 
                with open(file_path, "rb") as file: # Open the file in binary mode
                    response_body = file.read()
                    response = (
                        b"HTTP/1.1 200 OK\r\n"          # Status Line
                        b"Content-Type: application/octet-stream\r\n"                                             
                        b"Content-Length: " + str(len(response_body)).encode("utf-8") + b"\r\n"     
                        b"\r\n" # Empty line
                        + response_body                                                   
                    )
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    elif path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    return response

def handle_connection(connection, files_directory):
    """Handle a single connections"""
    try:
        # Read the request
        request = b""
        while True:
            data = connection.recv(1024)
            request += data
            if len(data) < 1024:
                break
        request = request.decode("utf-8")
        print(f"Received request: {request}")

        response = handle_request(request, connection, files_directory)
        print(f"Sending response: {response.decode('utf-8', errors='ignore')}")
        connection.sendall(response)
    except Exception as e:
        print(f"Error handling request: {e}")
        connection.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
    finally:
        connection.close()

def start_server(host, port, files_directory):
    """Start the HTTP server and handle incoming connections"""
    server_socket = socket.create_server((host, port), reuse_port=True)
    print(f"Server started on {host}:{port}")

    while True:
        # Accept a connection
        connection, address = server_socket.accept()
        # Create a new thread to handle the connection
        thread = threading.Thread(target=handle_connection, args=(connection, files_directory))
        thread.start()               
        

def main():
    # Create an argument parser to handle command line arguments
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    # Add an argument to specify the directory where files are stored
    parser.add_argument("--directory", type=str, required=False, help="Directory where files are stored")
    args = parser.parse_args()
    print("Logs from your program will appear here!")
    start_server("localhost", 4221, args.directory)
        

if __name__ == "__main__":
    main()
