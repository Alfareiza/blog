from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from mysite.blog.forms import EmailPostForm
from mysite.blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # O padrão é 'object_list caso não seja informado
    paginate_by = 3
    template_name = 'blog/post/list.html'  # O padrão é blog/list.html


def post_list(request):
    object_list = Post.published.all()
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
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


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
