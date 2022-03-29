from django.shortcuts import render, redirect
from random import sample
from . import util
import markdown2
from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label="",max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class':'search'}))

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-lg-6'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-lg-6', 'rows': '5'}))

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-lg-6', 'rows': '5'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

def index(request):
    if request.method == "GET":
        all_entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })

def entry(request, qname):
    entry = util.get_entry(qname)
    
    if entry != None:
        content = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {"title": qname, "content": content, "search_form": SearchForm()})
    else:
        return render(request, "encyclopedia/entry.html", {"title": qname, "error": "Page not found.", "search_form": SearchForm()})

def result(request):
    query = request.GET.get('q')
    title = query
    if query != None:
        if query != "":
            all_entries = util.list_entries()
            match_entry = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    match_entry.append(entry)
                if query.lower() == entry.lower():
                    return redirect('entry', qname=title)
            if len(match_entry) > 0:
                return render(request, "encyclopedia/result.html", {"title": query, "match_entry": match_entry, "search_form": SearchForm()})
            else:
                return render(request, "encyclopedia/result.html", {"title": query, "error": "There were no results matching the query.", "search_form": SearchForm()})
    else:
        return redirect('index')

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return redirect('entry', qname=title)
            else:
                return render(request, "encyclopedia/new_page.html", {"error": "Page already exists.", 'form': NewPageForm(), "search_form": SearchForm()})

    return render(request, "encyclopedia/new_page.html", {'form': NewPageForm(), "search_form": SearchForm()})

def random(request):
    all_entries = util.list_entries()
    entry = sample(all_entries, len(all_entries))[0]
    return redirect('entry', qname=entry)

def edit(request):
    title = request.GET['title']
    content = util.get_entry(title)
    if content != None:
        if request.method == "POST":
            form = EditPageForm(request.POST)
            if form.is_valid():
                new_content = form.cleaned_data['content']
                util.save_entry(title, new_content)
                return redirect('entry', qname=title)
    else:           
        return redirect('wiki')

    return render(request, "encyclopedia/edit.html", {"title": title, "form": EditPageForm(initial={'content': content}), "search_form": SearchForm()})

def wiki(request):
    return redirect('index')