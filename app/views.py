from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

questions = [{
        "title": f"Title {i}",
        "text": f"This is text for {i} question. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "count_answers": f"{i}"
    } for i in range(1, 10)
]

def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    data = paginator.get_page(page)
    return data

def index(request):
    data = paginate(questions, request)
    return render(request, "index.html", {'questions': data, 'block_name': 'Questions'})

def hot(request):
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
    data = paginate(q_with_tag(question_tag), request)
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
    data = paginate(ans_for_q(question_id), request)
    return render(request, "question.html", {'question': q(question_id), 'answers': data})

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

def ask(request):
    return render(request, "ask.html", {})

def settings(request):
    return render(request, "settings.html", {})
