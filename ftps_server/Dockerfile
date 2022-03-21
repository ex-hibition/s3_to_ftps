FROM centos:7

# vsftpd, opensslインストール
RUN yum install -y vsftpd openssl

# https://dev.classmethod.jp/articles/ftps_on_centos7/
# 秘密鍵、証明書の作成
# openssl genrsa -aes256 2048 > vsftpd.key
# openssl req -new -key vsftpd.key -x509 -days 365 -out vsftpd.pem

RUN mkdir -p /etc/pki/tls/certs/ /etc/pki/tls/private/ /etc/vsftpd/
COPY ftps_server/etc/pki/tls/certs/vsftpd.pem /etc/pki/tls/certs/
COPY ftps_server/etc/pki/tls/private/vsftpd.key /etc/pki/tls/private/
COPY ftps_server/etc/vsftpd/vsftpd.conf /etc/vsftpd/

# ftpユーザ作成 & ユーザリスト追加
RUN useradd ftpsuser && echo ftpsuser | passwd ftpsuser --stdin
RUN echo "ftpsuser" >> /etc/vsftpd/user_list

# chroot設定
RUN touch /etc/vsftpd/chroot_list
RUN mkdir -p /tmp/ftpsuser/ftp_root && chown ftpsuser:ftpsuser /tmp/ftpsuser/ftp_root
RUN mkdir /etc/vsftpd/chroot_user_conf && \
    echo "local_root=/tmp/ftpsuser" >> /etc/vsftpd/chroot_user_conf/ftpsuser

EXPOSE 21

# 以下でコンテナ立ち上げてからvsftpd実行
# docker run -itd --rm --privileged --name=ftps_server ftps_server /sbin/init
# systemctl start vsftpd
CMD ["bash"]
