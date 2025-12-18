# from django.template.loader import render_to_string
# from io import BytesIO
# from datetime import datetime, timedelta
# from django.http import HttpResponse
# from django.conf import settings
# import os

# class AttendancePDFGenerator:
#     """Utility class for generating attendance PDF reports using WeasyPrint"""

#     @staticmethod
#     def _render_pdf_from_html(html_string):
#         """Helper to render PDF from HTML string using WeasyPrint"""
#         try:
#             # Import here to allow fallback if WeasyPrint fails
#             from weasyprint import HTML
#             result = BytesIO()
            
#             # Generate PDF with WeasyPrint
#             HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(result)
#             return result.getvalue()
            
#         except ImportError:
#             # Fallback to xhtml2pdf if WeasyPrint is not available
#             from xhtml2pdf import pisa
#             result = BytesIO()
#             pdf = pisa.CreatePDF(src=html_string, dest=result)
#             if pdf.err:
#                 raise Exception(f"Error generating PDF: {pdf.err}")
#             return result.getvalue()
            
#         except Exception as e:
#             # Final fallback - try xhtml2pdf if WeasyPrint fails
#             try:
#                 from xhtml2pdf import pisa
#                 result = BytesIO()
#                 pdf = pisa.CreatePDF(src=html_string, dest=result)
#                 if pdf.err:
#                     raise Exception(f"PDF generation failed: {e}")
#                 return result.getvalue()
#             except:
#                 raise Exception(f"PDF generation failed: {e}")

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
#             'report_type': 'company',
#         }
#         print("Total employees with attendance:", unique_employees)

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
#             'report_type': 'employee',
#         }

#         html_string = render_to_string('attendances/attendance_report.html', context)
#         pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
#         return pdf_file

#     @staticmethod
#     def generate_pdf_response(pdf_content, filename="attendance_report.pdf"):
#         """Create HTTP response with PDF"""
#         response = HttpResponse(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{filename}"'
#         response['Content-Length'] = len(pdf_content)
#         response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#         response['Pragma'] = 'no-cache'
#         response['Expires'] = '0'
#         return response





from django.template.loader import render_to_string
from io import BytesIO
from datetime import datetime
from xhtml2pdf import pisa
from django.http import HttpResponse


class AttendancePDFGenerator:
    """Utility class for generating attendance PDF reports using xhtml2pdf"""

    @staticmethod
    def _render_pdf_from_html(html_string):
        """Helper to render PDF from HTML string"""
        result = BytesIO()
        pdf = pisa.CreatePDF(src=html_string, dest=result)
        if pdf.err:
            raise Exception("Error generating PDF")
        return result.getvalue()

    @staticmethod
    def generate_report(attendances, company, filters=None):
        """Generate PDF report for company attendance"""
        total_records = attendances.count()
        nfc_count = attendances.filter(code='NFC').count()
        qr_count = attendances.filter(code='QR').count()
        unique_employees = attendances.values('user').distinct().count()

        # date range
        date_range = None
        if filters:
            start_date = filters.get('start_date')
            end_date = filters.get('end_date')
            if start_date and end_date:
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
            'date_range': date_range,
        }
        print("Total employee" , unique_employees)

        html_string = render_to_string('attendances/attendance_report.html', context)
        pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
        return pdf_file

    @staticmethod
    def generate_employee_report(attendances, employee, filters=None):
        """Generate PDF report for a specific employee"""
        total_records = attendances.count()
        nfc_count = attendances.filter(code='NFC').count()
        qr_count = attendances.filter(code='QR').count()

        # date range
        date_range = None
        if filters:
            start_date = filters.get('start_date')
            end_date = filters.get('end_date')
            if start_date and end_date:
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
        }

        html_string = render_to_string('attendances/attendance_report.html', context)
        pdf_file = AttendancePDFGenerator._render_pdf_from_html(html_string)
        return pdf_file





