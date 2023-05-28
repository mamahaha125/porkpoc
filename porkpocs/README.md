# porkpocs

### 支持三种模式：

- **verify**(验证模块)
- **attack**（利用模块）
- **shell**（getshell）待实现...

```
usage: test01.py [-h] [-c] [-v] [-a] [-u URL] [-r FILE] [-t POC] [-F] [-s]
                                                                          
PORKPOCS !!!                                                              
                                                                          
  -F, --FOFA            fofa url
  -s, --singlepoc       single poc

Example:
        run.py -u example.com  -t pocs/Redis  -v           #verify
        run.py -r url file     -t pocs/Redis  -a           #load file to get url
        run.py -F api(FOFA...) -t pocs/Redis  -s           #get fofa api to get url
```

### 示例：

```
python3 test01.py -r Redis.txt -t pocs/Redis -v
# -r *.txt 					批量导入url

# -u example.com   			单个url

# -v -a -c 					选择脚本利用模式

# -t pocs/(选择全部poc)  pocs/Redis(选择一个poc模块) pocs/Redis/redisnone.py(选择单个poc)
```

