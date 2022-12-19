import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import json

# function for show song list
def show_my_song_list(limit, offset, user_id):
    try:
        
        #data = json.load(open('user_info/U00179aea462d20ed50e7973e17829732.json'))
        data = json.load(open('user_info/'+user_id+'.json'))
        #print(data['client_id'])
        #print(data['client_secret'])
        try:
            auth_manager=SpotifyOAuth(client_id=data['client_id'],
                                                client_secret=data['client_secret'],
                                                redirect_uri="https://fa79-36-237-102-99.jp.ngrok.io/spotify",
                                                scope="user-library-read")
            sp = spotipy.Spotify(auth_manager=auth_manager)
            results = sp.current_user_saved_tracks(limit=limit, offset=offset) #at most get 50 once
            return results
        except Exception:
            return None
    except Exception:
        return None
    
def get_artist_info(user_id, name):
    try:
        # init spotify api
        data = json.load(open('user_info/'+user_id+'.json'))
        client_credentials_manager = SpotifyClientCredentials(client_id=data['client_id'], client_secret=data['client_secret'])
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        results = sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return results
        else:
            return None
    except Exception:
        return "error in get data"

def show_all_album(user_id):
    data = json.load(open('user_info/'+user_id+'.json'))
    client_credentials_manager = SpotifyClientCredentials(client_id=data['client_id'], client_secret=data['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    current_artist_info = json.load(open('user_info/current_artist.json'))
    artist_name = current_artist_info['artist_name']
    results = json.load(open('artist_info/'+artist_name+'.json'))
    artist = results['artists']['items'][0]

    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    founded_album = None
    unique = set()  # skip duplicate albums
    album_list = []
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            unique.add(name)
            album_list.append(name)
    return "\n".join(album_list)

def get_album_info(user_id, album_name):
    # init spotify api
    data = json.load(open('user_info/'+user_id+'.json'))
    client_credentials_manager = SpotifyClientCredentials(client_id=data['client_id'], client_secret=data['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    current_artist_info = json.load(open('user_info/current_artist.json'))
    artist_name = current_artist_info['artist_name']
    results = json.load(open('artist_info/'+artist_name+'.json'))
    artist = results['artists']['items'][0]

    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    founded_album = None
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            unique.add(name)
            if name == album_name:
                founded_album = album
    return founded_album

def show_all_track(user_id):
    data = json.load(open('user_info/'+user_id+'.json'))
    client_credentials_manager = SpotifyClientCredentials(client_id=data['client_id'], client_secret=data['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    current_artist_info = json.load(open('user_info/current_artist.json'))
    album = json.load(open('artist_info/'+current_artist_info['artist_name'] + '_' + current_artist_info['album_name'] + '.json'))

    founded_track = None
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    song_list = [track['name'] for track in tracks]
    return '\n'.join(song_list)
        

def get_track_info(user_id, track_name):
    # init spotify api
    data = json.load(open('user_info/'+user_id+'.json'))
    client_credentials_manager = SpotifyClientCredentials(client_id=data['client_id'], client_secret=data['client_secret'])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    current_artist_info = json.load(open('user_info/current_artist.json'))
    album = json.load(open('artist_info/'+current_artist_info['artist_name'] + '_' + current_artist_info['album_name'] + '.json'))

    founded_track = None
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        if track['name'] == track_name:
            founded_track = track
    return founded_track
