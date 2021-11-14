#ZENATI Mohamed TP 2

from re import A, L, S
from numpy.core import numeric
import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
from streamlit.elements.color_picker import ColorPickerMixin
import plotly_express as px
import plotly.graph_objects as go
import seaborn as sns
import time
import os
import streamlit.components.v1 as components
from bokeh.plotting import figure
from streamlit.state.session_state import Value
import altair as alt
import random

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Momobillier",page_icon="🔑",layout="wide", initial_sidebar_state="auto")
st.title("Projet Mohamed ZENATI")
def run_the_app():
    @st.cache
    def load_metadata(url):
        return pd.read_csv(url)

placeholder = st.empty()

def timer(func):
    def wrapper(*args,**kwargs):
        
        with open("décorateur.txt","a") as f:
            before=time.time()
            timestamp=datetime.datetime.now()
            val=func(*args,**kwargs)
            f.write("Function "+ func.__name__ +" started at "+ str(timestamp)+" and took: "+str(time.time()-before)+" seconds to execute\n")
        return val
    return wrapper
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("Sélectionnez votre DataSet !")
app_mode = st.sidebar.selectbox("",
        ["Accueil","2016", "2017", "2018", "2019", "2020","Evolution"])
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

n = 100
df20 = pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/projet/2020.csv", sep=',', error_bad_lines=False,header=0, skiprows=lambda i: i % n != 0, low_memory=False)
df20['date_mutation']=pd.to_datetime(df20["date_mutation"])
df19 = pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/projet/2019.csv", sep=',', error_bad_lines=False,header=0, skiprows=lambda i: i % n != 0, low_memory=False)
df19['date_mutation']=pd.to_datetime(df19["date_mutation"])
df18 = pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/projet/2018.csv", sep=',', error_bad_lines=False,header=0, skiprows=lambda i: i % n != 0, low_memory=False)
df18['date_mutation']=pd.to_datetime(df18["date_mutation"])
df17 = pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/projet/2017.csv", sep=',', error_bad_lines=False,header=0, skiprows=lambda i: i % n != 0, low_memory=False)
df17['date_mutation']=pd.to_datetime(df17["date_mutation"])
df16 = pd.read_csv("C:/Users/zmoha/OneDrive/Bureau/Data VIZ/LAB2/st_app/projet/2016.csv", sep=',', error_bad_lines=False,header=0, skiprows=lambda i: i % n != 0, low_memory=False)
df16['date_mutation']=pd.to_datetime(df16["date_mutation"])

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
@timer
def supression(df):
        df.drop(df.loc[df['code_departement']=='2A'].index, inplace=True)
        df.drop(df.loc[df['code_departement']=='2B'].index, inplace=True)
supression(df20)
supression(df19)
supression(df18)
supression(df17)
supression(df16)

@timer
def get_dom(dt):
    return dt.day

@timer
def get_month(dt):
    return dt.month

@timer
def datetime_(df):
        df['Date/Time']=pd.to_datetime(df['date_mutation'])
        df['month'] = df['Date/Time'].map(get_month)
datetime_(df20)
datetime_(df19)
datetime_(df18)
datetime_(df17)
datetime_(df16)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------


df20.rename(columns={'valeur_fonciere':'valeur_fonciere_en_2020'},inplace=True)
df19.rename(columns={'valeur_fonciere':'valeur_fonciere_en_2019'},inplace=True)
df18.rename(columns={'valeur_fonciere':'valeur_fonciere_en_2018'},inplace=True)
df17.rename(columns={'valeur_fonciere':'valeur_fonciere_en_2017'},inplace=True)
df16.rename(columns={'valeur_fonciere':'valeur_fonciere_en_2016'},inplace=True)


df20['month']=df20['date_mutation'].map(get_month)
df19['month']=df19['date_mutation'].map(get_month)
df18['month']=df18['date_mutation'].map(get_month)
df17['month']=df17['date_mutation'].map(get_month)
df16['month']=df16['date_mutation'].map(get_month)



