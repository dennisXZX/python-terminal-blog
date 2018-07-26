from database import Database
from models.blog import Blog


class Menu():
    def __init__(self):
        self.user = input('Enter your author name: ') or 'Dennis'
        self.user_blog = None

        if self._user_has_account():
            print('Welcome back {}'.format(self.user))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = Database.find_one('blogs', {'author': self.user})

        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    def _prompt_user_for_account(self):
        title = input('Enter blog title: ')
        description = input('Enter blog description: ')
        blog = Blog(author=self.user,
                    title=title,
                    description=description)

        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        # User read or write blogs?
        read_or_write = input('Do you want to read (R) or write (W) blogs? ') or 'R'

        if read_or_write == 'R':
            self._list_blogs()
            self._view_blog()
        elif read_or_write == 'W':
            self._prompt_write_post()
        else:
            print('Thank you for blogging!')

    def _prompt_write_post(self):
        self.user_blog.new_post()

    def _list_blogs(self):
        # retrieve all the blog documents
        blogs = Database.find(collection='blogs',
                              query={})

        # iterate the blogs  each blog document
        for blog in blogs:
            print('ID: {}, Title: {}, Author: {}'.format(blog['id'], blog['title'], blog['author']))

    def _view_blog(self):
        blog_to_see = input("Enter the ID of the blog you'd like to read: ") or '5c0d7e250ba044e58ee3655cd61b9c26'
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()

        for post in posts:
            print("======================")
            print("Title: {}\nDate: {}\n\n{}\n".format(post['title'], post['created_date'], post['content']))
