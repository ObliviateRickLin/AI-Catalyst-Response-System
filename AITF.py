from transformers import BertTokenizerFast
import pandas as pd
import re
import sys
import json
import re
from numpy import NAN, NaN
import numpy as np
import matplotlib
from pandas import read_excel
import pandas as pd
import pylab as p
from ase.db import connect
from ase.visualize import view
import matplotlib.transforms
import math
from cathub.query import get_reactions
from sklearn.preprocessing import OneHotEncoder
from tools import ordered_metals, get_AB_from_formula, references, site2int, site_labels
from sklearn.ensemble import RandomForestRegressor
import joblib

def is_number(num):
    
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        if "^" in num:
            x=num.split("^")
            for i in x:
                result2=pattern.match(i)
                if result2==False:
                    return False
            return True
        return False


def get_num(i,element,catalyst):
    stopwords="(),!?><∼-[]@;:–&"
    contwords="."
    j=i+len(element)-1
    while True:
        j=j+1
        if j==len(catalyst)-1:
            j += 1
            break
        temp=catalyst[j]
        if temp in contwords:
            continue
        if temp.isupper() or temp in stopwords:
            break

    num=catalyst[i+len(element):j]
    # for s in stopwords:
    #     num=num.replace(s,"")
    if is_number(num)==True:
        return num
    return None


def get_element(element,catalyst, data):
    inds=[m.start() for m in re.finditer(element, catalyst)] #catalyst.findall(element)
    for ind in inds:
        if len(catalyst)==(ind+len(element)):
            data.append(element)
            data.append(1)
            continue
            #return True
        # if ind==0:
        #     #before=catalyst[ind-1]
        #     after=catalyst[ind+len(element)]
        #     if after.isupper() or is_number(after):
        #         return True
        # else:
        #     before=catalyst[ind-1]
        after=catalyst[ind+len(element)]
        # if after.isupper() or is_number(after):
        #     return True
        if after.isupper() or after in "/-":
            data.append(element)
            data.append(1)
        elif after.islower():
            continue
        elif is_number(after):
            num=get_num(ind, element, catalyst)
            data.append(element)
            data.append(num)


    return data
        #return False

def get_compo(data):
        try:
            element_temp=data
            for ii in range(len(element_temp)-1,-1,-1):
                # print(ii)
                # print(element_temp[ii])
                x=element_temp[ii]
                if ii%2==1 and type(element_temp[ii-1])==str:
                    break
                if math.isnan(float(x)): #element_temp[ii] is NaN:
                    element_temp = np.delete(element_temp, ii)
                    #element_temp.drop(ii)
                else:
                    break
            print(element_temp)

            element_dic={element_temp[2*k]:float(element_temp[2*k+1]) for k in range(round(len(element_temp)/2))}
            sorted_element_dic={k:v for k, v in sorted(element_dic.items(),reverse=True, key=lambda item: item[1])}
            metals_dic={}
            nonmetals_dic={}
            for k,v in sorted_element_dic.items():
                if k in ordered_metals:
                    metals_dic[k]=v
                else:
                    nonmetals_dic[k]=v
            if len(metals_dic)>=2:
                A=list(metals_dic.keys())[0]
                A_for=metals_dic[A]
                B=list(metals_dic.keys())[1]
                B_for=metals_dic[B]
            elif len(metals_dic)==0:
                if len(nonmetals_dic)>=2:
                    A=list(nonmetals_dic.keys())[0]
                    A_for=nonmetals_dic[A]
                    B=list(nonmetals_dic.keys())[1]
                    B_for=nonmetals_dic[B]
                elif len(nonmetals_dic)==1:
                    A=list(nonmetals_dic.keys())[0]
                    A_for=nonmetals_dic[A]
                    B=A
                    B_for=A_for
                else:
                    A=None
                    B=None
                    A_for=None
                    B_for=None
            else:
                A=list(metals_dic.keys())[0]
                A_for=metals_dic[A]
                if len(nonmetals_dic)==0:
                    B=A
                    B_for=A_for
                else:
                    B=list(nonmetals_dic.keys())[0]
                    B_for=nonmetals_dic[B]
            return A, A_for, B, B_for
        except:
            return None, None, None, None


element_list = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K",
            "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
            "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I",
            "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
            "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr",
            "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf",
            "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og", "Uue"]


# Organize the elements in terms of their groups
IA=['H','Li','Na','K','Rb','Cs','Fr']
IIA=['Be','Mg','Ca','Sr','Ba']
IIIB=['Sc','Y','La']
IVB=['Ti','Zr','Hf']
VB=['V','Nb','Ta']
VIB=['Cr','Mo','W']
VIIB=['Mn','Tc','Re']
VIII=['Fe','Co','Ni','Ru','Rh','Pd','Os','Ir','Pt']
IB=['Au','Ag','Cu']
IIB=['Zn','Cd','Hg']
IIIA=['B','Al', 'Ga', 'In', 'Tl']
IVA=['C','Si','Ge','Pb','Sn']
VA=['N','P','As','Sb','Bi']
VIA=['O','S','Se','Te']
VIIA=['F','Cl','Br','I']
Groups_list=[IA,IIA,IIIB,IVB,VB,VIB,VIIB,VIII,IB,IIB,IIIA,IVA,VA,VIA,VIIA]
Groups_str=['IA','IIA','IIIB','IVB','VB','VIB','VIIB','VIII','IB','IIB','IIIA','IVA','VA','VIA','VIIA']

