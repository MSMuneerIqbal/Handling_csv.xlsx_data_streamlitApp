# Data Explorer and Preprocessing App

This Streamlit-based application provides a comprehensive, user-friendly interface for exploring, preprocessing, and visualizing your data. It is designed to handle datasets in both CSV and XLSX formats and includes a variety of features that facilitate data cleaning, analysis, and conversion.

## Key Features

### Data Upload and Overview
- **File Upload:** Easily upload CSV or XLSX files.
- **Data Preview:** Automatically display the first 10 rows of your dataset.
- **Dataset Insights:** View dataset shape, a detailed statistical summary, and a count of missing values.

### Row and Column Management
- **View Specific Rows:** Enter a desired number of rows to view and display them with a simple button click.
- **Display Column Names:** Get a quick overview of all column names.
- **Display Column Data Types:** See the data type for each column.
- **Column Removal:** Select and remove unwanted columns from your dataset via a dedicated button.

### Missing Value Handling
- **Numeric Columns:** Choose to fill missing numeric values using Mean, Median, or Mode.
- **Object Columns:** Handle missing object-type data by filling with Mode, a default value ("Unknown"), or a custom value provided by the user.
- **Apply Treatments:** Use a button to apply the selected missing value treatment methods to your data.

### Data Visualization
- **Plot Options:** Generate various plots including Line, Bar, Scatter, Histogram, and Correlation Heatmap.
- **Dynamic Selection:** Choose which columns to include in the plots.
- **Generate & Download Plots:** Create plots with a button click and download them as PNG images.

### File Conversion
- **Format Conversion:** Convert between XLSX and CSV formats.
- **Download Converted Files:** Instantly download the file in the converted format.

### Final Dataset Download
- **Export Data:** After preprocessing, download the final dataset as a CSV file for further analysis.

## How It Works
1. **Upload:** Start by uploading your dataset using the sidebar.
2. **Explore:** View the dataset overview including rows, columns, and missing values.
3. **Customize:** Remove unwanted columns and view specific rows as needed.
4. **Clean:** Apply various missing value treatments tailored for numeric and object columns.
5. **Visualize:** Generate visualizations with dynamic column selection and download your plots.
6. **Convert:** Switch between file formats (CSV ↔ XLSX) with ease.
7. **Download:** Save your preprocessed dataset for future use.

## Technologies Used
- **Streamlit:** For creating the interactive web application interface.
- **Pandas:** For data manipulation and analysis.
- **Matplotlib & Seaborn:** For data visualization.
- **XlsxWriter:** For handling Excel file exports during format conversion.

This app is an ideal tool for data scientists, analysts, and anyone looking to quickly explore and preprocess their data with a powerful yet simple interface.
