import datetime
import uuid

from database import Database
from models.post import Post


class Blog():
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def new_post(self):
        title = input('Enter post title: ')
        content = input('Enter post contents: ')
        created_date = input('Enter post date, or leave blank for today (in format DDMMYYYY): ')

        # check if the created_date is left empty
        if created_date == '':
            created_date = datetime.datetime.utcnow()
        else:
            created_date = datetime.datetime.strptime(created_date, "%d%m%Y")

        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=created_date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'id': self.id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'id': id})

        return cls(author=blog_data['author'],
                    title=blog_data['author'],
                    description=blog_data['description'],
                    id=blog_data['id'])
