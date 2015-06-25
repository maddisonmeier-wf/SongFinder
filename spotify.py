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
        new_playlist_id = filter(lambda playlist: playlist['name'] == new_playlist_name, playlists['items'])[0]['id']

        playlist_tracks = spotify.user_playlist(user['id'],
                                    playlist['id'])['tracks']['items']

        songs = [track['track'] for track in playlist_tracks]
        existing_song_ids = [song['id'] for song in songs]

        playlist_artists = []

        for song in songs:
            for artist in song['artists']:
                if artist['id'] not in playlist_artists:
                    playlist_artists.append(artist['id'])

        tracks_to_add = [] # ids of new tracks

        for artist in playlist_artists:
            print "INFO: grabbing %s top songs" % artist
            top_tracks = spotify.artist_top_tracks(artist)['tracks']
            for track in top_tracks:
                if track['id'] not in existing_song_ids and \
                    track['uri'] not in tracks_to_add:
                    tracks_to_add.append(track['uri'])


        print tracks_to_add[0]
        #add new tracks
        for track in tracks_to_add:
            spotify._post("users/%s/playlists/%s/tracks" % (user['id'], new_playlist_id),
                            payload = {'uris': [track]})
        # spotify.user_playlist_add_tracks(user['id'], new_playlist_id, tracks_to_add)


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
