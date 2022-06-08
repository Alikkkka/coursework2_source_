import logging
from flask import Blueprint, request, jsonify

from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO
logger = logging.getLogger("basic")


api_blueprint = Blueprint('api_blueprint', __name__)

posts_dao = PostsDAO("data/data.json")
comments_dao = CommentsDAO("data/comments.json")


@api_blueprint.route('/api/posts/')
def all_posts():
    logger.debug("Запрошены все посты через API")
    posts=posts_dao.get_all()
    return jsonify(posts)


@api_blueprint.route('/api/posts/<int:post_pk>/')
def one_post(post_pk):
    logger.debug("Запрошен пост через API")
    post = posts_dao.get_by_pk(post_pk)
    return jsonify(post)
