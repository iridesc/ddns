# ddns

## 如何运行

### Docker 方式
1. 修改下面的json并保存到文件 ```config.json``` 
    ```json
    {
        "resolver_infos": [{
            "Resolver": "NamesiloResolver",
            "domain": "a.your.doamin.com",
            "resolve_type": "AAAA",
            "key": "your Namesilo api key",
            "ttl": 7000
        },
        {
            "Resolver": "NamesiloResolver",
            "domain": "b.your.doamin.com",
            "resolve_type": "A",
            "ttl": 7000,
            "key": "your Namesilo api key"
        }],
        "wait_minute_pre_check": 30
    }
    ```
2. 运行 ```docker run -d -v ./conf.json:/ddns/conf/conf.json --name ddns irid/ddns```
    

### 源码运行

1. 克隆本项目
2. 安装依赖 
   ```shell
   pip install -r pip install -r requirements.txt
   ```
3. 修改配置文件```ddns/conf/conf.json```
4. ```python ddns.py```
   