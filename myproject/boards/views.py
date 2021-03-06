from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from .models import  Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
from . import templates
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
    #board = get_object_or_404(Board,pk=pk)
    try:
        board=Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    # get admin user
    #user = User.objects.first()

    if request.method == 'POST':
        #subject = request.POST['subject']
        #message = request.POST['message']
        #board.topics.filter(subject__contains='Hello') get for sepecific filter
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board=board
            topic.starter=request.user
            topic.save()

        #topic = Topic.objects.create( subject=subject,board=board,starter=user) in case not use forms.py
        post=Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            #get loggin user
            created_by=request.user,
        )
        return redirect('board_topics',pk=board.pk)

    else:
        form = NewTopicForm()
        return render(request,'new_topic.html',{'board':board,'form':form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})



