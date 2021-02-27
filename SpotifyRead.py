#to set environment variables
import os
#for spotipy api
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#sets necessary environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'YOUR CLIENT ID'
os.environ["SPOTIPY_CLIENT_SECRET"]='YOUR CLIENT SECRET'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/'

#checks if a playlist has been found
found = False

#sets up spotify oauth this could jsut be done in the code later I just made it a method
def setup():
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp

#returns a list of the user's playlists
def getPLList(sp):
    #default limit at 50 playlists, can change this later this works for testing
    plList = sp.current_user_playlists()
    return plList

def parsePL(listIn, sp):
    #Note: any titles with emoji don't work
    plName = input("Which playlist would you like to convert?: ")
    #holds playlists
    pList = None
    #holds track info
    trackList = []

    #isolates currList as the items field of the current playlist
    # which basically isolates all data about that specific list
    for currList in listIn['items']:
        #finds name of current list
        name = currList['name']
        #if the current list is the right one it runs
        if name == plName:
            #isolates the playlit id from the URI wihc is normally formatted as spotify:playlist:PLAYLISTID
            currID = currList['uri'].split(":")[2]

            # finds length of the full list because playlist_items has a max limit of 100 that it can
            # pull at a time so if length > 100 I need to parse through it
            fullList = int(sp.playlist_items(currID, fields='total').pop('total'))

            # playlist_items allows for you to set a default offset that you can use to start parsing
            # the playlist from so i use this variable to keep track of how many I've already read
            currOff = 100

            # gets the first <=100 items
            pList = sp.playlist_items(currID)['items']

            # loops through the full playlist by using the offset if there is more than 100 items in the list
            while fullList > currOff:
                pList.extend(sp.playlist_items(currID,offset=currOff)['items'])
                currOff = currOff + 100

            found = True
            break
    
    #in case an incorrect title was typed
    if not found:
        print("Playlist \"", plName, "\" not found :(\n")
        return
    
    for currTrack in pList:
        #stores artist and title info in tuple format
        trackList.append((currTrack['track']['album']['artists'][0]['name'], currTrack['track']['name']))
    
    writeToFile(plName, trackList)

def writeToFile(listName, trackList):
    #creates a new file if it doesn't exist already
    f = open("tracks.txt", 'w')
    # writes playlist title to top of file
    f.write(listName + '\n')
    #writes to file in "'song' by 'artist'" format
    for curr in trackList:
        currStr = curr[1] + " by " + curr[0] + "\n"
        f.write(currStr)
    f.close()

def run():
    spObj = setup()
    listList = getPLList(spObj)
    parsePL(listList, spObj)

    return True
