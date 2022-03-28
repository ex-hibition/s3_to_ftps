import datetime
import os
import boto3
import logging
from ftplib import FTP_TLS, FTP

# logging
logging.basicConfig(level=logging.INFO)

# 環境変数取得
TARGET_ENV = os.getenv("TARGET_ENV", "local")

# 相手先がvsftpdかつrequire_ssl_reuse=Trueの場合に必要なパッチ
# https://stackoverflow.com/questions/14659154/ftps-with-python-ftplib-session-reuse-required
class Patched_FTP_TLS(FTP_TLS):
    """Explicit FTPS, with shared TLS session"""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn,
                                            server_hostname=self.host,
                                            session=self.sock.session)  # this is the fix
        return conn, size

def handler(target_filename: str):
    """ハンドラ"""
    # ファイル取得
    get_file_from_s3(target_filename=target_filename)
    # ファイル転送
    put_ftps_to_saas(target_filename=target_filename)

def get_file_from_s3(target_filename: str):
    """S3からファイルをgetする

    Args:
        target_filename (str): S3から取得するファイル
    """
    bucket_name = f"minio-input-{TARGET_ENV}"
    key_name = target_filename
    local_filename = f"/tmp/{target_filename}"

    session, s3 = '', ''
    if TARGET_ENV == 'local':
        session = boto3.session.Session(profile_name='minio')
        s3 = session.client('s3', endpoint_url='http://host.docker.internal:9000')
    else:
        session = boto3.session.Session()
        s3 = session.client('s3')

    try:
        s3.download_file(Bucket=bucket_name, Key=key_name, Filename=local_filename)
        logging.info(f"downloaded. : bucket_name={bucket_name}, key_name={key_name}, local_filename={local_filename}")
    except Exception as e:
        logging.error(f"get s3 error. : {e}")
        raise

def put_ftps_to_saas(target_filename: str):
    """ファイルを相手先のftpサーバにftpsでputする

    Args:
        target_filename (str): ローカルに取得した転送するファイル
    """
    # ファイル名と拡張子に分割
    filename, extention = os.path.splitext(target_filename)
    yyyymmdd = datetime.datetime.now().strftime('%Y%m%d')
    local_path = os.path.join('/tmp', target_filename)
    # 転送先ファイル名はyyyymmddを追加
    remote_path = os.path.join('ftp_root', f"{filename}_{yyyymmdd}{extention}")

    try:
        # ftpsファイル転送
        with Patched_FTP_TLS(host='172.17.0.2',user='ftpsuser', passwd='ftpsuser', timeout=60) as ftps:
            ftps.prot_p()
            logging.info(f"before list={ftps.nlst('ftp_root')}")
            ftps.storbinary(cmd=f"STOR {remote_path}", fp=open(file=local_path, mode='rb'))
            logging.info(f"after list={ftps.nlst('ftp_root')}")
    except Exception as e:
        logging.error(f"ftps error. : {e}")
        raise


if __name__ == "__main__":
    filename = "test.txt"
    handler(target_filename=filename)