from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="home"), # name คือชื่อที่อยากจะตั้ง
    path('index',views.index , name='index'), # http://127.0.0.1:8000/processing3  ใส่เลขไปได้เลย 
    path('index/preprocess',views.preprocess,name='preprocess'),
    path('index/terminates',views.terminates,name='terminates'),
    path('index/time',views.time,name="time"),
    path('index/addIO',views.add_io,name='add_io'),
    path('index/close_io',views.close_io,name="close_io")
]