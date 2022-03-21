# s3_to_ftps
## Description
- vsftpdが動いているサーバに対してpythonからftpsでファイル連携するサンプルプログラム

## Usage
### ftpsサーバをbuild & run
```bash
# build
docker build -t ftps_server -f ftps_server/Dockerfile .
# run
docker run -itd --rm --privileged --name=ftps_server -p 21:21 ftps_server /sbin/init
# コンテナに入って
docker exec -it xxxxx bash
# vsftpdを起動
systemctl start vsftpd
systemctl status vsftpd
```

### Dev Containerに入って動作確認
```bash
pipenv run python3.8 main.py
```