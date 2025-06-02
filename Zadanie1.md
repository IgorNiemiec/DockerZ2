POLECENIA NIEZBĘDNE DO:

a) zbudowania opracowanego obrazu kontenera,

docker build -t weather-backend ./weather-backend
docker build -t weather-frontend ./weather-frontend

b) Uruchamianie kontenerów:

docker run -d -p 8000:8000 --name weather-backend weather-backend
docker run -d -p 3000:80 --name weather-frontend weather-frontend

c) Sprawdzanie logów:

docker logs weather-backend
docker logs weather-frontend

d) Sprawdzanie liczby warstw i rozmiaru obrazu:

docker history weather-backend
docker image inspect weather-backend --format='{{.Size}}'

docker history weather-frontend
docker image inspect weather-frontend --format='{{.Size}}'