import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Wordle Game", layout="centered")

# Load words from CSV
@st.cache_data
def load_words():
    csv_path = os.path.join(os.path.dirname(__file__), "words.csv")
    df = pd.read_csv(csv_path)
    return df

# Get today's word
def get_todays_word():
    df = load_words()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find word for today
    word_row = df[df['date'] == today]
    if not word_row.empty:
        return word_row['word'].values[0].upper()
    else:
        # Fallback to first word if date not found
        return df['word'].values[0].upper()

# Get today's hint
def get_todays_hint():
    df = load_words()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find hint for today
    word_row = df[df['date'] == today]
    if not word_row.empty and 'hint' in df.columns:
        hint = word_row['hint'].values[0]
        # Return hint if it exists and is not NaN
        if pd.notna(hint) and hint.strip():
            return str(hint)
    return "No hint available for today"

# Initialize session state
if 'word' not in st.session_state:
    st.session_state.word = get_todays_word()
    st.session_state.hint = get_todays_hint()
    st.session_state.guesses = []
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.current_guess = ""
    st.session_state.hint_revealed = False

# Helper function to check guess
def check_guess(guess, target):
    """
    Returns color feedback for each letter
    Green: correct position
    Yellow: correct letter, wrong position
    Gray: not in word
    """
    guess = guess.upper()
    target = target.upper()
    feedback = []
    
    # Count letters in target for proper marking
    target_counts = {}
    for letter in target:
        target_counts[letter] = target_counts.get(letter, 0) + 1
    
    # First pass: mark greens
    result = ['gray'] * 5
    for i, letter in enumerate(guess):
        if letter == target[i]:
            result[i] = 'green'
            target_counts[letter] -= 1
    
    # Second pass: mark yellows and grays
    for i, letter in enumerate(guess):
        if result[i] != 'green':
            if letter in target_counts and target_counts[letter] > 0:
                result[i] = 'yellow'
                target_counts[letter] -= 1
            else:
                result[i] = 'gray'
    
    return result

# Template for styled letter boxes
def display_guess_row(guess, feedback):
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    colors = {
        'green': '#6aaa64',
        'yellow': '#c9b458',
        'gray': '#787c7e'
    }
    
    for i, (letter, status) in enumerate(zip(guess, feedback)):
        with cols[i]:
            st.markdown(
                f"""
                <div style='
                    background-color: {colors[status]};
                    color: white;
                    padding: 20px;
                    border-radius: 5px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                '>
                    {letter}
                </div>
                """,
                unsafe_allow_html=True
            )

# Title
st.title("❤️ Valentine's Wordle")
st.write(f"**Today's Date:** {datetime.now().strftime('%A, %B %d, %Y')}")
st.divider()

# Display previous guesses
if st.session_state.guesses:
    st.write("**Your Guesses:**")
    for guess, feedback in st.session_state.guesses:
        display_guess_row(guess, feedback)
    st.divider()

# Game status
if st.session_state.won:
    st.success(f"🎉 **You Won!** The word was **{st.session_state.word}**")
    st.info(f"Guesses: {len(st.session_state.guesses)}/6")
elif st.session_state.game_over:
    st.error(f"💔 **Game Over!** The word was **{st.session_state.word}**")
else:
    remaining_guesses = 6 - len(st.session_state.guesses)
    st.info(f"Guesses remaining: {remaining_guesses}/6")
    
    # Hint button
    if st.button("💡 Get Hint"):
        st.session_state.hint_revealed = True
    
    if st.session_state.hint_revealed:
        st.info(f"**Hint:** {st.session_state.hint}")

# Input for new guess
if not st.session_state.game_over and not st.session_state.won:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        guess_input = st.text_input(
            "Enter a 5-letter word:",
            value=st.session_state.current_guess,
            max_chars=5,
            key="guess_input"
        ).upper()
    
    with col2:
        submit_btn = st.button("Submit", use_container_width=True)
    
    if submit_btn and guess_input:
        # Validate guess
        if len(guess_input) != 5:
            st.error("Please enter exactly 5 letters!")
        elif not guess_input.isalpha():
            st.error("Please enter only letters!")
        else:
            # Process guess
            feedback = check_guess(guess_input, st.session_state.word)
            st.session_state.guesses.append((guess_input, feedback))
            st.session_state.current_guess = ""
            
            # Check if won
            if guess_input == st.session_state.word:
                st.session_state.won = True
            
            # Check if out of guesses
            if len(st.session_state.guesses) >= 6 and not st.session_state.won:
                st.session_state.game_over = True
            
            st.rerun()

# Reset button
col1, col2, col3 = st.columns([1, 1, 1])

if st.session_state.game_over or st.session_state.won:
    with col2:
        if st.button("Play Again", use_container_width=True):
            st.session_state.word = get_todays_word()
            st.session_state.hint = get_todays_hint()
            st.session_state.guesses = []
            st.session_state.game_over = False
            st.session_state.won = False
            st.session_state.current_guess = ""
            st.session_state.hint_revealed = False
            st.rerun()
