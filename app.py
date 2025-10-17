from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io, os, re

app = Flask(__name__)

LOGO_PATH = os.path.join("static", "logo.png")

def only_digits(s):
    return re.sub(r"\D", "", s or "")

def is_valid_email(email):
    if not email or "@" not in email:
        return False
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar_pdf", methods=["POST"])
def gerar_pdf():
    data = request.json or {}
    cliente = data.get("cliente", {})
    filial = data.get("filial", {})
    itens = data.get("itens", [])
    obs = data.get("obs", "")
    pagamento = data.get("pagamento", "")
    prazo = data.get("prazo", "")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    styles = getSampleStyleSheet()
    title = ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER, spaceAfter=12)
    normal = ParagraphStyle(name='Normal', fontSize=10, alignment=TA_LEFT, spaceAfter=6)

    elements = []

    # Logo
    if os.path.exists(LOGO_PATH):
        elements.append(Image(LOGO_PATH, width=80, height=40))
        elements.append(Spacer(1, 6))

    # Título
    elements.append(Paragraph("Ordem de Compra", title))
    elements.append(Spacer(1, 12))

    # Empresa Solicitante
    elements.append(Paragraph("<b>Empresa Solicitante</b>", styles["Heading4"]))
    data_cliente = [[k, v] for k, v in cliente.items() if v.strip()]
    table_cliente = Table(data_cliente, colWidths=[5 * cm, 10 * cm])
    table_cliente.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, 'black'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table_cliente)
    elements.append(Spacer(1, 12))

    # Filial / Fornecedor
    elements.append(Paragraph("<b>Filial / Fornecedor</b>", styles["Heading4"]))
    data_filial = [[k, v] for k, v in filial.items() if v.strip()]
    table_filial = Table(data_filial, colWidths=[5 * cm, 10 * cm])
    table_filial.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, 'black'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table_filial)
    elements.append(Spacer(1, 12))

    # Condições de pagamento
    elements.append(Paragraph("<b>Condições de Pagamento:</b> " + pagamento, normal))
    elements.append(Paragraph("<b>Prazo de Entrega:</b> " + prazo, normal))
    elements.append(Spacer(1, 12))

    # Observações
    if obs:
        elements.append(Paragraph("<b>Observações:</b>", styles["Heading4"]))
        elements.append(Paragraph(obs, normal))
        elements.append(Spacer(1, 12))

    # Itens
    elements.append(Paragraph("<b>Inclusão de Produtos</b>", styles["Heading4"]))
    data_itens = [["Produto", "Quantidade", "Valor (R$)"]] + [[i["produto"], i["quantidade"], i["valor"]] for i in itens]
    table_itens = Table(data_itens, colWidths=[8 * cm, 3 * cm, 4 * cm])
    table_itens.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, 'black'),
        ('GRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('BACKGROUND', (0, 0), (-1, 0), '#f0f0f0'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER')
    ]))
    elements.append(table_itens)

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Ordem_Compra.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
