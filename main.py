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
    with Patched_FTP_TLS(host='172.17.0.2',user='ftpsuser', passwd='ftpsuser', timeout=60) as ftps:
        ftps.prot_p()
        ftps.dir()


if __name__ == "__main__":
    filename = "test.txt"
    handler(target_filename=filename)