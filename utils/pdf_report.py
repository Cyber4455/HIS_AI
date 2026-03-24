from fpdf import FPDF
from datetime import datetime
import json

class HealthReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 100, 150)
        self.cell(0, 10, 'Health Intelligence System - Medical Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def generate_health_report(consultation_data: dict, output_path: str = None):
    pdf = HealthReportPDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 100, 150)
    pdf.cell(0, 10, 'Patient Symptoms', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, consultation_data.get('symptoms', 'Not provided'))
    pdf.ln(5)
    
    if consultation_data.get('predicted_diseases'):
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 100, 150)
        pdf.cell(0, 10, 'Predicted Conditions', 0, 1)
        
        try:
            diseases = json.loads(consultation_data['predicted_diseases'])
            for disease in diseases:
                pdf.set_font('Arial', 'B', 11)
                pdf.set_text_color(0, 0, 0)
                prob = disease.get('probability', 0) * 100
                pdf.cell(0, 8, f"• {disease.get('name', 'Unknown')}: {prob:.1f}%", 0, 1)
                
                if disease.get('precautions'):
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(0, 6, f"  Precautions: {', '.join(disease['precautions'])}", 0, 1)
                if disease.get('medicines'):
                    pdf.set_font('Arial', '', 10)
                    pdf.cell(0, 6, f"  Suggested medicines: {', '.join(disease['medicines'])}", 0, 1)
                pdf.ln(3)
        except:
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 8, consultation_data['predicted_diseases'])
        pdf.ln(5)
    
    if consultation_data.get('health_score'):
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 100, 150)
        pdf.cell(0, 10, 'Health Score', 0, 1)
        pdf.set_font('Arial', 'B', 20)
        
        score = consultation_data['health_score']
        if score > 75:
            pdf.set_text_color(0, 150, 0)
        elif score > 50:
            pdf.set_text_color(200, 150, 0)
        else:
            pdf.set_text_color(200, 0, 0)
        
        pdf.cell(0, 15, f"{score}/100", 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f"Risk Level: {consultation_data.get('risk_level', 'Unknown')}", 0, 1)
        pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 10, 'Medical Disclaimer', 0, 1)
    pdf.set_font('Arial', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, "This report is generated for demonstration purposes only. educational and It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for any medical concerns.")
    
    if output_path:
        pdf.output(output_path)
        return output_path
    else:
        return pdf.output(dest='S').encode('latin-1')
