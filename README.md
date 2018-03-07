# Deploy - A deploy tool
参考AWS CodeDeploy的标准部署服务到本地服务器的工具。
- [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/zh_cn/codedeploy/latest/userguide/welcome.html)

## Install
```shell
$ python setup.py install
```

## Usage
```shell
$ deploycli --bundle=example.zip
```
--bundle参数指定zip包的路径，可以是本地文件路径也可以是HTTP地址。

## Limit
与标准的AWS CodeDeploy相比，appspec.yml文件需要新增一个workdir参数，用于指定hooks中命令的执行CWD，其他参数配置可参考AWS CodeDeploy。

## Example
一个可用的appspec.yml文件如下所示：
```yaml
version: 0.0
os: linux
workdir: /app
files:
  - source: /
    destination: /app
hooks:
  ApplicationStart:
    - location: bin/startup.sh
  ApplicationStop:
    - location: bin/stop.sh
  BeforeInstall:
    - location: bin/backup.sh
  AfterInstall:
    - location: chmod a+x bin -R
```
将该文件与待部署文件一起打成zip包（appspec.yml文件必须位于zip包顶层），将该zip包上传至HTTP server或待部署机器本地。
在服务运行的机器上执行如下命令，即可将部署zip包文件部署到机器上，并停止、启动服务（与hooks中配置相关）：
```shell
$ deploycli --bundle=http://127.0.0.1/example.zip
```