moy_valeur_fonciere_2020=df20.groupby('month').valeur_fonciere_en_2020.mean()
moy_valeur_fonciere_2019=df19.groupby('month').valeur_fonciere_en_2019.mean()
moy_valeur_fonciere_2018=df18.groupby('month').valeur_fonciere_en_2018.mean()
moy_valeur_fonciere_2017=df17.groupby('month').valeur_fonciere_en_2017.mean()
moy_valeur_fonciere_2016=df16.groupby('month').valeur_fonciere_en_2016.mean()


@st.cache(suppress_st_warning=True)
def linechart(df,dropdown):
    if len(dropdown)>0:
        if '2020' in dropdown:
            df = pd.concat([df,moy_valeur_fonciere_2020],axis=1)
        if '2019' in dropdown:
            df = pd.concat([df,moy_valeur_fonciere_2019],axis=1)
        if '2018' in dropdown:
            df = pd.concat([df,moy_valeur_fonciere_2018],axis=1)
        if '2017' in dropdown:
            df = pd.concat([df,moy_valeur_fonciere_2017],axis=1)
        if '2016' in dropdown:
            df = pd.concat([df,moy_valeur_fonciere_2016],axis=1)
    st.bar_chart(df) 
    st.line_chart(df)
    st.table(df)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
@timer
def type(df):
        df["code_departement"] = df["code_departement"].astype(str).astype(int)
        df["nature_culture"] = df["nature_culture"].astype(str)
        df["type_local"] = df["type_local"].astype(str)
        df["nature_mutation"] = df["nature_mutation"].astype(str)
type(df20)
type(df19)
type(df18)
type(df17)
type(df16)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
@timer
def map(df):
    map_france=df
    map_france.dropna(subset = ["latitude"], inplace=True)
    map_france.dropna(subset = ["longitude"], inplace=True)
    mois = st.slider('Selectionner un mois afin de voir les mobiliés présent à cette période', 1, 12,1) 
    map_france_mois = map_france[map_france["month"] == mois] 
    st.map(map_france_mois,zoom=2)

@st.cache(suppress_st_warning=True)
def table20():
        st.subheader('Voici un tableau présentant les informations avec laquelle la page 2020 a été créé')
        tableau_coloree = go.Figure(data=go.Table(
                header=dict(values=list(df20[['code_departement','latitude','longitude',
                'valeur_fonciere_en_2020','nature_culture','type_local']].columns),
                        fill_color='#e40303',
                        align='center'),
                cells=dict(values=[df20.code_departement,df20.latitude,
                df20.longitude,df20.valeur_fonciere_en_2020,df20.nature_culture,df20.type_local],
                        fill_color='#000105',
                        align='left')))
        st.write(tableau_coloree)
    
@st.cache(suppress_st_warning=True)
def table19():
        st.subheader('Voici un tableau présentant les informations avec laquelle la page 2019 a été créé')
        tableau_coloree = go.Figure(data=go.Table(
                header=dict(values=list(df19[['code_departement','latitude','longitude',
                'valeur_fonciere_en_2019','nature_culture','type_local']].columns),
                        fill_color='#e40303',
                        align='center'),
                cells=dict(values=[df19.code_departement,df19.latitude,
                df19.longitude,df19.valeur_fonciere_en_2019,df19.nature_culture,df19.type_local],
                        fill_color='#000105',
                        align='left')))             
        st.write(tableau_coloree)   
        
@st.cache(suppress_st_warning=True)        
def table18():
        st.subheader('Voici un tableau présentant toute les informations avec laquelle la page 2018 a été créé')
        tableau_coloree = go.Figure(data=go.Table(
                header=dict(values=list(df18[['code_departement','latitude','longitude',
                'valeur_fonciere_en_2018','nature_culture','type_local']].columns),
                        fill_color='#e40303',
                        align='center'),
                cells=dict(values=[df18.code_departement,df18.latitude,
                df18.longitude,df18.valeur_fonciere_en_2018,df18.nature_culture,df18.type_local],
                        fill_color='#000105',
                        align='left')))                
        st.write(tableau_coloree)
        
