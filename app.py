import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import tempfile
from gtts import gTTS
import numpy as np

st.set_page_config(page_title='GERADOR TIKTOK LEVE', layout='centered')
st.title('🎬 Gerador TikTok - Celular Fraco')
st.caption('Cole o roteiro > Gera video vertical com legenda')

texto = st.text_area('Roteiro (30s)', 'Perdi 100 reais em 1 minuto no futuro. Entrei com 150x no QNT. Resultado? Liquidado. Aprendi: alavanca nao e atalho.', height=150)

cor_fundo = st.color_picker('Cor fundo', '#000000')
cor_texto = st.color_picker('Cor legenda', '#FFFFFF')

duracao = st.slider('Duração segundos', 10, 60, 20)

if st.button('GERAR VIDEO'):
    with st.spinner('Gerando... isso leva 20s no celular fraco'):
        # 1. Cria audio com gTTS (voz IA gratis)
        try:
            tts = gTTS(text=texto, lang='pt', slow=False)
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_audio.name)
            audio_path = temp_audio.name
        except:
            audio_path = None

        # 2. Cria imagem vertical 1080x1920 com texto
        W, H = 1080, 1920
        img = Image.new('RGB', (W, H), cor_fundo)
        draw = ImageDraw.Draw(img)

        # Tenta fonte, se nao tiver usa padrao
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()

        # Quebra texto
        linhas = textwrap.wrap(texto, width=28)
        texto_junto = "\n".join(linhas)

        # Centraliza
        bbox = draw.multiline_textbbox((0,0), texto_junto, font=font, spacing=20)
        text_w = bbox[2]-bbox[0]
        text_h = bbox[3]-bbox[1]
        x = (W - text_w)//2
        y = (H - text_h)//2 - 200

        # Sombra pra ler melhor
        draw.multiline_text((x+4, y+4), texto_junto, font=font, fill="black", spacing=20, align="center")
        draw.multiline_text((x, y), texto_junto, font=font, fill=cor_texto, spacing=20, align="center")

        # Salva imagem
        img_path = "/tmp/frame.png"
        img.save(img_path)

        # 3. Gera video MP4 a partir da imagem (sem precisar ffmpeg pesado)
        try:
            from moviepy.editor import ImageClip, AudioFileClip
            clip = ImageClip(img_path, duration=duracao)
            if audio_path:
                audio = AudioFileClip(audio_path)
                clip = clip.set_audio(audio.set_duration(duracao))
            video_path = "/tmp/tiktok_final.mp4"
            clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac', verbose=False, logger=None)
            st.success('Video gerado!')
            st.video(video_path)
            with open(video_path, 'rb') as f:
                st.download_button('BAIXAR VIDEO TIKTOK', f, file_name='video_tiktok.mp4')
        except Exception as e:
            # Fallback: se moviepy falhar, entrega imagem que vira video no TikTok
            st.warning('Seu Streamlit nao tem ffmpeg, mas da pra usar assim:')
            st.image(img_path)
            st.download_button('Baixar como imagem (posta como video no TikTok)', open(img_path,'rb'), file_name='tiktok.png')
            st.info('Dica: No TikTok, importa essa imagem > adiciona som > dura 20s automaticamente')

st.divider()
st.write('**Como postar:** Baixa > abre TikTok > + > Enviar > escolhe o video > adiciona legenda #trading #futuros #qnt')
