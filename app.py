import pandas as pd
import streamlit as st
import os
from io import BytesIO

# Setup Streamlit App
st.set_page_config(page_title="🧹 Data Sweeper", layout="wide")
st.title("🧹 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

# Process files if uploaded
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name.lower())[-1]  # Ensure case-insensitive extension check

        # Read the file into a DataFrame
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display file information
        st.write(f"**📂 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {round(file.size / 1024, 2)} KB")

        # Display data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🔄 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

        # Column Selection
        st.subheader("📌 Select Columns")
        selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]  # Keep only selected columns

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            numeric_df = df.select_dtypes(include="number")
            if numeric_df.shape[1] >= 2:  # Ensure at least 2 numeric columns exist
                st.bar_chart(numeric_df.iloc[:, :2])  # Show first two numeric columns
            else:
                st.warning("⚠️ Not enough numeric columns to visualize!")

        # File Conversion Options
        st.subheader("🔁 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Reset buffer position for downloading

            # Download Button
            st.download_button(
                label=f"📥 Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All Files Processed!")
