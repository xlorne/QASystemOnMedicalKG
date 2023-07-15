# QABasedOnMedicaKnowledgeGraph & ChatGLM-6B问答

self-implement of disease centered Medical graph from zero to full and sever as question answering base. 从无到有搭建一个以疾病为中心的一定规模医药领域知识图谱，并以该知识图谱完成自动问答与分析服务。


## 项目说明

本项目完全参考 https://github.com/liuhuanyong/QASystemOnMedicalKG  

由于QASystemOnMedicalKG项目工程时间比较久，很多代码已经与最新的技术不兼容，因此重新修改了Neo4j层面的代码，然后重新适配的项目。

ChatGLM-6B大模型问答功能代码，由[assmdx](https://github.com/assmdx)贡献

## 运行说明

### 依赖环境

* python
* docker

### 运行步骤

* 运行docker启动neo4j服务
```
cd scripts/

sh install.sh

```

* 修改neo4j密码

为了与项目代码的环境配置一致，默认密码为neo4j/neo4j，建议修改密码为Lorne@2022


* 运行jupyter代码

> [install.ipynb](install.ipynb)

> [json2csv.ipynb](json2csv.ipynb)

> [csv2neo4j.ipynb](csv2neo4j.ipynb)

> [run_textmatch.ipynb](run_textmatch.ipynb) | 基于Neo4j的规则匹配的问答系统

> [run_chatglm6b.ipynb](run_chatglm6b.ipynb) | 基于ChatGLM-6B的问答优化的问答系统



## 引用

https://github.com/liuhuanyong/QASystemOnMedicalKG   
https://github.com/TommyZihao/QASystemOnMedicalKG/tree/master/notebook_tutorials  


