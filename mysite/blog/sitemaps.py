from django.contrib.sitemaps import Sitemap

from mysite.blog.models import Post


class PostSitemap(Sitemap):
    """
    Um mapa do site é um arquivo XML em seu site que informa aos indexadores de mecanismos
    de pesquisa com que frequência suas páginas mudam e quão “importantes” certas páginas
    são em relação a outras páginas em seu site. Essas informações ajudam os mecanismos de
    pesquisa a indexar seu site.

    A estrutura do sitemap do Django automatiza a criação desse arquivo XML permitindo que
    você expresse essas informações em código Python.
    """

    changefreq = "weekly"
    priority = 0.9

    # changefreq e priority informam a frequência de mudança das páginas e sua relevância no site (valor máximo é 1)

    def items(self):
        """
        @return: Query set dos objetos a serem incluidos nesse mapa de site.
        O padrão é chamar o get_absolute_url() de cada objeto
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        Recebe cada objeto do método items e retorna a última vez em que o objeto foi modificado.
        @param obj:
        @return:
        """
        return obj.updated
