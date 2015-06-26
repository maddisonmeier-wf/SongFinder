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
        playlist_artist_ids = []
        playlist_artist_names = []

        for song in songs:
            # add existing song info for no repeats
            existing_song_ids.append(song['id'])

            for artist in song['artists']:
                if artist['id'] not in playlist_artist_ids:
                    playlist_artist_ids.append(artist['id'])
                    playlist_artist_names.append(artist['name'])

        tracks_to_add = [] # ids of new tracks

        for index, artist in enumerate(playlist_artist_ids):
            print "INFO: grabbing %s top songs" % playlist_artist_names[index]
            top_tracks = spotify.artist_top_tracks(artist)['tracks']
            for track in top_tracks:
                if track['id'] not in existing_song_ids and \
                    track['uri'] not in tracks_to_add:
                    print "not found adding: %s " % track['name']
                    tracks_to_add.append(track['uri'])


        new_track_count = len(tracks_to_add)
        print "found %s new songs to add" % new_track_count

        for x in range(0,new_track_count/100):
            print "adding values in range %s-%s" % (x, x+100)
            adding_tracks = {'uris': tracks_to_add[x:x+100]}
            #add new tracks
            # for track in tracks_to_add:
            print spotify._post("users/%s/playlists/%s/tracks" % (user['id'], new_playlist_id),
                                payload = adding_tracks)


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
