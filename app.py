import streamlit as st
import tictactoe as ttt
from streamlit_js_eval import streamlit_js_eval
import os
from streamlit_feedback import streamlit_feedback

def reset_game_state():
    st.session_state.board = ttt.initial_state()
    st.session_state.user = None
    st.session_state.ai_turn = False
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.minimax_moves = []
    st.session_state.cell_states = {}
    st.session_state.update_needed = False

def update_cell(i, j):
    key = f"cell_{i}_{j}"
    if not st.session_state.game_over and st.session_state.board[i][j] == ttt.EMPTY and not st.session_state.ai_turn:
        st.session_state.board = ttt.result(st.session_state.board, (i, j))
        st.session_state.cell_states[key] = st.session_state.user
        st.session_state.ai_turn = True
        check_game_state()
        st.session_state.update_needed = True

def ai_move():
    if not st.session_state.game_over and st.session_state.ai_turn:
        ttt.minimax_moves = []
        move = ttt.minimax(st.session_state.board)
        if move:
            i, j = move
            key = f"cell_{i}_{j}"
            st.session_state.board = ttt.result(st.session_state.board, move)
            st.session_state.cell_states[key] = ttt.O if st.session_state.user == ttt.X else ttt.X
            st.session_state.ai_turn = False
        st.session_state.minimax_moves = ttt.minimax_moves
    check_game_state()
    st.session_state.update_needed = False

def check_game_state():
    st.session_state.winner = ttt.winner(st.session_state.board)
    st.session_state.game_over = st.session_state.winner is not None or ttt.terminal(st.session_state.board)

def create_footer_html():
    social_links = [
        ("facebook.png", "https://www.facebook.com/profile.php?id=100010437153747"),
        ("x_twitter.png", "https://x.com/Cisco_research"),
        ("linkedin.png", "https://www.linkedin.com/in/francisco-teixeira-barbosa-55040816/"),
        ("youtube.png", "https://www.youtube.com/channel/UCqI7TrKqPZ5nHQcPozra6DA"),
        ("instgram.png", "https://www.instagram.com/tuminha_dds/"),
        ("github.png", "https://github.com/Tuminha"),
        ("periospot.png", "https://periospot.com/")
    ]
    
    image_path = os.path.join(os.path.dirname(__file__), 'images')
    icons_html = "".join([f'<a href="{link}" target="_blank"><img src="data:image/png;base64,{get_image_base64(os.path.join(image_path, image))}" width="30" style="margin: 0 5px;"></a>' for image, link in social_links])
    
    return f"""
    <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #333; color: white; padding: 10px; text-align: center;">
        <p style="margin-bottom: 5px;">Created by Francisco Teixeira Barbosa</p>
        {icons_html}
    </div>
    """

def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def main():
    st.set_page_config(layout="wide", page_title="Tic-Tac-Toe with Minimax AI")

    # Set up local path for images
    image_path = os.path.join(os.path.dirname(__file__), 'images')
    st.markdown(f'<style>img {{ max-width: 100%; height: auto; }}</style>', unsafe_allow_html=True)

    # Initialize session state
    if 'initialized' not in st.session_state:
        reset_game_state()
        st.session_state.initialized = True

    # Custom CSS
    st.markdown("""
    <style>
        .stButton > button {
            font-size: 60px;
            height: 100px;
            width: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            line-height: 1;
        }
        .stButton > button:hover {
            background-color: #f0f0f0;
        }
        div[data-testid="column"] {
            display: flex;
            justify-content: center;
        }
        .stButton > button > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        .stButton > button > div > p {
            font-size: 60px !important;
            transform: scale(1.2);
            margin: 0 !important;
        }
        button[kind="secondary"][data-testid="stButton"] {
            font-size: 14px !important;
            padding: 5px 10px !important;
            height: auto !important;
            width: auto !important;
        }
        .explanation-box {
            background-color: rgba(70, 131, 180, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .game-status {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
        body {
            padding-bottom: 100px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎮 Tic-Tac-Toe with Minimax AI 🤖")

    # Game explanation
    with st.expander("ℹ️ About this game", expanded=True):
        st.markdown("""
        <div class="explanation-box">
        <h3>Welcome to Tic-Tac-Toe with Minimax AI! 🧠</h3>
        <p>This game showcases the power of the Minimax algorithm in decision-making for simple games. Here's what makes it special:</p>
        <ul>
            <li>🤖 <strong>Minimax AI:</strong> The computer uses the Minimax algorithm to make optimal moves.</li>
            <li>🌳 <strong>Decision Tree:</strong> Minimax explores all possible future game states to choose the best move.</li>
            <li>🏆 <strong>Unbeatable AI:</strong> When playing against the AI, the best you can do is tie!</li>
            <li>🧮 <strong>Perfect for Tic-Tac-Toe:</strong> Minimax works well for simple games with a limited number of possible states.</li>
            <li>⚠️ <strong>Limitations:</strong> For more complex games like Chess, Minimax alone would be too slow due to the vast number of possible moves.</li>
        </ul>
        <p>Enjoy playing against the AI and observe how it always makes the best possible move!</p>
        </div>
        """, unsafe_allow_html=True)

    # Game controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("New Game", key="new_game_button", help="Start a new game"):
            reset_game_state()
            st.rerun()

    with col3:
        opponent = st.selectbox("Opponent", ["AI", "Human"], key="opponent")

    # Player selection
    if st.session_state.user is None:
        st.write("Choose your player:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❎", key="play_x"):
                st.session_state.user = ttt.X
                st.rerun()
        with col2:
            if st.button("⭕️", key="play_o"):
                st.session_state.user = ttt.O
                st.session_state.ai_turn = True
                st.rerun()

    # Game board
    if st.session_state.user:
        game_status = st.empty()
        board_container = st.empty()

        with board_container.container():
            for i in range(3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    with col:
                        key = f"cell_{i}_{j}"
                        cell_state = st.session_state.cell_states.get(key, ttt.EMPTY)
                        if cell_state == ttt.EMPTY:
                            if st.button(" ", key=key, on_click=update_cell, args=(i, j)):
                                st.rerun()
                        else:
                            symbol = "❎" if cell_state == ttt.X else "⭕️"
                            st.button(symbol, key=key, disabled=True)

        # Game status
        with game_status:
            if st.session_state.winner:
                st.success(f"🏆 Player {st.session_state.winner} wins!")
            elif st.session_state.game_over:
                st.info("🤝 It's a tie!")
            else:
                current_player = "❎" if st.session_state.user == ttt.X else "⭕️"
                st.markdown(f"<div class='game-status'>Player {current_player}'s turn</div>", unsafe_allow_html=True)
                if st.session_state.ai_turn:
                    with st.spinner("🤖 AI is thinking..."):
                        ai_move()
                    st.rerun()

    # Minimax moves (for demonstration)
    with st.sidebar:
        st.header("🧠 Minimax Moves")
        for move in st.session_state.minimax_moves:
            st.write(move)

    # Feedback
    if st.session_state.game_over:
        st.markdown("### How was your experience?")
        feedback = streamlit_feedback(
            feedback_type="thumbs",
            key="feedback"
        )
        if feedback:
            st.write(f"Thank you for your feedback {feedback}!")

    # Add footer
    st.markdown(create_footer_html(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()