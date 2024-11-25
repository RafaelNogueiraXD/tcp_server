# Use a versão 12 do Python oficial como base
FROM python:3.12-slim

# Configuração do diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos principais do Poetry e o restante do projeto
COPY pyproject.toml poetry.lock ./
COPY tcp_server/ ./tcp_server/
COPY tests/ ./tests/

# Instalar o Poetry
RUN pip install --no-cache-dir poetry

# Instalar dependências do projeto com Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Expõe a porta para o servidor Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "python", "-m", "tcp_server.server"]
