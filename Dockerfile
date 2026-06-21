# Usamos a imagem oficial do Airflow como base.
# A versão deve combinar com a versão usada no docker-compose.yml.
FROM apache/airflow:2.10.3-python3.11

# Copia o arquivo de dependências do nosso projeto (pandas, requests, pyarrow)
COPY requirements.txt /requirements.txt

# Instala as dependências do projeto dentro da imagem do Airflow.
# Importante: o usuário "airflow" é quem deve instalar, nunca o root,
# por exigência da própria imagem oficial.
RUN pip install --no-cache-dir -r /requirements.txt