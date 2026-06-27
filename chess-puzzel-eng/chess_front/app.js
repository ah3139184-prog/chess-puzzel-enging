
const API_BASE_URL = 'http://127.0.0.1:8000/api/';

let board = null;
let game = new Chess(); 
let currentPuzzleId = null;

const statusMsg = document.getElementById('status-msg');
const puzzleRating = document.getElementById('puzzle-rating');
const nextBtn = document.getElementById('next-btn');

async function loadNewPuzzle() {
    statusMsg.innerText = ' Loading next puzzle...';
    statusMsg.style.color = '#fff';
    
    try {
        const response = await fetch(`${API_BASE_URL}get-puzzle/`);
        if (!response.ok) throw new Error('Failed to fetch puzzle');
        
        const data = await response.json();
        
        currentPuzzleId = data.id;
        puzzleRating.innerText = data.rating;
        statusMsg.innerText = data.description || 'Find the best move for this position!';
        
        game.load(data.fen);
        
        const orientation = game.turn() === 'w' ? 'white' : 'black';
        board.orientation(orientation);
        board.position(data.fen);
        
    } catch (error) {
        console.error(error);
        statusMsg.innerText = 'Error loading puzzle. Is Django server running?';
        statusMsg.style.color = '#ff4a4a';
    }
}


function onDrop(source, target) {

    const moveNotation = source + target;
    

    const move = game.move({
        from: source,
        to: target,
        promotion: 'q' 
    });

    if (move === null) return 'snapback';

    verifyMoveWithBackend(moveNotation);
}

async function verifyMoveWithBackend(moveNotation) {
    try {
        const response = await fetch(`${API_BASE_URL}check-move/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                puzzle_id: currentPuzzleId,
                move: moveNotation
            })
        });

        const data = await response.json();

        if (data.status === 'correct') {
            statusMsg.innerText = `🎉 ${data.message}`;
            statusMsg.style.color = '#4caf50'; 
        } else {
            statusMsg.innerText = `❌ ${data.message}`;
            statusMsg.style.color = '#ff4a4a';

            setTimeout(() => {
                game.undo();
                board.position(game.fen());
            }, 1000);
        }

    } catch (error) {
        console.error(error);
        statusMsg.innerText = 'Connection error with the backend.';
    }
}


const config = {
    draggable: true, 
    position: 'start', 
    onDrop: onDrop, 
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png' 
};

board = Chessboard('myBoard', config);

nextBtn.addEventListener('click', loadNewPuzzle);

loadNewPuzzle();
