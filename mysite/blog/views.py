from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

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
