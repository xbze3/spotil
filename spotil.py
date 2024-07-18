import base64
import json
import requests
import urllib.request
import re
import os
import yt_dlp


from dotenv import load_dotenv
load_dotenv()

from requests import post

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#   Function to get session token from spotify API

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)

    json_result = json.loads(result.content)
    
    token = json_result["access_token"]

    return token

token = get_token()

#   Function to create authorisation header when token value is passed

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#   Function to get the track names from the specified spotify playlist

def get_playlist_tracks(token, playlist_id):

    readInstalledFile = open("dependencies/installed.txt","r")
    writeInstalledFile = open("dependencies/installed.txt","a")

    field = "fields=tracks.items(track(name, artists(name)))"
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "&" + field
    headers = get_auth_header(token)

    result = requests.get(url, headers = headers)
    result = result.json()['tracks']['items']

    trackList = []
    alreadyInstalled = []
    new = []

    for track in readInstalledFile.readlines():
        alreadyInstalled.append(track)

    for track in result:
        currentData = f"{track['track']['name']} - {track['track']['artists'][0]['name']}"
        trackList.append(currentData)

        if(f"{currentData}\n" not in alreadyInstalled):
            new.append(currentData)
            writeInstalledFile.writelines(f"{currentData}\n")

    for track in new:
        get_youtube_link(track)

    readInstalledFile.close()
    writeInstalledFile.close()

#   Function to query Youtube API for the link to the top related video associated with the song name pulled from the spotify playlist
    
def get_youtube_link(track_name):
    search_keyword = track_name.replace(" ", "+")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    download_video(url)

# Function to download videos associated with the previously created links
    
def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': r'.\downloaded\%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#   Main Script

playlist_id = "4zjRKXhbBEkoz8iaDLhYKj?si=848546a7348b4514"

get_playlist_tracks(token, playlist_id)