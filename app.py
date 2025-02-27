import streamlit as st 
import pandas as pd
import os
from io import BytesIO 
file_ext = ".txt"  # Define the variable first
print(file_ext)    # Now it's defined and you can use it



# Set up our app:
st.set_page_config(page_title="Data Sweeper",layout='wide')
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV oR Excel):", type=["csv","xlsx"],accept_multiple_files=True)


if uploaded_files:
    for file in uploaded_files:
        file.ext = os.path.splitext(file.name)[-1].lower()


        if file.ext ==".csv":
            df = pd.read_csv(file)
        elif file.ext ==".xlsx":
         df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type : {file.ext}")
            continue    

        #Info about the file:
        st.write(f"**File Name:** {file.name}")

        st.write(f"**File Size:** {file.size/1024}") 

        # Shows 5 rows of our dataframe(df)
        st.write("Preview the head of dataframe")
        st.dataframe(df.head()) 

        # Options for Data cleaning:
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for{file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")

            with col2:
                if st.button(f"Filled  missing values for {file.name}"):
                    numeric_cols = df.select_dftypes(include=[ 'number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

                    #Choose specific column to keep or convert:
                    st.subheader("Select Column to Convert")
                    columns = st.multiselect(f"Choose Column for {file.name}" , df.columns, default=df.columns)
                    df = df[columns]

                    # Create some visualizatuions:
                    st.subheader("Data Visulization ")
                    if st.checkbox("Show Visualiztatipon for{file.name}"):
                        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

                    #CAonvert the file -> CSV or Excel:
                    st.subheader("🔁Conversion Options")
                    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV","Excel"],key=file.name)
                    if st.button(f"Convert{file.name}"):
                        buffer = BytesIO
                        if conversion_type =="CSV":
                            df.to_csv(buffer, index=False)
                            file_name = file.name.replace(file_ext , ".csv")
                            mime_type ="text/csv"


                        elif conversion_type =="Excel":
                            df.to_excel(buffer, index=False)
                            file_name = file.name.replace(file_ext , ".xlxs")
                            mime_type ="text/excel"
                            buffer.seek(0)

                            #download button:
                            st.download_button(
                            label = f"Download {file_name} as{conversion_type}",
                            data = buffer,
                            file_name = file.name,
                            mime = mime_type
                            )
                            st.success("All files processed!")
