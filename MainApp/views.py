from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        "snippets": snippets,
        "count": snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def add_snippet_page(request):
    # Хотим получить чистую форму для заполнения полей
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    # Хотим создать новый Snippet на основе данных от формы
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets_list")
        return render(request,'add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        context = {
            'pagename': 'Просмотр сниппета',
            "snippet": snippet,
            "type": 'view'
            }
        return render(request, 'pages/snippet_detail.html', context)


@login_required
def snippet_delete(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if snippet.user == request.user:
            snippet.delete()
            return redirect("snippets_list")
        return HttpResponseForbidden("It's others snippets")


@login_required
def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    # Хотим получить страницу сниппета для редактирования
    if request.method == "GET":
        context = {
            'pagename': 'Редактирование сниппета',
            "snippet": snippet,
            "type": 'edit'
            }
        return render(request, 'pages/snippet_detail.html', context)
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form['name']
        snippet.lang = data_form['lang']
        snippet.creation_date = data_form['creation_date']
        snippet.code = data_form['code']
        snippet.public = data_form.get('public', False)
        snippet.save()
        return redirect('snippets_list')


def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           context = {
               "pagename": "PythonBin",
               "errors": ['wrong username or password']
           }
           return render(request, 'pages/index.html', context)
   return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def create_user(request):
    context = {'pagename': 'Регистрация пользователя'}
    # Хотим получить чистую форму для заполнения полей
    if request.method == "GET":
        form = UserRegistrationForm
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    # Хотим создать нового пользователя на основе данных от формы
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request,'pages/registration.html', context)


# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         print(vars(form))
#         if form.is_valid():
#             form.save()
#             return redirect("snippets_list")
#         return render(request,'add_snippet.html', {'form': form})