@st.cache(suppress_st_warning=True)        
def table17():
        st.subheader('Voici un tableau présentant toute les informations avec laquelle la page 2017 a été créé')
        tableau_coloree = go.Figure(data=go.Table(
                header=dict(values=list(df17[['code_departement','latitude','longitude',
                'valeur_fonciere_en_2017','nature_culture','type_local']].columns),
                        fill_color='#e40303',
                        align='center'),
                cells=dict(values=[df17.code_departement,df17.latitude,
                df17.longitude,df17.valeur_fonciere_en_2017,df17.nature_culture,df17.type_local],
                        fill_color='#000105',
                        align='left')))  
        st.write(tableau_coloree)

@st.cache(suppress_st_warning=True)        
def table16():
        st.subheader('Voici un tableau présentant toute les informations avec laquelle 2016 a été créé')
        tableau_coloree = go.Figure(data=go.Table(
                header=dict(values=list(df16[['code_departement','latitude','longitude',
                'valeur_fonciere_en_2016','nature_culture','type_local']].columns),
                        fill_color='#e40303',
                        align='center'),
                cells=dict(values=[df16.code_departement,df16.latitude,
                df16.longitude,df16.valeur_fonciere_en_2016,df16.nature_culture,df16.type_local],
                        fill_color='#000105',
                        align='left')))  
        st.write(tableau_coloree)

        
