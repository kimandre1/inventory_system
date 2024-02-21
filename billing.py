from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def create_pdf(order_id, billing_nr, results_inspect_order, customer_info, total_sum):
    pdf_filename = f"Ordre_{order_id}_{billing_nr}_faktura.pdf"

    # Create a PDF document
    pdf = canvas.Canvas(pdf_filename)

    # Add content to the PDF
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, 800, f"Faktura {billing_nr}")

    # Reset font
    pdf.setFont("Helvetica", 14)

    # Add order number below fakturanummer
    pdf.drawString(50, 780, f"Ordrenummer: {order_id}")

    # Add details from the results_inspect_order using a table
    data = [["Produkt", "Antall", "Pris per stykk", "Totalt"]]

    for row in results_inspect_order:
        data.append([row[1], row[3], row[4], row[5]])

    table = Table(data, colWidths=[150, 50, 100, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ]))

    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, 50, 740 - (len(results_inspect_order) + 1) * 20)

    # Add customer information
    pdf.drawString(50, 500, f"Kunde: {customer_info[0][0]} {customer_info[0][1]}")
    pdf.drawString(50, 480, f"Adresse: {customer_info[0][2]}, {customer_info[0][3]}")

    # Add total sum
    pdf.drawString(50, 460, f"Total Sum: {total_sum} kr")

    # Save the PDF
    pdf.save()

if __name__ == "__main__":
    # Testarguments
    create_pdf(order_id="123", results_inspect_order=[["1", "ProductA", 2, 10, 20], ["2", "ProductB", 3, 15, 45]],
               customer_info=[["John", "Doe", "Street", "City"]], total_sum=65)
