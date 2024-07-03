import socket
import threading
from Data import parse_database_file

DATABASE_FILE = "Pink_Floyd_DB.txt"

albums = parse_database_file(DATABASE_FILE)

def list_albums():
    return "\n".join(album['name'] for album in albums)

def list_songs_in_album(album_name):
    for album in albums:
        if album['name'].lower() == album_name.lower():
            return "\n".join(song['name'] for song in album['songs'])
    return "Album not found."

def get_song_length(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['duration']
    return "Song not found."

def get_song_lyrics(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['lyrics']
    return "song not found."

def get_song_by_word(word):
    matching_songs = []
    for album in albums:
        for song in album['songs']:
            if word.lower() in song['name'].lower():
                matching_songs.append(song['name'])
    if not matching_songs:
        return "Song not found."
    return "\n".join(matching_songs)


# Handle client connection
def handle_client(client_socket, address):
    welcome_message = "Welcome to the Pink Floyd server! Please choose a command.\n"
    client_socket.send(welcome_message.encode('utf-8'))

    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if not command:
                continue

            if command == '1':
                response = list_albums()
            elif command.startswith('2 '):
                album_name = command[2:].strip()
                response = list_songs_in_album(album_name)
            elif command.startswith('3 '):
                song_name = command[2:].strip()
                response = get_song_length(song_name)
                client_socket.send(response.encode('utf-8'))
            elif command.startswith('4 '):
                song_name = command[2:].strip()
                response = get_song_lyrics(song_name)
                client_socket.send(response.encode('utf-8'))
            elif command.startswith('5 '):
                song_name = command[2:].strip()
                response = get_song_by_word(song_name)
                client_socket.send(response.encode('utf-8'))
            elif command == '8':
                response = "Goodbye!"
                client_socket.send(response.encode('utf-8'))
                break
            else:
                response = "Invalid command."

            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

    client_socket.close()

# Main server function
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Adjust port as needed
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