@st.cache(suppress_st_warning=True)
def chart_pie(df):
        df_type = df.groupby("type_local")
        x=[]
        for a,b in df_type:
                x.append(b.shape[0])
        x.pop(0)
        labels = 'Appartement', 'Maison'
        explode = (0,0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(x, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=100)
        ax1.axis('equal')  
        st.pyplot(fig1)
 

@st.cache(suppress_st_warning=True)
def bar_chart(df):
        
        st.subheader('Nombre de maisons, appartements, locaux et dépendances présent dans toute la France : ')
        a = pd.DataFrame(df['type_local'].value_counts())

        st.bar_chart(a)

        st.subheader('Nombre de culture présent dans toute la France :') 
        b = pd.DataFrame(df['nature_culture'].value_counts())

        st.bar_chart(b)

@st.cache(suppress_st_warning=True)
def nuage_de_point(df):
        fig, ax = plt.subplots()
        plt.plot(df.type_local, df.nature_culture, '.', ms = 2, alpha = .5, color = 'y')
        plt.xticks(rotation=45)
        st.pyplot(fig)

@st.cache(suppress_st_warning=True)
def DateFonciere(df,x,y):
        df_date_fonciere = df.groupby('date_mutation').mean()
        df['date_mutation'] = pd.to_datetime(df['date_mutation'])
        figure = px.bar(df_date_fonciere,x,y)
        st.plotly_chart(figure)

@st.cache(suppress_st_warning=True)
def moisfonciere(df):
        fig1, ax1 = plt.subplots()
        ax1.hist(df.nature_mutation, bins = 30)
        plt.xlabel('nature_mutation')
        plt.ylabel('Frequency')
        st.pyplot(fig1)

@st.cache(suppress_st_warning=True)
def ValeurFoncièreParMois(df,h):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.bar(df['month'],df[h],color='purple')
        ax.set(xlabel="Mois de l'annèe cette année", ylabel="Somme valeur foncière", title="Somme total des valeurs foncières pour chaque mois")
        plt.setp(ax.get_xticklabels(), rotation=45)
        df.mean()
        plt.show()
        st.pyplot(fig)

@st.cache(suppress_st_warning=True)
def NombreVente(df): 
        group=df.groupby('nature_mutation').count()
        NBRventeFig = px.bar(group, x=group.index, y='date_mutation',color='date_mutation', labels = {'date_mutation' : 'nombre de vente total pour cette année !'})
        st.plotly_chart(NBRventeFig)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache(suppress_st_warning=True)
def mapDPT(df,département):
        map_dpt = df.mask(df["code_departement"]!=département)   
        map_dpt.dropna(subset = ["latitude"], inplace = True)
        map_dpt.dropna(subset = ["longitude"], inplace = True)
        st.map(map_dpt)

@st.cache(suppress_st_warning=True)
def map_des_aptm_DPT(df,département):
        st.header("Map des appartements dans tout paris!")
        map_apt = df.mask(df["code_departement"]!=département)
        map_apt = map_apt.mask(df["type_local"]!="Appartement")
        map_apt.dropna(subset = ["latitude"], inplace = True)
        map_apt.dropna(subset = ["longitude"], inplace = True)
        st.map(map_apt)


@st.cache(suppress_st_warning=True)
def map_des_maisons_DPT(df,département):
        st.header("Map des maisons dans tout paris!")
        map_maison = df.mask(df["code_departement"]!=département)
        map_maison = map_maison.mask(df["type_local"]!="Maison")
        map_maison.dropna(subset = ["latitude"], inplace = True)
        map_maison.dropna(subset = ["longitude"], inplace = True)
        st.map(map_maison)

@st.cache(suppress_st_warning=True)
def map_des_dépendances_DPT(df,département):
        st.header("Map des dépendances dans tout paris!")
        map_dépendances = df.mask(df["code_departement"]!=département)
        map_dépendances = map_dépendances.mask(df["type_local"]!="Dépendance")
        map_dépendances.dropna(subset = ["latitude"], inplace = True)
        map_dépendances.dropna(subset = ["longitude"], inplace = True)
        st.map(map_dépendances)

def map_des_locaux_DPT(df,département):
        st.header("Map des locaux dans tout Marseille !")
        map_locaux = df.mask(df["code_departement"]!=département)
        map_locaux = map_locaux.mask(df["type_local"]!="Local industriel. commercial ou assimilé")
        map_locaux.dropna(subset = ["latitude"], inplace = True)
        map_locaux.dropna(subset = ["longitude"], inplace = True)
        st.map(map_locaux)



@st.cache(suppress_st_warning=True)
def DateFonciere_DPT(df,département,x,y):
        date_fonciere0 = df.mask(df["code_departement"]!=département)
        date_fonciere = date_fonciere0.groupby('date_mutation').mean()
        df['date_mutation'] = pd.to_datetime(df['date_mutation'])
        fig2 = px.bar(date_fonciere,x,y)
        st.plotly_chart(fig2)

@st.cache(suppress_st_warning=True)
def NombreVente_DPT(df,département):
        group = df.mask(df["code_departement"]!=département)
        group=df.groupby('nature_mutation').count()
        fig2 = px.bar(group, x=group.index, y='date_mutation',color='date_mutation')
        st.plotly_chart(fig2)

@st.cache(suppress_st_warning=True)
def graph_bar_DPT(df,abs, ord,bar_dpt,département):
        bar_dpt = df.mask(df["code_departement"]!=département)
        bar_dpt=alt.Chart(bar_dpt).mark_bar().encode(x = abs, y = ord)
        bar_dpt

@st.cache(suppress_st_warning=True)
def bar_chart_DPT(df,département):
        chart_dpt = df.mask(df["code_departement"]!=département)
        chart_dpt = pd.DataFrame(df['type_local'].value_counts())
        plt.plot(df.type_local, df.nature_culture, '.', ms = 2, alpha = .5, color = 'y')
        st.bar_chart(chart_dpt)

@st.cache(suppress_st_warning=True)
def nuage_point(df,département,type_local_selectionner,x,y,V_F):
        df1 = df.mask(df["code_departement"]!=département)  
        df4 = df1.mask(df["type_local"]!=type_local_selectionner)
        df4 = df1.mask(df1[V_F]>100000)
        df4 = df1.mask(df1["surface_reelle_bati"]>100)
        df4.plot.scatter( x,y, marker = 'o',c = 'red')
        
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

@st.cache(suppress_st_warning=True)
def radar_chart(df,département):  
        df = pd.DataFrame(dict(
        r=[random.randint(0,10000),
        random.randint(0,10000),
        random.randint(0,10000),],
        theta=['Appartement', 'Dépendance','Maison']))
        df = df.sample(1000000, replace=True)
        
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        placeholder.write(fig)
            
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


if app_mode == "Accueil":
        
        st.title("Page d'accueil")
        st.header("Bienvenue sur mon site où vous pourrez retrouver un tas d'information sur l'immobilier et son évolution au cours des ces dernières années en France ! 📈")
        components.html("""
<link href="https://unpkg.com/tailwindcss@%5E2/dist/tailwind.min.css" rel="stylesheet">
<div class="max-w-sm rounded overflow-hidden shadow-lg mx-auto my-8">
    <img class="w-full" src="https://b2c.iselection.com/wp-content/uploads/sites/8/2017/02/prix-immobilier-neuf-2017.jpg.webp" alt="Sunset in the mountains">
    <div class="px-6 py-4">
    </div>
    <div class="px-6 py-4">
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-black-600 mr-2">Paris</span>
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-black-600 mr-2">Marseille</span>
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-black-600 mr-2">Lyon</span>
    </div>
  </div>
      </div>
    """,
    height=600,
)
        st.write("En plus de trouver des informations sur l'immobilier dans toute la France, vous trouverez des informations plus précise sur les villes cité ci-dessus ! :)")
        st.sidebar.success('')

if app_mode == "2016":
        app_mode2 = st.sidebar.radio('', ['France entière 🥖','Paris 🗼' ,'Marseille 🌞','Lyon 🦁'])
        if app_mode2 == 'France entière 🥖':

                

                app_mode4 = st.selectbox("",
        ["Proportion des maisons, appartements, locaux et dépendances","Tableau présentant les données avec lesquels cette page a été faite",
         "Evolution de la valeur foncière par mois !","Nombre de transaction effectué","Quantité pour chacun des cultures","Origine des cultures pour chaque mobilier"
         ,"Carte de la France pour chaque transaction par mois"]) 
                if app_mode4 =="Proportion des maisons, appartements, locaux et dépendances":
                        chart_pie(df16)
                if app_mode4 =="Tableau présentant les données avec lesquels cette page a été faite":
                        table16()
                if app_mode4 =="Evolution de la valeur foncière par mois !":
                        DateFonciere(df16,'month','valeur_fonciere_en_2016')
                        ValeurFoncièreParMois(df16,'valeur_fonciere_en_2016')
                if app_mode4 =="Nombre de transaction effectué":
                        NombreVente(df16)
                if app_mode4 =="Quantité pour chacun des cultures":
                        bar_chart(df16)
                if app_mode4 =="Origine des cultures pour chaque mobilier":
                        nuage_de_point(df16)
                if app_mode4 =="Carte de la France pour chaque transaction par mois":
                        map(df16)
                                
                
                st.sidebar.info('Vue global sur la France')


        if app_mode2 == 'Paris 🗼':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout":
                        
                        mapDPT(df16,75)

                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df16,75)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df16,75)

                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df16,75)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df16,75)

                radar_chart(df16,75)

                NombreVente_DPT(df16,75)
                DateFonciere_DPT(df16,75,'month','valeur_fonciere_en_2016')
                nuage_point(df16,75,'Maison','surface_reelle_bati','valeur_fonciere_en_2016','valeur_fonciere_en_2016')

                st.sidebar.info('Information sur Paris')




        if app_mode2 == 'Lyon 🦁':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df16,69)  
                                      
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df16,69)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df16,69)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df16,69)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df16,69)

                
                radar_chart(df16,69)

                NombreVente_DPT(df16,69)
                DateFonciere_DPT(df16,69,'month','valeur_fonciere_en_2016')
                nuage_point(df16,69,'Maison','surface_reelle_bati','valeur_fonciere_en_2016','valeur_fonciere_en_2016')
                
                st.sidebar.info('Information sur Lyon')

        if app_mode2 == 'Marseille 🌞':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df16,13)                
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df16,13)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df16,13)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df16,13)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df16,13)
                        
                radar_chart(df16,13)

                DateFonciere_DPT(df16,13,'month','valeur_fonciere_en_2016')
                NombreVente_DPT(df16,13)
                nuage_point(df16,13,'Maison','surface_reelle_bati','valeur_fonciere_en_2016','valeur_fonciere_en_2016')
        
        st.sidebar.success('')

