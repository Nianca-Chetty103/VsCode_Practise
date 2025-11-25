 // Unicode pieces
        const PIECES = {
            p: '♟', r: '♜', n: '♞', b: '♝', q: '♛', k: '♚',
            P: '♙', R: '♖', N: '♘', B: '♗', Q: '♕', K: '♔'
        };

        // Starting position as 8x8 array (rank 8 -> rank 1)
        const START = [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ];

        const boardEl = document.getElementById('board');
        const statusEl = document.getElementById('status');
        let board = []; // 8x8 array current
        let history = [];
        let selected = null;
        let turn = 'w'; // 'w' or 'b'

        // generate coordinates a8..h1
        const files = ['a','b','c','d','e','f','g','h'];
        function squareName(fileIdx, rankIdx) {
            // fileIdx 0..7 left->right, rankIdx 0..7 top->bottom (8->1)
            return files[fileIdx] + (8 - rankIdx);
        }

        function render() {
            boardEl.innerHTML = '';
            for (let r = 0; r < 8; r++) {
                for (let f = 0; f < 8; f++) {
                    const sq = document.createElement('div');
                    sq.className = 'square ' + (((r + f) % 2) ? 'dark' : 'light');
                    sq.dataset.r = r; sq.dataset.f = f;
                    sq.dataset.coord = squareName(f, r);
                    const piece = board[r][f];
                    if (piece) sq.textContent = PIECES[piece] || '?';
                    sq.addEventListener('click', onClickSquare);
                    boardEl.appendChild(sq);
                }
            }
            statusEl.textContent = (turn === 'w') ? 'White to move' : 'Black to move';
            highlightSelected();
        }

        function highlightSelected() {
            document.querySelectorAll('.square.selected').forEach(s => s.classList.remove('selected'));
            if (selected) {
                const el = document.querySelector(`.square[data-r="${selected.r}"][data-f="${selected.f}"]`);
                if (el) el.classList.add('selected');
            }
        }

        function onClickSquare(e) {
            const r = Number(this.dataset.r), f = Number(this.dataset.f);
            const piece = board[r][f];
            // select square with your side's piece, or move selected to target
            if (selected) {
                // attempt move
                if (selected.r === r && selected.f === f) { selected = null; render(); return; }
                const moving = board[selected.r][selected.f];
                // basic turn enforcement: uppercase = white, lowercase = black
                if (!moving) { selected = null; render(); return; }
                if ((turn === 'w' && moving === moving.toLowerCase()) || (turn === 'b' && moving === moving.toUpperCase())) {
                    // wrong piece for turn, clear selection
                    selected = null; render(); return;
                }
                // perform move (no legality checking)
                history.push({ from: {r:selected.r,f:selected.f, piece: moving }, to: {r,f, piece: board[r][f] }, turn });
                board[r][f] = moving;
                board[selected.r][selected.f] = '';
                selected = null;
                turn = (turn === 'w') ? 'b' : 'w';
                render();
            } else {
                // pick up a piece if present and matches turn
                if (!piece) return;
                if ((turn === 'w' && piece === piece.toLowerCase()) || (turn === 'b' && piece === piece.toUpperCase())) return;
                selected = { r, f };
                highlightSelected();
            }
        }

        document.getElementById('reset').addEventListener('click', () => {
            loadStart();
            history = [];
            selected = null;
            turn = 'w';
            render();
        });

        document.getElementById('undo').addEventListener('click', () => {
            const last = history.pop();
            if (!last) return;
            board[last.from.r][last.from.f] = last.from.piece;
            board[last.to.r][last.to.f] = last.to.piece;
            turn = last.turn;
            selected = null;
            render();
        });

        function loadStart() {
            board = START.map(row => row.slice());
        }

        // initialize and render
        loadStart();
        render();