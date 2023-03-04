# Second Strike Bot

Discord bot for setting up games in a small Valorant league I have with my friends.

## Current Features

- Map and side pick/ban system

## Limitations

- Only supports the pick/ban format described here:
![image](https://user-images.githubusercontent.com/23241280/219310485-55e1fcd6-da3b-4f7e-9d0e-1fbaa3c937a5.png)


## Getting Started

### Prerequisites

- `python` 3.8.7 (as of the last commit on 2/6/21)
- `pip` 
- `virtualenv`

### Setup

#### 0. Discord bot setup
This section is only necessary once to add the bot to your server.

1. Follow [this setup guide](https://discord.com/developers/docs/getting-started). Be sure to save your bots token for later!
2. Uncheck the "PUBLIC BOT" setting, unless you want other people to use the bot
3. Enaable the "MESSAGE CONTENT INTENT" setting
4. Follow [this setup guide](https://discord.com/developers/docs/getting-started) until you get to the **Adding scopes and permissions** section
5. For the "BOT PERMISSIONS" section, add the following permissions:
  [] Send Messages
  [] Add Reactions
  [] Read Messages / View Channels
6. Continue the the setup guide until you reach the "Running your app" section


#### 1. Installing dependencies
1. Clone this repo
2. Run `[python -m venv env](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)` in the root folder (the top-level `second-strike-bot` one). This will create a new `env` directory
3. Run the `activate` script in this newly created directory to create an isolated virtual development environment
  - Windows: `.\env\Scripts\activate`
  - Unix: `source env/bin/activate`
4. Run `pip install -r requirements.txt`

#### 2. Setting up your .env file
1. Create a file called `.env` in the root folder
2. Add this line: `DISCORD_TOKEN=token_from_step_0.1_here`
3. Add this line: `DISCORD_GUILD="Your Server Name Here"` (with the quotes)


### Development
Branch per feature with codeowner reviews.

Linting: `black <path/to/second_strike_bot>`

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>


## Using the Bot

### Hosting/Deployment

With your virtual environment activated, simply run the `bot.py` file (`python second-strike-bot\second_strike_bot\bot.py`). You should see your bot come online. Keep in mind that you need to be running the script in order for the bot to function. AWS EC2 or a Raspberry Pi would let you run this 24/7.

### Setting up a match

All you need to do is send a `/setup` command in a text channel and follow the messages/instructions from there. Here's an example text/voice channel setup:

![image](https://user-images.githubusercontent.com/23241280/219309579-ab6bd52c-4127-4be5-847d-598919467a20.png)


## License

This project is licensed under the Apache License - see the LICENSE file for details

## Acknowledgments

* [This readme template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)