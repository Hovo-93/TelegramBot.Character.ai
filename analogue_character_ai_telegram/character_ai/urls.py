from django.urls import path, include
from character_ai.views import character_view,choose_character

urlpatterns = [

    path('test', character_view, name='test'),
    path('my_endpoint',choose_character,name='choose_character')

]
