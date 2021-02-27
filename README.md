# Spotify To YouTube Playlist Converter

## Requirements
* Python3
* YouTube Data v3 API
* Spotipy API

## OAuth Requirements
* For Spotipy I used the Authorization Code flow and got my client id and secret from the Spotify developers project
  * NOTE: I set the client id and secret as environment variables
* For YouTube Data I created an OAuth consent screen and got a Client ID
  * NOTE: I used a Client Secrets file that you will also need to download and rename to CLIENT_SECRET.json

### Notes:
* Google Cloud limits how many requests you can make per day so it's possible large playlists might cause your program to be blocked if they use up too many requests and meet your quota
* Program works best with smaller playlists and has been tested working for small laylists but it will still all work for larger ones as long as the quota isn't exceeded