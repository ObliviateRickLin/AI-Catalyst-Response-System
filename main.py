import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from streamlit_option_menu import option_menu as om
from sklearn.preprocessing import *

from sqlcnx import *
from AITF import *
from pages import *

with st.sidebar:
    st.image("./image/cuhksz.png")
    '''
    st.write("    ")
    st.write("    ")
    bt0 = st.button("Introduction of the System", key=0)
    bt1 = st.button("True or False Question", key=1)
    bt2 = st.button("Completion Question", key=2)
    bt3 = st.button("Response Question", key=3)
    bt4 = st.button("Choice Question",  key=4)
    bt5 = st.button("Research Recommendation", key=5)
    bt6 = st.button("View our database", key=6)
    st.write("    ") 
    '''
    selected = om("AI Catalyst System", 
                    ["Introduction", 
                    'True or False Question',
                    'Completion Question',
                    'Response Question',
                    'Choice Question',
                    'Research Recommendation',
                    'View our database'], 
                menu_icon =  "None",
                icons=['house', 'ui-checks','columns','text-indent-right','ui-radios-grid','heptagon-half','eye-fill'], 
                default_index=1)
    st.sidebar.info(
            """
           The model is still under improvement.
           Feel free to contact us at 117010254@link.cuhk.edu.cn.
            """
    )

#st.title("AI Catalyst Response System")
if selected == 'Introduction':
    p0()
elif selected == 'True or False Question':
    p1()
elif selected == 'Research Recommendation':
    p5()
elif selected == 'View our database':
    p6()






