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

readPullFile = open("dependencies/pullPlaylist.txt","r")
writePullFile = open("dependencies/pullPlaylist.txt","a")

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

    print("\n")
    print("--------START--------")

    for track in result:
        currentData = f"{track['track']['name']} - {track['track']['artists'][0]['name']}"
        print(currentData)
        trackList.append(currentData)

        if(f"{currentData}\n" not in alreadyInstalled):
            new.append(currentData)
            writeInstalledFile.writelines(f"{currentData}\n")

    
    print("---------END---------")
    print("\n")

    print("---------NEW---------")

    for track in new:
        print(f"New: {track}")
        get_youtube_link(track)


    print("---------------------")
    print("\n")

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
        'outtmpl': '.\downloaded\%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#   Function to clear the text file in which the pull-playlist ID is stored when ID is updated

def clearPullFile():
    writePullFile = open("dependencies/pullPlaylist.txt","w")
    writePullFile.close()
    writePullFile = open("dependencies/pullPlaylist.txt","a")

#   Function to clear file containing all previously installed songs when playlist ID is changed

def clearInstalledFile():
    writeInstalledFile = open("dependencies/installed.txt","w")
    writeInstalledFile.close()
    writeInstalledFile = open("dependencies/installed.txt","a")

#   This portion check whether the playlist ID has been specified or not, but checking tho see whether the pullPlaylist file is
# is empty or not

first_char = readPullFile.read(1)

if not first_char:
    pullSet = False

else:
    pullSet = True
    playlist_id = first_char + readPullFile.readline().strip()

#   Main program loop

while True:
    userCommand = input("spotil> ")

    if(userCommand == "set-id"):
        pullChange = input("Playlist ID: ")
        playlist_id = pullChange
        pullSet = True
        clearPullFile()
        writePullFile.write(pullChange)

    elif(userCommand == "pull"):
        if(pullSet == True):
            get_playlist_tracks(token, playlist_id)

        else:
            print("Pull playlist not set, default will be used (Use command 'pull-set' to specify playlist ID)")
            playlist_id = "4zjRKXhbBEkoz8iaDLhYKj?si=848546a7348b4514"
            get_playlist_tracks(token, playlist_id)

    elif(userCommand == "show-id"):
        print(f"Pull Playlist ID: {playlist_id}")


    elif(userCommand == "exit"):
        print("Thank you for using :)")
        break