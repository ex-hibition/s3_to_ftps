FROM amazonlinux:2

# 必要なモジュールをインストール
RUN yum -y install tar zip git

# python3.8インストール
RUN amazon-linux-extras install -y python3.8
# pipenvインストール
RUN pip3.8 install pipenv

# 仮想環境構築
RUN pipenv install

CMD ["bash"]