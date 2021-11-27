from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from taggit.models import Tag

from mysite.blog.forms import EmailPostForm, CommentForm, SearchForm
from mysite.blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # O padrão é 'object_list caso não seja informado
    paginate_by = 3
    template_name = 'blog/post/list.html'  # O padrão é blog/list.html


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        # A seguinte linha retorna o modelo obtido no banco a partir do tag_slug
        tag = get_object_or_404(Tag, slug=tag_slug)
        # De todos os posts publicados, filtra segundo a tag (objeto obtido anteriormente)
        # Filtragem de um modelo baseado em outro
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # tres postagens em cada página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora fo intervalo, exibe a última página de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Se um comentário foi postado, captura os dados do comentário
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Cria o objeto Comment, mas nao salva ainda no banco de dados
            new_comment = comment_form.save(commit=False)
            # Atribui a postagem atual ao comentario e dessa forma enxerga o primary key desde o foreign key
            new_comment.post = post
            # Salve o comentario no banco de dados
            new_comment.save()
            return redirect(post)
    else:
        comment_form = CommentForm()

    # Pag. 87
    # Lista de id de tags do post atual. Ex.: <QuerySet [3, 5]>
    post_tags_ids = post.tags.values_list('id', flat=True)

    # Lista de postagens semelhantes Ex. :<QuerySet [<Post:  __str__ do model>, <Post: __str__ do model >]>
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # Lista dos 4 primeiros objetos tipo posts baseado no atributo criado -same_tags-
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments,
                   'new_comment': new_comment, 'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    # Obtém a postagem com base no id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # cd recebe um dict com os valores obtidos
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} te recomenda ler {post.title}"
            message = f"Te recomendo que leia o post \'{post.title}\' em {post_url}\n\nComentários de {cd['name']}: {cd['comments']}"
            send_mail(subject, message, 'alfareiza@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    # request.GET é o que está na URL, dessa forma se acha a
    # palavra 'query' quer dizer que a pessoa submeteu o form e entra no if

    # Ex. de request.GEt: <QueryDict: {'query': ['artista']}>
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
