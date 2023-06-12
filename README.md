# cocktaillog_crawler
## setup

selenium

``` bash
$ sudo apt install python3-selenium # ←こいつっていります？
$ pip install selenium
```

chrome
``` bash
$ cd /tmp
$ wget https://dl.google.com/linux/linux_signing_key.pub
$ sudo apt-key add linux_signing_key.pub
$ echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
$ sudo apt-get update
$ sudo apt -f install -y
$ sudo apt-get install google-chrome-stable

# chrome
$ google-chrome --version
Google Chrome 114.0.5735.106

# webdriver
$ chromedriver -v
ChromeDriver 113.0.5672.126 (c541687b21a73452ab403e2dced7033ddc97ee9d-refs/branch-heads/5672@{#1202})
```

pip
``` bash
# tqdm
$ pip install -r requirements.txt
```


## usage
``` bash
$ python crawl.py
```
