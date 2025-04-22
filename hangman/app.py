import streamlit as st
import requests

def random_word():
    url = "https://random-word-api.herokuapp.com/word"
    req = requests.get(url)
    if req.status_code == requests.codes.ok: # 200
        result = req.json()
        return result[0]
        # return "hello"
    return None

def main():
    st.title(":female-detective: Hangman")
    st.write("___")

    if "word" not in st.session_state:
        word = random_word()
        st.session_state["word"] = word
        st.session_state["correct_letters"] = []
        st.session_state["incorrect_letters"] = []
    else:
        word = st.session_state["word"]

    pl_word = st.empty()
    # st.write(word)
    st.write("___")

    col1, col2 = st.columns(2)
    letter = col1.text_input("Enter your character", value="", max_chars=1).lower()
    pl_hangman = col2.empty()

    if letter in word:
        col1.success("Yup!")
        st.session_state["correct_letters"].append(letter)
    else:
        col1.error("Wrong!")
        st.session_state["incorrect_letters"].append(letter)

    guess_word = ""
    missing_letters = len(word)
    for chr in word:
        if chr in st.session_state["correct_letters"]:
            guess_word += chr + " "
            missing_letters -= 1
        else:
            guess_word += " \_ "

    no_incorrect = len(st.session_state['incorrect_letters'])
    pl_hangman.image(f"images/hangman_{no_incorrect}.png")
    pl_word.header(guess_word)

    if no_incorrect == 7:
        st.error(f"Game Over! The word was **{word}**")
    if missing_letters == 0:
        # del st.session_state["word"]
        st.balloons()
    
if __name__ == "__main__":
    main()
    