# Use uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos
COPY requirements.txt .

ENV PROFILE=${PROFILE}
ENV BASE_URL_API_BITRIX=${BASE_URL_API_BITRIX}
ENV CODIGO_BITRIX=${CODIGO_BITRIX}
ENV PORT=${PORT}


# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 57

# Comando para rodar a aplicação (ajustado para main.py)
CMD ["python", "main.py"]
