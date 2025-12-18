from django.template.loader import render_to_string
from io import BytesIO
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.conf import settings
import os

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("Warning: WeasyPrint is not installed. Falling back to xhtml2pdf.")


class AttendancePDFGenerator:
    """Utility class for generating attendance PDF reports using WeasyPrint"""
    
    @staticmethod
    def _render_pdf_from_html(html_string):
        """Helper to render PDF from HTML string using WeasyPrint"""
        result = BytesIO()
        
        try:
            if WEASYPRINT_AVAILABLE:
                # Create font configuration
                font_config = FontConfiguration()
                
                # Base CSS for PDF
                base_css = '''
                    @page {
                        size: A4;
                        margin: 1.5cm;
                        @bottom-right {
                            content: "Page " counter(page) " of " counter(pages);
                            font-size: 10px;
                            color: #666;
                        }
                        @top-center {
                            content: "Attendance Report";
                            font-size: 12px;
                            color: #666;
                        }
                    }
                    
                    body {
                        font-family: Arial, Helvetica, sans-serif;
                        font-size: 12px;
                        line-height: 1.4;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }
                    
                    h1, h2, h3, h4 {
                        margin-top: 0;
                    }
                    
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    
                    th {
                        text-align: left;
                        font-weight: bold;
                    }
                    
                    .text-center {
                        text-align: center;
                    }
                    
                    .text-right {
                        text-align: right;
                    }
                    
                    .bold {
                        font-weight: bold;
                    }
                '''
                
                # Generate PDF with WeasyPrint
                HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(
                    result,
                    stylesheets=[CSS(string=base_css)],
                    font_config=font_config
                )
            else:
                # Fallback to xhtml2pdf if WeasyPrint is not available
                from xhtml2pdf import pisa
                pdf = pisa.CreatePDF(src=html_string, dest=result)
                if pdf.err:
                    raise Exception(f"Error generating PDF: {pdf.err}")
                
        except Exception as e:
            # Final fallback - try xhtml2pdf if WeasyPrint fails
            try:
                from xhtml2pdf import pisa
                result = BytesIO()
                pdf = pisa.CreatePDF(src=html_string, dest=result)
                if pdf.err:
                    raise Exception(f"PDF generation failed: {e}")
            except:
                raise Exception(f"PDF generation failed: {e}")
        
        return result.getvalue()

    @staticmethod
    def generate_report(attendances, company, filters=None):
        """Generate PDF report for company attendance"""
        total_records = attendances.count()
        nfc_count = attendances.filter(code='NFC').count()
        qr_count = attendances.filter(code='QR').count()
        unique_employees = attendances.values('user').distinct().count()
        
        # Get total company employees for better reporting
        total_company_employees = company.users.count() if hasattr(company, 'users') else 0

        # Date range formatting
        date_range = None
        if filters:
            start_date = filters.get('start_date')
            end_date = filters.get('end_date')
            if start_date and end_date:
                if start_date == end_date:
                    date_range = start_date.strftime('%B %d, %Y')
                else:
                    date_range = f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
            elif start_date:
                date_range = f"From {start_date.strftime('%B %d, %Y')}"
            elif end_date:
                date_range = f"Until {end_date.strftime('%B %d, %Y')}"

        context = {
            'attendances': attendances,
            'company_name': company.company_name,
            'location': company.location or 'N/A',
            'report_date': datetime.now().strftime('%B %d, %Y'),
            'generated_at': datetime.now().strftime('%B %d, %Y at %H:%M'),
            'total_records': total_records,
            'nfc_count': nfc_count,
            'qr_count': qr_count,
            'unique_employees': unique_employees,
            'total_company_employees': total_company_employees,
            'date_range': date_range,
            'report_type': 'company',
        }

        html_string = render_to_string('attendances/attendance_report.html', context)
        pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
        return pdf_file

    @staticmethod
    def generate_employee_report(attendances, employee, filters=None):
        """Generate PDF report for a specific employee"""
        total_records = attendances.count()
        nfc_count = attendances.filter(code='NFC').count()
        qr_count = attendances.filter(code='QR').count()
        
        # Calculate attendance rate if date range is provided
        attendance_rate = None
        if filters and filters.get('start_date') and filters.get('end_date'):
            start_date = filters.get('start_date')
            end_date = filters.get('end_date')
            # Calculate working days (Monday-Friday)
            delta = (end_date - start_date).days + 1
            working_days = 0
            for i in range(delta):
                day = start_date + timedelta(days=i)
                if day.weekday() < 5:  # 0-4 = Monday to Friday
                    working_days += 1
            
            if working_days > 0:
                attendance_rate = round((total_records / working_days) * 100, 1)

        # Date range formatting
        date_range = None
        if filters:
            start_date = filters.get('start_date')
            end_date = filters.get('end_date')
            if start_date and end_date:
                if start_date == end_date:
                    date_range = start_date.strftime('%B %d, %Y')
                else:
                    date_range = f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
            elif start_date:
                date_range = f"From {start_date.strftime('%B %d, %Y')}"
            elif end_date:
                date_range = f"Until {end_date.strftime('%B %d, %Y')}"

        context = {
            'attendances': attendances,
            'company_name': employee.company.company_name if employee.company else 'N/A',
            'location': employee.company.location if employee.company else 'N/A',
            'report_date': datetime.now().strftime('%B %d, %Y'),
            'generated_at': datetime.now().strftime('%B %d, %Y at %H:%M'),
            'total_records': total_records,
            'nfc_count': nfc_count,
            'qr_count': qr_count,
            'unique_employees': 1,
            'date_range': date_range,
            'employee_name': employee.full_name,
            'attendance_rate': attendance_rate,
            'report_type': 'employee',
        }

        html_string = render_to_string('attendances/attendance_report.html', context)
        pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
        return pdf_file

    @staticmethod
    def generate_pdf_response(pdf_content, filename="attendance_report.pdf"):
        """Create HTTP response with PDF"""
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(pdf_content)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response















