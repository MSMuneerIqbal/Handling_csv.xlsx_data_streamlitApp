import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format!")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("Data Explorer and Preprocessing App")

    # File Upload Section
    st.sidebar.header("Upload Your Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load data into session state if not already present
        if 'df' not in st.session_state:
            df = load_data(uploaded_file)
            if df is None:
                st.stop()
            st.session_state.df = df
        else:
            df = st.session_state.df

        # Data Overview Section
        st.subheader("Dataset Overview")
        st.write("**First 10 rows:**")
        st.dataframe(df.head(10))
        st.write("**Dataset Shape:**", df.shape)
        st.write("**Statistical Summary:**")
        st.write(df.describe(include="all"))
        st.write("**Missing Values:**")
        st.write(df.isnull().sum())
        
        # Option to Show a Specific Number of Rows
        st.subheader("View Data Rows")
        num_rows = st.number_input("Enter number of rows to display", min_value=1, 
                                   max_value=len(df), value=10, step=1)
        if st.button("Show Rows"):
            st.dataframe(df.head(num_rows))
        
        # Show Column Information
        st.subheader("Column Information")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show All Column Names"):
                st.write(list(df.columns))
        with col2:
            if st.button("Show Column Data Types"):
                st.write(df.dtypes)
        
        # Column Removal Section in Sidebar
        st.sidebar.header("Column Removal")
        all_columns = list(df.columns)
        cols_to_remove = st.sidebar.multiselect("Select columns to remove", all_columns)
        if st.sidebar.button("Remove Selected Columns"):
            if cols_to_remove:
                df = df.drop(columns=cols_to_remove)
                st.session_state.df = df
                st.success("Selected columns removed!")
                st.write("**Updated dataset shape:**", df.shape)
                st.dataframe(df.head(10))
            else:
                st.sidebar.warning("Please select at least one column to remove.")
        
        # Missing Value Handling Section
        st.header("Missing Value Handling")
        st.write("Handle missing values for numeric and object columns separately.")
        col_numeric, col_object = st.columns(2)
        with col_numeric:
            numeric_method = st.selectbox("Numeric columns fill method", 
                                          ["None", "Mean", "Median", "Mode"], key="num_method")
        with col_object:
            object_method = st.selectbox("Object columns fill method", 
                                         ["None", "Mode", "Fill with 'Unknown'", "Custom Value"], key="obj_method")
            custom_fill = None
            if object_method == "Custom Value":
                custom_fill = st.text_input("Enter custom fill value for object columns", value="Missing")
        
        if st.button("Apply Missing Value Treatment"):
            # Process numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if numeric_method != "None":
                for col in numeric_cols:
                    if df[col].isnull().sum() > 0:
                        if numeric_method == "Mean":
                            df[col].fillna(df[col].mean(), inplace=True)
                        elif numeric_method == "Median":
                            df[col].fillna(df[col].median(), inplace=True)
                        elif numeric_method == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
            # Process object columns
            object_cols = df.select_dtypes(include=['object']).columns
            if object_method != "None":
                for col in object_cols:
                    if df[col].isnull().sum() > 0:
                        if object_method == "Mode":
                            df[col].fillna(df[col].mode()[0], inplace=True)
                        elif object_method == "Fill with 'Unknown'":
                            df[col].fillna("Unknown", inplace=True)
                        elif object_method == "Custom Value" and custom_fill is not None:
                            df[col].fillna(custom_fill, inplace=True)
            st.session_state.df = df
            st.success("Missing values handled!")
            st.subheader("Data After Missing Value Treatment (First 10 Rows)")
            st.dataframe(df.head(10))
        
        # Visualization Section
        st.header("Visualization")
        plot_type = st.selectbox("Select Plot Type", 
                                 ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Correlation Heatmap"])
        selected_columns = st.multiselect("Select columns for plotting", list(df.columns))
        if st.button("Generate Plot"):
            if plot_type in ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"]:
                if selected_columns:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    if plot_type == "Line Plot":
                        df[selected_columns].plot(ax=ax, marker='o')
                        ax.set_title("Line Plot")
                        ax.set_xlabel("Index")
                        ax.set_ylabel("Values")
                        ax.legend(title="Columns")
                    elif plot_type == "Bar Plot":
                        df[selected_columns].plot(kind="bar", ax=ax)
                        ax.set_title("Bar Plot")
                        ax.set_xlabel("Index")
                        ax.set_ylabel("Values")
                        ax.legend(title="Columns")
                    elif plot_type == "Scatter Plot":
                        if len(selected_columns) >= 2:
                            x, y = selected_columns[0], selected_columns[1]
                            ax.scatter(df[x], df[y])
                            ax.set_xlabel(x)
                            ax.set_ylabel(y)
                            ax.set_title(f"Scatter Plot: {x} vs {y}")
                        else:
                            st.error("Please select at least two columns for a scatter plot.")
                            st.stop()
                    elif plot_type == "Histogram":
                        for col in selected_columns:
                            ax.hist(df[col].dropna(), alpha=0.5, label=col)
                        ax.set_title("Histogram")
                        ax.set_xlabel("Value")
                        ax.set_ylabel("Frequency")
                        ax.legend(title="Columns")
                    st.pyplot(fig)
                    # Download option for the plot image
                    buf = BytesIO()
                    fig.savefig(buf, format="png")
                    buf.seek(0)
                    st.download_button(label="Download Plot as PNG",
                                       data=buf,
                                       file_name=f"{plot_type.lower().replace(' ', '_')}.png",
                                       mime="image/png")
                else:
                    st.error("Please select columns for plotting.")
            elif plot_type == "Correlation Heatmap":
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
                ax.set_title("Correlation Heatmap")
                st.pyplot(fig)
                buf = BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.download_button(label="Download Heatmap as PNG",
                                   data=buf,
                                   file_name="correlation_heatmap.png",
                                   mime="image/png")
        
        # File Conversion Section
        st.header("Convert Data Format")
        conversion_type = st.selectbox("Select conversion type", ["xlsx to csv", "csv to xlsx"])
        if st.button("Convert"):
            if conversion_type == "xlsx to csv":
                csv_data = df.to_csv(index=False)
                st.download_button(label="Download CSV",
                                   data=csv_data,
                                   file_name="converted_data.csv",
                                   mime="text/csv")
            elif conversion_type == "csv to xlsx":
                excel_data = convert_df_to_excel(df)
                st.download_button(label="Download XLSX",
                                   data=excel_data,
                                   file_name="converted_data.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # Final Download of Preprocessed Dataset
        st.header("Download Preprocessed Dataset")
        csv_preprocessed = df.to_csv(index=False)
        st.download_button(label="Download Final CSV",
                           data=csv_preprocessed,
                           file_name="preprocessed_data.csv",
                           mime="text/csv")
    else:
        st.info("Please upload a CSV or XLSX file to begin.")

if __name__ == "__main__":
    main()
