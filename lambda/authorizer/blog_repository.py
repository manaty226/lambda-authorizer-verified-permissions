class BlogRepository:
    blogs = {}    
    def __init__(self):
        self.blogs = {
            1: {
                "title": "Title of blog 1",
                "content": "This is blog 1",
                "owner": "このブログはオーナーシップを持っているのでverify時にでトークンのsubをいれる" 
            },
            2: {
                "title": "Title of blog 2",
                "content": "This is blog 2",   
                "owner": "このブログはオーナーシップを持っていないので適当なIDをいれる"       
            }
        }
    
    def find_by_id(self, id, owner_id):
        if id == 1:
            self.blogs[id]["owner"] = owner_id
        elif id == 2:
            self.blogs[id]["owner"] = "dummy_owner_id"

        return self.blogs[id] if id in self.blogs else None
