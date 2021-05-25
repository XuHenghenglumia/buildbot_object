from django.test import TestCase,TransactionTestCase
import datetime
from django.utils import timezone
from .models import Question
from .export_data import export_data
import os.path
import time
from functools import wraps
from django.test import Client
from .models import Choice
import requests

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
        #self.assertIs(False,False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class ExportDataTests(TestCase):
    def test_could_write_head_and_data_info(self):
        head=["th1","th2","th3"]
        data=["td1","td2","td3"]
        data_2=["newdata1","newdata2","newdata3"]
        filename="temp.csv"
        export_data(head, data, filename)
        export_data(head, data_2, filename)
        self.assertIs(os.path.exists(filename), True)
        with open(filename,'r') as tempFile:
            strList=tempFile.readlines()
            self.assertEqual(strList[0], "th1,th2,th3\n")
            self.assertEqual(strList[1], "td1,td2,td3\n")
            self.assertEqual(strList[2], "newdata1,newdata2,newdata3\n")
        os.remove(filename)
    
class performanceTests(TestCase):
    #databases = {'default'}

    def test_request(self):
        start_time=time.perf_counter()
        url = 'http://127.0.0.1:8000/'
        r=requests.get(url)
        self.assertEqual(r.status_code,200)
        url += 'polls/'
        r=requests.get(url)
        self.assertEqual(r.status_code,200)
        url += 'vote/'
        data = {
            '1':'14',
            '2':'16',
            '3':'18',
            '4':'22',
            '5':'24',
            '6':'28',
            '7':'30'
        }
        r=requests.post(url,data=data)
        self.assertEqual(r.status_code,200)
        end_time=time.perf_counter()
        cost_time=end_time-start_time
        print("cost time: ",cost_time)
        with open('performance.log','w') as pf:
            pf.write("cost time: {}\n".format(cost_time))