import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from sklearn.preprocessing import *

from sqlcnx import *
from AITF import *

def on_active(key):
    st.session_state[key] = True
    return

def p0():
    st.title("AI Catalyst Response System")
    st.tabs(["AI Catalyst Response System", ">>","Introduction"])
    st.write("""
            The development of material science has long faced the problem of uncertainty. 
            Since material science is mostly empirical, large amounts of trials and experiments are needed. 
            Researchers usually have no idea of the performance of a catalyst until it is tested.  
            To solve this problem, we present the AI Catalyst Response System, which consists of four parts based on the question type: 
            True or False question, Choice question, Completion question, and Response question. 
            The system utilizes natural language processing (NLP) and machine learning (ML) to analyze tens of thousands of published papers.  
            """)
    
    return

def p1():
    st.title("True or False Question")
    st.tabs(["AI Catalyst Response System", ">>","True or False Question"])
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
            ('bulk', 'nanoarray','nanobar','nanocluster','nanofiber','nanofilm',
            'nanopolyhedron','nanoporous','nanoribbon','nanorod','nanosheet','nanosphere',
            'nanovesicle','nanotube','others')) 
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
    
    return

def p2():
    st.title("Completion question")
    st.tabs(["AI Catalyst Response System", ">>","Completion question"])
    st.write("In this part, we will output the most suited reaction or catalyst based on your input.")
    st.selectbox("Input datatype",["Catalyst","Reaction"])
    st.text_area("Output suggestions")
    return 

def p3():
    st.title("Response question")
    st.write("In the response question, we want to explain any question that a catalyst research may encounter.")
    st.text_input("Input the question")
    st.button("Result")
    st.text_area("Result provided")
    st.text_area("Result related")

def p4():
    st.title("Choice Question")
    st.tabs(["AI Catalyst Response System", ">>","Choice Question"])
    st.write("In the choice question, we wish to select the best catalyst for a given reaction among the given candidates.")
    st.button("Add Catalyst")
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
            ('bulk', 'nanoarray','nanobar','nanocluster','nanofiber','nanofilm',
            'nanopolyhedron','nanoporous','nanoribbon','nanorod','nanosheet','nanosphere',
            'nanovesicle','nanotube','others')) 
    Acidity = st.selectbox(
        'Acidity of the environment',
        ('acidic', 'neutral','alkaline'))     
    st.button("Go")
    st.write("Result")
    return

def p5():
    st.title("Research Recommendation")
    st.tabs(["AI Catalyst Response System", ">>","Research Recommendation"])
    st.file_uploader("Upload a txt file")
    sc1, sc2, sc3, sc4, sc5 = st.columns((1,1,1,1,1))
    sc1.metric("Overall Rating", 9.5, delta="13%")
    sc2.metric("Material", 8.1, delta="7%" )
    sc3.metric("Method", 9.2, delta="11%")
    sc4.metric("Application", 9.1, delta="9%")
    sc5.metric("Characterization", 5.9, delta="-7%", delta_color="normal")
    st.text_area(label="Improvement Points", 
                value= '''
                It’s compulsory to demonstrate personal ideas and ways to investigate, 
                solve a specific issue, or develop strategies to expand the scope of examinations. 
                A chemistry research proposal is an extremely important paper 
                that promotes a student’s candidacy when applying to the advanced course. 
                To succeed in the application process to the chemistry PhD program, 
                a student should do their best to impress the admission committee 
                and persuade it of their high competence level in the chemistry area.
                ''', 
                height=300)
    return

def p6():
    st.title("View our database")
    st.tabs(["AI Catalyst Response System", ">>","View our database"])
    st.header("1. Retrieve Papers")
    doi = st.text_input(label="Seach by DOI",value="https://doi.org/10.1016/j.chs.2003.09.018")
    title, year, journal, abstract = retrieve_paper_info(doi)
    st.subheader(title)
    sc1, sc2 = st.columns((1,2.8))
    sc2.text_area("Abstract", value=abstract,height=130)
    sc1.metric("Journal", value= journal)
    sc1.metric("Year", value= year)
    df_paper = count_paper()
    df_journal = count_journal()
    df_paper_journal = count_journal_paper()
    st.write("   ")
    st.write("   ")
    st.write("   ")
    
    st.header("2. Visualize Database")
    sc1, sc2 = st.columns((3,1))
    sc2.bar_chart(df_journal, x="journal", height=280)
    sc2.area_chart(df_paper, x="year", height=140)
    sc1.line_chart(df_paper_journal,height=450)
    #st.table(df_paper_journal)
    return 
