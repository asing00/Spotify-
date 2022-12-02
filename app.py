
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


import requests



client_id = 'CLIENT ID '
client_secret = 'Y SECRET KEY'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


artist_name = "Ludwig van Beethoven"

result = sp.search(artist_name) #search query

#print(result['tracks']['items'][0]['artists'][0])


def call_playlist(creator, playlist_id):


    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
        
    playlist_df = pd.DataFrame(columns = playlist_features_list)

    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]

    for track in playlist:
            # Create empty dict
            playlist_features = {}
            # Get metadata
            playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
            playlist_features["album"] = track["track"]["album"]["name"]
            playlist_features["track_name"] = track["track"]["name"]
            playlist_features["track_id"] = track["track"]["id"]
            
            # Get audio features
            audio_features = sp.audio_features(playlist_features["track_id"])[0]
            for feature in playlist_features_list[4:]:
                playlist_features[feature] = audio_features[feature]
            
            # Concat the dfs
            track_df = pd.DataFrame(playlist_features, index = [0])
            playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

        #Step 3
            
    return playlist_df

df = pd.DataFrame(call_playlist("spotify","37i9dQZF1DXdTVW77weWfh"))

print(df.to_string())
