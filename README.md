# ptarmigan
地震や噴火情報を取得し各アプリに通知するシステム

`ptarmigan/src/notify/yamap/user` の`config.ini`を設定する

```
[DEFAULT]
email = 
password = 
user_list_id
public_type
```

# raspiでやること
### vim
```
$ sudo apt-get install vim
```
### ip固定
```
ifconfig
```
wlan0のinetメモする
```
$ sudo vim /etc/dhcpcd.conf
```
```
interface wlan0
static ip_address=192.168.xxx.n/24 #<-任意
static routers=192.168.xxx.1
static domain_name_servers=192.168.xxx.1
```
再起動

### user追加
```
$ sudo adduser [username]
```
```
$ sudo gpasswd -a [username] sudo
```

### ssh設定
```
$ sudo raspi-config
```
`Interfacing Options` > `SSH` > `<はい>`
再起動

## pythonのインストール
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install -y git openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev
```
```
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
```
```
$ sudo vim ~/.bash_profile
```
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
```
$ source ~/.bash_profile
```
```
$ pyenv --version
```

### cron
cron開放
```
$ sudo vim /etc/rsyslog.conf
```
コメントアウト解除
```
cron.*                          /var/log/cron.log
```
```
$ sudo /etc/init.d/rsyslog restart
```
ログレベル
```
$ sudo vim /etc/default/cron
```
```
EXTRA_OPTS='-L 15'
```

ジョブ
```
$ sudo vim /etc/cron.d/ptarmigan
```
```
* * * * * [username] sh /home/[username]/ptarmigan/src/notify/yamap/moment/main.sh >> /tmp/ptarmigan_error.log 2
```

### pip
```
$ pip install requests
$ pip install python-dateutil
```
