from django.apps import AppConfig

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'


class PostsConfig(AppConfig):
    name = 'posts'
