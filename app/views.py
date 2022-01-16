from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Question, Answer, Tag
from app.forms import LoginForm, SignupForm, AskForm, AnswerForm, SettingsForm

questions = [{
        "title": f"Title {i}",
        "text": f"This is text for {i} question. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "count_answers": f"{i}"
    } for i in range(1, 10)
]

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    data = paginator.get_page(page)
    return data

def index(request):
    questions = Question.m.new()
    data = paginate(questions, request)
    return render(request, "index.html", {'questions': data, 'block_name': 'Questions'})

def hot(request):
    questions = Question.m.hot()
    data = paginate(questions, request)
    return render(request, "index.html", {'questions': data, 'block_name': 'Hot questions'})

def q_with_tag(question_tag):
    question = [{
        "title": f"Title {i} with tag {question_tag}",
        "text": f"This is text for {i} question. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "count_answers": f"{i}"
    } for i in range(5, 0, -1)
    ]
    return question

def tag(request, question_tag):
    questions = Question.m.by_tag(question_tag)
    data = paginate(questions, request)
    return render(request, "index.html", {'questions': data, 'block_name': f'Tag \'{question_tag}\''})


def q(i):
    question = {
        "title": f"Title {i}",
        "text": f"This is text for {i} question. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
    return question

def ans_for_q(i):
    answers = [{
        "text": f"Answer {j} for question {i}. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatu."
    } for j in range(5)
    ]
    return answers

def question(request, question_id):
    cur_question = Question.m.by_id(question_id)
    answers = cur_question.answers.all()
    pag_answers = paginate(answers, request)

    if request.method == 'GET':
        form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            ans = Answer(text=form.cleaned_data['text'], question=cur_question, author=request.user)
            ans.save()
            return redirect(reverse('question', args=[question_id]))
    return render(request, "question.html", {'question': cur_question, 'answers': pag_answers, 'form': form})


@login_required(login_url='login')
def ask(request):
    if request.method == 'GET':
        q_form = AskForm()
    if request.method == 'POST':
        q_form = AskForm(data=request.POST)
        if q_form.is_valid():
            q = Question(title=q_form.cleaned_data['title'], text=q_form.cleaned_data['text'], author=request.user)
            q.save()
            tag_for_q, created = Tag.objects.get_or_create(name=q_form.cleaned_data['tags'])
            q.tags.add(tag_for_q)
            return redirect(reverse('question', args=[q.id]))
    return render(request, "ask.html", {"form" : q_form})


@login_required(login_url='login')
def settings(request):
    my_user = request.user
    if request.method == 'GET':
        form = SettingsForm(data={'login': my_user.username, 'username': my_user.username, 'email': my_user.email})
    if request.method == 'POST':
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            #my_user = User.objects.create_user(form.cleaned_data['login'], form.cleaned_data['email'], form.cleaned_data['password'])
            my_user.username = form.cleaned_data['login']
            my_user.email = form.cleaned_data['email']
            my_user.set_password(form.cleaned_data['password'])
            my_user.save()
            auth.login(request, my_user)
            return redirect(reverse('index'))
    return render(request, "settings.html", {'form': form})


def register(request):
    if request.method == 'GET':
        form = SignupForm()
    elif request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            my_user = User.objects.create_user(form.cleaned_data['login'], form.cleaned_data['email'], form.cleaned_data['password'])
            # profile = Profile.objects.create(avatar=form.cleaned_data['avatar'], user=my_user)
            auth.login(request, my_user)
            return redirect(reverse('index'))
    return render(request, "register.html", {"form": form})

def login(request):
    print(request.POST)
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, 'User not found.')
            else:
                auth.login(request, user)
                return redirect(reverse('index'))
    return render(request, "login.html", {"form": form})

def logout_view(request):
    auth.logout(request)
    return redirect(reverse('index'))
