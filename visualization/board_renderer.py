import streamlit as st
from .styles import (
    COLOR_BOARD_LIGHT,
    COLOR_BOARD_DARK,
    COLOR_HIGHLIGHT_PLACED,
    COLOR_HIGHLIGHT_INVALID,
    COLOR_HIGHLIGHT_BACKTRACK
)


def render_board(state=None, n=8, max_size=520, key_suffix=""):
    """
    Renders the N-Queen board using HTML/CSS.

    key_suffix:
    - REQUIRED when rendering multiple boards (solutions grid)
    """

    board_css = """
    <style>
        .board-frame {
            padding: 6px;                 /* slight breathing space */
            background: #2b3a2b;          /* neutral dark backdrop */
            border-radius: 6px;
            aspect-ratio: 1 / 1;
            width: 100%;
            max-width: var(--board-size);
            margin: 0 auto;
            overflow: hidden;
            box-sizing: border-box;
        }


        .chessboard {
            display: grid;
            grid-template-columns: repeat(var(--n), 1fr);
            grid-template-rows: repeat(var(--n), 1fr);
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }

        .cell {
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            user-select: none;
        }

        .queen {
            font-size: clamp(0.9rem, 4vw, 2.4rem);
            line-height: 1;
            color: #1f1f1f;   /* chess.com-like piece tone */
        }

    </style>
    """

    board_data = [-1] * n
    active_row = active_col = -1
    action = None

    if state:
        board_data = state.get("board", board_data)
        active_row = state.get("current_row", -1)
        active_col = state.get("current_col", -1)
        action = state.get("action")

    cells_html = ""

    for r in range(n):
        for c in range(n):
            is_dark = (r + c) % 2 != 0
            bg_color = COLOR_BOARD_DARK if is_dark else COLOR_BOARD_LIGHT

            if r == active_row and c == active_col:
                if action == "place":
                    bg_color = COLOR_HIGHLIGHT_PLACED
                elif action in ("remove", "backtrack"):
                    bg_color = COLOR_HIGHLIGHT_BACKTRACK
                elif action == "invalid":
                    bg_color = COLOR_HIGHLIGHT_INVALID

            content = ""
            if board_data[r] == c:
                content = '<span class="queen">♛</span>'

            cells_html += (
                f'<div class="cell" style="background:{bg_color};">{content}</div>'
            )

    full_html = f"""
    {board_css}
    <div class="board-frame" style="--n:{n}; --board-size:{max_size}px;">
        <div class="chessboard">
            {cells_html}
        </div>
    </div>
    """

    # ✅ KEY FIX: stable identity per board instance
    st.markdown(full_html, unsafe_allow_html=True)