if app_mode == "2017":
        
        
        app_mode2 = st.sidebar.radio('', ['France entière 🥖','Paris 🗼' ,'Marseille 🌞','Lyon 🦁'])

        if app_mode2 == 'France entière 🥖':

                

                app_mode4 = st.selectbox("",
        ["Proportion des maisons, appartements, locaux et dépendances","Tableau présentant les données avec lesquels cette page a été faite",
         "Evolution de la valeur foncière par mois !","Nombre de transaction effectué","Quantité pour chacun des cultures","Origine des cultures pour chaque mobilier"
         ,"Carte de la France pour chaque transaction par mois"]) 
                if app_mode4 =="Proportion des maisons, appartements, locaux et dépendances":
                        chart_pie(df17)
                if app_mode4 =="Tableau présentant les données avec lesquels cette page a été faite":
                        table17()
                if app_mode4 =="Evolution de la valeur foncière par mois !":
                        DateFonciere(df17,'month','valeur_fonciere_en_2017')
                        ValeurFoncièreParMois(df17,'valeur_fonciere_en_2017')
                if app_mode4 =="Nombre de transaction effectué":
                        NombreVente(df17)
                if app_mode4 =="Quantité pour chacun des cultures":
                        bar_chart(df17)
                if app_mode4 =="Origine des cultures pour chaque mobilier":
                        nuage_de_point(df17)        
                if app_mode4 =="Carte de la France pour chaque transaction par mois":
                        map(df17)
 
                
                st.sidebar.info('Vue global sur la France')


        if app_mode2 == 'Paris 🗼':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout":
                        
                        mapDPT(df17,75)

                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df17,75)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df17,75)

                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df17,75)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df17,75)
                radar_chart(df17,75)

                NombreVente_DPT(df17,75)
                DateFonciere_DPT(df17,75,'month','valeur_fonciere_en_2017')
                nuage_point(df17,75,'Maison','surface_reelle_bati','valeur_fonciere_en_2017','valeur_fonciere_en_2017')

                st.sidebar.info('Information sur Paris')




        if app_mode2 == 'Lyon 🦁':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df17,69)  
                                      
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df17,69)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df17,69)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df17,69)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df17,69)

                
                radar_chart(df17,69)

                NombreVente_DPT(df17,69)
                DateFonciere_DPT(df17,69,'month','valeur_fonciere_en_2017')
                nuage_point(df17,69,'Maison','surface_reelle_bati','valeur_fonciere_en_2017','valeur_fonciere_en_2017')
                
                st.sidebar.info('Information sur Lyon')

        if app_mode2 == 'Marseille 🌞':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df17,13)                
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df17,13)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df17,13)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df17,13)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df17,13)
                radar_chart(df17,13)

                DateFonciere_DPT(df17,13,'month','valeur_fonciere_en_2017')
                NombreVente_DPT(df17,13)
                nuage_point(df17,13,'Maison','surface_reelle_bati','valeur_fonciere_en_2017','valeur_fonciere_en_2017')
        st.sidebar.success('')


