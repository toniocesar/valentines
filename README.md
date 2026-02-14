# Wordle Game - Streamlit App

A fun Python-based Wordle game built with Streamlit that loads a different word for each day of the year.

## Features

- 🎮 **Classic Wordle Gameplay** - 6 attempts to guess the 5-letter word
- 📅 **Daily Words** - A unique word for each day of the year loaded from CSV
- 🎨 **Visual Feedback** - Color-coded tiles:
  - 🟩 Green: Correct letter in correct position
  - 🟨 Yellow: Correct letter in wrong position
  - ⬜ Gray: Letter not in the word
- 📊 **Game Stats** - Track your guesses and wins
- 🔄 **Play Again** - Resume with a new word when game ends

## Installation

1. Install the required dependencies:
```bash
pip install streamlit pandas
```

2. Ensure you have the following files in your project directory:
   - `app.py` - The main Streamlit application
   - `words.csv` - CSV file with dates and 5-letter words

## Running the App

```bash
streamlit run app.py
```

The app will open in your default browser. You can also access it at `http://localhost:8501` if needed.

## CSV Format

The `words.csv` file should have two columns:
- `date`: Format YYYY-MM-DD (e.g., 2026-02-14)
- `word`: A 5-letter word (e.g., THEME)

```csv
date,word
2026-02-14,THEME
2026-02-15,THERE
```

## How to Play

1. Start the app and you'll see today's Wordle puzzle
2. Type a 5-letter word and press Submit
3. The tiles will show you feedback for each letter:
   - Green: Correct position
   - Yellow: In word but wrong position
   - Gray: Not in the word
4. You have 6 guesses to find the word
5. Win by guessing the word correctly, or see the answer when you run out of guesses

## Features

- Words are stored in `words.csv` with one entry per date
- The current day's word is automatically loaded based on your system date
- Game state is saved during your session in Streamlit's session state
- Responsive design works on desktop and mobile browsers