import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind
from itertools import product
from itertools import product
import scipy.stats as stats
from statsmodels.stats.libqsturng import psturng
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px



###################### - Tab Structures

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Home", "Data Cleaning", "Statistical Functions", "Contact"]    ###### Tab Names
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Home"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Home")
    active_tab = "Home"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


######################################### - Home tab

if active_tab == "Home":
    st.markdown("# Welcome")
    st.markdown(''' You have arrived at a web app highlighting work done to assist in the data preparation
    	, analysis, and visualisation of a dissertation project at the [Universidad de Bernardo O'Higgins](https://www.ubo.cl/).''')
    
    st.markdown(''' The project studies how impulsivity impacted the following of sanitary measures in the covid-19 pandemic in Santiago de Chile.
    	A [Barratt Test](https://www.impulsivity.org/measurement/bis11/) was used to collect data on impulsivity, with a seperate questionaire designed to identify level of compliance with sanitary measures.
    	''')

    st.markdown(''' The data was collected via the advertising of a GoogleForms questionaire a copy of which can be 
    	found [here](https://docs.google.com/forms/d/1Z12vlvceuCFjo9BqElblVENrYaGdsnwNRPLm_qaHFnA/viewform?edit_requested=true#responses).
    	A total of 181 responses were collected. ''')

    st.markdown(''' This web app is divided into two sections:''')

    st.markdown('''
    	* ***Data Cleaning -*** highlights the steps carried out in the cleaning of the raw data collected from the questionaire.
    	* ***Statistical Functions -*** a user friendly interactive function which was created to allow various statistical tests to be conducted according to a user defined set of configurations.


    	''')
   


###################################### - Data Cleaning tab

elif active_tab == "Data Cleaning":
	st.markdown('# Data Cleaning')
	st.markdown('''The data cleaning and preperation was conducted in python. The key steps were:''')
	st.markdown('''

    	* Remove personal information of respondents (emails, names)
    	* Remove respondents who did not consent to their information being included in the study. 
    	* Convert categrocial object variables to numeric data. 
    	* Deal with 'other' response for type of work. 
    	* Create new variable combining if a respondent lived with someone at high risk from covid and the type of risk that person was categorised as"
    	* Create summary variables for the Barratt Test (total score, cognitive, motor, not planned scores)
    	* Create summary variables for compliance with health measures test (total score, hygine, social distancing, sanitary measures scores)
    	* Create variable categorising respondents in two groups according to their age (18-25, 26-40)


    	'''

    	)

	st.markdown('''The full code used in the cleaning process is available on [Github](https://github.com/JamesAttwood1910/Diplomado_USACH/blob/main/Data_cleaning_DissertationProject.ipynb)''')



###################################### - Statistical Functions

elif active_tab == "Statistical Functions":
    st.markdown('''# Function''')
    st.markdown('The preprocessed data is loaded.')
    data = pd.read_csv('DatasJaviParaProfe3.csv')
    data = data[['Sexo:', 'Edad', 'Nivel Educacional', 'IPC', 'Ocupación', 'Vivió con alguien de alto riesgo',
	'MSTotal', 'BarrattTotal', 'Impulsividad_Cognitiva_Total', 'Impulsividad_Motora_Total',
	'Impulsividad_no_planeada_Total', 'Higiene_Total', 'Distanciamiento_Social_Total', 
	'Medidas_Sanitarias_Total', 'Grupos_Etarios']]

    st.write(data.head())


    st.markdown('### Ages')

    st.markdown('The below barchart shows the number of respondents within each age group.')


    fig = px.bar(data_frame = data['Grupos_Etarios'].value_counts().reset_index(), x = 'index', y = 'Grupos_Etarios')
    st.plotly_chart(fig, use_container_width=True)



    st.markdown('### Variables to select for significance: ')

    st.markdown('''The below drop down bar allows a variable to be selected upon which a T Student Test will be
    conducted to see if there is a statisitically significant difference between the means for Adults (26 - 40 years),
    and Young Adults (18 - 25 years). For there to be a significant difference a p value of <= 0.05 is required.''')


    variable = st.selectbox(
    	'',
    	('BarrattTotal', 'MSTotal',
       'Impulsividad_Cognitiva_Total', 'Impulsividad_Motora_Total',
       'Impulsividad_no_planeada_Total', 'Higiene_Total',
       'Distanciamiento_Social_Total', 'Medidas_Sanitarias_Total')

    	)   

    data['Age_Ttest_Group'] = np.where(data.Edad.isin(range(18,26)), 'Young_Adult', 'Adult')
    Young_Adult_Variable = data[data['Age_Ttest_Group'] == 'Young_Adult'][variable].values
    Adult_Variable = data[data['Age_Ttest_Group'] == 'Adult'][variable].values
    _,p_value=ttest_ind(a=Young_Adult_Variable,b=Adult_Variable,equal_var=False)
    if p_value < 0.05:
    	st.markdown('T Test Null Hypotesis Rejected - There is a statistically significance')
    	st.write(p_value)
    	
    else: 
    	st.markdown('T Test Null Hypotesis Rejected - There is not a statistically significant difference')
    	st.write('p value = ', p_value)


    fig = px.violin(
    	data_frame = data, y = variable, facet_col = 'Age_Ttest_Group',
    	orientation = 'v')
    for i, label in enumerate(data['Age_Ttest_Group'].unique()):
    	fig.layout.annotations[i]['text'] = label

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('### Conclusion')

    st.markdown('''There only exists a statistically significant difference between 
    	the means of the two age groups for the Barratt test sub group of cognative impulsivity.''')



     








###################################### - Contact
elif active_tab == "Contact":
    st.markdown('''This application was made with [streamlit](https://docs.streamlit.io/)
    and python. The code for the web app is available on [Github](https://github.com/JamesAttwood1910/Diplomado_USACH/blob/main/main.py).
    If you would like to contact the author please contact attwood1910@gmail.com or visit his [website](https://www.statcitypro.com/)''')
else:
    st.error("Something has gone terribly wrong.")

