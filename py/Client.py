import socket

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 12345)  # Adjust host and port as needed
    client_socket.connect(server_address)

    try:
        while True:
            # Receive welcome message from server
            welcome_message = client_socket.recv(1024).decode()
            print(welcome_message)

            while True:
                # Get user input for command
                print("=========================")
                print("1. List of albums")
                print("2. Songs in an album")
                print("3. Length of a song")
                print("4. Lyrics of a song")
                print("5. Find album of a song")
                print("6. Search song by name")
                print("7. Search song by lyrics")
                print("Type exit to exit")
                command = input("=========================\n")


                #Send command to server
                client_socket.send(command.encode())

                # Receive response from server
                response = client_socket.recv(1024).decode()

                # Handle exit command
                if command.lower() == 'exit':
                    break

    finally:
        # Close the socket connection
        client_socket.close()

if __name__ == "__main__":
    main()
