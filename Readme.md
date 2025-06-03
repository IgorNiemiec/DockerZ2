Sprawozdanie - Zadanie 2
# 1. Tagowanie

Zastosowano cache z wykorzystaniem type=registry, co umożliwia współdzielenie danych pomiędzy buildami:

Źródło: docker.io/<user>/myapp-build-cache:main
Tryb: mode=max – cache zapisuje wszystkie możliwe warstwy

Tag cache'a odzwierciedla gałąź, czyli w naszym przypadku main, co pozwala na niezależne cache’owanie dla innych gałęzi/developerów.


Zastosowano dwa typy tagów:

latest – wskazuje zawsze na najnowszy build z gałęzi main

sha-<hash> – unikalny identyfikator powiązany z commitem, np. sha-ab12cd3


# 2. Konfiguracja związana z DOCKERHUB

Ustawione zostały zmienne USERNAME, DOCKERHUB_USERNAME oraz DOCKERHUB_TOKEN 

# 3. Plik 99635.yml


```yaml
name: igorniemiec99635

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4


      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
        

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to DockerHub (cache)
        uses: docker/login-action@v3
        with:
          registry: docker.io
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Log in to GitHub Container Registry (GHCR)
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build Docker image with cache
        id: build-image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          platforms: linux/amd64,linux/arm64
          tags: |
             ghcr.io/igorniemiec/myapp:latest
             ghcr.io/igorniemiec/myapp:sha-${{ github.sha }}
          cache-from: type=registry,ref=docker.io/${{ secrets.DOCKERHUB_USERNAME }}/myapp-build-cache:main
          cache-to: type=registry,ref=docker.io/${{ secrets.DOCKERHUB_USERNAME }}/myapp-build-cache:main,mode=max

      - name: Install Trivy
        run: |
              sudo apt-get update && sudo apt-get install -y wget
              wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.51.1_Linux-64bit.deb
              sudo dpkg -i trivy_0.51.1_Linux-64bit.deb

      - name: Scan image for CVEs
        run: |
             trivy image --exit-code 1 --severity CRITICAL,HIGH ${{ steps.meta.outputs.tags }}


      - name: Push image if scan passed
        if: success()
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
              ghcr.io/igorniemiec/myapp:latest
              ghcr.io/igorniemiec/myapp:sha-${{ github.sha }}
          cache-from: type=registry,ref=docker.io/${{ secrets.DOCKERHUB_USERNAME }}/myapp-build-cache:main
          cache-to: type=registry,ref=docker.io/${{ secrets.DOCKERHUB_USERNAME }}/myapp-build-cache:main,mode=max

     
