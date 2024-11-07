import pandas as pd 
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
     page_title= 'PREVENTION ACTIVITIES DASHBOARD'
)
# st.write('BEING UPDATED, WILL RETURN AFTER THE NEW BUDGETS')
# st.stop()
cola,colb,colc = st.columns([1,2,1])
cola.write('')
colb.markdown("<h4><b>PREVENTION ACTIVITIES DASHBOARD</b></h4>", unsafe_allow_html=True)
colc.write('')
current_time = time.localtime()
k = time.strftime("%V", current_time)
t = int(k) -39
cola,colb,colc = st.columns([1,2,1])
cola.write(f'**CALENDAR WEEK IS: {k}**')
colc.write(f'**SURGE WEEK IS: {t}**')
try:
     conn = st.connection('gsheets', type=GSheetsConnection)     
     dfb = conn.read(worksheet='PREV', usecols=list(range(11)), ttl=5)
     dfb = dfb.dropna(how='all')
     conn = st.connection('gsheets', type=GSheetsConnection)     
     dfm = conn.read(worksheet='AMOUNT', usecols=list(range(11)), ttl=5)
     dfm = dfm.dropna(how='all')
except:
     st.write(f"**Your network is poor, couldn't connect to the google sheet**")
     st.write(f"**TRY AGAIN WITH BETTER INTERNET**")
     st.stop()
#st.write(dfb.columns)
dfb= dfb[['CLUSTER','DISTRICT','ACTIVITY', 'DONE', 'WEEK','FACILITY', 'ID']]
file = r'PLANNED.csv'
dfa = pd.read_csv(file)
dfa['AMOUNT'] = pd.to_numeric(dfa['AMOUNT'], errors='coerce')#.astype(int)
dfb = dfb[dfb['WEEK']>0].copy()
dfb['WEEK'] = dfb['WEEK'].astype(int)
dfb['CLUSTER'] = dfb['CLUSTER'].astype(str)
#dfb['AREA'] = dfb['AREA'].astype(str)
dfb['ACTIVITY'] = dfb['ACTIVITY'].astype(str)
dfb['DONE'] = dfb['DONE'].astype(int)

dfa['CLUSTER'] = dfa['CLUSTER'].astype(str)
#dfa['AREA'] = dfa['AREA'].astype(str)
dfa['ACTIVITY'] = dfa['ACTIVITY'].astype(str)
dfa = dfa[dfa['PLANNED']>0].copy()
dfa['PLANNED'] = dfa['PLANNED'].astype(int)

st.sidebar.subheader('Filter from here ')
cluster = st.sidebar.multiselect('Pick a cluster', dfa['CLUSTER'].unique())

if not cluster:
    dfa2 = dfa.copy()
    dfb2 = dfb.copy()
    dfm2 = dfm.copy()
else:
    dfa2 = dfa[dfa['CLUSTER'].isin(cluster)]
    dfb2 = dfb[dfb['CLUSTER'].isin(cluster)]
    dfm2 = dfm[dfm['CLUSTER'].isin(cluster)]
 
#for facility
activity = st.sidebar.multiselect('Choose an activity', dfa2['ACTIVITY'].unique())

#Filter Week, District, Facility
if not cluster  and not activity:
    filtered_dfa = dfa
    filtered_dfb = dfb
    filtered_dfm = dfm
elif not activity:
    filtered_dfa = dfa[dfa['CLUSTER'].isin(cluster)].copy()
    filtered_dfb = dfb[dfb['CLUSTER'].isin(cluster)].copy()
    filtered_dfm = dfm[dfm['CLUSTER'].isin(cluster)].copy()

elif cluster and activity:
     #
    filtered_dfa = dfa2[dfa2['CLUSTER'].isin(cluster)& dfa2['ACTIVITY'].isin(activity)].copy()
    filtered_dfm = dfm2[dfm2['CLUSTER'].isin(cluster)& dfm2['ACTIVITY'].isin(activity)].copy()
     #
    filtered_dfb = dfb2[dfb2['CLUSTER'].isin(cluster)& dfb2['ACTIVITY'].isin(activity)].copy()
elif activity:
    filtered_dfa = dfa2[dfa2['ACTIVITY'].isin(activity)].copy()
    filtered_dfb = dfb2[dfb2['ACTIVITY'].isin(activity)].copy()
    filtered_dfm = dfm2[dfm2['ACTIVITY'].isin(activity)].copy()
################################################################################################
#FACILITY
# facilities = list(','.join(filtered_dfb['FACILITY'].unique()))
st.sidebar.subheader('CHECK FACILITY PERFORMANCE')
fac = st.sidebar.multiselect('Pick a cluster', filtered_dfb['FACILITY'].unique())
if fac:
     if not activity:
          st.warning('FIRST CHOOSE AN ACTIVITY THAT YOU WANT TO MONITOR FOR THIS ACTIVITY')
          st.stop()
     else:     
          facd = filtered_dfb[filtered_dfb['FACILITY'].isin(fac)].copy()
          conducted = facd['DONE'].sum()
          st.write(f'FOR {activity}, {fac} HAS CONDUCTED {conducted}')
