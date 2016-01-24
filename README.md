# WolfBot
A Wolfram Alpha Discord bot.

## Requirements
- Python 3.4.2+
- `aiohttp` library
- `websockets` library
- `discord.py` library (`pip install git+https://github.com/Rapptz/discord.py@async`)
- `wolframalpha` library

`pip install` can handle these for you. 

Make sure you're using the python3 versions of the pip libraries.
```
sudo apt-get install python3-pip
sudo pip3 install MODULE_NAME
```
## Setup
1. Create an account on [Wolfram Alpha](https://developer.wolframalpha.com/portal/apisignup.html) and get yourself an app ID.
2. Create an account for the bot on [Discord](discordapp.com).
3. Copy `credentials_example.py` to `credentials.py` and fill in the Wolfram Alpha and Discord details.
4. Find your own Discord user ID and put it into the `owner_id` section of the credentials.
5. Run the bot `python3 wolfbot.py`.

## Using the bot
### Bot commands
The bot can be called into action using `!wolf` which also provides a list of commands:

Command       | Description
------------- | -------------
!wolf \<query\> | Queries Wolfram with anything you desire (replace \<query\>). Provides a short two section output.
!wolf+ \<query\>| Works the same was as !wolf <query> but provides the entire output from Wolfram.
!wolf kill    | Kills the bot process, only the owner can use this.
!wolf clean   | Cleans up the bots previous outputs.

## Examples

<img src="https://zippy.gfycat.com/DimpledDependentEagle.gif" width="800">
<img src="https://zippy.gfycat.com/FreeWaryBittern.gif" width="800">
<img src="https://zippy.gfycat.com/SophisticatedPerkyElkhound.gif" width="800">

## Shoutouts
Thanks to [Rapptz](https://github.com/Rapptz) for [discordpy](https://github.com/Rapptz/discord.py) which this bot uses.
