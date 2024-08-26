# 算命大师安装文档



下载Nodejs， 版本信息

```
node 18.6.0 
npm 9.6.2 
vue3
```



## 1. 前端部分使用vue框架进行开发

这一部分是使用多模态的代码， 基于gpt4-o来开发的多模态和Yuan2B开发的应用，另一个版本的前端页面是取消了多模态， 采用单纯原生的Yuan2B大模型来开发的， 可以clone下面的代码拿到原生的前端代码


基于Yuan2B模型开发的页面
```shell
git clone https://github.com/hh404358/fortune_teller

npm install
# 运行页面
npm run dev
```

基于gpt4-o的多模态页面可以使用下面命令进行安装

```shell
# 下载代码
git clone https://github.com/gzhuuser/fortune_teller.git
# 进入项目目录按照依赖
cd front
npm install
# 运行页面
npm run dev
```

运行界面如下所示，说明前端界面启动：
![](./img/4.png)

## 2. 后端部分使用flask框架进行开发

可以使用pip进行安装python
采用autoDL云计算平台，新建一个虚拟机环境， 环境为python3.12 torch为2.3.0
![](./img/5.png)

进去后先clone github仓库

```shell
git clone https://github.com/gzhuuser/fortune_teller.git
```

然后进行环境配置

```shell
pip install -r requirements.txt
```

运行前记得在.env_template里面填写好4.0的key和自己的阿里云oss的key

运行后端程序app.py

```shell    
python app.py
```

运行界面如下所示，说明后端程序启动：
![](./img/6.png)

下载ssh工具进行端口映射，将本地端口映射到云端虚拟机端口

### ssh隧道软件如下

![](./img/7.png)

### 打开效果图（注意这里的端口映射看看6006有没有反应，没有的话改成9000）

![](./img/8.png)

### 输入ssh指令和密码，就可以访问本地的http://localhost:6006/v1和v2了

![](./img/9.png)

多模态运行效果图片

## 运行效果图片

![](./img/11.png)

### 结束记得关机

![](./img/10.png)