# from django.template.loader import render_to_string
# from io import BytesIO
# from datetime import datetime
# from xhtml2pdf import pisa
# from django.http import HttpResponse


# class AttendancePDFGenerator:
#     """Utility class for generating attendance PDF reports using xhtml2pdf"""

#     @staticmethod
#     def _render_pdf_from_html(html_string):
#         """Helper to render PDF from HTML string"""
#         result = BytesIO()
#         pdf = pisa.CreatePDF(src=html_string, dest=result)
#         if pdf.err:
#             raise Exception("Error generating PDF")
#         return result.getvalue()

#     @staticmethod
#     def generate_report(attendances, company, filters=None):
#         """Generate PDF report for company attendance"""
#         total_records = attendances.count()
#         nfc_count = attendances.filter(code='NFC').count()
#         qr_count = attendances.filter(code='QR').count()
#         unique_employees = attendances.values('user').distinct().count()

#         # date range
#         date_range = None
#         if filters:
#             start_date = filters.get('start_date')
#             end_date = filters.get('end_date')
#             if start_date and end_date:
#                 date_range = f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
#             elif start_date:
#                 date_range = f"From {start_date.strftime('%B %d, %Y')}"
#             elif end_date:
#                 date_range = f"Until {end_date.strftime('%B %d, %Y')}"

#         context = {
#             'attendances': attendances,
#             'company_name': company.company_name,
#             'location': company.location or 'N/A',
#             'report_date': datetime.now().strftime('%B %d, %Y'),
#             'generated_at': datetime.now().strftime('%B %d, %Y at %H:%M'),
#             'total_records': total_records,
#             'nfc_count': nfc_count,
#             'qr_count': qr_count,
#             'unique_employees': unique_employees,
#             'date_range': date_range,
#         }
#         print("Total employee" , unique_employees)

#         html_string = render_to_string('attendances/attendance_report.html', context)
#         pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
#         return pdf_file

#     @staticmethod
#     def generate_employee_report(attendances, employee, filters=None):
#         """Generate PDF report for a specific employee"""
#         total_records = attendances.count()
#         nfc_count = attendances.filter(code='NFC').count()
#         qr_count = attendances.filter(code='QR').count()

#         # date range
#         date_range = None
#         if filters:
#             start_date = filters.get('start_date')
#             end_date = filters.get('end_date')
#             if start_date and end_date:
#                 date_range = f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
#             elif start_date:
#                 date_range = f"From {start_date.strftime('%B %d, %Y')}"
#             elif end_date:
#                 date_range = f"Until {end_date.strftime('%B %d, %Y')}"

#         context = {
#             'attendances': attendances,
#             'company_name': employee.company.company_name if employee.company else 'N/A',
#             'location': employee.company.location if employee.company else 'N/A',
#             'report_date': datetime.now().strftime('%B %d, %Y'),
#             'generated_at': datetime.now().strftime('%B %d, %Y at %H:%M'),
#             'total_records': total_records,
#             'nfc_count': nfc_count,
#             'qr_count': qr_count,
#             'unique_employees': 1,
#             'date_range': date_range,
#             'employee_name': employee.full_name,
#         }

#         html_string = render_to_string('attendances/attendance_report.html', context)
#         pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
#         return pdf_file

