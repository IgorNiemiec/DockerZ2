# Etap 1: Budowanie aplikacji
FROM node:20-alpine AS builder

LABEL maintainer="Igor Niemiec"


WORKDIR /app/source/weather-backend


ENV NODE_OPTIONS=--openssl-legacy-provider


COPY package.json package-lock.json ./
RUN npm install


COPY ./ ./


RUN npm run build


FROM nginx:alpine


RUN rm /etc/nginx/conf.d/default.conf


COPY nginx.conf /etc/nginx/conf.d


COPY --from=builder /app/build /usr/share/nginx/html


EXPOSE 80


CMD ["nginx", "-g", "daemon off;"]


FROM python:3.11-slim AS builder


LABEL maintainer="Igor Niemiec"


WORKDIR /app

RUN apt-get update && apt-get install -y build-essential


RUN python -m venv /app/venv

# Aktywacja środowiska wirtualnego i instalacja zależnościd
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

ENV VISUAL_CROSSING_API_KEY=H93TEQFCKP7YYMVYGABJPAHLB


EXPOSE 8000


CMD ["/app/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
