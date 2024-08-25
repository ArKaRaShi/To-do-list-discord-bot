from itertools import zip_longest
from typing import List, Dict
from discord import Embed, Colour


class EmbedUtils:
    def create_embed(self, name:str) -> Embed:
        return Embed(title=name, colour=Colour.random())
    
    def to_embed(self, embed_dict:Dict) -> Embed:
        return Embed.from_dict(embed_dict)
    
    def add_field(self, embed:Embed, name_list:List[str] = None, value_list:List[str] = None,\
                   fillname_index:bool = False, dotname_index:bool = False, bracket:bool = False) -> Embed:

        """
        Add multiple field from name and value list,
        Either name_list or value_list must not be None.
        """

        if name_list is None:
            name_list = []
        if value_list is None:
            value_list = []

        start_index = len(embed.fields) + 1
        for i, (name, value) in enumerate(zip_longest(name_list, value_list, fillvalue=''), start=start_index):
            if name is not None:
                if fillname_index:
                    name = f"{i}. {name}"
                if dotname_index:
                    name = f"- {name}"
                if bracket:
                    name = f"[]{name}"
            embed.add_field(name=name, value=value, inline=False)
        return embed
    
    def edit_field(self, embed:Embed, index:int, new_name:str, change_name_index:bool = False) -> Embed:
        if change_name_index:
            name_index = embed.fields[index].name.split(' ')[0]
            new_name = f"{name_index} {new_name}"
        embed.set_field_at(index=index, name=new_name, value='', inline=False)
        return embed

    def remove_field(self, embed:Embed, index:int = None, with_bracket:bool = False) -> Embed:
        if index == -1:
            embed.remove_field(index=index)
            return embed
        
        field_length = len(embed.fields)
        if index >= 0 and index < field_length:
            embed.remove_field(index=index)
            for i in range(index, field_length - 1):
                field_name = embed.fields[i].name
                if with_bracket:
                    close_bracket_index = field_name.index(']')
                    name_index = f"{field_name[:close_bracket_index + 1]}{i+1}."
                else:
                    name_index = f"{i+1}." 
                new_filed_name = f"{name_index} {embed.fields[i].name.split(' ')[1]}"
                self.edit_field(embed=embed, index=i, new_name=new_filed_name)
            return embed
        else:
            raise IndexError
    
    def check_mark(self, embed:Embed, index:int) -> Embed:
        field_length = len(embed.fields)
        if index >= 0 and index < field_length:
            field_name = embed.fields[index].name
            close_bracket_index = field_name.index(']')
            right_side_name = field_name[close_bracket_index + 1:]

            if close_bracket_index == 1:
                new_name = f"[✅]{right_side_name}"
            elif close_bracket_index == 2:
                new_name = f"[]{right_side_name}"
            embed.set_field_at(index=index, name=new_name, value='', inline=False)
            
            return embed
        else:
            raise IndexError
    
    # def
# clss = EmbedTool.create_embed()
        