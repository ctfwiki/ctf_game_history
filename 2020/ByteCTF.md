## 比赛信息

> 比赛时间：2020-10-24 09:00:00 ~ 2020-10-25 21:00:00
>
> 比赛网址：https://bytectf2020.xctf.org.cn/ad5/match/jeopardy/guide?event=32&hash=2d27a2da-9262-4f68-a592-8c234e783cad.event

<br/>

### writeup

[ByteCTF 2020 部分题目 官方Writeup](https://bytectf.feishu.cn/docs/doccnqzpGCWH1hkDf5ljGdjOJYg)

[Bytectf2020 writeup by W&M](https://mp.weixin.qq.com/s/4OVC10crL1rBFrNf9wyUTg)

网盘文档（链接见README.md）：

2020-ByteCTF部分题目-官方Writeup.pdf

2020-ByteCTF-WriteUp-byNu1L.pdf

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1ZUyJRSvC1_95JLJHnleD1g 提取码：xing

链接：https://pan.xunlei.com/s/VMdtuD1uMMliGEf4es_Jm1qgA1 提取码：zs57

链接：https://ctf.lanzoui.com/b02c7s3zi 密码:xing

<br/>

## 题目信息

### PWN

#### pwndroid(4solved,869pt)

> 题目地址：http://112.126.65.213:30771/
>
> hint1: jsbridge
>
> hint2: heap in jemalloc

附件下载：95c5afea92ceb58c3c4933623b50674b.zip

<br/>

#### gun(43solved,322pt)

> nc 123.57.209.176 30772
> 备用：nc 123.56.96.75 30772

附件下载：270961c9d5404345b0bd13e813e26315.zip

<br/>

#### ohmyjson(2solved,952pt)

> nc 123.57.209.176 30773
> 备用：nc 123.56.96.75 30773
>
> hint1: buger/jsonparser

附件下载：f7d6ff8d0a714e159e97d7410ecf8613.zip

<br/>

#### easyheap(33solved,384pt)

> nc 123.57.209.176 30774
> 备用：nc 123.56.96.75 30774

附件下载：cc388fc5b354402688765c8c371392b3.zip

<br/>

#### leak(13solved,625pt)

> nc 123.57.209.176 30775
> 备用：nc 123.56.96.75 30775

<br/>

### CRYPTO

#### noise(20solved,512pt)

> nc 182.92.153.117 30101
> 备用：nc 182.92.215.134 30101

附件下载：8be1633cd52a449caa46c9b199d4cdc9.zip

<br/>

#### APAKE(8solved,740pt)

> nc 182.92.153.117 30102
> 备用：nc 182.92.215.134 30102

附件下载：7452831fac254b0d94800631fb7c2a47.zip

<br/>

#### threshold(15solved,588pt)

> nc 182.92.153.117 30103
> 备用：nc 182.92.215.134 30103

附件下载：4f2f3dc4980041839f2fe0bf72323da0.zip

<br/>

### REVERSE

#### Where are you GOing(4solved,869pt)

> Where are you GOing with so many ROUTINEs?
>
> hint1: graph algorithm

附件下载：94df23fa53bd42b3ae211be20768a81b.zip

<br/>

#### Easy Flutter(0solved,1000pt)

> A bite of flutter.
>
> hint1: libapp.so

附件下载：151abe691959ea9e037dcbe2ea2ea557.zip

<br/>

#### Reverse Algorithm(2solved,952pt)

> What algorithm is this？
>
> hint1: 如果有满足输入条件的解，请联系逆向答疑
>
> hint2: 求出满足条件的解可以通过https://aliyun.gwyn.me:8000/reverse_algorithm?flag=what_you_input获取flag

附件下载：080547fdd4f04b5fb98f6e12da348ee7.zip

<br/>

#### DaShen Decode AES(28solved,425pt)

> DaShen Decode AES

附件下载：363999908d964620989f92a5eb84793a.zip

<br/>

#### App1c(8solved,740pt)

> extract app1c sdk secret key

附件下载：b8f297a103014f5d9526cebabcadf6a4.zip

<br/>

#### CrackMe(12solved,645pt)

> "This is a Ciphertext of the flag:""2d186a3e172a14673789f499cd6cfbcd29b6c73f4b4a27c23464776825af90b2"".
> You can decrypt it directly or input a password to get the flag."
>
> hint1: Is it a real SHA256?

附件下载：0c26e1ac7f4f4bbc94f65a71ac4b9c89.zip

<br/>

#### creakme(8solved,740pt)

> please input the correct decryption key and decrypt the flag

附件下载：a3f108d44cd14301b440eecf97c5314c.zip

<br/>

#### QIAO(39solved,344pt)

> who is qiaoqiao?

附件下载：4abe9bde20084233b9aa4f1a311742b1.zip

<br/>

### WEB

#### douyin_video(10solved,689pt)

> Do you like douyin video?
> Submit your payload at http://c.bytectf.live:30002/
>
> ( Server URLs which only admin can access:
> http://a.bytectf.live:30001/
> http://b.bytectf.live:30001/ )
>
> hint1: Look carefully at the name of the contest topic. There is a way that can help you bypass.

附件下载：55faef1777b640f7b5c06c63110afbef.zip

<br/>

#### easy_scrapy(3solved,909pt)

> The next generation distributed crawler system.
>
> http://101.200.50.18:30010/
> http://39.102.56.46:30010/
> http://39.102.68.152:30010/
> http://39.102.69.151:30010/
>
> hint1: Try to read the spider source code, maybe you can test it locally
>
> hint2: How to attack distributed system and get rce on the spider node?
>
> hint3: scrapy_redis

<br/>

#### Wallbreaker 2020(1solved,1000pt)

> http://123.57.91.179:(30080 to 30089)
> http://39.102.69.87:(30080 to 30089)
>
> (Environment will reset every 10 minutes)

<br/>

#### beaker_browser(0solved,1000pt)

> 用CVE-2020-12079攻击后台bot吧，将你的URL提交到：http://123.57.90.190:30500/code.php ，尝试获取bot的shell。 源码参考：https://github.com/beakerbrowser/beaker/commit/7206281e786c9a7628d294d5440881f0a70a9837
>
> 备用提交链接：http://39.102.60.253:30500/code.php
>
> hint1: 漏洞需要一定的用户交互，后台bot已模拟相关逻辑
>
> hint2: 更新附件，可npm install && npm start启动； 链接: https://r4j9ybdfv1.feishu.cn/file/boxcnyN87JKq7pNfkqTfkpRF2pg 密码: UlAo； 用户交互为点击关闭页面按钮

附件下载：beaker_browser_attachment.zip、beaker_browser.zip（更新附件，106M）

<br/>

#### secure_website(1solved,1000pt)

> No one knows my uri. haha
>
> http://182.92.174.109:30080/
> http://182.92.174.109:30081/
> http://182.92.174.109:30082/
> http://182.92.174.109:30083/
> http://182.92.174.109:30084/
>
> http://39.102.70.108:30080/
> http://39.102.70.108:30081/
> http://39.102.70.108:30082/
> http://39.102.70.108:30083/
> http://39.102.70.108:30084/

<br/>

#### jvav(4solved,869pt)

> This is an elementary school level challenge.
> Environment: fmw_12.2.1.4.0_wls.jar with Apr patch@Java 1.8.0_192
>
> [https://101.200.140.238:30443](https://101.200.140.238:30443/)
> https://47.94.154.215:30443/
> (If chrome shows error, just type "thisisunsafe" to bypass.)

<br/>

### MISC

#### girl_gift(8solved,740pt)

> 隔壁老哥发我一个压缩包，听说是暗恋已久的妹子送给我的，赶紧打开来看看……

附件下载：d4a1a7ab64e1c906ed2bb897d235212d.zip

<br/>

#### double_game(9solved,714pt)

> 双倍的快乐
>
> Server IP: 182.92.4.49 Port: 30888
> (Backup Server IP: 123.57.66.79 Port: 30888)

附件下载：816e0e9044dc4353a7ab8856bf3181b3.zip

<br/>

#### PT Site(20solved,512pt)

> Welcome to ByteCTF private file sharing server. Notice that this is not a web challenge.
>
> [http://182.92.4.49:30080](http://182.92.4.49:30080/)
> [http://123.57.66.79:30080](http://123.57.66.79:30080/)

<br/>

#### Hardcore Watermark 01(6solved,800pt)

> 厌烦了用工具解图片题？那么来点硬核的～

附件下载：cd26292189e709a8348e6b453894a8dd.zip

<br/>

#### Hardcore Watermark 02(2solved,952pt)

> hint1: 分块隐藏

附件下载：529e6b0fc59b4720ac7167da58d75faa.zip

<br/>

#### checkin(456solved,42pt)

> 关注微信公众号“字节跳动安全中心”，并回答问题“字节跳动在哪些城市进行安全与风控岗位招聘？”领取你的flag

```
ByteCTF{3b6ff69f-8a29-4236-9383deaafb}
```

<br/>

#### survey(152solved,116pt)

> 2020 ByteCTF 初赛问卷调研，填写完领取flag
>
> https://docs.google.com/forms/d/e/1FAIpQLSfywaRSNkCAes3yY7-NdyL_bI7Y9cIw80AKDoMgGISgvAK-fA/viewform?usp=sf_link

```
ByteCTF{Thank_you_for_playing_ByteCTF_2020}
```

