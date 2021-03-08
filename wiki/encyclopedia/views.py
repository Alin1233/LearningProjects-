from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from markdown2 import markdown
from django.urls import reverse
from django import forms
import random

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(widget=forms.Textarea)

class EditEntryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":

        name = request.POST
        name = name ['q']
        
        if util.get_entry(name):
            return HttpResponseRedirect(reverse("EntryPage", args = [name]))
        else:
            return HttpResponseRedirect(reverse("Search", args = [name]))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def EntryPage(request,name):

    if util.get_entry(name):
        path = f"entries\{name}.md"
        with open(path) as markdown_file:
            entry = markdown(markdown_file.read())

        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": entry
        })
    else: 
        return HttpResponse (f"Entry {name} does not exist")

def Search(request,name):

    entries = util.list_entries()
    sub_string = []
    name = name.lower()
   
    for entry in entries:
        if name in entry.lower():
            sub_string.append(entry)

    if not sub_string:
        return render(request, "encyclopedia/search.html")
    else:
        return render(request, "encyclopedia/search.html", {
                "entries": sub_string
            })

    
def New(request):
    
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
        
        if util.get_entry(title):
            return HttpResponse("That entry exists")
        else:
            path = f"entries\{title}.md"
            f = open(path,"w")
            f.write(text)
            f.close()
            return HttpResponseRedirect(reverse("EntryPage", args = [title]))
          

def Random(request):

    entries = util.list_entries()
    entries = random.choice(entries)
    return HttpResponseRedirect(reverse("EntryPage", args = [entries]))

def Edit(request,name):
    
    if request.method == "GET":
        path = f"entries\{name}.md"
        with open(path) as markdown_file:
            entry = markdown(markdown_file.read())
            form = EditEntryForm(initial={"text": entry })
        
        return render(request,"encyclopedia/edit.html", {
            "entry": entry,
            "form": form,
            "name": name
        })
    
    if request.method == "POST":

        form = EditEntryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
        
        
        
        path = f"entries\{name}.md"
        f = open(path,"w")
        f.write(text)
        f.close()
        return HttpResponseRedirect(reverse("EntryPage", args = [name]))

