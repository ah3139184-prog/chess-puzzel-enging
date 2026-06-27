from rest_framework import serializers
from .models import Puzzle

class PuzzleSerializer(serializers.ModelSerializer):
    """
    Serializer used to send puzzle data to the frontend.
    Excludes the solution field to prevent cheating.
    """
    class Meta:
        model = Puzzle
        fields = ['id', 'fen', 'rating', 'description']


class PuzzleSolutionSerializer(serializers.ModelSerializer):
    """
    Serializer used for admin purposes or complete data manipulation.
    Includes all fields including the solution.
    """
    class Meta:
        model = Puzzle
        fields = '__all__'