import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import numpy as np
import time
import gspread
import traceback
import datetime as dt
from datetime import datetime, date
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
     page_title= 'SALES TRACKER'
)
                                                                        
# numbers = []
# amounts = []
# dates = []
# weeks = []
# areas = []
# starts= []
# ends = []
# activit = []
# themes = []
# uniques = []
# facilitiesy = []
if 'bbt' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'GIVEN', usecols=list(range(4)),ttl=5)
        bbt = exist.dropna(how='all')
        st.session_state.bbt = bbt
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO THE DATABASE")
         st.stop()
dfl = st.session_state.bbt.copy()
st.write(dfl)

secrets = st.secrets["connections"]["gsheets"]
credentials_info = {
        "type": secrets["type"],
        "project_id": secrets["project_id"],
        "private_key_id": secrets["private_key_id"],
        "private_key": secrets["private_key"],
        "client_email": secrets["client_email"],
        "client_id": secrets["client_id"],
        "auth_uri": secrets["auth_uri"],
        "token_uri": secrets["token_uri"],
        "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": secrets["client_x509_cert_url"]
    }
        
try:
    # Define the scopes needed for your application
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
    
     
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        
        # Authorize and access Google Sheets
    client = gspread.authorize(credentials)
        
        # Open the Google Sheet by URL
    spreadsheetu = "https://docs.google.com/spreadsheets/d/1XzTOKXJuG28J4TYsjjuOUOv8Ra1zmnXCRekhmNumVXY/edit?gid=662839431#gid=662839431"     
    spreadsheet = client.open_by_url(spreadsheetu)
except Exception as e:
        # Log the error message
    st.write(f"CHECK: {e}")
    st.write(traceback.format_exc())
    st.write("COULDN'T CONNECT TO GOOGLE SHEET, TRY AGAIN")
    st.stop()

st.markdown("<h4><b>SALES  TRACKER</b></h4>", unsafe_allow_html=True)
#sss
done = ''
category = ''
prod = r'products.csv'
df = pd.read_csv(prod)


themes = ['STOCK STATUS', 'EXPENDITURE', 'CREDIT GIVEN']

theme = st.radio("**WHAT DO YOU WANT TO INPUT?**", themes,horizontal=True, index=None)
if not theme:
     st.stop()
else:
     pass

