from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io, os, re

app = Flask(__name__)

LOGO_PATH = os.path.join("static", "logo.png")
PDF_PREFIX = "Ordem_Compra"

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

    # Criar PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.2 * cm, bottomMargin=2 * cm   # 🔹 Subido topo
    )

    s = getSampleStyleSheet()
    st = {
        "title": ParagraphStyle("title", parent=s["Heading1"], alignment=TA_CENTER, fontSize=16),
        "n": ParagraphStyle("n", parent=s["Normal"], fontSize=9),
        "small": ParagraphStyle("small", parent=s["Normal"], fontSize=8),
        "tabela": ParagraphStyle("tabela", parent=s["Normal"], fontSize=8.5, alignment=TA_LEFT),
        "center": ParagraphStyle("center", parent=s["Normal"], fontSize=10, alignment=TA_CENTER, spaceAfter=6)
    }

    e = []
    # 🔹 Subiu a logo e título
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=7.5 * cm, height=2.3 * cm)
        logo.hAlign = "CENTER"
        e += [logo, Spacer(1, 4)]

    e += [Paragraph("<b>ORDEM DE COMPRA</b>", st["title"]), Spacer(1, 6)]

    # 🔹 Empresa solicitante (centralizado)
    e.append(Paragraph("<b>EMPRESA SOLICITANTE</b>", st["center"]))
    cliente_data = [[Paragraph(f"<b>{k}</b>", st["n"]), Paragraph(str(v), st["n"])] for k, v in cliente.items()]
    tabela_cliente = Table(cliente_data, colWidths=[4 * cm, 11 * cm])
    tabela_cliente.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey)]))
    e += [tabela_cliente, Spacer(1, 10)]

    # 🔹 Filial / Fornecedor (centralizado)
    e.append(Paragraph("<b>FILIAL / FORNECEDOR</b>", st["center"]))
    filial_data = [[Paragraph(f"<b>{k}</b>", st["n"]), Paragraph(str(v), st["n"])] for k, v in filial.items()]
    tabela_filial = Table(filial_data, colWidths=[4 * cm, 11 * cm])
    tabela_filial.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey)]))
    e += [tabela_filial, Spacer(1, 12)]

    e.append(Paragraph(f"<b>Prazo de Entrega:</b> {prazo}", st["n"]))
    e.append(Spacer(1, 16))

    # 🔹 Lista de produtos (renomeado e espaçamento ajustado)
    e.append(Paragraph("<b>LISTAGEM DE PRODUTOS</b>", st["center"]))
    e.append(Spacer(1, 8))

    cols = [1.2*cm, 1.0*cm, 3.2*cm, 8.3*cm, 3.1*cm, 2.3*cm]
    data_table = [["ITEM", "QTD", "CÓDIGO", "DESCRIÇÃO", "PREÇO UNIT (R$)", "TOTAL (R$)"]]
    total = 0

    for i, item in enumerate(itens, start=1):
        q = item["qtd"]
        cod = item["cod"]
        desc = item["desc"]
        preco = float(item["preco"].replace(",", ".")) if item["preco"] else 0
        tot = float(item["tot"].replace(",", ".")) if item["tot"] else 0
        total += tot
        p_fmt = f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")   # 🔹 Adiciona R$
        t_fmt = f"R$ {tot:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")     # 🔹 Adiciona R$
        data_table.append([str(i), q, cod, Paragraph(desc, st["tabela"]), p_fmt, t_fmt])

    total_fmt = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    data_table.append(["", "", "", Paragraph("<b>TOTAL GERAL</b>", st["tabela"]), "", f"R$ {total_fmt}"])

    t = Table(data_table, colWidths=cols, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004C99")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "LEFT"),
        ("ALIGN", (4, 1), (5, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),  # 🔹 Mais respiro nas linhas
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    e += [t, Spacer(1, 20)]  # 🔹 Aumentado espaço após a tabela

    # 🔹 Pagamento e observações
    e.append(Paragraph(f"<b>Condição de Pagamento:</b> Boleto em {pagamento}", st["n"]))
    e.append(Spacer(1, 10))

    if obs:
        e.append(Paragraph("<b>OBSERVAÇÕES:</b>", st["n"]))
        e.append(Paragraph(obs, st["n"]))
        e.append(Spacer(1, 12))

    e.append(Paragraph("A ORDEM DE COMPRA DEVE SER ENVIADA PARA <b>convenios@farmaciassaojoao.com.br</b>", st["small"]))
    e.append(Paragraph("<i>*A via original deve ser entregue na filial da venda*</i>", st["small"]))
    e.append(Spacer(1, 36))
    e.append(Paragraph("Assinatura e carimbo: _________________________________", st["n"]))

    doc.build(e)
    buffer.seek(0)
    nome_arquivo = f"{PDF_PREFIX}_{cliente.get('Empresa', 'Documento').replace(' ', '_')}.pdf"
    return send_file(buffer, as_attachment=True, download_name=nome_arquivo, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
