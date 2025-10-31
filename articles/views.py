from django.shortcuts import render, get_object_or_404
from .models import Article


def article_list(request):
    articles = Article.objects.all().prefetch_related('scopes__tag')
    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(
        Article.objects.prefetch_related('scopes__tag'),
        id=article_id
    )

    scopes = article.scopes.select_related('tag').all()
    main_scope = None
    other_scopes = []

    for scope in scopes:
        if scope.is_main:
            main_scope = scope
        else:
            other_scopes.append(scope)

    other_scopes.sort(key=lambda x: x.tag.name)

    sorted_scopes = []
    if main_scope:
        sorted_scopes.append(main_scope)
    sorted_scopes.extend(other_scopes)

    context = {
        'article': article,
        'scopes': sorted_scopes
    }
    return render(request, 'articles/article_detail.html', context)