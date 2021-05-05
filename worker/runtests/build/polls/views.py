from django.shortcuts import render
from django.http import HttpResponse, Http404
from polls.models import Question, Choice
from django.template import loader
from . import export_data

# Create your views here.
from django.http import HttpResponse
def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list':latest_question_list}
    return render(request,'polls/polls.html', context)

def home(request):
    return render(request,'home/home.html')

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "you're looking at the results of question %s"
    return HttpResponse(response % question_id)

def vote(request):
    str =  ''
    if request.method == 'POST':
        data=[]
        head=[]
        for key,value in request.POST.items():
            #str=str+key+" "+value+"\n"
            if key == 'csrfmiddlewaretoken':
                continue
            c=Choice.objects.get(pk=value)
            q=Question.objects.get(pk=key)
            data.append(c.choice_text)
            head.append(q.question_text)
            c.votes=c.votes+1
            c.save()
        export_data.export_data(head,data,'data.csv')
        return render(request, 'polls/finish.html')
    else:
        return HttpResponse("no data")