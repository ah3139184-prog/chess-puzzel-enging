Chess Puzzle Engine
A lightweight backend engine for managing chess puzzles.

Setup Instructions
Set up the virtual environment:

Bash
# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Populate the Database:

Open puzzles_seed.py and add your puzzle data to the puzzles_data variable.

Run the seed script to import the puzzles into the database:

Bash
python puzzles_seed.py
Run the Backend:

Bash
python manage.py runserver
Frontend:

Navigate to the frontend folder and open the index.html file in your browser to interact with the engine.
