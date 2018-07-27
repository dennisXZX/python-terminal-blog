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

    # create a new post
    def new_post(self):
        # ask users for the post info
        title = input('Enter post title: ')
        content = input('Enter post contents: ')
        created_date = input('Enter post date, or leave blank for today (in format DDMMYYYY): ')

        # check if the created_date is left empty
        if created_date == '':
            created_date = datetime.datetime.utcnow()
        else:
            created_date = datetime.datetime.strptime(created_date, "%d%m%Y")

        # create a post
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=created_date)

        # save the post to database
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
        # find the blog with the specified id
        blog_data = Database.find_one(collection='blogs',
                                      query={'id': id})

        # create a Blog object, cls() represents the current class
        # so later when we change the class name our code is still intact
        return cls(author=blog_data['author'],
                   title=blog_data['author'],
                   description=blog_data['description'],
                   id=blog_data['id'])
