import streamlit as st
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from datetime import date, timedelta
import io

# PDF-Erzeugung aus HTML
def convert_html_to_pdf(source_html):
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=result)
    return result.getvalue() if not pisa_status.err else None

# Template-Rendering aus templates/
def render_template(template_name, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    return template.render(context)

# Streamlit UI
st.title("RPAS Operations Manual Form")

version_number = st.text_input("Version Number", value="1")
company_name = st.text_input("Company Name", value="FlyFast")
chief_remote_pilote = st.text_input("Chief Remote Pilote", value="John Doe")
include_tethered_ops = st.checkbox("Include tethered operations?")

# PDF Creation

if st.button("PDF generieren") and company_name:
    issue_date = date.today().strftime("%d-%m-%Y")
    next_review_date = (date.today() + timedelta(days=365)).strftime("%d-%m-%Y")

    context = {
        "company_name": company_name,
        "issue_date": issue_date,
        "next_review_date": next_review_date,
        "approved_by": chief_remote_pilote,
        "version_number": version_number,
        "tethered_ops": include_tethered_ops
    }

    # Render templates
    section_templates = ["title.html", "applicability.html", "1_operate"]
    section_html = [render_template(tmpl, context) for tmpl in section_templates]
    combined_content = "\n".join(section_html)

    # embed in layout
    env = Environment(loader=FileSystemLoader("templates"))
    layout_template = env.get_template("layout.html")
    full_html = layout_template.render(context | {"content": combined_content})

    pdf_bytes = convert_html_to_pdf(full_html)

    if pdf_bytes:
        st.success("PDF erfolgreich erstellt!")
        st.download_button("Download PDF", data=pdf_bytes, file_name="Titelblatt.pdf", mime="application/pdf")
    else:
        st.error("Fehler beim Erstellen der PDF.")
