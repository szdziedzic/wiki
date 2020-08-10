from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import Http404  
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search'}))

markdowner = Markdown()
list_of_results = []
def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if util.get_entry(q):
                return HttpResponseRedirect(reverse("entry", args=[q]))
            else:
                list_of_results.clear()
                for entry in util.list_entries():
                    tmp = entry.lower()
                    q = q.lower()
                    if q in tmp:
                        list_of_results.append(entry)
                
                return HttpResponseRedirect(reverse("search"))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, name):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if util.get_entry(q):
                return HttpResponseRedirect(reverse("entry", args=[q]))
            else:
                list_of_results.clear()
                for entry in util.list_entries():
                    tmp = entry.lower()
                    q = q.lower()
                    if q in tmp:
                        list_of_results.append(entry)
                
                return HttpResponseRedirect(reverse("search"))

    content = util.get_entry(name)
    if not content:
        raise Http404
    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "content": markdowner.convert(util.get_entry(name)),
        "form": SearchForm()
    })


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if util.get_entry(q):
                return HttpResponseRedirect(reverse("entry", args=[q]))
            else:
                list_of_results.clear()
                for entry in util.list_entries():
                    tmp = entry.lower()
                    q = q.lower()
                    if q in tmp:
                        list_of_results.append(entry)
                
                return HttpResponseRedirect(reverse("search"))
                
    return render(request, "encyclopedia/search.html", {
        "entries": list_of_results,
        "form": SearchForm()
    })