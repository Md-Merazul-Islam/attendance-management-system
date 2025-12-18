

# from django.template.loader import render_to_string
# from weasyprint import HTML
# from datetime import datetime


# class AttendancePDFGenerator:
#     """Utility class for generating attendance PDF reports"""
    
#     @staticmethod
#     def generate_report(attendances, company, filters=None):
#         """
#         Generate PDF report from attendance data
#         """
#         # Calculate for  statistics
#         total_records = attendances.count()
#         nfc_count = attendances.filter(code='NFC').count()
#         qr_count = attendances.filter(code='QR').count()
#         unique_employees = attendances.values('user').distinct().count()
        
#         #  date range and convert to string
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
        
#         # context for template
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
        
#         # Render HTML template
#         html_string = render_to_string('attendances/attendance_report.html', context)
        
#         # Generate PDF
#         html = HTML(string=html_string)
#         pdf_file = html.write_pdf()
        
#         return pdf_file
    
#     @staticmethod
#     def generate_employee_report(attendances, employee, filters=None):
#         """
#         Generate PDF report for a specific employee
#         """
#         # Calculate statistics report 
#         total_records = attendances.count()
#         nfc_count = attendances.filter(code='NFC').count()
#         qr_count = attendances.filter(code='QR').count()
        
#         #  date range convert to string
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
        
#         # context for template
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
        
#         # Render HTML template
#         html_string = render_to_string('attendances/attendance_report.html', context)
        
#         # Generate PDF
#         html = HTML(string=html_string)
#         pdf_file = html.write_pdf()
        
#         return pdf_file