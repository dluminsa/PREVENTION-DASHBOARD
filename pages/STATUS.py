import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time
import datetime as dt
from datetime import datetime, date


st.set_page_config(
     page_title= 'ACTIVITIES REVIEW STATUS'
)
st.write('BEING UPDATED, WILL RETURN AFTER THE NEW BUDGETS')
st.stop()
st.markdown("<h4><b>CHECK REVIEW STATUS OF PAPER WORK</b></h4>", unsafe_allow_html=True)

total= 0
district = ''
cluster = ''
ids = ''
Intention = st.radio('**HOW MAY I HELP YOU?**', options=['MARK REVIEWED PAPER WORK', 'CHECK REVIEW STATUS'], index=None)
file = r'PLANNED.csv'
df = pd.read_csv(file)

if Intention:
    pass
else:
    st.stop()

if Intention == 'MARK REVIEWED PAPER WORK':
    coln, colm = st.columns([1,2])
    c = 'HOW MANY DO YOU HAVE?'
    total = coln.number_input(label=f'**{c}**', value=None, max_value=None, min_value=None,step=1, format="%d")
    if total:
         pass
    else:
         st.stop()
    id = []
    if total:
        if int(total)==1:     
            col1, col2,col3 = st.columns(3)
            m = 'IN PUT PAPER WORK ID'
            idea = col1.number_input(label=f'**{m}**', value=None, max_value=None, min_value=None,step=1, format="%d")
            #id.append(ids)
            col2.write('')
            col2.write('')
            submit = col2.button('SUBMIT')
        else:
            col1, col2,col3 = st.columns(3)
            m = 'IN PUT PAPER WORK ID'      
            for each in range(int(total)):
                col1, col2,col3 = st.columns(3)
                every = each+1
                ids = col1.number_input(label=f'**{m} for paper work {every}**', value=None,key=each, max_value=None, min_value=None,step=1, format="%d")
                id.append(ids)
            col2.write('')
            col2.write('')
            submit = col2.button('SUBMIT')
   
    if submit:
            if int(total)==1:
                data1 = pd.DataFrame([{'PAID': idea}])
            else:                  
                data1 = pd.DataFrame(id, columns=['PAID'])
            data2 = data1.dropna(how='all')
            try:
                st. write('SUBMITING ID')
                conn = st.connection('gsheets', type=GSheetsConnection)
                exist2 = conn.read(worksheet= 'PAID', usecols=list(range(1)),ttl=5)
                existing2= exist2.dropna(how='all')
                updated = pd.concat([existing2, data2], ignore_index =True)
                existing2= exist2.dropna(how='all')
                conn.update(worksheet = 'PAID', data = updated)         
                st.success('ID above has been submitted')
                st.write('RELOADING PAGE')
                time.sleep(2)
                st.markdown("""
                <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)

            except:
                    st.write("Couldn't submit, poor network") 
                    st.write("Submit again")
else:

    clusters  = df['CLUSTER'].unique()
    cluster = st.radio("**Choose a cluster:**", clusters,horizontal=True, index=None)
    if cluster:
        try:
             conn = st.connection('gsheets', type=GSheetsConnection)
             exist1 = conn.read(worksheet= 'PREV', usecols=list(range(10)),ttl=5)
             exist2 = conn.read(worksheet= 'PAID', usecols=list(range(2)),ttl=5)
             existing1= exist1.dropna(how='all')
             existing2= exist2.dropna(how='all')
        except:
             st.write("POOR INTERNET, COULDN'T CONNECT TO THE GOOGLE SHEETS")
             st.write('Get better internet and try again')
             st.stop()
        sent = existing1[existing1['CLUSTER'] == cluster].copy()
        sent['ID'] =sent['ID'].astype(int)
        existing2['PAID'] =existing2['PAID'].astype(int)
        unpaid = sent[~sent['ID'].isin(existing2['PAID'])].copy()
        a = unpaid.shape[0]
        if int(a) == 0:
            st.write('**NO PAPER WORK PENDING**')
            st.stop()
        else:
            unpaid = unpaid[['DISTRICT', 'FACILITY', 'ACTIVITY', 'ID','START DATE', 'END DATE', 'DATE OF SUBMISSION']]
            st. markdown(f'YOU HAVE NOT REVIEWED {a} PAPER WORKS')
            with st.expander('CLICK HERE TO VIEW THEM'):
                st.write(unpaid)
    else:
        st.stop()





