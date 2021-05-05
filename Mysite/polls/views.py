from django.shortcuts import render
from django.http import HttpResponse, Http404
from polls.models import Question, Choice
from django.template import loader
from . import export_data
import csv

# Create your views here.
from django.http import HttpResponse
def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list':latest_question_list}
    return render(request,'polls/polls.html', context)

def home(request):
    return render(request,'home/home.html')


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

def show_table(request):
    content=[]
    with open('data.csv','r') as dataFile:
        reader=csv.reader(dataFile)
        for row in reader:
            content.append(row)
    return render(request,'polls/result.html',{'table_data':content})