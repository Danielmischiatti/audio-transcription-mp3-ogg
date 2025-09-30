import streamlit as st
from trasncrever import transcrever_audio  # Importa a função de transcrição

# Interface Streamlit
st.title("Transcrição de Áudio para Texto")
st.write("Carregue um arquivo de áudio (.mp3, .ogg, .opus) para transcrevê-lo.")

# Uploader de arquivo, agora com suporte a .opus
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["mp3", "ogg", "opus"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")  # Exibe o áudio carregado
    
    # Realiza a transcrição quando o arquivo for carregado
    if st.button("Transcrever"):
        with st.spinner('Transcrevendo o áudio...'):
            transcricao = transcrever_audio(uploaded_file)  # Chama a função de transcrição
        
        st.write("### Transcrição:")
        st.write(transcricao)
        
        # Fornecer a transcrição para o download sem salvar no arquivo local
        st.download_button(
            label="Baixar a transcrição em TXT",
            data=transcricao,  # Passa o texto diretamente como dados
            file_name="transcricao_audio.txt",  # Nome do arquivo de download
            mime="text/plain"  # Tipo MIME do arquivo
        )
