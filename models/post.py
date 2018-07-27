import uuid
from database import Database
import datetime


class Post():

    # return the post with the specified id
    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'id': id})

        cls(blog_id=post_data['blog_id'],
            title=post_data['title'],
            content=post_data['content'],
            author=post_data['author'],
            created_date=post_data['created_date'],
            id=post_data['id'])

    # return all the posts associated with the specified blog
    # use list comprehension to convert the MongoDB cursor into a list
    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self.id = uuid.uuid4().hex if id is None else id

    # save the post to posts collection in MongoDB
    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    # convert the Post object into a JSON
    def json(self):
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }
