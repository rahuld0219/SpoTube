import YoutubeWrite as yw
import SpotifyRead as sr


complete = sr.run()

if complete:
    yw.run()