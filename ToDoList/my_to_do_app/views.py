from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse # 역으로 index로 전환
from .models import *


# Create your views here.
def index(request):
    todos = ToDo.objects.all()   # DB전체조회

    content = {'todos' : todos}  # Dictionary에 담아서 다시 보내기

    return render(request, 'my_to_do_app/index.html', content)  #request , 보여질 view , 보일 객체

        # content : Key-value // key를 통해 조회하므로 key가 필요함

def createTodo(request):
    input = request.POST['todoContent']

    content = ToDo(contents = input) # DB의 Column 값 contents
    content.save()
    return HttpResponseRedirect(reverse('index'))   # view를 거치지않고 DB값을 createTodo 함수로 받은 후
                                                    # 바로 index 함수로 보내주어 출력
    #return HttpResponse('createTodo page :' + input )

def doneTodo(request):
    done_id = request.GET['todoNum']
    todo = ToDo.objects.get(id = done_id)
    todo.delete()
    return HttpResponseRedirect(reverse('index'))

def completeTodo(request):
    complete_id = request.GET['todoNum']
    todo = ToDo.objects.get(id = complete_id)
    todo.doDone = True
    todo.save()
    return HttpResponseRedirect(reverse('index'))

