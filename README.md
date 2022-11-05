# porkpocs
### 仅供学习交流，禁止使用该工具进行非法的渗透测试！！！
### 支持三种模式：

- **verify**(验证模块)
- **attack**（利用模块）
- **shell**（getshell）待实现...

```
usage: main.py [-h] [-c] [-v] [-a] [-u URL] [-r FILE] [-t POC] [-F] [-s]
                                                                          
PORKPOCS !!!                                                              
                                                                          
  -F, --FOFA            fofa url
  -s, --singlepoc       single poc

Example:
        main.py -u example.com  -t pocs/Redis  -v           #verify
        main.py -r url file     -t pocs/Redis  -a           #load file to get url
        main.py -F api(FOFA...) -t pocs/Redis  -s           #get fofa api to get url
        main.py -F api(FOFA...) -t pocs/Redis  -v -p payload.txt      #add payload
```

### 示例：

```
python3 main.py -r Redis.txt -t pocs/Redis -v
# -r *.txt 					批量导入url

# -u example.com   			单个url

# -v -a -c 					选择脚本利用模式

# -t pocs/(选择全部poc)  pocs/Redis(选择一个poc模块) pocs/Redis/redisnone.py(选择单个poc)

python3 main.py -l -t pocs                     #查看所有poc
python3 main.py -l -t pocs/Redis               #查看单个poc模块
```

