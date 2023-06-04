#!/usr/bin/env python
# LED-Matrix code written by HZeller, altercations by Lucas Potter

# imports, you know the deal
import time
import feedparser
import random
import requests

from samplebase import SampleBase
from RGBMatrixEmulator import graphics
# from rgbmatrix import graphics

# depending on need, you can emulate the matrix. default output is localhost:8888

# LISTEN HERE. MOST THINGS WILL NOT WORK IF YOU DO NOT PUT IN YOUR OWN API KEYS.
# DO THAT HERE OR BE SAD WHEN YOUR SPOTIFY DOESN'T WORK

# mc server vars
mcURL = "https://api.mcsrvstat.us/2/[your server ip here]"
mcName = "your mc server name here"

# owm vars
# no spaces in the cityName var, or else the request will fail
cityName = "CityName,State,Country"
openweathermapAPIKey = "your OpenWeatherMap API key (or App ID) here"

# spotify vars
spotRefreshToken = 'a refresh token'  # follow this tutorial to get your refresh token / https://benwiz.com/blog/create-spotify-refresh-token/
spotClientID: 'a client id'  # get this from the spotify dev dashboard / https://developer.spotify.com/dashboard/
spotClientSecret: 'shhhhh very secret'  # this too


def getRequestFromQueue():  # get a request from the queue
    with open("data.txt", 'r+') as f:
        firstLine = f.readline()
        data = f.read()
        f.seek(0)
        f.write(data)
        f.truncate()
        print(firstLine)
        return firstLine


def checkQueue():  # see if there's anything in the queue
    with open("data.txt", "r") as qTest:
        if len(qTest.readlines()) > 0:
            return True
        else:
            return False


def mcStatus():  # check status of my minecraft server lol
    if mcName == "your mc server name here":
        return "Minecraft server status not set up, please do so"

    url = mcURL
    response = requests.get(url)
    data = response.json()
    if data["online"]:
        print(mcName + " is online, player count of" + str(data["players"]['online']))
        return mcName + " is online with " + str(data["players"]['online']) + " player(s)"
    else:
        print(mcName + " is offline, check server")
        return mcName + " is offline :("


def nOutput():  # get random news from the bbc & nyt
    bbc = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml?edition=us#")
    nyt = feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')

    newsList = []
    bbcLen = len(bbc.entries)
    nytLen = len(nyt.entries)
    print("nyt is " + str(nytLen) + " bbc is " + str(bbcLen) + " smallest is " + str(min(nytLen, bbcLen)))

    if min(nytLen, bbcLen) <= 0:
        return "News error, try again later"

    for i in range(min(nytLen, bbcLen)):  # oh hey. i fixed it.
        newsList.append(bbc.entries[i].title)
        newsList.append(nyt.entries[i].title)

    output = newsList[random.randint(0, min(nytLen, bbcLen)*2-1)]

    print(output)
    return output


def wOutput():  # get weather from OpenWeatherMap
    if openweathermapAPIKey == "your OpenWeatherMap API key (or App ID) here":
        return "Weather not set up, please do so"

    global wRequest
    weather = "https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&units=imperial&appid=" + openweathermapAPIKey

    wRequest = requests.get(weather)
    data = wRequest.json()
    temp = round(data['main']['temp'])
    cond = data['weather'][0]['description']
    output = "The weather in " + cityName + " is " + str(
        temp) + " degrees, " + cond  # listen i hardcoded the city name, you should do the same

    print(output)
    return output


def nowPlaying():  # get currently playing song from spotify
    global response

    if spotClientID == "a client id":
        return "Spotify not set up, please do so"

    tURL = 'https://accounts.spotify.com/api/token'  # get a fresh token
    tPayload = {
        'grant_type': 'refresh_token',
        'refresh_token': spotRefreshToken,
        'client_id': spotClientID,
        'client_secret': spotClientSecret,
    }

    data = requests.post(tURL, tPayload)
    token = data.json()['access_token']

    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:  # bug fix?
        response.status_code = "Connection refused"
        output = "Connection error, try again later"

    code = response.status_code
    print("Response Code: " + str(code))
    if code == 200:  # make sure everything's a-ok
        song = response.json()["item"]["name"]
        artist = response.json()["item"]["artists"][0]["name"]
        print("Current Song: " + song)
        print("Current Artist: " + artist)
        return "Now Playing: " + song + " by " + artist
    else:
        print("No song playing or request failed")
        return "No song playing"


class RunText(SampleBase):  # tbh no clue what's going on here, stole this from hzeller
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=wOutput())

    def run(self, newOut=True):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("7x13.bdf")
        textColor = graphics.Color(163, 171, 212)  # should be a nice color. maybe.
        pos = offscreen_canvas.width
        choices = [mcStatus, mcStatus, nowPlaying, nowPlaying, wOutput, wOutput, nOutput, nOutput, nOutput, nOutput,
                   nOutput, nOutput]
        # 1/6 mc, 1/6 spotify, 1/6 weather, 1/2 news

        while True:
            if newOut:  # is there something new?
                if checkQueue():  # is there something in the queue?
                    my_text = getRequestFromQueue().rstrip()
                    newOut = False
                else:
                    my_text = random.choice(choices)()  # pick something from a rigged slot machine
                    newOut = False
            offscreen_canvas.Clear()
            length = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if pos + length < 0:
                newOut = True  # this one's over, get something new
                pos = offscreen_canvas.width

            time.sleep(0.03)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":  # wtf is __name__ and __main__ anyway?
    run_text = RunText()
    if not run_text.process:
        run_text.print_help()
