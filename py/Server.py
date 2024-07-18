import socket
import threading
from Data import parse_database_file
from Packet import packet

numberOfLiseners = 5
Port = 12345

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
    return "Song not found."

def get_album_by_song_name(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return album['name']
    return "Album not found."

def get_song_by_word(word):
    matching_songs = []
    word = word.lower()
    for album in albums:
        for song in album['songs']:
            if word in song['name'].lower().split():
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

def handle_client(client_socket, address):
    welcome_message = "Welcome to the Pink Floyd server! Please choose a command.\n"
    packet.write_packet(client_socket, 0, welcome_message, 0)

#Error 1: "Album not found"
#Error 2: "Song not found"
#Error 3: "Invalid commend"
    while True:
        request_call, command, error = packet.read_packet(client_socket)
        if not command:
            continue

        response = ""
        error_code = 0
        if command == '1':
            response = list_albums()
        elif command.startswith('2 '):
            album_name = command[2:].strip()
            response = list_songs_in_album(album_name)
            if response == "Album not found.":
                error_code = 1
        elif command.startswith('3 '):
            song_name = command[2:].strip()
            response = get_song_length(song_name)
            if response == "Song not found.":
                error_code = 2
        elif command.startswith('4 '):
            song_name = command[2:].strip()
            response = get_song_lyrics(song_name)
            if response == "Song not found.":
                error_code = 2
        elif command.startswith('5 '):
            song_name = command[2:].strip()
            response = get_album_by_song_name(song_name)
            if response == "Album not found.":
                error_code = 1
        elif command.startswith('6 '):
            word = command[2:].strip()
            response = get_song_by_word(word)
            if response == "Song not found.":
                error_code = 2
        elif command.startswith('7 '):
            lyrics = command[2:].strip()
            response = get_song_by_lyrics(lyrics)
            if response == "Song not found.":
                error_codse = 2
        elif command == '8':
            response = "Goodbye!"
            packet.write_packet(client_socket, 8, response, 0)
            break
        else:
            response = "Invalid command."
            error_code = 3

        packet.write_packet(client_socket, 1, response, error_code)

    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', Port))
    server_socket.listen(numberOfLiseners)
    print(f"Server is listening on port {Port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from {client_address} has been established.")
        #Using threading so mulipule clients can join the server
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
