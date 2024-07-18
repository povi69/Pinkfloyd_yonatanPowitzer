def parse_database_file(database_file):
    albums = []

    with open(database_file, 'r', encoding='utf-8') as dataFile:
        current_album = None
        current_song = None
        for line in dataFile:
            line = line.strip()
            if line.startswith('#'):
                # New album header
                album_info = line[1:].strip().split('::')
                album_name = album_info[0]
                release_year = album_info[1]
                current_album = {
                    'name': album_name,
                    'year': release_year,
                    'songs': []
                }
                albums.append(current_album)
            elif line.startswith('*'):
                # Song line
                #strip() removes spaces or blank spaces
                #split() seperate the object with a paremeter
                if current_album is not None:
                    song_info = line[1:].strip().split('::')
                    song_name = song_info[0]
                    composer = song_info[1]
                    duration = song_info[2]
                    lyrics = song_info[3]
                    current_song = {
                        'name': song_name,
                        'composer': composer,
                        'duration': duration,
                        'lyrics': lyrics
                    }
                    current_album['songs'].append(current_song)
            else:
                # Continuing lyrics for the current song
                if current_song is not None:
                    current_song['lyrics'] += f'\n{line}' if len(line) > 0 else ''

    return albums
