from typing import Dict
from discord.ext import commands
from utils import embedutils

class CommandsDescription:
    def __init__(self) -> None:
        self.commands_descriptions = {"create": {"attr": "<name>",
                                                 "description": "To-Do List will have your given name. Default name if name is not given. Example.",
                                                 "example": ["!create", "!create ToDoThings"]},
                                      "delete": {"attr": "<index>",
                                                 "description": "Remove the To-Do List given index. The last To-Do List if the index is not given. Example.",
                                                 "example": ["!delete", "!delete 2"]}
                                     }
    def get_commands_descriptions(self, command:str) -> Dict | None:
        return self.commands_descriptions.get(command)

class Help(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__()
        self.embed_utils = embedutils.EmbedUtils()
        self.descriptions = CommandsDescription()

    # async def send_bot_help(self, mapping):
    #     embed = discord.Embed(title="Bot help")
    #     # `mapping` is a dict of the bot's cogs, which map to their commands
    #     for cog, cmds in mapping.items():  # get the cog and its commands separately
    #         embed.add_field(
    #             name = cog.qualified_name,       # get the cog name
    #             value = f"{len(cmds)}"  # get a count of the commands in the cog.
    #         )
            
    #     channel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
    #     await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        """
        This is triggered when !help is invoked.

        This example demonstrates how to list the commands that the member invoking the help command can run.
        """

        # filtered = await self.filter_commands(self.context.bot.command, sort=True) # returns a list of command objects
        # names = [cogs for command in filtered] # iterating through the commands objects getting names
        # available_commands = "\n".join(names) # joining the list of names by a new line

        # cog_name = cog.qualified_name
        for cog in mapping:
            if cog is not None:
                commands_list = ['!' + command.name for command in mapping[cog]]
                # commands_list.append(f"{cog.qualified_name}: {', '.join(['!' + command.name for command in mapping[cog]])}")
        embed = self.embed_utils.create_embed(name="All RoseToDo's commands!")
        embed = self.embed_utils.add_field(embed=embed, name_list=commands_list, fillname_index=True)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command:commands):
        """This is triggered when !help <command> is invoked."""
        command_name = str(command)
        current_descriptions = self.descriptions.get_commands_descriptions(command=command_name)
        if current_descriptions is not None:
            embed = self.embed_utils.create_embed(name=f"!{command_name}  {current_descriptions['attr']}")
            embed.description = current_descriptions["description"]
            embed = self.embed_utils.add_field(embed=embed, name_list=current_descriptions["example"], dotname_index=True)
            await self.context.send(embed=embed)

    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        # """This is triggered when !help <cog> is invoked."""
        # cog_name = cog.qualified_name
        # # description = helpscommand.cogsdescription.description_provide(cog_name)
        # if description is not None:
        #     embed = discord.Embed(title=cog_name, description=description)
        #     await self.get_destination().send(embed=embed)
        print('in cog help')

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        channel = self.get_destination() # this defaults to the command context channel
        await channel.send(error)