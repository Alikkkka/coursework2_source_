import json


class PostsDAO:
    def __init__(self, path):
        self.path = path

    def _load(self):
        with open(f"{self.path}", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_all(self):
        return self._load()

    def get_by_pk(self, pk):
        posts = self.get_all()
        for post in posts:
            if post["pk"] == pk:
                return post

    def get_by_blogger(self, blogger_name):
        posts = self.get_all()
        posts_by_blogger = []
        for post in posts:
            if post["poster_name"] == blogger_name:
                posts_by_blogger.append(post)

        return posts_by_blogger

    def search(self, query):
        posts = self.get_all()
        posts_by_query = []
        for post in posts:
            if query.lower() in post["content"].lower():
                posts_by_query.append(post)

        return posts_by_query
