from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from mysite.blog.models import Post

# Documentation: https://docs.djangoproject.com/en/3.2/ref/contrib/syndication/

# Pág 106
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'Newposts of my blog.'

    def items(self):
        """
        @return: Primeiros 5 objetos a serem adicionados ao feed.
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        """
        Recebe cada objeto devolvido por items()
        @param item: Post
        @return: Título do Post
        """
        return item.title

    def item_description(self, item):
        """
        Recebe cada objeto devolvido por items()
        @param item: Post
        @return: Corpo do Post
        """
        return truncatewords(item.body, 30)
