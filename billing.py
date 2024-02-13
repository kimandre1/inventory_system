from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def create_pdf(order_id, results_inspect_order, customer_info, total_sum):
    pdf_filename = f"Ordere_{order_id}_faktura.pdf"

    # Create a PDF document
    pdf = canvas.Canvas(pdf_filename)
    
    # Add content to the PDF
    pdf.drawString(100, 800, f"Orderenummer: {order_id}")
    
    # Add details from the results_inspect_order
    for i, row in enumerate(results_inspect_order, start=1):
        y_position = 800 - i * 20
        pdf.drawString(100, y_position, f"Produkt: {row[1]}, Antall: {row[3]}, Pris per stykk: {row[4]}, Totalt: {row[5]}")

    # Add customer information
    pdf.drawString(100, 600, f"Kunde: {customer_info[0][0]} {customer_info[0][1]}")
    pdf.drawString(100, 580, f"Adresse: {customer_info[0][2]}, {customer_info[0][3]}")

    # Add total sum
    pdf.drawString(100, 560, f"Total Sum: {total_sum} kr")

    # Save the PDF
    pdf.save()

if __name__ == "__main__":
    create_pdf()