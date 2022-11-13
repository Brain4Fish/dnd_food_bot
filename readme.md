#  DND Party Food Tracker

## Why?

We love to play DND (dungeon and dragons) RPG game. It takes pretty big amout of time and of cource we wanna eat somethig except snacks. We order food via deliver but we have one problem, we spend plenty amount of time to decide, who should order food today an what kind of food was in previous times. To help us save some time on this we've decided to write this small telegram bot, that will help us save some time and start adventure a little bit earlier

In first view you can think, that we spend not so much time on this. BUT, let's calculate. For example, we spend 10 minutes to choose who should order the food every play. Every month we play at least 4 times, that means that we spend 40 minutes per month to remembering past orders. But sometimes we play 6-8 times per month which will give 80 (!) minutes of choosing food every month or 12 * 80 = 960 minutes or 16 hours of choosing per year! You can spend this time in cool fighting with ogre or licking mimic door

## How to install (without docker)

1. Create new bot via BotFather. Disable bot privacy to read input from chat

2. Place your token into file `config.py` like this

```TOKEN = 'XXXXXX:YYYYYYYYYYYY'```

Or if you wanna use env var, then you can use:

```export BOT_TOKEN=XXXXXX:YYYYYYYYYYYY```

3. Download all dependencies via: ```pytohn3 -m pip install -r requirements.txt```

4. Then start your bot with ```python3 ./bot.py```

5. Add your bot to telegram group with your friends!

6. Clean all dungeons!

## Use dockerised version

Docker/Podman should be installed and then you can simply build image with:

```docker build -t dnd-bot:latest .```

After successful build run it like:

```docker run --restart=always -d -e BOT_TOKEN='XXXXXX:YYYYYYYYYYYY' -v ./db:/modules/db dnd-bot:latest```

where:

 * **-d** - detach from console. Your container will run in background
 * **-e BOT_TOKEN** - define your token in env var
 * **-v ./db:/modules/db** - define your host folder that will be user as host mount bind for database 


## Commands

This bot has two main commands:

 * ```/start``` - it's user menu, where you can check, who should make next order, check last 10 orders and add today's order
 * ```/settings``` - it's kind of admin menu where you can define users that should be in your food rotation and where you can define food types

## TODO

 * Allow delete users and food types
 * Add docker-compose file
