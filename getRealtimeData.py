#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, Response
from prometheus_client import Counter, generate_latest,Gauge,CollectorRegistry
import requests
import json

app = Flask(__name__)

def GetNowPeopleNum():

    url = "http://booking.tpsc.sporetrofit.com/Home/loadLocationPeopleNum"

    payload={}
    headers = {
    'Cookie': 'ASP.NET_SessionId=qmhfrdhzdymzvfh1g5px51yo; _culture=zh-TW'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    rsp = json.loads(response.text)

    json_body = []
    for lid in rsp['locationPeopleNums']:
        json_body.append(
            {
                "LID" : lid['LID'],
                "lidName" : lid['lidName'],
                "fields": {
                    "swPeopleNum" : int(lid['swPeopleNum']),
                    "swMaxPeopleNum" : int(lid['swMaxPeopleNum']),
                    "gymPeopleNum" : int(lid['gymPeopleNum']),
                    "gymMaxPeopleNum" : int(lid['gymMaxPeopleNum']),
                }
            }
        )
    return json_body

@app.route('/')
def healthCheck():
    return "OK"
@app.route('/metrics')
def metrics():
    lidStatus = GetNowPeopleNum()
    registry = CollectorRegistry()
    for rsp in lidStatus:
        g = Gauge(
                rsp['LID'],
                rsp['lidName'], 
                ["label"],
                registry=registry)
        swPeopleNum = int(rsp['fields']['swPeopleNum'])
        g.labels({"label" : "swPeopleNum"}).set(swPeopleNum)
        swMaxPeopleNum = int(rsp['fields']['swMaxPeopleNum'])
        g.labels({"label" : "swMaxPeopleNum"}).set(swMaxPeopleNum)
        gymPeopleNum = int(rsp['fields']['gymPeopleNum'])
        g.labels({"label" : "gymPeopleNum"}).set(gymPeopleNum)
        gymMaxPeopleNum = int(rsp['fields']['gymMaxPeopleNum'])
        g.labels({"label" : "gymMaxPeopleNum"}).set(gymMaxPeopleNum)
        gymMaxPeopleNum = int(rsp['fields']['gymMaxPeopleNum'])
        g.labels({"label" : "gymCapacityPercentage"}).set(gymPeopleNum/gymMaxPeopleNum*100)
        g.labels({"label" : "swCapacityPercentage"}).set(swPeopleNum/swMaxPeopleNum*100)
    return Response(generate_latest(registry), mimetype='text/plain')


if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8000)