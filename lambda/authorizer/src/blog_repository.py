class BlogRepository:
    blogs = {}    
    def __init__(self):
        self.blogs = {
            "1": {
                "title": "Title of blog 1",
                "content": "This is blog 1",
                "owner": "このブログはオーナーシップを持っているのでverify時にでトークンのsubをいれる" 
            },
            "2": {
                "title": "Title of blog 2",
                "content": "This is blog 2",   
                "owner": "このブログはオーナーシップを持っていないので適当なIDをいれる"       
            }
        }
    def find_by_id(self, id, owner_id):
        if id not in self.blogs:
            return None
        blog = Blog(id, self.blogs[id]["title"], self.blogs[id]["content"], owner_id if id == "1" else "dummy_owner_id")
        return blog

    

class Blog:
    id: str
    title: str
    content: str
    owner: str
    
    def __init__(self, id, title, content, owner):
        self.id = id
        self.title = title
        self.content = content
        self.owner = owner
    
    def to_avp_resource(self):
        return {
            "entityType": "MyBlogApp::Blog",
            "entityId": self.id
        }