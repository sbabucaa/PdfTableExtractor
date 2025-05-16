import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.title("PDF Table Extractor to Excel (.xlsx)")

uploaded_files = st.file_uploader("Upload one or more PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_tables = []
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                    else:
                        df = pd.DataFrame(table)
                    all_tables.append(df)
    if all_tables:
        excel_df = pd.concat(all_tables, ignore_index=True)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            excel_df.to_excel(writer, index=False, sheet_name="AllTables")
        st.success("Tables extracted and combined from all PDFs!")
        st.download_button(
            label="Download Excel file",
            data=output.getvalue(),
            file_name="tables_combined.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the uploaded PDF(s).")