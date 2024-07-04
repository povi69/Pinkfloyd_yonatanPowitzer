import socket
import threading
from Data import parse_database_file

DATABASE_FILE = "Pink_Floyd_DB.txt"

albums = parse_database_file(DATABASE_FILE)
#returns the list of albums
def list_albums():
    return "\n".join(album['name'] for album in albums)
#returns all the songs name in the album the user inputs
def list_songs_in_album(album_name):
    for album in albums:
        if album['name'].lower() == album_name.lower():
            return "\n".join(song['name'] for song in album['songs'])
    return "Album not found."
#returns the song length (the user inputs the song name)
def get_song_length(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['duration']
    return "Song not found."
#returns the lyrics of a song (the user inputs the song name)
def get_song_lyrics(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['lyrics']
    return "Song not found."
#return the album by inputing the song name
def get_album_by_song_name(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return album['name']
import re

#done by chat gpt beacuse I was stuck on it for a while
def get_song_by_word(word):
    matching_songs = []
    for album in albums:
        for song in album['songs']:
            # Use regex to match whole words only (I didn't really get what does this line do but it works)
            if re.search(rf'\b{re.escape(word.lower())}\b', song['name'].lower()):
                matching_songs.append(song['name'])
    if not matching_songs:
        return "Song not found."
    return "\n".join(matching_songs)

def get_song_by_lyrics(lyrics):
    matching_songs = []
    for album in albums:
        for song in album['songs']:
            if lyrics.lower() in song['lyrics'].lower():
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
                response = get_album_by_song_name(song_name)
                client_socket.send(response.encode('utf-8'))
            elif command.startswith('6 '):
                song_name = command[2:].strip()
                response = get_song_by_word(song_name)
                client_socket.send(response.encode('utf-8'))
            elif command.startswith('7 '):
                song_name = command[2:].strip()
                response = get_song_by_lyrics(song_name)
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
    server_socket.bind(('localhost', 12345))  # Adjust port as needed and can change the "localhost" to ip of another pc to connect to it
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
