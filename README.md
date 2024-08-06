# spotil
A python program that can download songs listed in a public Spotify Playlist.

This is done in a few steps:

- First the tracks present in the playlist are read, along with the artist associated with them through the Spotify API (The desired playlist is specified using its ID, which is the last portion of URL that is generated when the playlist is shared).

- The program then constructs search queries to YouTube containing each track name along with the associated artist. When the search results are returned, the ID of the first result is pulled then used to construct a watch query.

- This watch query is then passed to the Python library yt-dlp, which then downloads the audio of the video associated with the watch query.

The program also makes use of two `.txt` files, a `.env` file and a directory called `downloaded` in order to function properly:
- pullPlaylist.txt
  - This is used by the program to store the ID of the playlist which is currently being read from.

- installed.txt
  - This is used by the program to keep track of the songs which have already been downloaded from the current playlist. This allows the program to be used on the same playlist more than once and only download tracks which it has not yet downloaded.

- downloaded `DIRECTORY`
  - This is the directory where tracks will be placed after being downloaded.

## Important
The program requires a `.env` file containing the two environment varibles `CLIENT_ID` and `CLIENT_SECRET`. These can both be accessed by creating a free [Spotify Developer](https://developer.spotify.com/) account.

The format of this file should be:
```
CLIENT_ID = "YOUR-ID"
CLIENT_SECRET = "YOUR-SECRET"
```

## Required Libraries

- base64
- josn
- requests
- post from requests
- urllib.request
- re
- os
- yt_dlp
- load_dotenv from dotenv

These can all be installed using `pip install LIBRARY-NAME` or by using the command:
- `pip install -r requirements.txt`

## Program Usage
`set-id` - Set the current pull-playlist ID.

`pull` - Used to download new tracks present in the playlist.

`show-id` - Shows the current pull-playlist ID.

`exit` - Used to exit the program.



  
