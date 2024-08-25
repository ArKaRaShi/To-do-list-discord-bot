from discord import Embed
from discord.ext import commands
from utils import embedutils


ADD = 1
REMOVE = 2
EDIT = 3
CLEAR = 4
MARK = 5

class CommandMsgHandle:
    def message_split(self, msg:str, operation:int):
        if operation == ADD:
            try:
                first_blank_index = msg.index(' ')
            except ValueError:
                raise ValueError
            
            return msg[first_blank_index + 1:]

        if operation == REMOVE:
            try:
                first_blank_index = msg.index(' ')
            except ValueError:
                return -1
            
            content = msg[first_blank_index + 1:]
            if content.isdigit() and content != '0':
                return int(content) - 1
            
            raise ValueError

            
        if operation == EDIT:
            try:
                first_blank_index = msg.index(' ')
            except ValueError:
                raise ValueError
            
            content = msg[first_blank_index + 1:].split()
            try:
                index, name = content[0], "".join(content[1:])
            except IndexError:
                raise IndexError
            
            if index.isdigit():
                return int(index) - 1, name
            
            raise ValueError


        if operation == MARK:
            index = msg
            if index.isdigit():
                return int(index) - 1
            
            raise ValueError
            
class CommandValidator:
    def __init__(self) -> None:
        self.command = {'add': ('+', 'add'),
                        'rev': ('-', 'rev','remove'),
                        'edit': ('e', 'edit'),
                        'clr': ('c', 'clear'),
                        }

    def command_identifier(self, command:str) -> int:
        '''
        If command valid, Return integer, specific number, to perform an operation e.g. 1,2,3,...
        Else -1
        '''
        if command in self.command["add"]:
            return ADD
        if command in self.command["rev"]:
            return REMOVE
        if command in self.command["edit"]:
            return EDIT
        if command in self.command["clr"]:
            return CLEAR
        if command.isdigit():
            return MARK

        return -1
        
class CommandOperations:
    def __init__(self) -> None:
        self.message_handle = CommandMsgHandle()
        self.embed_utils = embedutils.EmbedUtils()

    def perform_add(self, embed:Embed, text:str) -> Embed:
        embed = self.embed_utils.add_field(embed=embed, name_list=[text], fillname_index=True, bracket=True)
        return embed
    
    def perform_remove(self, embed:Embed, index:int) -> Embed:
        embed = self.embed_utils.remove_field(embed=embed, index=index, with_bracket=True)
        return embed

    def perform_edit(self, embed:Embed, index:int, new_name:str) -> Embed:
        embed = self.embed_utils.edit_field(embed=embed, index=index, new_name=new_name, change_name_index=True)
        return embed

    def perform_clear(self, embed:Embed) -> Embed:
        return embed.clear_fields()
    
    def perform_mark(self, embed:Embed, index:int) -> Embed:
        embed = self.embed_utils.check_mark(embed=embed, index=index)
        return embed

    def process(self, embed:Embed, msg:str, operation:int) -> Embed:

        if operation == ADD:
            try:
                text = self.message_handle.message_split(msg=msg, operation=operation)
                embed = self.perform_add(embed=embed, text=text)
            except Exception as e:
                raise commands.BadArgument(f"Bad Input, add operation unsuccess. {e}")
            
        elif operation == REMOVE:
            try:
                index = self.message_handle.message_split(msg=msg, operation=operation)
                embed = self.perform_remove(embed=embed, index=index)
            except Exception as e:
                raise commands.BadArgument(f"Bad Input, remove operation unsuccess. {e}")
            
        elif operation == EDIT:
            try:
                index, name = self.message_handle.message_split(msg=msg, operation=operation)
                embed = self.perform_edit(embed=embed, index=index, new_name=name)
            except Exception as e:
                raise commands.BadArgument(f"Bad Index Input, edit operation unsuccess. {e}")
            
        elif operation == CLEAR:
            embed = self.perform_clear(embed=embed)

        elif operation == MARK:
            try:
                index = self.message_handle.message_split(msg=msg, operation=operation)
                embed = self.perform_mark(embed=embed, index=index)
            except Exception as e:
                raise commands.BadArgument(f"Bad Index Input, mark operation unsuccess. {e}")
        return embed        