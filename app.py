##########################################################################
#libraries & packages
import streamlit as st
import pandas as pd
import re
import numpy as np
import PyPDF2
##########################################################################
import pathlib
try:
    from bs4 import BeautifulSoup
except :
    from BeautifulSoup import BeautifulSoup 
import logging
import shutil

from bs4 import BeautifulSoup
import pathlib
import shutil
import streamlit as st

def inject_ga():
    GA_ID = "google_analytics"

    # Note: Please replace the id from G-XXXXXXXXXX to whatever your
    # web application's id is. You will find this in your Google Analytics account
    
    GA_JS = """
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-3XHJ5EL5Q5"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-3XHJ5EL5Q5');
    </script>
    """

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID):  # if cannot find tag
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


inject_ga()
##########################################################################
#function
def clean(text):
    text = re.sub('[^a-zA-Z]+', ' ', text)
    text = text.replace('\n',' ')
    text = re.split(' ', text)
    text = [x.lower() for x in text]
    return text

badword_idn = open('dataset/indonesia.csv','r')
badword_eng = open('dataset/english.csv','r')
badword_id_en = open('dataset/eng_in.csv','r')
badword_idn = list(badword_idn)
badword_eng = list(badword_eng)
badword_id_en = list(badword_id_en)

bad_words_idn= []
for w in badword_idn:
    bad_words_idn.append(re.sub(r'\n','',w))
bad_words_eng= []
for w in badword_eng:
    bad_words_eng.append(re.sub(r'\n','',w))
all_badwords = []
for w in badword_id_en:
    all_badwords.append(re.sub(r'\n','',w))

bad_words =[]
def find_bad_words(review,finded,bad_words):
    target_word = bad_words
    count = 0
    finded = []
    for t in target_word:
        if t in review != -1:
            finded.append(t)
    finded = [*set(finded)]
    return finded

##########################################################################
# sidebar
st.sidebar.image(
    "https://www.indiewire.com/wp-content/uploads/2014/03/bad-words.jpg?w=680",
    width = 300
)
st.sidebar.title("Hi there, Welcome 👋")
st.sidebar.caption("""
            Want to know if a sentence or text file contains bad words quickly? Let's find out here!
            We will help you with pleasure. Hope you guys enjoy your time here 😄
            """)
page = st.sidebar.selectbox("Menu",("Badwords in Sentences","Badwords in Text File"))
st.sidebar.caption(" ")
st.sidebar.caption("Creator : Annida Nur Islami [(LinkedIn)](https://www.linkedin.com/in/annida-nur-islami-a23694214/)")
##########################################################################
#page1
if page == "Badwords in Sentences":
    st.title(f"{page} Menu")
    language = ("Indonesia","English","Mix (Indonesian-English)")
    language = st.selectbox("What language is used in the sentences ?", language)
    text = st.text_area('Write down what the sentences is about')
    ok = st.button("Go")
    
    if ok :
        if language == 'Indonesia':
            bad_words = bad_words_idn
        elif language == 'English':
            bad_words = bad_words_eng
        else :
            bad_words = all_badwords
            
        finded = []
        text = clean(text)
        find = find_bad_words(text,finded,bad_words)
        df = pd.DataFrame(find,columns=['Bad Words Found'])
        
        if len(find)==0 :
            st.subheader("The Sentences doesn't contain any badwords ✅✅")
        else :
            st.subheader("The Sentences  contains any badwords ❗❗❗❗")
            st.subheader("Check what we have found 👇👇")
            
            st.dataframe(df)
            
##########################################################################
#page2  
else :
    st.title(f"{page} Menu")
    language = ("Indonesia","English","Mix (Indonesian-English)")
    language = st.selectbox("What language is used in the file ?", language)
    upload_file = st.file_uploader("Upload Your Text File", type = ['txt'])
    ok = st.button("Go")
    
    if ok:
        if language == 'Indonesia':
            bad_words = bad_words_idn
        elif language == 'English':
            bad_words = bad_words_eng
        else :
            bad_words = all_badwords
            
        if upload_file:
            file_name = upload_file.name
            file_name = file_name.split(".",1)
            file_extension = file_name[1]
            st.write(file_extension)
            
            sentences = []
            for line in upload_file:
                line = line.decode()
                sentences.append(line)
            text = ' '.join(map(str, sentences))
            st.subheader("Text of The File 📜")
            with st.expander(upload_file.name, expanded=False):
                st.write(text)

            finded = []
            text = clean(text)
            find = find_bad_words(text,finded,bad_words)
            df = pd.DataFrame(find,columns=['Bad Words Found'])

            if len(find)==0 :
                st.subheader("The File doesn't contain any badwords ✅✅")
            else :
                st.subheader("The File  contains any badwords ❗❗❗❗")
                st.subheader("Check what we have found 👇👇")
                st.dataframe(df)
