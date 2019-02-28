# 通过邮箱远程操控电脑

> 欢迎大家访问我的博客：[overfit blog](http://overfit.ml)
>
> 其实这个程序是我 1 年前写的，今天，在整理我之前写的代码时，突然找到了，在这篇博客里，我会分析一下这个小程序的实现步骤

![](https://overfit-photo-1257758577.cos.ap-guangzhou.myqcloud.com/2019/01/20/test.PNG)

## 我们的目的

用 python 做一个小程序，使得可以远程操控电脑，实现**关机，重启，打开网页..** 一系列的功能

## 分析

**远程：**有没有一种方法能够实现信息的交换，且不需要钱呢？当然有，那就是网上到处都可以找到的免费邮箱

**操控：**为了实现实现关机，重启，打开网页..一系列的功能，我们使用 windows 自带的 `cmd` 命令行，比如

```cmd
::1200秒后关机
shutdown -s -t 1200
::打开网页
start http://overfit.ml
::删除文件
del /f /im test.txt
::新建文件夹
md test
```

## 使用

python 3.6

## 程序文件

```fold
config.json ---> 配置文件
maillib.py ---> 接收、发送、处理邮件的库
远程cmd.py  ---> 主程序
```

## config.json

```txt
{
  "mailAccount" : "你的163邮箱@163.com",
  "mailPassword" : "邮箱密码",
  "RefreshWait" : 刷新时间（推荐填写5）,
  "setNope" : false, 后台运行
  "sendLogToMail" : false 发送“运行成功”信息到邮箱
}
```

## 更新日志

+ 增加后台运行功能
+ 增加`config`选项
+ 一些小功能