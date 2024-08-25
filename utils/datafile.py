import json
import utils.dirpath as dp
from typing import Dict

class DataFile:
    def __init__(self, filename:str = 'user_todolist.json') -> None:
        self.filename = filename
        self.filepath = dp.get_path() + f'\\data\\{filename}'

    def create(self) -> None:
        with open(self.filepath, 'w') as f:
            json.dump({}, f, indent=4)
        
    def rewrite(self, data:Dict[str, any]) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)
 
    def load(self) -> Dict[str, Dict] | None:
        try:
            with open(self.filepath, 'r') as f:
                loads_data = json.load(f)
            return loads_data
        except FileNotFoundError:
            self.create()
            return None

def test():
    datacls = DataFile()
    print(datacls.filepath)
    datacls.create_data_file()
    datacls.rewrite_data_file({
        "123456789": {
            "username": "name",
            "default_order": "0",
            "todolist": {
                "name1": "embed1",
                "name2": "embed2"
            }
        }
    })

'''
{
    "123456789": {
        "username": "name",
        "default_order": "0",
        "todolist": {
            "name1": "embed1",
            "name2": "embed2"
        }
    }
}
'''