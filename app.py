import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.title("PDF Table Extractor to Excel (.xlsx)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    all_tables = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # Convert to DataFrame, assuming first row as header if possible
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                else:
                    df = pd.DataFrame(table)
                all_tables.append(df)
    if all_tables:
        # Concatenate all DataFrames, ignore index and headers mismatch
        excel_df = pd.concat(all_tables, ignore_index=True)
        # Output to Excel in-memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            excel_df.to_excel(writer, index=False, sheet_name="AllTables")
        st.success("Tables extracted and combined!")
        st.download_button(
            label="Download Excel file",
            data=output.getvalue(),
            file_name="tables_combined.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the uploaded PDF.")