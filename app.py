import streamlit as st
from azure_openai import Sentence_Segmentor
import pandas as pd
import numpy as np

def sentence_segmentation():
    if input_text != "":
        segmentor = Sentence_Segmentor()
        responce = segmentor.get_responce(input_text=input_text)
        if responce != False:
            st.divider()
            st.write("**Disclaimer :**", responce['Disclaimer'])

            st.subheader("Description")
            st.write(responce['Short Description'])
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Input Sentences")
                for i in range(len(responce['Input Sentences'])):
                    st.write(i+1,' :',responce['Input Sentences'][i])

            with col2:
                st.subheader("Logical Segments")
                for i in range(len(responce["Logocal broken sentences"])):
                    st.write(i+1," :", responce['Logical broken sentences'][i])
            
        return responce
    
    elif input_text=="":
        pass
    else:
        st.write("Something went wrong ! ! ! !")


st.markdown("<h1 style='text-align:center; color:orange;'>Text Ease</h1>", unsafe_allow_html=True)
domain = ''
input_text = st.text_area(label="Enter the text here", height=200, value='')
btn_simplify = st.button(label="Simplify Text", type='primary')
if btn_simplify:
    sentence_segmentation()