if app_mode == "2018":
        
        app_mode2 = st.sidebar.radio('', ['France entière 🥖','Paris 🗼' ,'Marseille 🌞','Lyon 🦁'])

        if app_mode2 == 'France entière 🥖':

                
 
        
                app_mode4 = st.selectbox("",
        ["Proportion des maisons, appartements, locaux et dépendances","Tableau présentant les données avec lesquels cette page a été faite",
         "Evolution de la valeur foncière par mois !","Nombre de transaction effectué","Quantité pour chacun des cultures","Origine des cultures pour chaque mobilier"
         ,"Carte de la France pour chaque transaction par mois"]) 
                if app_mode4 =="Proportion des maisons, appartements, locaux et dépendances":
                        chart_pie(df18)
                if app_mode4 =="Tableau présentant les données avec lesquels cette page a été faite":
                        table18()
                if app_mode4 =="Evolution de la valeur foncière par mois !":
                        DateFonciere(df18,'month','valeur_fonciere_en_2018')
                        ValeurFoncièreParMois(df18,'valeur_fonciere_en_2018')
                if app_mode4 =="Nombre de transaction effectué":
                        NombreVente(df18)
                if app_mode4 =="Quantité pour chacun des cultures":
                        bar_chart(df18)
                if app_mode4 =="Origine des cultures pour chaque mobilier":
                        nuage_de_point(df18)
                if app_mode4 =="Carte de la France pour chaque transaction par mois":
                        map(df18)
                
                
                st.sidebar.info('Vue global sur la France')


        if app_mode2 == 'Paris 🗼':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout":
                        
                        mapDPT(df18,75)

                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df18,75)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df18,75)

                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df18,75)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df18,75)
                radar_chart(df18,75)

                NombreVente_DPT(df18,75)
                DateFonciere_DPT(df18,75,'month','valeur_fonciere_en_2018')
                nuage_point(df18,75,'Maison','surface_reelle_bati','valeur_fonciere_en_2018','valeur_fonciere_en_2018')

                st.sidebar.info('Information sur Paris')




        if app_mode2 == 'Lyon 🦁':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df18,69)  
                                      
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df18,69)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df18,69)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df18,69)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df18,69)

                
                radar_chart(df18,69)

                NombreVente_DPT(df18,69)
                DateFonciere_DPT(df18,69,'month','valeur_fonciere_en_2018')
                nuage_point(df18,69,'Maison','surface_reelle_bati','valeur_fonciere_en_2018','valeur_fonciere_en_2018')
                
                st.sidebar.info('Information sur Lyon')

        if app_mode2 == 'Marseille 🌞':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df18,13)                
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df18,13)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df18,13)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df18,13)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df18,13)
                radar_chart(df18,13)

                DateFonciere_DPT(df18,13,'month','valeur_fonciere_en_2018')
                NombreVente_DPT(df18,13)
                nuage_point(df18,13,'Maison','surface_reelle_bati','valeur_fonciere_en_2018','valeur_fonciere_en_2018')

        st.sidebar.success('')

