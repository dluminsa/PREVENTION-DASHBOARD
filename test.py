    if submit:
        try:
            st. write('SUBMITING')
            sheet2 = spreadsheet.worksheet("EXPENDITURE")
            dfz[['START', 'END']] = dfz[['START', 'END']].astype(str)
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