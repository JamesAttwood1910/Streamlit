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

######################################### - Home tab

welcome = st.container()

welcome.markdown("# Welcome")
welcome.markdown(''' You have arrived at a web app highlighting work done to assist in the data preparation
        , analysis, and visualisation of a dissertation project at the [Universidad de Bernardo O'Higgins](https://www.ubo.cl/).''')
    
welcome.markdown(''' The project studies how impulsivity impacted the following of sanitary measures in the covid-19 pandemic in Santiago de Chile.
        A [Barratt Test](https://www.impulsivity.org/measurement/bis11/) was used to collect data on impulsivity, with a seperate questionaire designed to identify level of compliance with sanitary measures.
        ''')

welcome.markdown(''' The data was collected via the advertising of a GoogleForms questionaire a copy of which can be 
        found [here](https://docs.google.com/forms/d/1Z12vlvceuCFjo9BqElblVENrYaGdsnwNRPLm_qaHFnA/viewform?edit_requested=true#responses).
        A total of 181 responses were collected. ''')

welcome.markdown(''' This web app is divided into two sections:''')

welcome.markdown('''
        * ***Data Cleaning -*** highlights the steps carried out in the cleaning of the raw data collected from the questionaire.
        * ***Statistical Functions -*** a user friendly interactive function which was created to allow various statistical tests to be conducted according to a user defined set of configurations.


        ''')

###################################### - Data Cleaning tab

cleaning = st.container()

cleaning.markdown('# Data Cleaning')
cleaning.markdown('''The data cleaning and preperation was conducted in python. The key steps were:''')
cleaning.markdown('''

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
cleaning.markdown('''The full code used in the cleaning process is available on [Github](https://github.com/JamesAttwood1910/Diplomado_USACH/blob/main/Data_cleaning_DissertationProject.ipynb)''')



###################################### - Statistical Functions

statistical = st.container()


statistical.markdown('''# Function''')
statistical.markdown('The preprocessed data is loaded.')
data = pd.read_csv('DatasJaviParaProfe3.csv')
data = data[['Sexo:', 'Edad', 'Nivel Educacional', 'IPC', 'Ocupación', 'Vivió con alguien de alto riesgo',
'MSTotal', 'BarrattTotal', 'Impulsividad_Cognitiva_Total', 'Impulsividad_Motora_Total',
'Impulsividad_no_planeada_Total', 'Higiene_Total', 'Distanciamiento_Social_Total', 
'Medidas_Sanitarias_Total', 'Grupos_Etarios']]

statistical.write(data.head())


statistical.markdown('### Ages')

statistical.markdown('The below barchart shows the number of respondents within each age group.')


fig = px.bar(data_frame = data['Grupos_Etarios'].value_counts().reset_index(), x = 'index', y = 'Grupos_Etarios', title = 'Count of age groups', 
    labels = {'index':'Age Groups'})
statistical.plotly_chart(fig, use_container_width=True)



statistical.markdown('### Variables to select for significance: ')

statistical.markdown('''The below drop down bar allows a variable to be selected upon which a T Student Test will be
conducted to see if there is a statisitically significant difference between the means for Adults (26 - 40 years),
and Young Adults (18 - 25 years). For there to be a significant difference a p value of <= 0.05 is required. 
The below violin plots, whilst not identifiying the means of the two groups, 
allow comparison of their distributions.''')


variable = statistical.selectbox(
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
	st.write('''T Test Null Hypotesis Rejected - There is a statistically significant difference between
        the means of''', variable, 'for young adults and adults.')
	st.write('p value = ', p_value)
	
else: 
	st.write('''T Test Null Hypotesis Rejected - There is not a statistically significant difference between
        the means of''', variable, 'for young adults and adults.')
	st.write('p value = ', p_value)


fig = px.violin(
	data_frame = data, y = variable, facet_col = 'Age_Ttest_Group',
	orientation = 'v', title = 'Distribution of selected variable for two age groups')
for i, label in enumerate(data['Age_Ttest_Group'].unique()):
	fig.layout.annotations[i]['text'] = label
statistical.plotly_chart(fig, use_container_width=True)


###################################### - Conclusion

Conclusion = st.container()

Conclusion.markdown('### Conclusion')

Conclusion.markdown('''There only exists a statistically significant difference between 
	the means of the two age groups for the Barratt test sub group of cognative impulsivity.''')


###################################### - Contact

contact = st.container()

contact.markdown('''This application was made with [streamlit](https://docs.streamlit.io/)
and python. The code for the web app is available on [Github](https://github.com/JamesAttwood1910/Diplomado_USACH/blob/main/main.py).
If you would like to contact the author please contact attwood1910@gmail.com or visit his [website](https://www.statcitypro.com/)''')

