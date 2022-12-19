# Shows a user's playlists

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="5ec8cb5e8fc6497ba83ab58506023110", 
    client_secret="2f8b2adc346b475ab7edfb735927c94f", 
    redirect_uri="http://loacalhost:8888/callback", 
    scope=scope))

results = sp.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
    print("%d %s" % (i, item['name']))