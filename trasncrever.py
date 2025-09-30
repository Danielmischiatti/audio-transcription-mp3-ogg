import whisper
import tempfile
import os
import subprocess
import time

def transcrever_audio(arquivo):
    # Carregar o modelo Whisper
    model = whisper.load_model("small")
    
    # Verificar o tipo do arquivo
    arquivo_ext = arquivo.name.split('.')[-1].lower()  # Obtém a extensão do arquivo

    # Se for um arquivo .ogg, realizar a conversão
    if arquivo_ext == 'ogg':
        # Criar um arquivo temporário para salvar o arquivo convertido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile_path = tmpfile.name
            
            # Salvar o arquivo .ogg temporariamente para conversão
            with open(tmpfile_path, 'wb') as f:
                f.write(arquivo.getvalue())
            
            # Converter o arquivo .ogg para .wav (ou .mp3) usando FFmpeg
            converted_file_path = tmpfile_path.replace(".mp3", ".wav")  # Mudar para .wav
            try:
                # Chama o FFmpeg para converter o arquivo de áudio
                subprocess.run(['ffmpeg', '-i', tmpfile_path, converted_file_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erro ao converter o arquivo: {e}")
                return "Erro ao converter o arquivo de áudio."
            
            # Transcrever o arquivo convertido
            result = model.transcribe(converted_file_path, language="pt")
            
            # Espera mais tempo para garantir que o arquivo foi fechado antes de removê-lo
            time.sleep(3)  # Aumenta o tempo de espera

            # Remover os arquivos temporários após o uso com tentativas
            for _ in range(3):  # Tentativas de remoção (3 tentativas)
                try:
                    if os.path.exists(tmpfile_path):
                        os.remove(tmpfile_path)  # Remove o arquivo temporário original
                    break  # Se removido com sucesso, sai do loop
                except PermissionError:
                    print(f"Erro ao remover o arquivo temporário: {tmpfile_path}")
                    time.sleep(1)  # Aguarda 1 segundo e tenta novamente

            for _ in range(3):  # Tentativas de remoção do arquivo convertido
                try:
                    if os.path.exists(converted_file_path):
                        os.remove(converted_file_path)  # Remove o arquivo convertido
                    break  # Se removido com sucesso, sai do loop
                except PermissionError:
                    print(f"Erro ao remover o arquivo convertido: {converted_file_path}")
                    time.sleep(1)  # Aguarda 1 segundo e tenta novamente

            return result["text"]
    else:
        # Caso o arquivo não seja .ogg, prosseguir com a transcrição diretamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile_path = tmpfile.name
            
            # Salvar o arquivo original temporariamente
            with open(tmpfile_path, 'wb') as f:
                f.write(arquivo.getvalue())
            
            # Transcrever o arquivo original
            result = model.transcribe(tmpfile_path, language="pt")
            
            # Espera mais tempo para garantir que o arquivo foi fechado antes de removê-lo
            time.sleep(3)  # Aumenta o tempo de espera

            # Remover o arquivo temporário após o uso com tentativas
            for _ in range(3):  # Tentativas de remoção (3 tentativas)
                try:
                    if os.path.exists(tmpfile_path):
                        os.remove(tmpfile_path)  # Remove o arquivo temporário
                    break  # Se removido com sucesso, sai do loop
                except PermissionError:
                    print(f"Erro ao remover o arquivo temporário: {tmpfile_path}")
                    time.sleep(1)  # Aguarda 1 segundo e tenta novamente
            
            return result["text"]



