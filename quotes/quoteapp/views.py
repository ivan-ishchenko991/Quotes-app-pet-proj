from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import AuthorForm, QuoteForm
from .models import Authors, Tag, Quotes


# Create your views here.
def main(request, page=1):
    """
    The main function is the main page of the website. It displays all quotes,
        and also shows a list of top 10 tags.

    :param request: Get the request object
    :param page: Determine which page of the paginated quotes to display
    :return: The rendered index
    :doc-author: Trelent
    """
    tags_with_count = Tag.objects.annotate(usage_count=Count('quotes'))
    top_10_tags = sorted(tags_with_count, key=lambda x: x.usage_count, reverse=True)[:10]
    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request,
                  'quoteapp/index.html',
                  {"quotes": quotes_on_page,
                   'top_tags': top_10_tags}
                  )


def tag(request, tag_name, page=1):
    """
    The tag function takes a tag_name and page number as arguments. It then gets all the tags with their usage count,
    sorts them in descending order by usage count, and gets the top 10 tags. Then it filters quotes by the given tag
    name, paginates them (10 per page), and returns an index template with those quotes.

    :param request: Get the request object
    :param tag_name: Filter the quotes by tag
    :param page: Get the page number from the url
    :return: A list of quotes that have the tag_name tag
    :doc-author: Trelent
    """
    tags_with_count = Tag.objects.annotate(usage_count=Count('quotes'))
    top_10_tags = sorted(tags_with_count, key=lambda x: x.usage_count, reverse=True)[:10]
    quotes = Quotes.objects.filter(tags__name=tag_name)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request,
                  'quoteapp/index.html',
                  {"quotes": quotes_on_page,
                   'tag': tag_name,
                   'top_tags': top_10_tags}
                  )


def search(request):
    """
    The search function is responsible for searching the database for quotes, authors and tags.
    It takes a GET request with a query string as an argument and returns the search results page.
    If no query string is provided, it will return all quotes.

    :param request: Get the request object
    :return: A list of quotes that match the query
    :doc-author: Trelent
    """
    query = request.GET.get('q')  # Отримайте рядок запиту з форми
    tags_with_count = Tag.objects.annotate(usage_count=Count('quotes'))
    top_10_tags = sorted(tags_with_count, key=lambda x: x.usage_count, reverse=True)[:10]

    if query:
        # Виконується пошук в вашій моделі Quote
        results = Quotes.objects.filter(
            Q(quote__icontains=query) |  # Пошук за цитатами
            Q(author__fullname__icontains=query) |  # Пошук за ім'ям автора
            Q(tags__name__icontains=query)  # Пошук за тегами
        ).distinct()
    else:
        results = Quotes.objects.all()  # Якщо запит порожній, покаже всі цитати

    return render(request,
                  'quoteapp/search_results.html',
                  {'results': results,
                   'query': query,
                   'top_tags': top_10_tags}
                  )


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Authors.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            author = Authors.objects.filter(fullname=request.POST.get('author'))[0]
            new_quote.author = author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_quote.html', {"tags": tags, "authors": authors, "form": form})

    return render(request, 'quoteapp/add_quote.html', {"tags": tags, "authors": authors, "form": QuoteForm()})


def author_info(request, author_name):
    author = Authors.objects.get(fullname=author_name)
    return render(request, 'quoteapp/author.html', {'author': author})
