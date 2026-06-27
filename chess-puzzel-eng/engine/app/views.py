import chess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Puzzle
from .serializers import PuzzleSerializer

class GetRandomPuzzleView(APIView):
    """
    API endpoint that fetches a random chess puzzle from the database
    and returns it to the frontend without the solution field.
    """
    def get(self, request):
        # Fetch a single random puzzle from the database
        puzzle = Puzzle.objects.order_by('?').first()
        
        if not puzzle:
            return Response(
                {"error": "No puzzles found in the database."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PuzzleSerializer(puzzle)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckMoveView(APIView):
    """
    API endpoint that verifies if the user's move is legal and correct
    according to the puzzle's solution.
    """
    def post(self, request):
        puzzle_id = request.data.get('puzzle_id')
        player_move = request.data.get('move')  # Expected in UCI format, e.g., "e2e4"

        if not puzzle_id or not player_move:
            return Response(
                {"error": "Missing puzzle_id or move in request data."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            puzzle = Puzzle.objects.get(id=puzzle_id)
        except Puzzle.DoesNotExist:
            return Response(
                {"error": "Puzzle not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Parse the stored solution moves into a list
        solution_moves = puzzle.solution.split()
        if not solution_moves:
            return Response(
                {"error": "Puzzle has an empty or corrupt solution line."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Initialize the chess board using the puzzle's FEN
        try:
            board = chess.Board(puzzle.fen)
        except ValueError:
            return Response(
                {"error": "Invalid FEN string stored in database."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 1. Check if the move is parseable and legal on the current board
        try:
            move_obj = chess.Move.from_uci(player_move)
        except ValueError:
            return Response(
                {"status": "error", "message": "Invalid move format. Use UCI (e.g., e2e4)."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if move_obj not in board.legal_moves:
            return Response(
                {"status": "illegal", "message": "This move is illegal in this position!"}, 
                status=status.HTTP_200_OK
            )

        # 2. Verify if the move matches the first correct move of the solution
        correct_move = solution_moves[0]
        
        if player_move == correct_move:
            # If the puzzle has subsequent moves, we can handle them later, 
            # for the MVP, matching the first move confirms success or progression.
            return Response(
                {"status": "correct", "message": "Excellent move! That is correct."}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "wrong", "message": "Legal move, but not the best tactical solution."}, 
                status=status.HTTP_200_OK
            )