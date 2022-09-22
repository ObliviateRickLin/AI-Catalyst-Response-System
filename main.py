import streamlit as st
import pandas as pd
import numpy as np
import os
import numpy as pd
import joblib
import pandas as pd
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torch import nn
from sklearn.preprocessing import *

from AITF import *

with st.sidebar:
    sc1, sc2 = st.columns((1, 1.5))
    with sc1:
        st.write("")
        st.image("./image/cuhksz.png")
    with sc2:
        st.title("AI Catalyst Response System")
    st.write("    ")
    st.write("    ")
    bt0 = st.button("Introduction of the system", key=0)
    bt1 = st.button("True or False question", key=1)
    bt2 = st.button("Completion question", key=2)
    bt3 = st.button("Response question", key=3)
    bt4 = st.button("Choice question",  key=4)
    st.write("    ")

    st.sidebar.info(
            """
           The model is still under improvement.
           Feel free to contact us at 117010254@link.cuhk.edu.cn.
        """
    )

#st.title("AI Catalyst Response System")
if bt0:
    st.header("AI Catalyst Response System")
    st.write("""
            The development of material science has long faced the problem of uncertainty. 
            Since material science is mostly empirical, large amounts of trials and experiments are needed. 
            Researchers usually have no idea of the performance of a catalyst until it is tested.  
            To solve this problem, we present the AI Catalyst Response System, which consists of four parts based on the question type: 
            True or False question, Choice question, Completion question, and Response question. 
            The system utilizes natural language processing (NLP) and machine learning (ML) to analyze tens of thousands of published papers.  
            """)
elif bt1 or (not bt0):
    st.title("True or False Question")
    st.write("""
            In the True or False question part, we simply categorize the catalysts into groups of “good” and “bad” based on their predicted performance. 
            In this way, we hope to provide some references for researchers before they conduct their experiments and save valuable time and resources.
            """)

    Catalyst = st.text_input("Chemical formula of your catalyst",
        help = "Please enter the chemical formula of your catalyst, such as Ag, Pt3Cu, NiCo2O4, or NiCo2O4@Pt.")
    Reaction = st.selectbox(
        'Applied Reaction',
        ('HER', 'OER', 'ORR'))    
    NanoBulk = st.selectbox(
        'Is your material nano or bulk?',
        ('nano', 'bulk'))  
    if NanoBulk == "bulk":
        Nanostructure = st.selectbox(
            'Nanostructure of your material',
            ('bulk',)) 
    else:  
        Nanostructure = st.selectbox(
            'Nanostructure of your material',
            ('bulk', 'nanoparticles','nanoporous','nanoshell/mesoporous','nanostructures','nanotubes')) 
    Acidity = st.selectbox(
        'Acidity of the environment',
        ('acidic', 'neutral','alkaline')) 

    b1 = st.button("Click the button to see the result")
    sc3, sc4 = st.columns((1,4))
    if b1:
        try:
            predict = AITF(Catalyst,Reaction,NanoBulk,Nanostructure,Acidity)
            #st.write("The performance of this reaction is predicted to be: ",predict)
            sc3.metric("Reaction performance",predict)
            sc4.warning("Please note that the result is for reference only.")
        except:
            sc3.metric("Reaction performance","Null")
            sc4.error("Invalid catalyst: please check your input and try again.")
    else:
        sc3.metric("Reaction performance","Null")
        sc4.warning("Please note that the result is for reference only.")
        #predict_result = model.predict(predict_data)






