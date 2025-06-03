# Usa uma imagem oficial do Python como base
FROM python:3.13.2

# Define o diretório de trabalho
WORKDIR /app

# Copia primeiro o requirements.txt para aproveitar o cache de builds
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os ficheiros do projeto para o container
COPY . .

# Garante que a pasta /data existe (para JSON/XML)
RUN mkdir -p /app/data

# Exponha a porta do serviço SOAP
EXPOSE 55555

# Comando para iniciar o serviço
CMD ["python", "soapservice.py"]