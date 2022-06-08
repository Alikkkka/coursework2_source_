import logging
from json import JSONDecodeError


from flask import Blueprint, render_template, request, abort
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
posts_dao = PostsDAO("data/data.json")
comments_dao = CommentsDAO("data/comments.json")

logger = logging.getLogger("basic")


@posts_blueprint.route('/')
def all_posts_page():
    
    logger.debug("Загрузка ленты")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts=posts)

    except (FileNotFoundError, JSONDecodeError):
        return "Проблемы )): с загрузкой ленты"


@posts_blueprint.route('/search/')
def search_through_posts():
    logger.debug("Ищем посты по слову")
    query = request.args.get("s", "")
    if "s" in request.args:
        query = request.args["s"]
    else:
        query = ""

    if query != "":
        posts = posts_dao.search(query)
        posts_count = len(posts)
    else:
        posts = []
        posts_count = 0
    return render_template("search.html", query=query, posts=posts, posts_count=posts_count)


@posts_blueprint.route('/posts/<int:post_pk>/')
def one_post_page(post_pk):
    logger.debug(f"Загрузка поста по его pk {post_pk}")
    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_com_by_post_pk(post_pk)
        comments_count = len(comments)

    except (ValueError, JSONDecodeError, FileNotFoundError, KeyError):
        return "Проблемы )): c одним постом"

    else:
        if post == '':
            abort(404)
        return render_template("post.html", post=post, comments=comments, comments_count=comments_count)


@posts_blueprint.errorhandler(404)
def post_error(e):
    return "Нет такого поста", 404


@posts_blueprint.route('/bloggers/<blogger_name>/')
def search_by_blogger_name(blogger_name):
    posts = posts_dao.get_by_blogger(blogger_name)
    posts_count = len(posts)
    return render_template("user-feed.html", posts=posts, posts_count=posts_count)
