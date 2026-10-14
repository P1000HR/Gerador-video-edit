import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap

st.set_page_config(page_title='GERADOR TIKTOK', layout='centered')
st.title('Gerador TikTok - Celular Fraco')

texto = st.text_area('Roteiro (30s)', 'Perdi 100 reais em 1 minuto no futuro. Entrei com 150x no QNT. Resultado? Liquidado.', height=150)

def criar_imagem(txt):
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H), (0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    linhas = textwrap.wrap(txt, width=20)
    final = "\n".join(linhas)
    bbox = draw.multiline_textbbox((0,0), final, font=font, spacing=25)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    x = (W - tw)//2
    y = (H - th)//2
    for dx in [-3,0,3]:
        for dy in [-3,0,3]:
            draw.multiline_text((x+dx, y+dy), final, font=font, fill="black", align="center", spacing=25)
    draw.multiline_text((x, y), final, font=font, fill="white", align="center", spacing=25)
    return img

if st.button('GERAR VIDEO', type="primary", use_container_width=True):
    imagem = criar_imagem(texto)
    st.image(imagem, use_container_width=True)
    imagem.save("/tmp/final.png")
    with open("/tmp/final.png", "rb") as f:
        st.download_button('BAIXAR', f, 'tiktok.png', 'image/png', use_container_width=True)
