import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')
django.setup()

from app.models import Puzzle


puzzles_data = [
    {
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
        "solution": "c6e7",  
        "rating": 1000,
        "description": "Italian Game defense setup, consolidating the center."
    },
    {
        "fen": "r1b2rk1/pp3ppp/2n5/1B1p4/q7/5N2/PPP2PPP/R1BQR1K1 w - - 0 1",
        "solution": "b5a4",  
        "rating": 1100,
        "description": "Tactical blunder punishment: Free Queen capture on a4."
    },
    {
        "fen": "6k1/pp4p1/2p5/2bp4/8/2P5/PP1q2PP/4R2K w - - 0 1",
        "solution": "e1e8",  
        "rating": 1300,
        "description": "Back-rank tactical counter-attack opportunity."
    }
]

def seed_database():
    print("Starting to seed chess puzzles data...")
    count = 0
    for data in puzzles_data:

        puzzle, created = Puzzle.objects.get_or_create(
            fen=data["fen"],
            defaults={
                "solution": data["solution"],
                "rating": data["rating"],
                "description": data["description"]
            }
        )
        if created:
            count += 1
            print(f"Successfully added: Puzzle #{puzzle.id} [Rating: {puzzle.rating}]")
        else:
            print(f"Puzzle already exists, skipped.")
            
    print(f"Seeding completed! Added {count} new puzzles.")

if __name__ == '__main__':
    seed_database()
