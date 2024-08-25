import asyncio
import config
import customhelp
from discord import Intents
from discord.ext import commands

def run_discord_bot():
    token = config.TOKEN
    intents = Intents.default()
    intents.message_content = True
    command_prefix = config.command_prefix
    bot = commands.Bot(intents=intents, command_prefix=command_prefix, help_command=customhelp.Help())
    
    @bot.event
    async def on_ready():
        print("{0.user} on work!!".format(bot))

    async def load():
        await bot.load_extension("ToDoList")
        # for filename in os.listdir('./cogs'):
        #     if filename.endswith('.py'):
                # await bot.load_extension(f"cogs.{filename[:-3]}")

    async def main():
        await load()
        await bot.start(token=token)
        
    asyncio.run(main())

if __name__ == "__main__":
    run_discord_bot()