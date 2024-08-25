from typing import Optional
from discord import Message, NotFound
from discord.ext import commands
from utils import data, embedutils, response
from commands import onmessagetrig

class TodoList(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.user_data = data.UserData()
        self.user_context = data.UserContext()
        self.embed_utils = embedutils.EmbedUtils()
        # self.message_handle = handle.MessageHandle()
        self.command_opts = onmessagetrig.CommandOperations()
        self.command_validator = onmessagetrig.CommandValidator()
        self.response_msg = response.MessageResponse()

    @commands.command()
    async def create(self, ctx, todolist_name = None) -> None:
        """Create a new To-Do list."""
        async with self.user_data.lock:
            user = ctx.author
            user_name = str(user.display_name)
            user_id = str(user.id)

            user_data = self.user_data.get_user_data(user_id=user_id)
            if user_data is None:
                self.user_context.set_default()
                self.user_context.update_username(new_username=user_name)
            else:
                self.user_context.set_user_data(user_data=user_data)

            # user_data_copy = self.user_context.get_data().copy()
            if todolist_name is None:
                if user_name != self.user_context.get_username():
                    pass
                    
                    # embed.updateallname()

                todolist_order = self.user_context.get_default_order()
                embed_name = f"{user_name}'s To-Do list #{todolist_order}"
                name_type = "default"
                self.user_context.update_default_order(new_default_order=todolist_order + 1)
            else:
                embed_name = todolist_name
                name_type = "named"
            
            embed = self.embed_utils.create_embed(name=embed_name)
            last_msg = await ctx.send(embed=embed)

            self.user_context.add_todolist(embed=embed, embed_id=str(last_msg.id), name_type=name_type)
            self.user_data.update_user_data(user_id=user_id, user_data=self.user_context.to_dict())
            self.user_context.set_default()


    @commands.command()
    async def delete(self, ctx, todolist_index:Optional[str] = None):
        """Delete the last To-Do List if index is not provided, else To-Do List that index contain"""
        async with self.user_data.lock:
            user = ctx.author
            user_id = str(user.id)

            user_data = self.user_data.get_user_data(user_id=user_id)
            if user_data is None:
                await ctx.send(self.response_msg.on_none_user())
                return
            
            self.user_context.set_user_data(user_data=user_data)
            todolist_length = self.user_context.get_todolist_length()

            # print(todolist_length)
            if todolist_length == 0:
                await ctx.send(self.response_msg.on_todolist_delete_unsuccess())
                return
            
            try:

                if todolist_index is None:
                    self.user_context.remove_todolist()
                    message = self.response_msg.on_todolist_delete_sucess()

                elif todolist_index.isdigit():
                    todolist_index = int(todolist_index)
                    self.user_context.remove_todolist(index=todolist_index - 1)
                    message = self.response_msg.on_todolist_delete_sucess(index=todolist_index)

                else:
                    message = self.response_msg.on_wrong_input()

            except Exception as e:
                message = self.response_msg.on_todolist_delete_unsuccess(index=todolist_index)
                print(e)
                return

            else:
                self.user_data.update_user_data(user_id=user_id, user_data=self.user_context.to_dict())
                
            finally:
                self.user_context.clear_user()
                await ctx.send(message)

    
    @commands.command()
    async def clear(self, ctx):
        """Delete all To-Do List."""
        async with self.user_data.lock:
            user = ctx.author
            user_id = str(user.id)

            user_data = self.user_data.get_user_data(user_id=user_id)
            if user_data is None:
                await ctx.send(self.response_msg.on_none_user())
                return
            
            self.user_context.set_user_data(user_data=user_data)
            self.user_context.clear_todolist()

            self.user_data.update_user_data(user_id=user_id, user_data=self.user_context.to_dict())
            self.user_context.clear_user()  

        await ctx.send(self.response_msg.on_clear_todolist())
                
        
    @commands.command()
    async def mylist(self, ctx):
        """Show all To-Do List."""
        async with self.user_data.lock:
            user = ctx.author
            user_id = str(user.id)

            user_data = self.user_data.get_user_data(user_id=user_id)
            if user_data is None:
                await ctx.send(self.response_msg.on_none_user())
                return
            
            self.user_context.set_user_data(user_data=user_data) 
            todolist_names = self.user_context.get_all_todolist_names()
            self.user_context.clear_user()

        embed = self.embed_utils.create_embed(name="All To-Do List")
        embed = self.embed_utils.add_field(embed=embed, name_list=todolist_names, fillname_index=True)
        await ctx.send(embed=embed)

    

    @commands.command()
    async def call(self, ctx, todolist_index:Optional[str] = None):
        '''
        Call first To-Do List if index not provide, else To-Do List that index contain
        '''
        async with self.user_data.lock:
            user = ctx.author
            user_id = str(user.id)

            user_data = self.user_data.get_user_data(user_id=user_id)
            if user_data is None:
                await ctx.send(self.response_msg.on_none_user())
                return
            
            self.user_context.set_user_data(user_data=user_data)

            todolist_index:int = 0 if todolist_index is None else int(todolist_index) - 1

            try:
                todolist = self.user_context.get_todolist(index=todolist_index)

            except Exception:
                await ctx.send("ไม่เจอ To-Do List อันนั้นอ่าา")

            else:
                embed = self.embed_utils.to_embed(embed_dict=todolist["embed"])
                last_msg = await ctx.send(embed=embed)

                self.user_context.update_todolist_id(new_id=str(last_msg.id), index=todolist_index)

                todolist["id"] = str(last_msg.id)
                todolist["index"] = todolist_index

                self.user_context.update_using_todolist(new_using_todolist=todolist)
                self.user_data.update_user_data(user_id=user_id, user_data=self.user_context.to_dict())

            finally:
                self.user_context.clear_user()
            
           
                
                
    @commands.Cog.listener()
    async def on_message(self, message:Message):
        if message.author == self.bot.user:
            return
        
        msg_content = message.content
        channel = message.channel
        if msg_content[0] == '!':
            return
        
        command_opt = self.command_validator.command_identifier(command=msg_content.split(' ')[0])
        if command_opt != -1:
            async with self.user_data.lock:
                user = message.author
                user_id = str(user.id)

                user_data = self.user_data.get_user_data(user_id=user_id)
                if user_data is None:
                    return
                
                self.user_context.set_user_data(user_data=user_data)
                try:
                    todolist = self.user_context.get_using_todolist()
                    base_message_id = int(todolist["id"])
                    base_message = await channel.fetch_message(base_message_id)
                except NotFound:
                    # message on case not found
                    await channel.send(self.response_msg.on_message_not_found())
                    print(f"Message ID:{base_message_id} not found.")
                    return
                except Exception as e:
                    print(e)
                    return
                
                embed = self.embed_utils.to_embed(embed_dict=todolist["embed"])
                # embed_name = embed.title
                
                try:
                    embed = self.command_opts.process(embed=embed, msg=msg_content.strip(), operation=command_opt)
                except Exception as e:
                    print(f"Error catch in on_message function: {e}")
                    return
                else:
                    self.user_context.update_todolist_embed(new_embed=embed, index=todolist["index"])

                    todolist["embed"] = embed.to_dict()
                    self.user_context.update_using_todolist(new_using_todolist=dict(todolist))
                    self.user_data.update_user_data(user_id=user_id, user_data=self.user_context.to_dict())
                finally:
                    self.user_context.clear_user()

            await message.delete()
            await base_message.edit(embed=embed)
    
        # else:
        #     print("do something")
        await self.bot.process_commands(message)
    # '''



    '''
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user and self.first_create:
            if self.last_user_msg == "!create":
                self.base_message = await message.channel.fetch_message(message.id)
                self.first_create = False
        elif message.author == self.bot.user:
            return
        else:
            self.last_user_msg = message.content
        
        channel = message.channel    
        message_str = message.content.strip()
        message_check = handle_message(command=message_str.split()[0])
        if message_check:
            self.base_embed, self.total_field = perform_command(self.base_embed, self.total_field, message_str)
            await self.base_message.edit(embed=self.base_embed)
        else:
            return
        await self.bot.process_commands(message)
    '''

async def setup(bot):
    await bot.add_cog(TodoList(bot))