from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util
import markdown2

class search_form(forms.Form):
    q = forms.CharField()

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter the title of the page'}))
    textarea = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Text area for Markdown content'}))

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = search_form(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            q_as_sub = [i for i in entries if q in i]
            if q in entries:
                return HttpResponseRedirect(reverse("entry", args = (q,)))
            else:
                return render(request, "encyclopedia/search_results.html",{
                    "q_as_sub": q_as_sub, "q": q
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

def entry(request, title):
    page = util.get_entry(title)
    if page == None:
        return render(request, "encyclopedia/entry.html", {
            "file": None
        })
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/entry.html", {
        "file": html, "title": title
    })

def create(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            if title in entries:
                return render(request, "encyclopedia/create_page.html", {"form": form, "flag": 1})
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args = (title,)))

    else:
        return render(request, "encyclopedia/create_page.html", {
            "form": NewPageForm(), "flag": 0
        })

def edit(request):
    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
    page = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {"title": title, "page": page})
    
def editpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args = (title,)))

def randPage(request):
    entries = util.list_entries()
    q = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args = (q,)))
    