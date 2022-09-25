<h1 align="center">Echo To All Bot for Telegram</a> 
<img src="https://raw.githubusercontent.com/onilyxe/Echogram/main/image/telegram.webp" height="32"/></h1>
<p align="center">
	<b>Entertaining Telegram Bot.</b></p>
<p align="center">
	<a href="https://t.me/EchogramBot">Try the my bot
</p>

## About
**Echo To All Bot. Telegram bot that sends your message to all bot users. Everything is anonymous.**

## Commands
* /start - Старт
* /help - Помощь
* /rules - Правила
* /nick - Управление ником
* /stats - Статистика
* /cmd - Команды
* /admincmd - Админ команды

## Installation
```shell
# Clone the repository
$ git clone https://github.com/onilyxe/Echogram.git

# Change the working directory to Echogram
$ cd Echogram
```

## Configuring
**Open `data/config.ini` configuration file with text editor and set the token:**
* `bot_token` is token for your Telegram bot. You can get it here: [BotFather](https://t.me/BotFather)
```ini
bot_token=1234567890:AAA-AaA1aaa1AAaaAa1a1AAAAA-a1aa1-Aa
```

*  **Open `handlers/users.py` and change the channel id for logs on line `189`**
*  **Open `handlers/admins.py` and change the channel id for logs on line `117, 120, 223`**
```ini
-1001635530740
```
* `-100nnnnnnnnnn` channel id, leave -100 at the beginning, and then change the id to your own. You can find it through this bot: [Test Attach](https://t.me/asmico_attach_bot).

## Running
### Using Python
```shell
# Install requirements
$ python3 -m pip install -r requirements.txt

# Run script
$ python3 bot.py
```