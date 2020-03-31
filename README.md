# dice-boy
A simple bot for playing RPGs over discord

# Installation
1. [Follow these steps](https://discordpy.readthedocs.io/en/latest/discord.html) to setup a bot account. Be sure to hang on to your token from step 7.
2. Get [discord.py](https://github.com/Rapptz/discord.py) up and running (voice support not required. Python virtual environments recommended.)
3. Clone this repository.
4. Paste your token into environments_template.json in the "token" property. Rename this file to "environments.json".
5. Fill out the campaign and system info in environments.json as you see fit. It's all metadata. Be sure to set the "default" property to match the campaign name of the default environment.
6. Run dice_boy.py
7. You're done!

TODOs
automatic saving
finish rest of profile commands
refreshables (long / short rest)
voting
roll from profile without switching profile
show multi dice rolls results separately
timekeeping
dm can award xp (dm tools in general)

cleanup by using types, being consistent with __, cleanup files, rethink singletons and imports (learn python lol)
help command

fix file opening https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
