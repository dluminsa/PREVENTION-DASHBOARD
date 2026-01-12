import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import numpy as np
import time
import gspread
import datetime as dt
from datetime import datetime, date
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
     page_title= 'SALES TRACKER'
)
                                                                        
numbers = []
amounts = []
dates = []
weeks = []
areas = []
starts= []
ends = []
activit = []
themes = []
uniques = []
facilitiesy = []

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

# Show the facilities for the selected category and allow selection
if theme == 'STOCK STATUS':
    categories = df['category'].unique()
    
    category = st.radio(f"**Choose a category of the product:**", categories, horizontal=True, index=None)
     if not category:
          st.stop()
     else:
          pass
     dfa = df[df['category']==category].copy()
     items = dfa['Product'].unique()
     item =  st.select(f"**Choose a category of the product:**", categories, horizontal=True, index=None)

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

if category:
     area = st.radio('**CHOOSE A THEMATIC AREA**', theme, horizontal=True, index=None)
else:
     st.stop()

planned = r'PLANNED.csv'

dfa = pd.read_csv(planned)

if not area:
     st.stop()
else:
     pass

facilities = FACILITIES[category]

today = date.today()
activity = dfa[dfa['AREA']== area].copy()
activities = activity['ACTIVITY'].unique()
col1,col2 = st.columns([2,1])
if area:
      done = col1.selectbox(f'**SELECT THE {area} ACTIVITY YOU ARE PAYING FOR**', activities, index=None)
      doned = done
else:
     st.stop()

if not done:
     st.stop()
elif done:
     pass
current_time = time.localtime()
week = time.strftime("%V", current_time)
datey = datetime.now().date()
formatted = datey.strftime("%d-%m-%Y")
if done: 
     state = activity[activity['ACTIVITY']==done]
     statea = state[state['category']== category].copy()
     statement = statea['STATEMENT'].unique()
     counts = statea['COUNT'].unique()
     try:
        statement = statement[0]
     except:
          st.write('THIS ACTIVITY MAY NOT HAVE BEEN PLANNED FOR THIS category')
          st.write('CONTACT YOUR TEAM LEAD FOR SUPPORT')
          st.stop()
     counts = counts[0]
     cola, colb = st.columns(2)
     num = cola.number_input('**HOW MANY FACILITIES CONDUCTED THIS ACTIVITY?**',value=None, step=1)

     if not num:
          st.stop()
     elif num>10:
          st.warning('Maximum can be 10')
          st.stop()
     elif num == 0:
          st.warning("CAN'T BE ZERO")
          st.stop()
     else:
          st.markdown(f'**NOTE: {statement}**')

     #st.write(category)
     for i in range(num):
          colt,coly,colx = st.columns([1,1,1])
          colt.write(f'**FACILITY {i+1}**')
          
          coly,colz = st.columns(2)
          facility = coly.selectbox(f"**Name of facility {i+1}:**", facilities, index=None, key=f'y{i}')
          if not facility:
               st.stop()
          else:
               pass
          colt,coly,colx = st.columns([1,1,1])
          number = colt.number_input(label=f'**{counts}**', value=None, max_value=None, min_value=None,step=1, format="%d", key=f'{i}b')
          start = coly.date_input(label='**ACTIVITY START DATE**', value=None, key=f'a{i}')
          end = colx.date_input(label='**END DATE**',value=None, key= f'b{i}')
          amount = colt.number_input(label='**HOW MUCH ARE YOU PAYING FOR THIS FACILITY**', value=None, max_value= None, min_value=10000,step=1, format="%d", key= f'{i}a')
          if not start:
               st.stop()
          else:
               pass
          if not end:
               st.stop()
          else:
               pass
          if not amount:
               st.stop()
          else:
               pass
          themey = theme
          themes.append(themey)
          categoryy = category
          categorys.append(categoryy)
          weeky =int(week) + 13
          uniquey = int(st.session_state['unique_number'])
          areay = area
          doney = done
          formattedy = formatted
          weeks.append(weeky)
          uniques.append(uniquey)
          areas.append(areay)
          activit.append(doney)
          dates.append(formattedy)

          if number and start and end:
               if start > end:
                    st.warning("IMPOSSIBLE, ACTIVITY START DATE CAN'T BE GREATER THAN END DATE")
                    st.stop()
               elif end>today:
                    st.warning("IMPOSSIBLE, CHECK END DATE, IT'S GREATER THAN TODAY")
                    st.stop()
               else:
                    numbers.append(number)
                    facilitiesy.append(facility)
                    starts.append(start)
                    ends.append(end)
                    amounts.append(amount)
          else:
               st.stop()
               
#st.write(f'{categorys} this')

if num==1:
     categorys = [categorys[0]]
     weeks = [weeks[0]]
     uniques = [uniques[0]]
     areas = [areas[0]]
     activit = [activit[0]]
     dates = [dates[0]]
elif num>1:
     categorys = categorys[0:num]
     weeks = weeks[0:num]
     uniques = uniques[0:num]
     areas = areas[0:num]
     activit = activit[0:num]
     dates = dates[0:num]

df = pd.DataFrame({
          'DATE OF SUBMISSION': dates,
          'theme': themes,
          'category': categorys,
          'FACILITY': facilitiesy,
          'AREA': areas,
          'ACTIVITY': activit,
          'DONE': numbers,
          'START DATE': starts,
          'ID': uniques,
          'END DATE': ends,
          'WEEK': weeks,
          'AMOUNT': amounts
          })                                         
                                         
dfd = df[df.duplicated(subset='FACILITY')]
check = dfd.shape[0]

if check>0:
     dfd['FACILITY'] = dfd['FACILITY'].astype(str)
     disa = ', '.join(dfd['FACILITY'].unique())
     st.warning(f'**You repeated {disa}**')
     st.write("**ADD ALL THEIR TOTALS DONE AND SUBMIT THEM AT ONCE**")
     st.stop()
else:
     pass

st.write(f"UNIQUE ID: {st.session_state['unique_number']}")
col1,col2, col3 = st.columns([1,1,2])
col2.write('**SUMMARY**')

cola,colb = st.columns(2)
cola.write(f"**UNIQUE ID: {st.session_state['unique_number']}**")
cola.markdown(f'**category: {category}**')
colb.markdown(f'**FACILITY: {facility}**')
colb.markdown(f'**THEMATIC AREA: {area}**')
cola,colb,colc = st.columns(3)
colb.write(f'**ACTIVITY: {done}**')

dfa = df[['FACILITY', 'DONE', 'START DATE', 'END DATE', 'AMOUNT']].copy()

uniques = df['FACILITY']
cola,colb = st.columns([3,1])
cola.write(dfa) 
submit = colb.button('**SUBMIT**')

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
    spreadsheetu = " https://docs.google.com/spreadsheets/d/1IgIltX9_2yvppb4YYoebRyyYwCqYZng62h0cRYPmAdE"     
    spreadsheet = client.open_by_url(spreadsheetu)
except Exception as e:
        # Log the error message
    st.write(f"CHECK: {e}")
    st.write(traceback.format_exc())
    st.write("COULDN'T CONNECT TO GOOGLE SHEET, TRY AGAIN")
    st.stop()

if submit:
     try:
          st. write('SUBMITING')
          sheet1 = spreadsheet.worksheet("DONE")
          df[['START DATE', 'END DATE']] = df[['START DATE', 'END DATE']].astype(str)
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
