FROM python:3.7-slim

# required build args
ARG DISCORD_TOKEN
ARG MINECRAFT_URI

COPY . /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# propogate from cloud build and github secrets
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ENV MINECRAFT_URI=${MINECRAFT_URI}

RUN echo Looking for ${MINECRAFT_URI}

CMD ["python", "minecraftbot.py"]
