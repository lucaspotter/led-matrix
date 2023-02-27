# *lucas potter's* led matrix

## please read this before you get grabbing

this is not exactly end user friendly code. there's some setup to be done before experimentation.

## setup

- make sure you're on the latest version of python. 2.7 won't work.
- decide whether you want it emulated or not
  - if you want it emulated, you can skip this step
  - otherwise, you've some work to do.
    - make and install hzeller's python binding [here](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)
    - change the import functions in `main.py`, `app.py`, and `showtime.py`
      - more specifically, change `from RGBMatrixEmulator import xyz` to `from rgbmatrix import xyz`
- decide on your arguments
  - what do i mean? open `samplebase.py`. we get to hardcode values yayyyyyy
  - the important ones are rows, cols, chain length, and brightness
    - `options.rows` is the length of your panel(s) in leds. usually 32 or 64.
    - `options.cols` is the width of your panel(s) in leds. again, usually 32 or 64.
    - `options.chain_length` is how many panels you have connected. please, for your safety, have a proper power supply for your panels.
    - `options.brightness` is how blinding you want your panel(s) to be.
- decide if you care about certain features
  - spotify's cool and all but you can't have my api keys.
  - there are several variables to be changed, depending on feature set.
    - `mcURL` and `mcName` are for communication with the amazing [mcsrvstat.us](https://mcsrvstat.us) website and api. change if you have a minecraft server you want to keep the status of.
    - `cityName` and `openweathermapAPIKey` are for communication with openweathermap's api. change if you want to get weather data.
	  - `cityname` is a weird variable. the proper format is `cityName,state,countryCode` with no spaces. state is optional if you aren't in the US. probably.
    - `spotRefreshToken`, `spotClientID`, and `spotClientSecret` are for communication with spotify's api. change if you want the ticker to display your currently playing song.
      - get your refresh token by following [this tutorial](https://benwiz.com/blog/create-spotify-refresh-token/)
      - get your client id and secret in the [spotify dashboard](https://developer.spotify.com/dashboard/)
  - there's also a flask server in `app.py` if you would like to easily input your own things or let others toss something on there.
- pray.


## alright now what?

with enough luck you should be up and running. i hate to say this, but i can't offer support. i don't know how half this works, god forbid i try explaining it lol


## credits

big thanks to hzeller and co for their work. this project wouldn't be a quarter of what it is now without their work.

another big thanks to the wonderful people at hack club for the funding and community. this project quite literally wouldn't exist without their help.