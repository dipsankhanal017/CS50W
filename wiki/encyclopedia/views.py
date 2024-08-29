from django.shortcuts import render, redirect

from . import util
import markdown, random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def displayinfo(request, title):
    if request.method == "POST":
        head = request.POST.get("title")
        body = util.get_entry(head)
        return render(request, "encyclopedia/editpage.html", {"title":head, "content": body})
    try:
        markdownContent = util.get_entry(title)
        htmlContent = markdown.markdown(markdownContent)
        return render(request, "encyclopedia/infopage.html", {'title':title, 'htmlContent':htmlContent})
    except:
        return render(request, "encyclopedia/errorpage.html")

def editpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        url= "/wiki/"+ title
        return redirect(url)

def search(request):
    if request.method == "GET":
        to_search = request.GET.get("q")
        entries = util.list_entries()
        for entry in entries:
            if to_search.lower() == entry.lower():
                url = "/wiki/"+to_search
                return redirect(url)
        new_entries = []
        for entry in entries:
            if to_search.lower() in entry.lower():
                new_entries.append(entry)
        if new_entries != []:
            return render(request, "encyclopedia/searchpage.html", {"entries": new_entries})
        else:
            return render(request, "encyclopedia/searchpage.html", {"notfound": "notfound"})

def randompage(request):
    title = random.choice(util.list_entries())
    url = "/wiki/"+title
    return redirect(url)

def newpage(request):
    if request.method =="POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in util.list_entries():
            return render(request, "encyclopedia/newpage.html", {
                "message": "Title already exist",
                "title":title,
                "content":content
                })
        util.save_entry(title,content)
        url= "/wiki/"+ title
        return redirect(url)
    return render(request, "encyclopedia/newpage.html")