if app_mode == "2019":
        
        app_mode2 = st.sidebar.radio('', ['France entière 🥖','Paris 🗼' ,'Marseille 🌞','Lyon 🦁'])

        if app_mode2 == 'France entière 🥖':
 
                
      
        
                app_mode4 = st.selectbox("",
        ["Proportion des maisons, appartements, locaux et dépendances","Tableau présentant les données avec lesquels cette page a été faite",
         "Evolution de la valeur foncière par mois !","Nombre de transaction effectué","Quantité pour chacun des cultures","Origine des cultures pour chaque mobilier"
         ,"Carte de la France pour chaque transaction par mois"]) 
                if app_mode4 =="Proportion des maisons, appartements, locaux et dépendances":
                        chart_pie(df19)
                if app_mode4 =="Tableau présentant les données avec lesquels cette page a été faite":
                        table19()
                if app_mode4 =="Evolution de la valeur foncière par mois !":
                        DateFonciere(df19,'month','valeur_fonciere_en_2019')
                        ValeurFoncièreParMois(df19,'valeur_fonciere_en_2019')
                if app_mode4 =="Nombre de transaction effectué":
                        NombreVente(df19)
                if app_mode4 =="Quantité pour chacun des cultures":
                        bar_chart(df19)
                if app_mode4 =="Origine des cultures pour chaque mobilier":
                        nuage_de_point(df19) 
                if app_mode4 =="Carte de la France pour chaque transaction par mois":
                        map(df19)
                
                
                st.sidebar.info('Vue global sur la France')


        if app_mode2 == 'Paris 🗼':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout":
                        
                        mapDPT(df19,75)

                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df19,75)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df19,75)

                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df19,75)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df19,75)
                radar_chart(df19,75)

                NombreVente_DPT(df19,75)
                DateFonciere_DPT(df19,75,'month','valeur_fonciere_en_2019')
                nuage_point(df19,75,'Maison','surface_reelle_bati','valeur_fonciere_en_2019','valeur_fonciere_en_2019')

                st.sidebar.info('Information sur Paris')




        if app_mode2 == 'Lyon 🦁':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df19,69)  
                                      
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df19,69)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df19,69)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df19,69)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df19,69)
  
                radar_chart(df19,69)

                NombreVente_DPT(df19,69)
                DateFonciere_DPT(df19,69,'month','valeur_fonciere_en_2019')
                nuage_point(df19,69,'Maison','surface_reelle_bati','valeur_fonciere_en_2019','valeur_fonciere_en_2019')
                
                st.sidebar.info('Information sur Lyon')

        if app_mode2 == 'Marseille 🌞':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        
                        mapDPT(df19,13)                
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df19,13)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df19,13)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df19,13)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df19,13)
                radar_chart(df19,13)

                DateFonciere_DPT(df19,13,'month','valeur_fonciere_en_2019')
                NombreVente_DPT(df19,13)
                nuage_point(df19,13,'Maison','surface_reelle_bati','valeur_fonciere_en_2019','valeur_fonciere_en_2019')
                
        st.sidebar.success('')

