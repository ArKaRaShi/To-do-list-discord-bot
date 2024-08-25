import asyncio
from typing import Dict, List, Optional

from discord import Embed
from discord.ext import commands

from utils.datafile import DataFile

class UserData:
    def __init__(self) -> None:
        self.datafile = DataFile()
        self.user_data = self.datafile.load()
        self.lock = asyncio.Lock()

    def get_user_data(self, user_id:str) -> Optional[Dict]:
        return self.user_data.get(user_id)

    def delete_account(self, user_id:str) -> None:
        self.user_data.pop(user_id)
        self.datafile.rewrite(self.user_data)

    def update_user_data(self, user_id:str, user_data:Dict[str, any]) -> None:
        self.user_data.update({user_id:user_data})
        self.datafile.rewrite(self.user_data)


class UserContext:

    username : str
    default_order : int
    using_todolist : Dict
    all_todolist : List

    def set_user_data(self, user_data:Dict) -> None:
        self.username = user_data["username"]
        self.default_order = user_data["default_order"]
        self.using_todolist = user_data["using_todolist"]
        self.all_todolist = user_data["all_todolist"]

    def set_default(self) -> None:
        self.username = None
        self.default_order = 1
        self.using_todolist = {}
        self.all_todolist = []
        
    def update_username(self, new_username:str) -> None:
        self.username = new_username
    
    def update_default_order(self, new_default_order:int) -> None:
        self.default_order = new_default_order

    def update_using_todolist(self, new_using_todolist:Dict) -> None:
        self.using_todolist = new_using_todolist

    def update_todolist_embed(self, new_embed:Embed, index:int) -> None:
        self.all_todolist[index]["embed"] = new_embed.to_dict()

    def update_todolist_id(self, new_id:str, index:int) -> None:
        '''
        Update id in To-Do List, which index is given.
        '''
        self.all_todolist[index]["id"] = new_id

    # def update_todolist_embed(self, new_embed:Embed, index:int)
        

    def add_todolist(self, embed:Embed, embed_id:str, name_type:str) -> None:
        todolist = {"embed": embed.to_dict(),
                    "id": embed_id,
                    "type": name_type}
        
        self.all_todolist.append(dict(todolist))

        todolist["index"] = len(self.all_todolist) - 1
        self.update_using_todolist(new_using_todolist=dict(todolist))

    
    def remove_todolist(self, index:int = None) -> None:
        '''
        Remove To-Do List which key index is contain. 
        If key index isn't provided, Remove current using todolist.
        Give error message if error is occured.
        '''
        if index is None and len(self.using_todolist):
            for i, todolist in enumerate(self.all_todolist):

                # Check if considering id equal to To-Do List in all_todolist. Remove that one.
                if todolist["id"] == self.using_todolist["id"]:
                    self.update_using_todolist(new_using_todolist={})
                    index = i
                    break
                
        try:
            todolist_name_type = self.all_todolist[index]["type"]    
            self.all_todolist.pop(index)  
            pass  
        except IndexError:
            raise commands.BadArgument("Pop unsuccess, Index not found.")
        except TypeError:
            raise commands.BadArgument("Pop unsuccess, Index is None")
        else:
            if todolist_name_type == "default":
                self.default_order = self.default_order - 1

    def clear_todolist(self) -> None:
        self.default_order = 1
        self.using_todolist.clear()
        self.all_todolist.clear()

    def clear_user(self) -> None:
        self.set_default()
        

    def to_dict(self) -> Dict:
        data_dict = {"username": self.username,
                     "default_order": self.default_order,
                     "using_todolist": self.using_todolist,
                     "all_todolist": self.all_todolist}
        
        return data_dict
    
    # def get_index_from_todolist_id(self, todolist_id)

    def get_todolist(self, index:int = None) -> Dict:
        '''
        Get To-Do List which key index is contain. 
        If key index isn't provided, Return first todolist.
        Give error message if error is occured.
        '''
        if index is None:
            index = 0

        try:
            todolist = self.all_todolist[index]
        except IndexError:
            raise commands.BadArgument("Request unsuccess, Index not found.")
        else:
            return dict(todolist)

    def get_username(self) -> str:
        return self.username

    def get_default_order(self) -> int:
        return self.default_order
    
    def get_using_todolist(self) -> Dict:
        return dict(self.using_todolist)

    def get_todolist_length(self) -> int:
        return len(self.all_todolist)

    def get_all_todolist_names(self) -> List:
        todolist_names = [todolist["embed"]["title"] for todolist in self.all_todolist]
        return todolist_names    
