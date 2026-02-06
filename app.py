import streamlit as st
import sys
import os

# Add the project root to python path to allow imports from core, visualization, etc.
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ui.layout import render_layout

def main():
    st.set_page_config(page_title="N-Queen Visualizer", layout="wide")
    render_layout()

if __name__ == "__main__":
    main()