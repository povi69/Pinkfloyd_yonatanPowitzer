import socket
from Packet import packet

port = 12345

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    client_socket.connect(server_address)

    request_call, welcome_message, error = packet.read_packet(client_socket)
    print(welcome_message)

    while True:
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
            packet.write_packet(client_socket, 8, command, 0)
            request_call, response, error = packet.read_packet(client_socket)
            print(response)
            break

        if command in ['1']:
            packet.write_packet(client_socket, 1, command, 0)
        else:
            if command in ['2']:
                parameter = input("Enter the album name: ")
            elif command in ['3', '4', '5']:
                parameter = input("Enter the song name: ")
            elif command in ['6', '7']:
                parameter = input("Enter the keyword: ")
            else:
                print("Invalid Input. Please try again.")
                continue

            full_command = f"{command} {parameter}"
            packet.write_packet(client_socket, 1, full_command, 0)

        # Transfers the data in client_socket to request_call, response and error
        request_call, response, error = packet.read_packet(client_socket)
        print(response)
        if error != 0:
            print(f"Error: {error}")
            client_socket.close()
            break

if __name__ == "__main__":
    main()
