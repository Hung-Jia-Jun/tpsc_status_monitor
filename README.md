# 台北市運動中心健身房與游泳池人流監控儀表板
![](%E6%88%AA%E5%9C%96%202022-10-15%20%E4%B8%8B%E5%8D%884.12.05.png)

### 服務位置
* [Prometheus](https://tpscprom-isgde2b5lq-uw.a.run.app/)
* [Grafana 監控儀表板（快照）](https://tpscgrafana-isgde2b5lq-uw.a.run.app/dashboard/snapshot/jyAzSzYeUTI0hE4fPRvP6ykid9Fs6kkK?orgId=1)
* [Grafana 儀表板（需登入）](https://tpscgrafana-isgde2b5lq-uw.a.run.app/d/h9t8cWS4k/tai-bei-shi-yun-dong-zhong-xin-zhuang-tai-tu-biao?orgId=1&from=now-1h&to=now)


---
### Grafana DataSource setting
Local
* http://prometheus:9090

Online
* https://tpscprom-isgde2b5lq-uw.a.run.app/
---
### 部署google cloud functions指令
entry-point 請設定為flask程式起始的function
```
gcloud functions deploy tpsc-metrics --trigger-http --region=us-central1 --runtime=python39 --entry-point=metrics
```
---
## GCR 設定
```
gcloud projects list
gcloud auth login
gcloud auth configure-docker
```
---
## 打包並上傳image 到 GCR
在 Docker 19.03+ 版本中可以使用 `$ docker buildx build` 命令使用 BuildKit 构建镜像。该命令支持 --platform 参数可以同时构建支持多种系统架构的 Docker 镜像，大大简化了构建步

```
# Prometheus
#封裝成Docker image
docker buildx build -t tpsc_prom --platform linux/amd64 -f Prometheus_Dockerfile .

#打上Tag
docker tag tpsc_prom gcr.io/tpsc-d27f4/tpsc_prom

#上傳至GCR
docker push gcr.io/tpsc-d27f4/tpsc_prom

```
```
# Grafana
#下載Grafana Image
docker pull grafana/grafana

#封裝成Docker image
docker buildx build -t tpsc_grafana --platform linux/amd64 -f Grafana_Dockerfile . 

#打上Tag
docker tag tpsc_grafana gcr.io/tpsc-d27f4/tpsc_grafana

#上傳至GCR
docker push gcr.io/tpsc-d27f4/tpsc_grafana
```
---

部署Docker到Cloud Run
```
gcloud run deploy --image gcr.io/tpsc-d27f4/tpsc_prom --platform managed --port=9090

gcloud run deploy --image gcr.io/tpsc-d27f4/tpsc_grafana --platform managed --port=3000
```

---
## 本機測試的設定
因為要在本機起一個flask的web service
所以需要先取得宿主機IP 
`ifconfig | grep "inet "`
在此案例中，==172.20.10.2==是宿主機的IP
```
 ifconfig | grep "inet "                                                 13:53:31 
	inet 127.0.0.1 netmask 0xff000000
	inet 172.20.10.2 netmask 0xfffffff0 broadcast 172.20.10.15
```


啟動prometheus與Grafana
並去修改<mark>docker-compose.yml</mark>裡面的<mark>extra_hosts</mark>位置為資料收集來源的IP
這樣內部的prometheus才能call到外面的metrics
`docker-compose up`
在本機網頁打開[prometheus](http://127.0.0.1:9090/)
