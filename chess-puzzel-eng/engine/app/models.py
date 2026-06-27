from django.db import models


class Puzzle(models.Model):
    # Storing the complete board state
    fen = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="The standard FEN notation representing the board state."
    )
    
    # Storing the solution moves separated by spaces, e.g., "d2d4 g8f6 c2c4"
    solution = models.CharField(
        max_length=255, 
        help_text="The consecutive correct UCI moves separated by spaces."
    )
    
    # The tactical difficulty level of the puzzle
    rating = models.IntegerField(
        default=1200, 
        help_text="The estimated ELO rating/difficulty of the puzzle."
    )
    
    # Optional description (e.g., Mate in 2, Fork, Skewer)
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Optional description of the tactical theme or tactical motives."
    )
    
    # Timestamp for when the puzzle was added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Puzzle #{self.id} [Rating: {self.rating}]"