if theme == 'STOCK STATUS':
     categories = df['category'].unique()
    
     category = st.radio(f"**Choose a category of the product:**", categories, horizontal=True, index=None)
     if not category:
          st.stop()
     else:
          pass
     dfa = df[df['category']==category].copy()
     items = dfa['Product'].unique()
     items = list(items)
     st.write('**PERIOD OF STOCK COUNT**')
     cola, colb, colc = st.columns([2,1,2])
     startr = cola.date_input('FROM', value=None, key='startd')
     endr = colc.date_input('TO', value=None, key='endd')
     cola, colb = st.columns([2,1])
     if not startr:
            st.stop()
     if not endr:
            st.stop()
     if startr > endr:
          st.warning("IMPOSSIBLE, START DATE CAN'T BE GREATER THAN END DATE")
          st.stop()
     dfs = []
     for item in items:
          sell = dfa[dfa['Product']==item].copy()
          buy = sell['Buy'].sum()
          sell = sell['Sale'].sum()
          col1, col2, col3 = st.columns(3)
          item = item.strip()
          col1.write(f'**{item}**')
          col1, col2, col3 = st.columns(3)
          qty = col1.number_input(f'**STOCK IN OF {item}**', value=None, max_value=None, min_value=0,step=1, format="%d", key= f'stock_{item}')
          qty2 = col2.number_input(f'**STOCK OUT OF {item}**', value=None, max_value=None, min_value=0,step=1, format="%d", key= f'stocko_{item}')
          qty3 = col3.number_input(f'**STOCK AT HAND {item}**', value=None, max_value=None, min_value=0,step=1, format="%d", key= f'stocka_{item}')
          if qty is None:
               st.stop()
          if qty2 is None:
               st.stop()
          if qty3 is None:
               st.stop()
          data = {
               'START': startr,
               'END': endr,
               'CATEGORY': category,
               'ITEM': item,
               'IN': qty,
               'OUT': qty2,
               'HAND': qty3,
               'SALE': int(sell),
               'BUY': int(buy)
          }
          data = pd.DataFrame([data])
          dfs.append(data)
     df = pd.concat(dfs, ignore_index=True)
     st.write(df)
     cola, colb = st.columns([2,1])
     submit = cola.button('**SUBMIT STOCK DATA**', key='submit_stock')
     if submit:
          try:
               st. write('SUBMITING')
               sheet1 = spreadsheet.worksheet("STOCK")
               df[['START', 'END']] = df[['START', 'END']].astype(str)
               rows_to_append = df.values.tolist()
               sheet1.append_rows(rows_to_append, value_input_option='RAW')
               st.success('Your data above has been submitted')
               st.write('RELOADING PAGE')
               time.sleep(1)
               st.markdown("""
               <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)

          except:
                    st.write("Couldn't submit, poor network") 
                    st.write('Click the submit button again')
elif theme == 'EXPENDITURE':
     st.write('**PERIOD**')
     cola, colb, colc = st.columns([2,1,2])
     start = cola.date_input('FROM', value=None, key='start')
     end = colc.date_input('TO', value=None, key='end')
     cola, colb = st.columns([2,1])
     if not start:
            st.stop()
     if not end:
            st.stop()
     if start > end:
          st.warning("IMPOSSIBLE, START DATE CAN'T BE GREATER THAN END DATE")
          st.stop()

     amount = cola.number_input('**TOTAL AMOUNT SPENT**', value=None, max_value=None, min_value=500,step=1, format="%d", key= f'exp')
     if amount is None:
            st.stop()
     datan = {
          'START': start,
          'END': end,
          'AMOUNT': amount}
     dfn = pd.DataFrame([datan])
     submitn = cola.button('**SUBMIT EXPENDITURE**', key='submit_expenditure')
     if submitn:
          try:
               st. write('SUBMITING')
               sheet2 = spreadsheet.worksheet("EXPENDITURE")
               dfn[['START', 'END']] = dfn[['START', 'END']].astype(str)
               rows_to_append = dfn.values.tolist()
               
               sheet2.append_rows(rows_to_append, value_input_option='RAW')
               st.success('Your data above has been submitted')
               st.write('RELOADING PAGE')
               time.sleep(1)
               st.markdown("""
               <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)

          except:
                    st.write("Couldn't submit, poor network") 
                    st.write('Click the submit button again')
