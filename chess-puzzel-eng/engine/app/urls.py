from django.urls import path
from .views import GetRandomPuzzleView, CheckMoveView

urlpatterns = [
    path('get-puzzle/', GetRandomPuzzleView.as_view(), name='get_random_puzzle'),
    path('check-move/', CheckMoveView.as_view(), name='check_move'),
]