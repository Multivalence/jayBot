# Jay Bot

Bot for Fiverr.


# General Installation Guide (commands may differ based on the Operating System you use)

*Note: It is assumed that you already have Python 3.8 - 3.9.6+ installed and have obtained a bot token from the discord developer portal. If you have Python 3.10+, this bot may not work as it has not been tested on that version*


1. Download or clone this repository via the Green button on the top right that says "Code"
2. Drag the download to your Desktop and unzip it (if you downloaded it)
3. Open the file named `.env` in a text editor
4. Paste your bot token in the token field (`TOKEN = <your token here>`)
5. Type the prefix you would like the bot to have in the prefix field (`PREFIX = <your prefix here>`)
6. For the input-channel field, copy the channel ID of where your embeds are being sent and input it in this field (`INPUT-CHANNEL = <channel_id here>`)
7. For the output-channel field, copy the channel ID of where you want the formatted embeds to be sent and input it in this field (`OUTPUT-CHANNEL = <channel_id here>`)
8. Run command prompt and type `cd Desktop` followed by `cd jayBot-master`
9. Type `python3 -m pip install -r requirements.txt` and wait till the packages are finished installing
10. Type `python app.py` and you're all set. Keep the command prompt running to keep the bot online.