elif theme == 'CREDIT GIVEN':
    todo = st.radio(f"**Choose a category of the product:**", ['CREDIT GIVEN', 'CREDIT PAID'], horizontal=True, index=None)
    if not todo:
         st.stop()
    elif todo == 'CREDIT GIVEN':
        st.write('**PERIOD WHEN THE ITEMS WERE GIVEN OUT**')
        cola, colb, colc = st.columns([2,1,2])
        startx = cola.date_input('FROM', value=None, key='start1')
        endx = colc.date_input('TO', value=None, key='end1')
        cola, colb = st.columns([2,1])
        if not startx:
                st.stop()
        if not endx:
            st.stop()
        if startx > endx:
            st.warning("IMPOSSIBLE, START DATE CAN'T BE GREATER THAN END DATE")
            st.stop()

        amountx = cola.number_input('**TOTAL AMOUNT GIVEN**', value=None, max_value=None, min_value=500,step=1, format="%d", key= f'exp')
        if amountx is None:
                st.stop()
    
        def generate_unique_number():
            f = dt.datetime.now()  # Get the current datetime
            g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
            h = g.split('.')[1]  # Extract the microseconds part of the formatted string
            j = h[1:5]  # Get the second through fifth digits of the microseconds part
            return int(j)  # Convert the sliced string to an integer

        # Initialize the unique number in session state if it doesn't exist
        if 'unique_number' not in st.session_state:
            st.session_state['unique_number'] = generate_unique_number()
            unique = st.session_state['unique_number'] 

        else:
            pass
        unique = st.session_state['unique_number']
        datay = {
            'START': startx,
            'END': endx,
            'AMOUNT': amountx,
            'ID': unique}
        dfx = pd.DataFrame([datay])
        submitx = cola.button('**SUBMIT CREDIT GIVEN**', key ='submit_credit')
        if submitx:
          try:
               st. write('SUBMITING')
               sheet2 = spreadsheet.worksheet("GIVEN")
               dfx[['START', 'END']] = dfx[['START', 'END']].astype(str)
               rows_to_append = dfx.values.tolist()
               
               sheet2.append_rows(rows_to_append, value_input_option='RAW')
               st.success('Your data above has been submitted')
               st.write('RELOADING PAGE')
               time.sleep(1)
               st.markdown("""
               <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)

          except:
                    st.write("Couldn't submit, poor network") 
                    st.write('Click the submit button again')
    elif todo == 'CREDIT PAID':
        st.write('**EACH CREDIT GIVEN WILL BE TRACKED BY ITS UNIQUE ID**')
        dfl['ID'] = pd.to_numeric(dfl['ID'], errors='coerce')
        cola, colb, colc = st.columns([2,1,2])
        unique = cola.number_input('**ID FOR THE CREDIT BEING PAID FOR**', value=None, max_value=None, min_value=500,step=1, format="%d", key= f'exp2')
        if not unique:
                st.stop()
        if unique not in dfl['ID'].values:
            st.warning("THE ID YOU ENTERED DOESN'T EXIST")
            st.stop()
        else:
              debt = dfl[dfl['ID']==unique]['AMOUNT'].values[0]
              st.write(f'THE AMOUNT OWED FOR THE ID {unique} IS **{int(debt):,}**')
        cola, colb = st.columns([1,2])
        amountz = cola.number_input('**TOTAL AMOUNT PAID**', value=None, max_value=None, min_value=1,step=1, format="%d", key= f'exp3')
        if not amountz:
                st.stop()
        cola, colb, colc = st.columns([2,1,2])
        datex = cola.date_input('DATE PAID', value=None, key='start3')
        if not datex:
                st.stop()
        submitz = cola.button('**SUBMIT CREDIT PAID**', key ='submit_credit_paid')
        dataz ={
               'ID': unique,
               'AMOUNT': amountz,
               'DATE': datex
        }
        dfz = pd.DataFrame([dataz])
        if submitz:
          try:
               st. write('SUBMITING')
               sheet2 = spreadsheet.worksheet("PAID")
               dfz[['DATE']] = dfz[['DATE']].astype(str)
               rows_to_append = dfz.values.tolist()
               
               sheet2.append_rows(rows_to_append, value_input_option='RAW')
               st.success('Your data above has been submitted')
               st.write('RELOADING PAGE')
               time.sleep(1)
               st.markdown("""
               <meta http-equiv="refresh" content="0">
                    """, unsafe_allow_html=True)

          except:
                    st.write("Couldn't submit, poor network") 
                    st.write('Click the submit button again')
          

today = date.today()


# if submit:
#      try:
#           st. write('SUBMITING')
#           sheet1 = spreadsheet.worksheet("DONE")
#           df[['START DATE', 'END DATE']] = df[['START DATE', 'END DATE']].astype(str)
#           rows_to_append = df.values.tolist()
          
#           sheet1.append_rows(rows_to_append, value_input_option='RAW')
#           st.success('Your data above has been submitted')
#           st.write('RELOADING PAGE')
#           time.sleep(1)
#           st.markdown("""
#           <meta http-equiv="refresh" content="0">
#                """, unsafe_allow_html=True)

#      except:
#                st.write("Couldn't submit, poor network") 
#                st.write('Click the submit button again')
