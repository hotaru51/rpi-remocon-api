# rpi-remocon-api

Raspberry Pi学習リモコンのAPI

## Requirement

* [DHT11_Python](https://github.com/szazo/DHT11_Python)
* [IR Record and Playback(irrp.py)](http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py)

## Deploy

Pipfileに指定のあるもの以外は別途インストールする

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

### その他Pythonパッケージ

```sh
sudo pip3 install pipenv
pip3 lock -r > requirements.txt
sudo pip3 install -r requirements.txt
rm requirements.txt
```

### config.yamlの配置

```sh
cp -p config/config.yaml.sample config/config.yaml
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
