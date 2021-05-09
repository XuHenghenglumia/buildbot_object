from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from .export_data import export_data
import os.path
import time
from functools import wraps
from django.test import Client
from .models import Choice

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
    databases = {'default'}

    def test_vote(self):
        self.client = Client()
        #response = c.post(path='/polls/vote/',data='csrfmiddlewaretoken=Oy8l2VIsmooLYzlpNjkk6e8yo6yWGklGiF3BRbEVPGvpzv6OC3UJs5bvoltyhR2g&1=14&2=16&3=18&4=21&5=23&6=25&7=29',content_type='application/x-www-form-urlencoded')
        #response = c.get(path='/')
        #response = self.client.post(path='/polls/vote/',
        #          data='1=14&2=17&3=19&4=22&5=24&6=26&7=30',
        #          content_type='application/x-www-form-urlencoded')
        #self.assertEqual(200,response.status_code)
        q=Question.objects.get(pk=1)
        self.assertEqual(q.question_text,"你是计算机相关从业者或学生吗？")
