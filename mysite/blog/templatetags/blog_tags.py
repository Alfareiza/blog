import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from mysite.blog.models import Post

register = template.Library()


# Para register a tag com um nome diferente da função
# Deve se colocar o decorator assim: @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    """
    Em qualquer template ao longo do projeto poderá ser chamado como
    {% total_posts %}
    Retorna um string (número) com o valor calculado
    """
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    """ "
    O arquivo blog/post/latest_posts.html trata o resultado desta função.
    Dessa forma em qualquer parte do projeto pode ser chamado o {% show_latest_posts # %}
    E vai retornar o template renderizado com o chamado dessa função.
    """
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Totaliza o número de comentários para cada postagem.
    total_comments armazena o total de comentários para cada objeto.
    order_by ordena o QuerySet com base no campo total_comments na orden decrescente.
    count limita o número total de objetos devolvidos.
    Retorna um QuerySet com os objetos mais comentados.
    """
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


@register.filter(name="markdown")
def markdown_format(text):
    """

    @param text: str
    @return: <p>text</p>: <class 'django.utils.safestring.SafeString'>
    """
    return mark_safe(markdown.markdown(text))
