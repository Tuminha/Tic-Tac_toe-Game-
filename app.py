import streamlit as st
import tictactoe as ttt

def init():
    if 'board' not in st.session_state:
        st.session_state.board = ttt.initial_state()
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'ai_turn' not in st.session_state:
        st.session_state.ai_turn = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'minimax_moves' not in st.session_state:
        st.session_state.minimax_moves = []

def handle_click(i, j):
    if not st.session_state.game_over and st.session_state.board[i][j] == ttt.EMPTY:
        st.session_state.board = ttt.result(st.session_state.board, (i, j))
        st.session_state.ai_turn = True
        check_game_state()

def ai_move():
    if not st.session_state.game_over and st.session_state.ai_turn:
        ttt.minimax_moves = []  # Reset moves before each AI turn
        move = ttt.minimax(st.session_state.board)
        if move:
            st.session_state.board = ttt.result(st.session_state.board, move)
            st.session_state.ai_turn = False
        st.session_state.minimax_moves = ttt.minimax_moves  # Store moves in session state
        check_game_state()

def check_game_state():
    st.session_state.winner = ttt.winner(st.session_state.board)
    st.session_state.game_over = ttt.terminal(st.session_state.board)

def main():
    st.title("❎🅾️ Tic-Tac-Toe")

    init()

    # Sidebar to display minimax moves
    with st.sidebar:
        st.header("Minimax Moves")
        for move in st.session_state.minimax_moves:
            st.write(move)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("New Game"):
            st.session_state.board = ttt.initial_state()
            st.session_state.user = None
            st.session_state.ai_turn = False
            st.session_state.winner = None
            st.session_state.game_over = False
            st.session_state.minimax_moves = []

    with col3:
        opponent = st.selectbox("Opponent", ["Human", "AI"], key="opponent")

    if st.session_state.user is None:
        st.write("Choose your player:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play as X"):
                st.session_state.user = ttt.X
        with col2:
            if st.button("Play as O"):
                st.session_state.user = ttt.O
                st.session_state.ai_turn = True

    if st.session_state.user:
        for i in range(3):
            cols = st.columns([1, 1, 1])
            for j in range(3):
                with cols[j]:
                    if st.session_state.board[i][j] == ttt.EMPTY:
                        if st.button(" ", key=f"{i}-{j}", on_click=handle_click, args=(i, j)):
                            pass
                    else:
                        st.button(st.session_state.board[i][j], key=f"{i}-{j}", disabled=True)

        if opponent == "AI" and st.session_state.ai_turn:
            ai_move()

        check_game_state()

        if st.session_state.winner:
            st.success(f"Player {st.session_state.winner} wins!")
        elif st.session_state.game_over:
            st.info("It's a tie!")
        elif not st.session_state.ai_turn:
            st.write(f"Player {st.session_state.user}'s turn")
        else:
            st.write("AI is thinking...")

if __name__ == "__main__":
    main()