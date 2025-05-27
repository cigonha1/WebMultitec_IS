# Use uma imagem oficial do Python como base
FROM python:3.13.2

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos do serviço para o container
COPY ../../documentacao/requirements.txt .

# Copie o restante dos arquivos do serviço para o container
COPY . .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta usada pelo serviço REST
EXPOSE 55556

# Comando para iniciar o serviço
CMD ["python", "servidor/rest/rest_service.py"]