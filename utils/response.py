# from typing import Optional

class MessageResponse:
    def on_wrong_input(self) -> str:
        return "Input ไม่ถูกต้องน้าา" 
    
    def on_none_user(self) -> str:
        return "ไม่มีคุณเมมเบอร์อยู่ในดาต้างับ ลอง !create <name> สร้างก่อนน้า"
    
    def on_account_delete(self) -> str:
        return "ลบแอคเคาท์แล้วนะ;-;"
    
    def on_todolist_delete_sucess(self, index:int = None) -> str:
        if index is not None:
            return f"ลบ To-Do List ที่ {index} ให้ล้าา"
        else:
            return f"ลบ To-Do List ล่าสุดให้ละนะะ"
        
    def on_todolist_delete_unsuccess(self, index:int = None) -> str:
        if index is not None:
            return f"ไม่มี To-Do List ที่ {index} อ่ะ"
        else:
            return f"ไม่มี To-Do List ล่าสุดอ่าลอง !create <name> หรือ !call <index> ก่อนนะะะ"
    
    def on_clear_todolist(self) -> str:
        return "ลบ To-Do List ทั้งหมดให้ละน้าา"

    def on_message_not_found(self) -> str:
        return "ไม่เจอข้อความต้นฉบับอ่า ลอง !create <name> หรือ !call <index> นะ"
        
    def on_none_todolist(self) -> str:
        return "ไม่มี To-Do List อ่า !create <name> เพื่อสร้างใหม่นะ"
    
    def on_index_out_of_range(self) -> str:
        return "Index ที่ให้มาไม่มีอ่าา"
    