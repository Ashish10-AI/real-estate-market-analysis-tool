from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
import os
from datetime import date

def generate_market_report(df, output_filename="Market_Report.pdf"):
    """Generates a basic PDF market report using ReportLab."""
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports', output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"Real Estate Market Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Date: {date.today()}", styles['Normal']))
    story.append(Spacer(1, 20))

    if df.empty:
        story.append(Paragraph("No data available for the report.", styles['Normal']))
        doc.build(story)
        return output_path

    # Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    avg_price = df['price'].mean()
    total_listings = len(df)
    summary_text = f"The current market contains {total_listings} tracked properties with an average price of INR {avg_price:,.2f}."
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 20))

    # Locality Table
    story.append(Paragraph("Locality Price Summary", styles['Heading2']))
    
    # Calculate simple stats
    loc_stats = df.groupby('locality')['price'].mean().reset_index().round(2)
    loc_stats.columns = ['Locality', 'Avg Price (INR)']
    
    # Convert to list for ReportLab Table
    data = [loc_stats.columns.tolist()] + loc_stats.values.tolist()
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t)

    doc.build(story)
    return output_path
