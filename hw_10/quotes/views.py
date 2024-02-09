from bson.objectid import ObjectId
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorsForm, QuotesForm
from .models import Authors, Quotes
from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def about_author(request, id_: str):
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(id_)})
    return render(request, "quotes/about_author.html", context={"authors": author})


def quotes_by_tag(request, tag_slug):
    db = get_mongodb()
    tag = db.quotes.find_one({"tags": tag_slug})

    if tag:
        quotes = db.quotes.find({"tags": tag_slug})
        return render(
            request,
            "quotes/quotes_by_tag.html",
            {"tag": tag, "quotes": quotes, "tag_slug": tag_slug},
        )
    else:
        return render(request, "quotes/tag_not_found.html", {"tag_slug": tag_slug})


def post_author(request):
    if request.method == "POST":
        form = AuthorsForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data["author"]

            borns = form.cleaned_data.get("borns", None)
            borns_location = form.cleaned_data.get("borns_location", None)
            descriptions = form.cleaned_data.get("descriptions", None)

            author, created = Authors.objects.get_or_create(
                author=author_name,
                defaults={
                    "borns": borns,
                    "borns_location": borns_location,
                    "descriptions": descriptions,
                },
            )

            return redirect("quotes:root")
    else:
        form = AuthorsForm()

    return render(request, "quotes/post_author.html", {"author_form": form})


def post_quote(request):
    if request.method == "POST":
        quote_form = QuotesForm(request.POST)
        if quote_form.is_valid():
            author_name = quote_form.cleaned_data["author"]

            author, created = Authors.objects.get_or_create(author=author_name)

            quote = quote_form.save(commit=False)
            quote.author = author

            quote.save()

            return redirect("quotes:root")
        else:
            messages.error(
                request, "There was an error in the form. Please check your inputs."
            )
    else:
        quote_form = QuotesForm()

    return render(request, "quotes/post_quote.html", {"quote_form": quote_form})


def author_detail(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    return render(request, "your_template.html", {"author": author})


def quote_detail(request, quote_id):
    quote = get_object_or_404(Quotes, pk=quote_id)
    return render(request, "your_template.html", {"quote": quote})


@login_required
def detail(request, id_):
    page_404 = get_object_or_404(Quotes, pk=id_, quote=request.quote)
    return render(request, "quotes/detail.html", {"quotes": page_404})


@login_required
def set_done(request, id_):
    quote = get_object_or_404(Quotes, pk=id_, user=request.user)
    quote.done = True
    quote.save()
    return redirect(to="quotes:root")


@login_required
def delete_note(request, id_):
    quote = get_object_or_404(Quotes, pk=id_, quote=request.quote)
    quote.delete()
    return redirect(to="quotes:root")
