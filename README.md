# ADSDeck

## Run database (docker)

docker run --name dj_simple \
    -e POSTGRES_PASSWORD=q1w2e3R$ \
    -e POSTGRES_USER=user \
    -e POSTGRES_DB=hunting \
    -p 5432:5432 \
    -d \
    postgres:14.0-alpine