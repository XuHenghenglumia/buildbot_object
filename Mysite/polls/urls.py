from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('',views.index,name='index'),
    path('vote/',views.vote,name='vote'),
    path('result/',views.show_table,name='show_table')
]