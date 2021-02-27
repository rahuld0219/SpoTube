import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'CLIENT_SECRET.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

ACTIONS = ('get', 'list', 'set')

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

#reads in song titles and artists from file
def readFile(fileName):
    if(os.path.exists(fileName)):
        f = open(fileName,'r')
        text = f.readlines()
        for ind, curr in enumerate(text):
            #strips newlines on each element
            text[ind] = curr.strip()
        return text
    else:
        print("text file does not exist")

#creates a playlist with the name and inserts videos to it
def writePlaylist(yt, lines):
    #to define and create a new private playlist
    body = dict(
        snippet=dict(
            title=lines[0],
            description= "Music playlist created from your Spotify playlist"
        ),
        status=dict(
            privacyStatus='private'
        ) 
    )

    plID = yt.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()

    #holds song data specifically id
    songs = []
    #runs through every song title to search it
    for ind, query in enumerate(lines):
        #skips name of palylist
        if ind > 0:
            #finds the top 5 results of the song
            response = yt.search().list(
                q=query,
                part='id,snippet',
                maxResults = 5
            ).execute()
            #goes through and finds the first instance of a video with an accurate title
            #this is to skip over any channels or playlist results
            for currResult in response.get('items', []):
                if currResult['id']['kind'] == 'youtube#video':
                    #adds id to songs list that contain the video id
                    songs.append(currResult['id']['videoId'])
                    #this is so that the same song isn't added multiple times
                    break
    #runs through songs and adds them to our playlist
    for ind, curr in enumerate(songs):
        response = yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    #id from earlier
                    "playlistId": plID['id'], 
                    "resourceId": {
                        "kind": 'youtube#video',
                        # element of id
                        "videoId": curr
                    }
                }
            }
        ).execute()


def run():
    youtube = get_authenticated_service()
    lines = readFile("tracks.txt")
    writePlaylist(youtube, lines)