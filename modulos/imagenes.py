import re
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageOps

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
}
TAMANO_TARJETA = (480, 360)  # todas las imágenes salen con la misma proporción


def normalizar_url_imagen(valor):
    """Devuelve una URL directa de imagen o None. Es idempotente."""
    if valor is None:
        return None
    s = str(valor).strip().strip("\"'")
    if not s or s.lower() in ("nan", "none"):
        return None

    # Formato Markdown [texto](url)
    m = re.search(r"\]\((.+?)\)", s)
    if m:
        s = m.group(1).strip()
    # Fórmula =HYPERLINK("url","texto")
    m = re.search(r'HYPERLINK\(\s*"([^"]+)"', s, re.I)
    if m:
        s = m.group(1).strip()

    if s.startswith("//"):
        s = "https:" + s
    if not re.match(r"^https?://", s, re.I):
        return None

    # Google Drive -> enlace directo
    m = (re.search(r"drive\.google\.com/file/d/([\w-]+)", s)
         or re.search(r"drive\.google\.com/(?:open|uc)\?.*?id=([\w-]+)", s))
    if m:
        return f"https://drive.google.com/uc?export=view&id={m.group(1)}"

    # Dropbox -> enlace directo
    if "dropbox.com" in s:
        if re.search(r"[?&]dl=\d", s):
            s = re.sub(r"([?&])dl=\d", r"\1raw=1", s)
        elif "raw=1" not in s:
            s += ("&" if "?" in s else "?") + "raw=1"
    return s


@st.cache_data(ttl=86400, show_spinner=False)
def _descargar(url: str) -> bytes:
    # Si lanza excepción, Streamlit NO la cachea (así un fallo temporal no se queda 24 h)
    r = requests.get(url, headers=HEADERS, timeout=6)
    r.raise_for_status()
    if len(r.content) > 8_000_000:
        raise ValueError("Imagen demasiado grande")
    img = Image.open(BytesIO(r.content))
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageOps.fit(img, TAMANO_TARJETA)  # recorte tipo object-fit: cover
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def obtener_imagen(valor):
    url = normalizar_url_imagen(valor)
    if not url:
        return None
    try:
        return _descargar(url)
    except Exception:
        return None


def mostrar_imagen_producto(valor):
    data = obtener_imagen(valor)
    if data:
        st.image(data)
    else:
        st.markdown(
            "<div style='height:180px;display:flex;align-items:center;"
            "justify-content:center;border-radius:6px;background:#f0f2f6;"
            "font-size:2.5rem;'>📦</div>",
            unsafe_allow_html=True,
        )