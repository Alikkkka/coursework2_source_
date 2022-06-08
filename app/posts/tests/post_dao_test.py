import pytest

from app.posts.dao.posts_dao import PostsDAO


class TestPostDAO:

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO("data/data.json")

    @pytest.fixture
    def correct_keys(self):
        return {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    def test_get_all_type(self, posts_dao):
        posts = posts_dao.get_all()
        assert type(posts) == list, "Результат должен быть списком"
        for post in posts:
            assert type(post) == dict, "Результат должен быть словарем"

    def test_get_all_keys(self, posts_dao, correct_keys):
        posts = posts_dao.get_all()
        for post in posts:
            assert set(post.keys()) == correct_keys, "Ключи должны быть правильными"

    parameters_for_get_by_pk = [1, 2, 3, 4, 5, 6, 7, 8]

    @pytest.mark.parametrize("post_pk", parameters_for_get_by_pk)
    def test_pk(self, posts_dao, post_pk):
        post = posts_dao.get_by_pk(post_pk)
        assert post["pk"] == post_pk, "Полученный номер не соответствует действительности"

    post_parameters_by_blogger = [("leo", {1, 5}), ("hank", {3, 7}), ("johnny", {2, 6}), ("larry", {4, 8})]

    @pytest.mark.parametrize("blogger_name, post_pks_correct", post_parameters_by_blogger)
    def test_get_posts_by_blogger_name(self, posts_dao, blogger_name, post_pks_correct):
        posts = posts_dao.get_by_blogger(blogger_name)
        post_pks = set()
        for post in posts:
            post_pks.add(post["pk"])
        assert post_pks == post_pks_correct, "Наверное, вы ввели неправильное имя ((("

    post_parameters_by_query = [("пирог", {1}), ("погулять", {2}), ("проснулся", {4})]

    @pytest.mark.parametrize("query, post_pks_correct", post_parameters_by_query)
    def test_get_posts_by_query(self, posts_dao, query, post_pks_correct):
        posts = posts_dao.search(query)
        post_pks = set()
        for post in posts:
            post_pks.add(post["pk"])
        assert post_pks == post_pks_correct, "Видимо такого слова нет в постах блогеров"
