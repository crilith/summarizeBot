When the bot is running in your channel you can type `!summarize #` it will then take the last # hours of messages and send them to gemini 2.5 flash to have them summarized and then DM'd to the user.

You need to make a file named `.env` in the same folder as the python script. Inside you need to designate:
* `DISCORD_TOKEN=XXXXXXXXXXXXXXXXXXXXXXX`
* `GEMINI_TOKEN=YYYYYYYYYYYYYYYYYYYYYYYY`
