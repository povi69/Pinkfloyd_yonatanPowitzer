import socket

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 12345)  # Adjust host and port as needed
    client_socket.connect(server_address)

    try:
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
            print("8. Exit")
            command = input("=========================\n")

            if command == '8':
                client_socket.send(command.encode())
                response = client_socket.recv(1024).decode()
                print(response)
                break

            if command in ['1']:
                # Send command to server
                client_socket.send(command.encode())
            else:
                # Get the parameter for the command
                if command in ['2']:
                    parameter = input("Enter the album name: ")
                elif command in ['3', '4', '5']:
                    parameter = input("Enter the song name: ")
                elif command in ['6', '7']:
                    parameter = input("Enter the keyword: ")
                elif command in ['8']:
                    client_socket.send(command.encode())
                else:
                    print("Invalid Input. Please try again.")
                    continue

                # Send command and parameter to server
                client_socket.send(f"{command} {parameter}".encode())

            # Receive response from server
            response = client_socket.recv(1024).decode()
            print(response)

    finally:
        # Close the socket connection
        client_socket.close()

#If the source file is executed as the main program, the interpreter sets the __name__
# variable to have a value “__main__”. If this file is being imported from another module,
# __name__ will be set to the module’s name.
if __name__ == "__main__":
    main()
