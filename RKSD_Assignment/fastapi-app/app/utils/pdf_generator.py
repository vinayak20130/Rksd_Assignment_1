from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

# Define color scheme
PRIMARY_COLOR = colors.HexColor('#1a73e8')  # Google Blue
SECONDARY_COLOR = colors.HexColor('#4285f4')  # Lighter Blue
ACCENT_COLOR = colors.HexColor('#fbbc04')  # Yellow
TEXT_COLOR = colors.HexColor('#202124')  # Dark Gray
LIGHT_BG = colors.HexColor('#f8f9fa')  # Light Gray
SUCCESS_COLOR = colors.HexColor('#34a853')  # Green
PENDING_COLOR = colors.HexColor('#ea4335')  # Red
CURRENT_COLOR = colors.HexColor('#fbbc04')  # Yellow

def format_date(date_obj):
    """Format datetime object to a readable string"""
    if not date_obj:
        return "N/A"
    return date_obj.strftime("%B %d, %Y")

def generate_application_pdf(application_data):
    """
    Generate a PDF document with application details
    
    Args:
        application_data: Dictionary containing application details
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    
    # Create the document with margins
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    # Get the default styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    # Title style
    title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=SECONDARY_COLOR,
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    # Section header style
    section_style = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=LIGHT_BG,
        borderPadding=5,
        borderRadius=5,
        backColor=LIGHT_BG
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceAfter=8,
        fontName='Helvetica',
        leading=14
    )
    
    # Field label style
    label_style = ParagraphStyle(
        name='FieldLabel',
        parent=styles['Normal'],
        fontSize=11,
        textColor=SECONDARY_COLOR,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Field value style
    value_style = ParagraphStyle(
        name='FieldValue',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        fontName='Helvetica',
        leading=14
    )
    
    # Experience date style
    date_style = ParagraphStyle(
        name='DateStyle',
        parent=styles['Italic'],
        fontSize=10,
        textColor=colors.gray,
        fontName='Helvetica-Oblique',
        leading=12
    )
    
    # Create the document content
    content = []
    
    # Add a header with a horizontal line
    header = Paragraph("Candidate Application Details", title_style)
    content.append(header)
    
    # Add a horizontal line
    content.append(Spacer(1, 0.1 * inch))
    
    # Basic Information Section
    content.append(Paragraph("Basic Information", section_style))
    content.append(Spacer(1, 0.1 * inch))
    
    # Create a table for basic information
    basic_info_data = [
        [Paragraph("<b>Candidate Name:</b>", label_style), 
         Paragraph(application_data['candidate_name'], value_style)],
        [Paragraph("<b>Role:</b>", label_style), 
         Paragraph(application_data['role_name'], value_style)],
        [Paragraph("<b>Application Date:</b>", label_style), 
         Paragraph(format_date(application_data['application_date']), value_style)],
        [Paragraph("<b>Status:</b>", label_style), 
         Paragraph(application_data['status'].value.capitalize(), value_style)],
        [Paragraph("<b>Current Stage:</b>", label_style), 
         Paragraph(f"{application_data['current_stage_name']} (Sequence: {application_data['current_stage_sequence']})", value_style)]
    ]
    
    # Add rating if available
    if application_data.get('rating'):
        # Create star rating
        rating_value = application_data['rating']
        stars = "★" * rating_value + "☆" * (5 - rating_value)
        
        # Create a paragraph with the rating stars and apply color directly
        rating_paragraph = Paragraph(stars, ParagraphStyle(
            name='RatingStyle',
            parent=styles['Normal'],
            textColor=ACCENT_COLOR,
            fontName='Helvetica-Bold',
            fontSize=14
        ))
        
        rating_text = Paragraph(f"({rating_value}/5)", value_style)
        
        # Create a table to hold both the stars and the rating text
        rating_table = Table([[rating_paragraph, rating_text]], colWidths=[1*inch, 1*inch])
        rating_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 5),
        ]))
        
        basic_info_data.append([
            Paragraph("<b>Rating:</b>", label_style),
            rating_table
        ])
    
    # Create and style the table
    basic_info_table = Table(basic_info_data, colWidths=[1.5*inch, 4*inch])
    basic_info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_BG),
        ('RIGHTPADDING', (0, 0), (0, -1), 10),
        ('LEFTPADDING', (0, 0), (0, -1), 5),
    ]))
    
    content.append(basic_info_table)
    content.append(Spacer(1, 0.3 * inch))
    
    # Experience Section
    content.append(Paragraph("Work Experience", section_style))
    content.append(Spacer(1, 0.1 * inch))
    
    if application_data.get('experiences') and len(application_data['experiences']) > 0:
        for exp in application_data['experiences']:
            # Create a box for each experience
            exp_data = []
            
            # Experience title
            exp_title = f"{exp.position} at {exp.company_name}"
            exp_data.append([Paragraph(f"<b>{exp_title}</b>", subtitle_style)])
            
            # Date range
            date_range = f"{format_date(exp.start_date)} - {format_date(exp.end_date) if exp.end_date else 'Present'}"
            exp_data.append([Paragraph(date_range, date_style)])
            
            # Description
            if exp.description:
                exp_data.append([Paragraph(exp.description, normal_style)])
            
            # Create a table for the experience
            exp_table = Table(exp_data, colWidths=[5.5*inch])
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, LIGHT_BG),
                ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BG),
            ]))
            
            content.append(exp_table)
            content.append(Spacer(1, 0.2 * inch))
    else:
        content.append(Paragraph("No work experience provided", normal_style))
    
    content.append(Spacer(1, 0.2 * inch))
    
    # Role Stages Section
    content.append(Paragraph("Application Process Stages", section_style))
    content.append(Spacer(1, 0.1 * inch))
    
    if application_data.get('role_stages') and len(application_data['role_stages']) > 0:
        # Create a table for stages
        stage_data = [["Stage", "Sequence", "Status"]]
        
        current_stage_id = application_data['current_stage_id']
        
        # Check if application is already accepted
        is_accepted = application_data['status'].value.lower() == 'accepted'
        
        for stage in application_data['role_stages']:
            status = ""
            status_color = colors.black
            
            if is_accepted:
                # If application is accepted, all stages are completed
                status = "Completed"
                status_color = SUCCESS_COLOR
            elif stage.stage_sequence < application_data['current_stage_sequence']:
                status = "Completed"
                status_color = SUCCESS_COLOR
            elif stage.stage_id == current_stage_id:
                status = "Current"
                status_color = CURRENT_COLOR
            else:
                status = "Pending"
                status_color = PENDING_COLOR
                
            # Create a paragraph with the status text and apply color directly
            status_paragraph = Paragraph(status, ParagraphStyle(
                name=f'Status_{status}',
                parent=styles['Normal'],
                textColor=status_color,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
                
            stage_data.append([
                stage.stage_name, 
                str(stage.stage_sequence), 
                status_paragraph
            ])
        
        # Create and style the table
        stage_table = Table(stage_data, colWidths=[2.5*inch, 1*inch, 2*inch])
        stage_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        content.append(stage_table)
    else:
        content.append(Paragraph("No stages defined for this role", normal_style))
    
    # Add footer with timestamp
    content.append(Spacer(1, 0.5 * inch))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer_style = ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    content.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(content)
    buffer.seek(0)
    return buffer 