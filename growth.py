import streamlit as st
import pandas as pd
import os
from io import BytesIo
st.set_page_config(page_title= "Data Sweeper", layout='wide')

#Custom CSs
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white
        }
        </style>
        """,
        unsafe_allow_html=True
)

#Title and discription 
st.title ("Datasweeper strealing Integrator by Abdul Wahab")
st.write("Transform your file bitween CSV and Excel Formats with build in data cleaning and visulization creating the projecct for Q3!")

#file uploder
uploader_files =st.file_uploader("upload your file (accept CSv or Excel):", type=["cvs", "xlsx"], accept_multiple_files=(True))

if uploader_files:
    for file in uploader_files:
        file_exe = os.path.splitext(file.name)[-1].lower() 
        if file_exe == ".csv":  
            df = pd.read_csv(file)
        elif file_exe == "xlsx":
            df=pd.read_excel(file)
        else: 
            st.error(f"unsupported file type:{ file_exe}")
            continue

#file details
st.write("review the head of Dataframe")
st.dataframe(df.head())

#data cleaning option 

st.subheader("data cleaning options")
if st.checkbox(f"clean data for {file.name}"):
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Remove duplicate from the file:{file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("Duplicate remove!")
    with col2:
        if st.button(f"file missing value for {file.name}"):
            numeric_cols=df.select_dtypes(include=['number'].colums)
            df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write(f"missing value have been filled!")
    st.subheader("Select Colums to keep ")
    colums=st.multiselect(f"chose colums for {file.name}", df.columns, default=df.columns)
    df=df[colums]

    #data visuliazation 
    st.subheader("Data visualization")
    if st.checkbox(f"show visuliazation for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
    
    #Conversion option
    st.subheader("Conversion options")
    conversion_type= st.radio(f"Convert {file.name} to :",["CSV", "Excel"],key=file.name)


    st.button(f"convert {file.name}")
    buffer = BytesIo()
    if conversion_type == "CSV":
        df.to_csv(buffer, index=False)
        file_name = file.name.replace(file_exe, "csv")
        mime_type="text/cvs"

    elif conversion_type == "Excel":
        df.to_excel(buffer, index=False)
        file_name= file.name.replace(file_exe, "xlsx")
        mime_type="application/vnd.openxmlformate-officedocuments.spreadsheetml.sheet"
        buffer.seek(0)
        
        st.download_button(
        label=(f"Download {file.name} as {conversion_type}"),
        data=buffer, 
        file_name=file_name,
        mime=mime_type
    )
st.success("All file Process successfully!")
