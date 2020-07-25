# rpi-remocon-api

Raspberry Pi学習リモコンのAPI

## Requirement

* Python 3
* [DHT11_Python](https://github.com/szazo/DHT11_Python)
* [IR Record and Playback(irrp.py)](http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py)

## Deploy

### 専用ユーザ作成

```
sudo useradd -m remocon
```

### clone

```
cd /opt
sudo git clone https://github.com/hotaru51/rpi-remocon-api.git
sudo chown -R remocon:remocon rpi-remocon-api/
```

### 依存Pythonパッケージ

Pipfileに指定のあるもの以外は別途インストールする

```sh
sudo pip3 install pipenv
pip3 lock -r > requirements.txt
sudo pip3 install -r requirements.txt
rm requirements.txt
```

### irrp.pyのインストール

```sh
sudo apt install pigpio python-pigpio python3-pigpio
sudo mkdir /opt/irrp
sudo cp irrp/irrp.py /opt/irrp
sudo ln -s /opt/irrp/irrp.py /usr/local/bin/irrp
# 確認
irrp --help
```

### DHT11_Pythonのインストール

```sh
git submodule update -i
cd dht11
sudo python3 -m pip install .
```

### 信号の記録

エアコン用に以下の信号を作成

* 電源OFF
    * `aircon:off`
* 冷房(xxは温度)
    * `aircon:cool_xx`
* ドライ
    * `aircon:dry_xx`
* 暖房
    * `aircon:heat_xx`

```sh
cd signals
# 記録例)
#
# -rは記録
# -gは使用するGPIOピン
# -fはシグナルを記録するファイル名
# その後に「機器名:信号名」
# --postは信号が途絶えてから記録を終了する目安(ミリ秒)
irrp -r -g 23 \
    -f aircon aircon:off \
    --post 130
```

### NGINXの設定

NGNIXはインストール済みとする  
`remocon_api_nginx.conf` 配置後、 `server_name` をRaspberry PiのIPに変更する

```sh
sudo cp config/remocon_api_nginx.conf /etc/nginx/conf.d/
# server_nameの修正
vi /etc/nginx/conf.d/remocon_api_nginx.conf
# 自動起動確認
systemctl list-unit-files | grep nginx
# 設定されていなければ自動起動有効化
systemctl enable nginx
```

### systemdサービス追加

```
cp rpi-remocon-api.service rpi-remocon-api.socket /etc/systemd/system/
systemctl daemon-reload
systemctl enable rpi-remocon-api.service
systemctl enable rpi-remocon-api.socket
# 確認
systemctl list-unit-files | grep rpi-remocon-api
```