else:
     pass
#################################################################################################
if not fac:
     cols,cold = st.columns(2)
     clus = filtered_dfb['CLUSTER']. unique()
     if not cluster:
         pass
     elif len(clus) == 0:
         cols.write(f'**No data for this cluster**')
     else:
         cols.write(f'**You are viewing data for: {clus}**')
     
     act = filtered_dfb['ACTIVITY']. unique()
     
     if not activity:
         st.write(f'**No specific activity has been chosen**')
     elif len(act) == 0:
         st.write(f'**No data for the the activity chosen**')
     else:
         st.write(f'**ACTIVITIES INCLUDED ARE: {act}**')
     
     plan = filtered_dfa['PLANNED'].sum()
     conducted = filtered_dfb['DONE'].sum()
     notdone = plan - conducted
     if plan ==0:
          perc =0
     else:
         perc = round((conducted/plan)*100)
     
     exp = round((int(t)/12)*100)
     if conducted>plan:
         st.warning(f"SOMETHING IS WRONG, IT SEEMS ACTIVITIES DONE ARE MORE THAN THOSE THAT WERE PLANNED FOR!!")
     
     col1,col2,col3,col4, col5 = st.columns(5)#, gap='large')
     
     with col1:
         st.metric(label='**PLANNED**', value=f'{plan:,.0f}')
     with col2:
         st.metric(label='**DONE**', value=f'{conducted:,.0f}')
     with col3:
         st.metric(label='**%AGE**', value=f'{perc:,.0f}')
     with col4:
         st.metric(label='**EXPECTED**', value=f'{exp} %')
     with col5:
         st.metric(label='**BALANCE**', value=f'{notdone:,.0f}')
     #####################################################################################################f
     
     plan = filtered_dfa['AMOUNT'].sum()
     conducted = filtered_dfm['AMOUNT'].sum()
     notdone = plan - conducted
     
     if conducted>plan:
         st.warning(f"SOMETHING IS WRONG, IT SEEMS ACTIVITIES DONE ARE MORE THAN THOSE THAT WERE PLANNED FOR!!")
     
     col1,col2,col3 = st.columns(3)#, gap='large')
     with st.expander('CLICK HERE TO SEE EXPENDITURE'):
          col1,col2,col3 = st.columns(3)#,
          with col1:
              st.metric(label='**BUDGETED**', value=f'{plan:,.0f}')
          with col2:
              st.metric(label='**SPENT**', value=f'{conducted:,.0f}')
          with col3:
              st.metric(label='**BALANCE**', value=f'{notdone:,.0f}')
     
     #######################################################################################################
     #PIE CHART
     #st.divider()
     col1, col2,col3 = st.columns([1,4,1])
     labels = ['DONE', 'NOT DONE']
     # Values
     values = [conducted, notdone]
     colors = ['blue', 'red']
     # Creating the pie chart with specified colors and hole
     fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+value', 
                                  insidetextorientation='radial', marker=dict(colors=colors), hole=0.4)])
     
     # Updating the layout for better readability
     fig.update_traces(textposition='inside', textfont_size=20)
     fig.update_layout(title_text='DONE vs NOT DONE', title_x=0.3)
     
     col1, col2,col3 = st.columns([1,4,1])
     with col2:
          st.plotly_chart(fig, use_container_width=True)
     #############################################################################################
     #LINE GRAPH
     st.divider()
     
     grouped = filtered_dfb.groupby('WEEK').sum(numeric_only=True).reset_index()
     fig2 = px.line(grouped, x='WEEK', y='DONE', title='WEEKLY TRENDS',
                    markers=True)
     
     fig2.update_layout(xaxis_title='WEEK', yaxis_title='TOTAL DONE',
                         width=800,  # Set the width of the plot
                          height=400,  # Set the height of the plot
                          xaxis=dict(showline=True, linewidth=1, linecolor='black',tickmode='linear',tick0=25,dtick=1,),  # Show x-axis line
                          yaxis=dict(showline=True, linewidth=1, linecolor='black'))  # Show y-axis line)
     
     st.plotly_chart(fig2, use_container_width=True)
     
     #st.write(filtered_dfb.columns)
     filtered_dfc= filtered_dfb[['CLUSTER','FACILITY','ACTIVITY', 'DONE', 'WEEK','ID']]
     #filtered_dfc = filtered_dfc.set_index('CLUSTER')
     with st.expander(f'**CLICK HERE TO SEE FULL DATA SET**'):
         st.dataframe(filtered_dfc.reset_index(drop=True))
         csv_data = filtered_dfc.to_csv(index=False)
         st.download_button(
                             label=" DOWNLOAD THIS DATA SET",
                             data=csv_data,
                             file_name="ACTIVITIES.csv",
                             mime="text/csv")
         
