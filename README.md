# Echo To All Bot for Telegram
Entertaining Telegram Bot

[Try the my bot](https://t.me/EchogramBot)

About
------------
**Echo To All Bot. Telegram bot that sends your message to all bot users. Everything is anonymous**

Installation
------------
```shell
# Clone the repository
$ git clone https://github.com/onilyxe/Echogram.git

# Change the working directory to Echogram
$ cd Echogram
```

Configuring
------------
**Open `data/config.ini` configuration file with text editor and set the token:**

* `bot_token` is token for your Telegram bot. You can get it here: [BotFather](https://t.me/BotFather)
```ini
bot_token=0000000000:0000000000000000000000000000000000
```

**Open `handlers/users.py` and change the channel id for logs on line `189`**
**Open `handlers/admins.py` and change the channel id for logs on line `117, 120, 233`**
```ini
-100nnnnnnnnnn
```
* `-100nnnnnnnnnn` channel id, leave -100 at the beginning, and then change the id to your own. You can find it through this bot: [Test Attach](https://t.me/asmico_attach_bot).

**Install [SQLiteStudio](https://sqlitestudio.pl/) and open file `data/db.sql` and change the creator's id to your own so that you have access to the admin panel**

Running
------------
Using Python
```shell
# Install requirements
$ python3 -m pip install -r requirements.txt

# Run script
$ python3 bot.py
```