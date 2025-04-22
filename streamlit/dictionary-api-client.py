import streamlit as st
import requests
import urllib3


def lookup(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    api = requests.get(url)
    result = api.json()
    return result


def main():
    http = urllib3.PoolManager()
    
    st.title("Dictionary API")
    
    word = st.text_input("Word")
    if len(word) == 0:
        st.warning("Enter a word")
        return 0
    result = lookup(word)
    
    with st.expander("RAW JSON"):
        st.write(result)
        
    if not isinstance(result, list):
        st.error("The word does not exist")
        return 0
    
    st.header(f"{word}")

    # st.write(result[0]['phonetics'][1]['text'])
    for phonetic in result[0]['phonetics']:
        if 'audio' in phonetic:
            if 'text' in phonetic:
                pronounciation = phonetic['text']
                st.write(f"*{pronounciation}*")
            
            mp3_file = phonetic['audio']
            if len(mp3_file) > 0:
                contents = http.request('GET', mp3_file)
                mp3_data = contents.data

                st.audio(mp3_data, format='audio/mpeg') # MIME TYPE
            
    
    for meaning in result[0]['meanings']:
        st.subheader(f"{meaning['partOfSpeech']}")
        for definition in meaning['definitions']:
            st.write(f"- {definition['definition']}")
            if len(definition['synonyms']) > 0:
                st.write(f"-- Synonyms: {definition['synonyms']}")
            if len(definition['antonyms']) > 0:
                st.write(f"-- Antonyms: {definition['antonyms']}")
            if 'example' in definition and len(definition['example']) > 0:
                st.write(f"> *Example:* {definition['example']}")

    
if __name__ == "__main__":
    main()
    