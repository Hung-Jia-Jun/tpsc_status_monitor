# command document

取得宿主機IP 
ifconfig | grep "inet "
在此案例中，==172.20.10.2==是宿主機的IP
```
 ifconfig | grep "inet "                                                 13:53:31 
	inet 127.0.0.1 netmask 0xff000000
	inet 172.20.10.2 netmask 0xfffffff0 broadcast 172.20.10.15
```

啟動prometheus與Grafana，記得去修改docker-compose.yml裡面的extra_hosts位置為資料收集來源的IP
這樣內部的prometheus才能call到外面的metrics
```
docker-compose up
```
http://127.0.0.1:9090/

Grafana DataSource
http://prometheus:9090