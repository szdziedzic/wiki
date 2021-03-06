from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import Http404   
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

# class for searching bar form
class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search'}))

# class for add page form
class AddForm(forms.Form):
    title = forms.CharField(label="Title: ")
    text = forms.CharField(label="Text: ", widget=forms.Textarea)

# class for edit page form
class EditForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea())

# utility to convert markdown to HTML
markdowner = Markdown()

# list of recent search result
list_of_results = []

# main page view
def index(request):
    search = search_bar(request)
    if search:
        return search

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

# entry page view for every single entry
def entry(request, name):
    search = search_bar(request)
    if search:
        return search

    content = util.get_entry(name)
    if not content:
        raise Http404
    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "content": markdowner.convert(util.get_entry(name)),
        "form": SearchForm()
    })

# search page view
def search(request):
    search = search_bar(request)
    if search:
        return search

    return render(request, "encyclopedia/search.html", {
        "entries": list_of_results,
        "form": SearchForm()
    })

# add page view
def add(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            for entry in util.list_entries():
                if entry.lower() == title.lower():
                   raise forms.ValidationError("Page already exist.")
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    search = search_bar(request)
    if search:
        return search

        
    return render(request, "encyclopedia/add.html", {
        "form": SearchForm(),
        "add_form": AddForm()
    })

# search bar function
def search_bar(request):
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

    return None

# edit view
def edit(request, name):
    if not util.get_entry(name):
        raise Http404

    search = search_bar(request)
    if search:
        return search

    if request.method == "POST":
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():
            text = edit_form.cleaned_data["text"]
            util.save_entry(name, text)
            return HttpResponseRedirect(reverse("entry", args=[name]))
    else:
        edit_form = EditForm(initial={"text": util.get_entry(name)})
    return render(request, "encyclopedia/edit.html", {
        "form" : SearchForm(),
        "edit_form": edit_form,
        "name": name
    })

# random page view
def random_entry(request):
    entries = util.list_entries()
    max_val = len(entries) - 1
    ind = random.randint(0, max_val)
    entry_name = entries[ind]
    return HttpResponseRedirect(reverse("entry", args=[entry_name]))