Elements=[]
for i in range(1,119):
    f=open("ElementData/%s" %i, "r")
    lines=f.readlines()
    Elements.append(lines[1].split('|')[1].strip())
    f.close

## User Input
# Catalyst=""
# Reaction="" #HER, ORR, OER
# NanoBulk="" #True, False
# Nanostructure=""
# Acidity=""

def AITF(Catalyst,Reaction,NanoBulk,Nanostructure,Acidity):

    data=[]
    splits=["/","@"]
    catalyst=Catalyst

        
    try:    
        substrate="None "
        for s in splits:
            cat_sub=catalyst.split(s)
            if len(cat_sub)==1:
                continue
            else:
                catalyst=cat_sub[0]
                substrate=cat_sub[-1]
        for element in element_list:
            if element in catalyst:

                data=get_element(element, catalyst, data)

        num_cata=len(data)/2

    except Exception as ex:
        print(ex)

        
    # formula = catalyst
    # E = None
    # sites = None
    # facet=None
    # site = None

    predict_data=[]
    A,  A_for, B, B_for = get_compo(data) #A: metal 1, B: metal 2; formula: e.g., A2B3; SB: e.g., L10
    #print([A,B,SB])
    SB=None
    if A ==None:
        print("Invalid input. Please enter the chemical formula.")

    A_num=Elements.index(A)
    B_num=Elements.index(B)


    count=0
    for group in Groups_list:
        if A in group:
            A_group=Groups_str[count]
        if B in group:
            B_group=Groups_str[count]
        count=count+1


    f1=open("ElementData/%s" %(A_num+1), "r")
    lines1=f1.readlines()
    f2=open("ElementData/%s" %(B_num+1), "r")
    lines2=f2.readlines()

    predict_data.append(A)
    predict_data.append(B)
    predict_data.append(lines1[46].split('|')[1].strip())
    predict_data.append(lines2[46].split('|')[1].strip())
    predict_data.append(lines1[3].split('|')[1].strip())
    predict_data.append(lines1[4].split('|')[1].strip("g/cm\n"))
    predict_data.append(lines1[8].split('|')[1].strip("&deg;C\n"))
    predict_data.append(lines1[9].split('|')[1].strip("&deg;C\n"))
    predict_data.append(lines1[14].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines1[15].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines1[16].split('|')[1].strip("J/(kg K)\n"))
    predict_data.append(lines1[19].split('|')[1].strip("W/(m K)\n"))
    predict_data.append(lines1[47].split('|')[1].strip())
    predict_data.append(lines1[35].split('|')[1].strip())
    predict_data.append(lines1[36].split('|')[1].strip())
    predict_data.append(lines1[37].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines1[38].split('|')[1].strip())
    predict_data.append(lines1[7].split('|')[1].strip())
    predict_data.append(lines2[3].split('|')[1].strip())
    predict_data.append(lines2[4].split('|')[1].strip("g/cm\n"))
    predict_data.append(lines2[8].split('|')[1].strip("&deg;C\n"))
    predict_data.append(lines2[9].split('|')[1].strip("&deg;C\n"))
    predict_data.append(lines2[14].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines2[15].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines2[16].split('|')[1].strip("J/(kg K)\n"))
    predict_data.append(lines2[19].split('|')[1].strip("W/(m K)\n"))
    predict_data.append(lines2[47].split('|')[1].strip())
    predict_data.append(lines2[35].split('|')[1].strip())
    predict_data.append(lines2[36].split('|')[1].strip())
    predict_data.append(lines2[37].split('|')[1].strip("kJ/mol\n"))
    predict_data.append(lines2[38].split('|')[1].strip())
    predict_data.append(lines2[7].split('|')[1].strip())
    predict_data.append(A_for) #
    predict_data.append(B_for) #
    predict_data.append(substrate)
    predict_data.append(num_cata)
    predict_data.append(NanoBulk)
    predict_data.append(Nanostructure)
    predict_data.append(Acidity)
    f1.close
    f2.close

    if Reaction == "HER":
        regressor = joblib.load("./model/HER.model") 
        enc = joblib.load("./model/HER_enc.model")
        standard = 80
    elif Reaction == "OER":
        regressor = joblib.load("./model/OER.model")
        enc = joblib.load("./model/OER_enc.model")
        standard = 250
    elif Reaction == "ORR":
        regressor = joblib.load("./model/ORR.model")
        enc = joblib.load("./model/ORR_enc.model") 
        standard = 700
    
    predict_data=pd.DataFrame([predict_data])
    predict_data=enc.transform(predict_data).toarray()

    y_pred=regressor.predict(predict_data)
    if y_pred <= standard:
        return "Good"
    else:
        return "Bad"

    
#test=AITF("Pt2.0Ir3d","HER","nano","nanorod","acidic")
#print(test)