import pytest

from app.posts.dao.comments_dao import CommentsDAO


class TestCommentsDAO:

    @pytest.fixture
    def comments_dao(self):
        return CommentsDAO("tests/mock/comments.json")

    @pytest.fixture
    def correct_keys(self):
        return {"commenter_name", "post_pk", "pk", "comment"}

    def test_get_com_by_post_pk_type(self, comments_dao):
        comments = comments_dao.get_com_by_post_pk(1)
        assert type(comments) == list, "должно быть в формате списка"
        assert type(comments[0]) == dict, "должно быть в формате словаря"

    def test_get_com_by_post_pk_keys(self, comments_dao, correct_keys):
        comments = comments_dao.get_com_by_post_pk(1)[0]
        comment_keys = set(comments.keys())
        assert comment_keys == correct_keys, "несовпадение ключей"

    parameters_posts_and_coms = [
        (1, {1, 2}),
        (2, {7}),
        (0, set())
    ]

    pytest.mark.parametrize("post_pk, correct_pks", parameters_posts_and_coms)

    def test_get_com_by_post_pk_similarity(self, comments_dao, post_pk, correct_pks):
        comments = comments_dao.get_com_by_post_pk(post_pk)
        comment_pks = []
        for comment in comments:
            comment_pks.append(comment["pk"])
        assert set(comment_pks) == correct_pks, \
            "pk поста не совпадает с pk комментария"
