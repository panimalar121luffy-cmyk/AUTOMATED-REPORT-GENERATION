# Importing necessary libraries
import pandas as pd       # For handling CSV data and analysis
import numpy as np        # For generating random sample data
from fpdf import FPDF     # For creating PDF reports
from fpdf.enums import XPos, YPos   # Needed to avoid deprecation warnings
from datetime import datetime       # For timestamp in report

# Class to read and analyze data
class DataAnalyzer:
    def __init__(self, file_path):   
        # Load CSV file into a DataFrame
        self.df = pd.read_csv(file_path)
        self.file_path = file_path
    
    def analyze(self):
        """Perform comprehensive data analysis"""
        # Return dictionary with key metrics
        return {
            'records': len(self.df),   # Total rows
            'columns': len(self.df.columns),   # Total columns
            'total_revenue': self.df['Revenue'].sum() if 'Revenue' in self.df.columns else 0,
            'avg_revenue': self.df['Revenue'].mean() if 'Revenue' in self.df.columns else 0,
            'top_product': self.df.groupby('Product')['Revenue'].sum().idxmax() if 'Product' in self.df.columns else 'N/A',
            'missing_values': self.df.isnull().sum().sum()   # Count of missing values
        }

# Class to generate PDF report
class PDFReport(FPDF):
    def header(self):
        # Title
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(25, 85, 130)
        self.cell(0, 10, 'Data Analysis Report', align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)   # Fixed warning
        
        # Timestamp
        self.set_font('Helvetica', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)   # Fixed warning
        self.ln(10)
    
    def footer(self):
        # Page number at bottom
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
    
    def add_table(self, df, title):
        # Section title
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(25, 85, 130)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)   # Fixed warning
        
        col_width = (self.w - 30) / len(df.columns)
        row_height = 8
        
        # Table headers
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(25, 85, 130)
        self.set_text_color(255, 255, 255)
        for col in df.columns:
            self.cell(col_width, row_height, str(col), border=1, fill=True, align='C')
        self.ln()
        
        # Table data (first 10 rows only)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        for _, row in df.head(10).iterrows():
            for col in df.columns:
                self.cell(col_width, row_height, str(row[col])[:15], border=1, align='C')
            self.ln()
        self.ln(5)

# Main function to generate report
def generate_report(csv_file, output_pdf="report.pdf"):
    """Main function: Read → Analyze → Generate PDF"""
    
    # Step 1: Read data
    print("Reading data...")
    analyzer = DataAnalyzer(csv_file)
    
    # Step 2: Analyze data
    print("Analyzing...")
    analysis = analyzer.analyze()
    
    # Step 3: Generate PDF
    print("Creating PDF...")
    pdf = PDFReport()
    pdf.add_page()
    
    # Executive Summary section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Executive Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT)   # Fixed warning
    
    pdf.set_font('Helvetica', '', 11)
    metrics = [
        f"Records: {analysis['records']:,}",
        f"Columns: {analysis['columns']}",
        f"Total Revenue: ${analysis['total_revenue']:,.2f}",
        f"Avg Revenue: ${analysis['avg_revenue']:,.2f}",
        f"Top Product: {analysis['top_product']}",
        f"Missing Values: {analysis['missing_values']}"
    ]
    
    # Print metrics
    for metric in metrics:
        pdf.cell(0, 8, metric, new_x=XPos.LMARGIN, new_y=YPos.NEXT)   # Fixed warning
    
    # Add sample data table
    pdf.add_page()
    pdf.add_table(analyzer.df, "Sample Data (First 10 Records)")
    
    # Save PDF
    pdf.output(output_pdf)
    print(f"Report saved: {output_pdf}")

# Helper function to create sample data for testing
def create_sample_data():
    data = {
        'Date': pd.date_range('2025-01-01', periods=20),
        'Product': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor'], 20),
        'Quantity': np.random.randint(1, 10, 20),
        'Price': np.random.uniform(20, 1000, 20),
        'Revenue': np.random.uniform(50, 2000, 20),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 20)
    }
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)
    return 'data.csv'

# Run program
if __name__ == "__main__":   
    # Use sample data (can replace with your own CSV file)
    csv_file = create_sample_data()
    generate_report(csv_file)
