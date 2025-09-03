import os
import streamlit as st
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Get current directory of app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths for model and tokenizer
MODEL_PATH = os.path.join(BASE_DIR, "next_word_lstm.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pickle")

# Load Model
model = load_model(MODEL_PATH)

# Load Tokenizer
with open(TOKENIZER_PATH, "rb") as handle:
    tokenizer = pickle.load(handle)


# Function to predict the next word
def predict_next_word(model, tokenizer, text, max_sequence_len):
    token_list = tokenizer.texts_to_sequences([text])[0]
    if len(token_list) >= max_sequence_len:
        token_list = token_list[-(max_sequence_len-1):]  # Ensure the sequence length matches max_sequence_len
    
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding="pre")
    predicted = model.predict(token_list, verbose=0)
    predicted_word_index = np.argmax(predicted, axis=1)[0]  # <-- FIXED: Get scalar index
    
    for word, index in tokenizer.word_index.items():
        if index == predicted_word_index:
            return word
    return None

# Streamlit app 
st.title("Next Word Prediction with LSTM and Early Stopping")
input_text = st.text_input("Enter the sequence of Words", "To be or not to")

if st.button("Predict Next Word"):
    max_sequence_len = model.input_shape[1] + 1
    next_word = predict_next_word(model, tokenizer, input_text, max_sequence_len)
    st.write(f"**Next word:** {next_word if next_word else 'Not found'}")