if app_mode == "2020":
        st.sidebar.title("Sélectionnez votre Département !")
        app_mode2 = st.sidebar.radio('', ['France entière 🥖','Paris 🗼' ,'Marseille 🌞','Lyon 🦁'])
        if app_mode2 == 'France entière 🥖':
                app_mode4 = st.selectbox("",
        ["Proportion des maisons, appartements, locaux et dépendances","Tableau présentant les données avec lesquels cette page a été faite",
         "Evolution de la valeur foncière par mois !","Nombre de transaction effectué","Quantité pour chacun des cultures","Origine des cultures pour chaque mobilier"
         ,"Carte de la France pour chaque transaction par mois"]) 
                if app_mode4 =="Proportion des maisons, appartements, locaux et dépendances":
                        chart_pie(df20)
                        
                if app_mode4 =="Tableau présentant les données avec lesquels cette page a été faite":
                        table20()
                if app_mode4 =="Evolution de la valeur foncière par mois !":
                        DateFonciere(df20,'month','valeur_fonciere_en_2020')
                        ValeurFoncièreParMois(df20,'valeur_fonciere_en_2020')
                if app_mode4 =="Nombre de transaction effectué":
                        NombreVente(df20)
                if app_mode4 =="Quantité pour chacun des cultures":
                        bar_chart(df20)
                if app_mode4 =="Origine des cultures pour chaque mobilier":
                        nuage_de_point(df20) 
                if app_mode4 =="Carte de la France pour chaque transaction par mois":
                        map(df20)
                st.sidebar.info('Vue global sur la France')
        if app_mode2 == 'Paris 🗼':
                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout": 
                        mapDPT(df20,75)
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df20,75)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df20,75)

                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df20,75)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df20,75)
                radar_chart(df20,75)
                NombreVente_DPT(df20,75)
                DateFonciere_DPT(df20,75,'month','valeur_fonciere_en_2020')
                nuage_point(df20,75,'Maison','surface_reelle_bati','valeur_fonciere_en_2020','valeur_fonciere_en_2020')
                st.sidebar.info('Information sur Paris')
        if app_mode2 == 'Lyon 🦁':
                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                if app_mode3 == "Tout":      
                        mapDPT(df20,69)  
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df20,69)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df20,69)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df20,69)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df20,69)
                radar_chart(df20,69)
                NombreVente_DPT(df20,69)
                DateFonciere_DPT(df20,69,'month','valeur_fonciere_en_2020')
                nuage_point(df20,69,'Maison','surface_reelle_bati','valeur_fonciere_en_2020','valeur_fonciere_en_2020')
                
                st.sidebar.info('Information sur Lyon')

        if app_mode2 == 'Marseille 🌞':

                app_mode3 = st.select_slider('Multiselect', options=["Tout","Maison","Appartement","dépendances","locaux"])
                
                if app_mode3 == "Tout":
                        mapDPT(df20,13)                
                if app_mode3 == "Maison":
                        map_des_maisons_DPT(df20,13)
                if app_mode3 == "Appartement":
                        map_des_aptm_DPT(df20,13)
                if app_mode3 == "dépendances":
                        map_des_dépendances_DPT(df20,13)
                if app_mode3 == "locaux":
                        map_des_locaux_DPT(df20,13)
                radar_chart(df20,13)
                DateFonciere_DPT(df20,13,'month','valeur_fonciere_en_2020')

                NombreVente_DPT(df20,13)

                nuage_point(df20,13,'Maison','surface_reelle_bati','valeur_fonciere_en_2020','valeur_fonciere_en_2020')

                
                st.sidebar.info('Informations sur Marseille')
        
if app_mode== "Evolution":
        st.subheader("Les visuels ainsi que le tableau ont été fait en fonction de la moyenne des valeurs foncières pour chaque années.")
        tickers=('2017','2018','2019','2020')
        dropdown=st.multiselect('',tickers)
        first=moy_valeur_fonciere_2016    
        linechart(first,dropdown)
        st.balloons()
        st.sidebar.success('')
        