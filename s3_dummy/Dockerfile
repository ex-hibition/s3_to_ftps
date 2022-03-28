FROM minio/minio:latest

EXPOSE 9000\
       9001

# default
# ENV MINIO_ROOT_USER=minioadmin\
#     MINIO_ROOT_PASSWORD=minioadmin

CMD ["server", "/data", "--console-address", ":9001"]

# docker build -t minio -f s3_dummy/Dockerfile .
# docker run --rm -d -p 9000:9000 -p 9001:9001 --name minio minio