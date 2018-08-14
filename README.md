# Deploy4s - A deploy tool for simple, standard, stable and stupid

## About
受启发于AWS CodeDeploy的自动化部署服务，抽取其中标准化部署功能实现的一个本地部署组件。[AWS CodeDeploy User Guide](https://docs.aws.amazon.com/zh_cn/codedeploy/latest/userguide/welcome.html)
- Deploy是一个自动化部署组件，能够让用户方便快速地将应用自动部署到目标机器上。通过部署流程的标准化和自动化，加快部署的速度，控制部署节奏，降低应用升级更新的复杂度，减少手工部署操作的错误和风险。最终使得用户能够在快速地发布新特性的同时保证部署的质量，避免部署过程中的服务中断。   
- 传统应用代码和部署脚本是分离的，基于很多不同的部署工具开发，如Chef，Puppet，Ansible，或者开发人员自己写的Shell，Python部署脚本。随着DevOps理念的兴起，消除Dev和Ops之间的鸿沟，系统的开发和运维由一个自治团队全权负责，所以将代码与部署放在一起就非常自然，统一Dev和Ops的目标和部署。另外，将应用代码与部署脚本一体化，也简化了代码和部署脚本的管理，避免代码版本与部署脚本版本需要对应的问题。其实，这种设计也简化了用户的使用过程，不需要额外再做部署脚本版本的管理了。   
- Deploy定义了一个基于事件部署流程接口，在接口定义中，定义多个部署文件拷贝源目标部署映射(files->source->destination)，以及部署中各个步骤及步骤之间的执行顺序(ApplicationStop->BeforeInstall->Install->AfterInstall->ApplicationStart-> ValidateService)，各个步骤要执行的脚本。   
- Deploy仅处理代码部署问题，并不处理应用配置管理，资源管理，环境管理以及之后的监控和恢复，伸缩等环节，用户想要实现系统的持续自动化部署，仍然需要自行集成开发，比如需要自行实现应用新版本的打包和上传，之后通过Deploy提供的相应API接口以及CLI将其集成到自己的开发流程，实现持续交付。   

## Requirements
- Python
- PyYAML

## Install
下载最新的Release包，通过pip命令安装：
```shell
pip install deploy4s
```
或者通过下载源码包或clone代码至本地，然后通过如下命令安装：
```shell
python setup.py install
```

## Usage
```shell
deploycli --bundle=http://server/example.zip
```
使用--help查看更多使用帮助。  
--bundle参数指定zip包的路径，可以是本地文件路径也可以是HTTP地址。

## Release
- [deploy-0.0.1.zip](https://github.com/meanstrong/deploy/releases/download/v0.0.1/deploy-0.0.1.zip)

## Limit
与标准的AWS CodeDeploy相比，appspec.yml文件需要新增一个``workdir``参数，用于指定hooks中命令的执行Current Working Directory，其他参数配置可参考AWS CodeDeploy。

## Example
一个示例的appspec.yml文件如下所示：
```yaml
version: 0.0
os: linux
workdir: /app
files:
  - source: /
    destination: /app
hooks:
  ApplicationStart:
    - location: bin/start.sh
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
deploycli --bundle=http://server/example.zip
```

## Author
- <a href="mailto:pmq2008@gmail.com">Rocky Peng</a>
