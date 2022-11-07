# porkpoc
### 仅供学习交流，禁止使用该工具进行非法的渗透测试！！！
### 支持三种模式：

- **verify**(验证模块)
- **attack**（利用模块）
- **shell**（getshell）待实现...

```                                                            
usage: main.py [-h] [-c] [-v] [-a] [-u URL] [-r FILE] [-p PAYLOAD] [-t POC]
               [-F] [-l]

PORKPOCS !!!

optional arguments:
  -h           --help            show this help message and exit
  -c           --command         command shell
  -v           --verify          verify
  -a           --attack          attack
  -u URL       --url URL         target url
  -r FILE      --file FILE       url file
  -p PAYLOAD   --payload         PAYLOAD
  
  -t POC       --poc POC     choose poc nginx poc.py
  -F           --FOFA            fofa url
  -l           --pocdetail       poc detail

Example:
        main.py -u example.com  -t pocs/Redis  -v                            #verify
        main.py -r url file     -t pocs/Redis  -a                            #load file to get url
        main.py -F api(FOFA...) -t pocs/Redis  -v                            #get fofa api to get url
        main.py -l -t pocs/Redis                                             #get pocs detail
        main.py -u example.com  -t pocs/Redis  -v                            #verify
        main.py -u example.com  -t pocs/Redis  -v -p payload.txt             #add payload
```

### 示例：

```
python3 main.py -r Redis.txt -t pocs/Redis -v
# -r *.txt 					    批量导入url

# -u example.com   			单个url

# -v -a -c 					    选择脚本利用模式

# -t pocs/(选择全部poc)  pocs/Redis #选择一个poc模块 pocs/Redis/redisnone.py #选择单个poc

python3 main.py -l -t pocs                     #查看所有poc
python3 main.py -l -t pocs/Redis               #查看单个poc模块
```

