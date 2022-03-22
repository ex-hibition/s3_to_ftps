import datetime
import os
from ftplib import FTP_TLS, FTP

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
    pass

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

    # ftpsファイル転送
    with Patched_FTP_TLS(host='172.17.0.3',user='ftpsuser', passwd='ftpsuser', timeout=60) as ftps:
        ftps.prot_p()
        print(f"list={ftps.nlst('ftp_root')}")
        ftps.storbinary(cmd=f"STOR {remote_path}", fp=open(file=local_path, mode='rb'))


if __name__ == "__main__":
    filename = "test.txt"
    handler(target_filename=filename)