## 比赛信息

> 比赛名称：DASCTF x BJD 12月圣诞狂欢赛
>
> 比赛网址：https://www.linkedbyx.com/taskinfo/1458/detail
>
> 比赛时间：2020-12-25 09:00 -- 2020-12-25 18:00
>
> 出题人：https://shimo.im/docs/XRwTVPwYyq9QtJdJ

<br/>

## writeup

[BJD4th联合魔法少女野队Writeup](http://snowywar.top/wordpress/index.php/2020/12/25/bjd4th-writeup/)

[安恒12月月赛 X BJDCTF 4th WriteUp](https://l1near.top/index.php/2020/12/27/87.html)

[BJD4TH BLOCKCHAIN WP](https://imagin.vip/?p=1534)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1Kvu5q-ASaz-7bL9HTndT8A 提取码：5555

链接：https://share.weiyun.com/GtEsdljs 密码：555555

链接：https://t1m.lanzous.com/b0aff19kb 密码:5555

<br/>

## 题目信息

### WEB

#### easyjs(200p)

> 服务器每15秒会清理/tmp/log的内容；easyjs靶机中nodejs的端口是10300，并非附件中的80端口，抱歉给各位师傅造成不便
>
> 183.129.189.60:10034

附件下载：2012245fe42c7cf2fad.zip

<br/>

#### easyphp(200p)

> easyphp请用这个链接:http://8.129.41.25:10305/ 提交DASCTF{}内的MD5值
>
> 183.129.189.60:10018
>
> hint1: easyphp考察的是写入shell，命令执行，不是简单的文件读取
>
> hint2: easyphp重新更新了靶机，每60秒会清空uploads。出题的时候，没有考虑周全，给各位师傅造成不便，在此表示歉意

源码下载：easyphp.zip

<br/>

#### BabyLaminas(300p)

> 框架是最新的，GetShell,Have Fun!（提交DASCTF{}包裹的字符串）
>
> 183.129.189.60:10020

`/public/www.zip`

源码下载：www.zip

<br/>

### PWN

#### 快乐打砖块(200p)

> 连接方式：ssh ctf@host -p port (passwd:pwnme) 
>
> hint: 游戏是有通关码的:-p
>
> 183.129.189.60:10021

附件下载：2012245fe42c7bb8ea0.zip

<br/>

#### π(100p)

> 众所周知 π = 3.1415926
>
> 183.129.189.60:10022

附件下载：2012245fe42c7b37988.zip

<br/>

#### welcome(300p)

> Welcome to BJD4th. p.s.flag在环境变量中
>
> 183.129.189.60:10023

```bash run.sh
#!/bin/sh
timeout 90 ./welcome -c 'env FLAG=gagaga sh'
```

<br/>

### REVERSE

#### EasyVH(300p)

> This is easy VH 提交32位小写md5(flag) PS:flag为最短可满足输入

附件下载：2012245fe42c7c797dc.zip

<br/>

#### RakudaDou(200p)

> Neko, Nezumi and RakudaDou

附件下载：2012245fe42c7c21a6f.zip

<br/>

### CRYPTO

#### RelatedMessage(300p)

> RelatedMessage（提交DASCTF{}包裹的字符串）

附件下载：2012245fe42c6020005.zip

<br/>

#### asa(100p)

> 提交DASCTF{}内的MD5值

附件下载：2012245fe42c5fb2086.zip

<br/>

### MISC

#### FakePic(200p)

> 啪的一下，flag就拿到了

附件下载：2012245fe42c78e6945.rar

<br/>

#### FakePixel(300p)

> 当你凝视深渊的时候，深渊也凝视着你！

附件下载：2012245fe42c6089533.7z

<br/>

#### 马老师的秘籍(100p)

> 马老师把他的flag弄丢了，你能帮他找到吗？

附件下载：2012245fe42c799ae57.zip

<br/>

### BLOCKCHAIN

#### MAGA(300p)

> 你的朋友唐纳德·特朗普，不幸患上新冠病毒，他原计划参加下个月的美国总统大选，但是现在希望渺茫，因此请你替他进行参选。 Hint at 1608878475 : https://ipfs.infura.io:5001/api/v0
>
> 183.129.189.60:10024

<br/>

#### Fermat's_Mistake(100p)

> 我算错了？不，是费马错了！
>
> 183.129.189.60:10025

