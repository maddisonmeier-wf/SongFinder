import json
import sys
import spotipy
import spotipy.util as util

username = 'mmeier2'
new_playlist_name = 'Test Songs'



def find_songs():
    scope = 'playlist-read-collaborative'
    playlist_name = 'Tropical House Hoes and Hoodrat Shit'

    token = util.prompt_for_user_token(username, scope)

    if token:
        spotify = spotipy.Spotify(auth=token)

        user = spotify.current_user()
        playlists = spotify.user_playlists(user['id'])

        # filter out the playlists we dont want to look for
        playlist = filter(lambda playlist: playlist['name'] == playlist_name, playlists['items'])[0]

        # grab the id to add the new songs to
        new_playlist = filter(lambda playlist: playlist['name'] == new_playlist_name, playlists['items'])[0]
        new_playlist_id = new_playlist['id']
        print new_playlist['name']
        print new_playlist['id'] == playlist['id']

        # get how many songs each has
        playlist_song_count = playlist['tracks']['total']
        new_playlist_song_count = new_playlist['tracks']['total']

        print playlist_song_count
        print new_playlist_song_count

        for x in range(0,(playlist_song_count/100)+1):
            offset = 100*x
            print offset
            # the current targeted playlist tracks
            playlist_tracks = spotify.user_playlist_tracks(user['id'],
                                    playlist['id'], offset=offset)['items']
            print len(playlist_tracks)


        for x in range(0,(new_playlist_song_count/100)+1):
            offset = 100*x
            print offset
            # the current test playlist tracks
            new_playlist_tracks = spotify.user_playlist_tracks(user['id'], new_playlist['id'],
                offset=offset)['items']
            print len(new_playlist_tracks)

        # create a list of all songs currently in old playlist and
        # in test playlist
        songs = [track['track'] for track in playlist_tracks]
        songs.extend([track['track'] for track in new_playlist_tracks])

        existing_song_ids = []
        existing_song_names = []
        existing_song_albums = []

        playlist_artist_ids = []
        playlist_artist_names = []

        for song in songs:
            # add existing song info for no repeats
            existing_song_ids.append(song['id'])
            existing_song_names.append(song['name'])
            existing_song_albums.append(song['album']['name'])

            for artist in song['artists']:
                if artist['name'] not in playlist_artist_names and  \
                    artist['id'] not in playlist_artist_ids:
                    playlist_artist_ids.append(artist['id'])
                    playlist_artist_names.append(artist['name'])

        tracks_to_add = [] # ids of new tracks

        for index, artist in enumerate(playlist_artist_ids):
            print "INFO: grabbing %s top songs" % playlist_artist_names[index]
            top_tracks = spotify.artist_top_tracks(artist)['tracks']
            for track in top_tracks:
                if track['name'] in existing_song_names:
                    print "found %s already in here" % track['name']
                    track_index = existing_song_names.index(track['name'])
                    if track['id'] != existing_song_ids[track_index] and \
                        track['album']['name'] != existing_song_albums[track_index]:
                        tracks_to_add.append(track['uri'])
                else:
                    tracks_to_add.append(track['uri'])

        testing = {'uris': tracks_to_add[:100]}
        print json.dumps(testing)
        #add new tracks
        # for track in tracks_to_add:
        # print spotify._post("users/%s/playlists/%s/tracks" % (user['id'], new_playlist_id),
        #                     payload = testing)


def create_test_playlist():
    scope = 'playlist-modify-public'

    token = util.prompt_for_user_token(username, scope)

    if token:
        spotify = spotipy.Spotify(auth=token)
        user = spotify.current_user()

        test_playlist = spotify.user_playlist_create(user['id'], new_playlist_name)

        print test_playlist

option = sys.argv[1]

if option == 'create':
    create_test_playlist()

elif option == 'find_songs':
    find_songs()
