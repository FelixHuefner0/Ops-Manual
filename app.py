import streamlit as st
from xhtml2pdf import pisa
from jinja2 import Environment, FileSystemLoader
import io
import base64

def encode_image_to_base64(image_file):
    if image_file is not None:
        return base64.b64encode(image_file.read()).decode("utf-8")
    return None

# Funktion zum PDF-Export
def convert_html_to_pdf(source_html):
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=result)
    return result.getvalue() if not pisa_status.err else None

# Jinja2-Template laden
def render_template(template_name, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    return template.render(context)

# Streamlit App UI
st.title("Aviation Operations Manual Generator")

chief_pilot = st.text_input("Chief Pilot Name", value="Elisha Chandra")
company_name = st.text_input("Name der Firma")
night_ops = st.checkbox("Night Operations Approved?")
uploaded_image = st.file_uploader("Logo oder Bild hochladen", type=["png", "jpg", "jpeg"])

above_400ft = st.checkbox("Approved for operations above 400 ft AGL?")
# Init Session State für Drohnen
if "drones" not in st.session_state:
    st.session_state.drones = []

# Neue Drohne hinzufügen
if st.button("➕ Drohne hinzufügen"):
    st.session_state.drones.append({"name": "", "version": ""})

# Drohnen bearbeiten
for i, drone in enumerate(st.session_state.drones):
    st.session_state.drones[i]["name"] = st.text_input(f"Drohnenname {i+1}", value=drone["name"], key=f"name_{i}")
    st.session_state.drones[i]["version"] = st.text_input(f"Version {i+1}", value=drone["version"], key=f"version_{i}")



if st.button("PDF generieren"):
    # ← Bild zuerst in Base64 konvertieren
    image_base64 = encode_image_to_base64(uploaded_image)

    # Dann Kontext zusammenstellen
    context = {
        "chief_pilot": chief_pilot,
        "company_name": company_name,
        "night_ops": night_ops,
        "above_400ft": above_400ft,
        "drones": st.session_state.drones,
        "uploaded_image": image_base64
    }

    html_out = render_template("template.html", context)
    pdf_bytes = convert_html_to_pdf(html_out)

    if pdf_bytes:
        st.success("PDF erfolgreich erstellt!")
        st.download_button("Download PDF", data=pdf_bytes, file_name="Aviation_Manual.pdf", mime="application/pdf")
    else:
        st.error("Fehler beim Erstellen der PDF.")
