import streamlit as st
from trasncrever import transcrever_audio  # Importa a função de transcrição

# Interface Streamlit
st.title("Transcrição de Áudio para Texto")
st.write("Carregue um arquivo de áudio (.mp3 ou .ogg) para transcrevê-lo.")

# Uploader de arquivo, agora com suporte a .ogg
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["mp3", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")  # Exibe o áudio carregado
    
    # Realiza a transcrição quando o arquivo for carregado
    if st.button("Transcrever"):
        with st.spinner('Transcrevendo o áudio...'):
            transcricao = transcrever_audio(uploaded_file)  # Chama a função de transcrição
        
        st.write("### Transcrição:")
        st.write(transcricao)
        
        # Salvar o texto transcrito em um arquivo TXT
        output_file = "transcricao_audio.txt"  # Arquivo de saída
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcricao)
        
        # Link para download do arquivo TXT
        with open(output_file, "r", encoding="utf-8") as f:
            st.download_button(
                label="Baixar a transcrição em TXT",
                data=f.read(),
                file_name=output_file,
                mime="text/plain"
            )
