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
    result = lookup(word)
    
    st.subheader(f"{word} {result[0]['phonetics'][1]['text']}")

    # st.write(result[0]['phonetics'][1]['text'])
    for phonetic in result[0]['phonetics']:
        if 'audio' in phonetic:
            mp3_file = phonetic['audio']
                        
#             contents = http.request('GET', mp3_file, host='api.dictionaryapi.dev')
#             mp3_data = contents.data

#             st.audio(mp3_data, format='audio/mpeg') # MIME TYPE
            
    
    for meaning in result[0]['meanings']:
        st.write(f"**{meaning['partOfSpeech']}**")
        for definition in meaning['definitions']:
            st.write("- " + definition['definition'])
    
if __name__ == "__main__":
    main()
    