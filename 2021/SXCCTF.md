## 比赛信息

> 比赛名称：第一届SXC CTF比赛
>
> 比赛网址：http://sxc.starsnowsec.cn/
>
> 比赛时间：2021年02月09日 08:00~2021年02月09日 20:00

<br/>

## writeup

[第一届SXC CTF WP](https://mp.weixin.qq.com/s/xG_OHXsjIpat7GcovsCF2g)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1zoThDMetZ_FYIjCAbyHeLA 提取码：xing

链接：https://pan.xunlei.com/s/VMdv5KqlosGsVM9eXcJ1K8j2A1 提取码：nghi

链接：https://ctf.lanzoui.com/b02c7th3g 密码:xing

<br/>

## 题目信息

### Web

#### Base(10s,992p)

> 106.55.249.213:5001
> BaseBaseBase
> 你遇见过渗透中传输值为加密的嘛？
>
> 可以试着先跑出编码对应表
>
> ```
> http://106.55.249.213:5001/?user=Qg
> 回显Sorry,you are not admin!you are G
> Qg = G
> http://106.55.249.213:5001/?user=QQ
> 回显 Sorry,you are not admin!you are F
> QQ = F 
> http://106.55.249.213:5001/?user=QQQg
> 回显 Sorry,you are not admin!you are FG
> ```

源码下载：base.zip

<br/>

#### ClassCMS(1s,1000p)

> 156.253.68.196
> 真实的渗透环境，hhhhhh并且二开了哦！
> 不要爆破，不要爆破，不要爆破，重要的事情说三遍！
>
> hint:www.rar **escape**($str)

附件下载：www.rar

<br/>

#### Wechat(3s,1000p)

> 一个未完成的小程序！!因为没有过审的原因，只能省略一些过程 ，这是一个体验版的小程序包

附件下载：debug_1323872424_1_-625286023.zip

web源码（PHP/5.5.9）：html.zip

<br/>

### Reverse

#### Very easy Reverse(11s,991p)

> Very easy Reverse!!

附件下载：PyGame.exe

<br/>

#### Strange_Exe(2s,1000p)

> Strange_Exe!

附件下载：Strange_Exe.exe

<br/>

### PWN

#### pwn_guys(5s,999p)

> 121.37.189.111:23456
> 我们想要一个PWN佬
>
> ![](../img/sxc.jpg)

附件下载：pwn5.zip

<br/>

### Crypto

#### easy easy rsa(20s,964p)

> easy easy rsa!

附件下载：easyR5A.zip

<br/>

#### Easy_RSA(7s,997p)

> Easy_RSA!！

附件下载：easy_rsa.zip

<br/>

#### Hard RSA(7s,997p)

> Hard RSA!

附件下载：hardrsa.zip

<br/>

#### GAP(5s,999p)

> Gap
>
> hint:f 分隔符 疑惑？

附件下载：gap.txt

<br/>

### Misc

#### Flag不在这(45s,807p)

> Flag真的不在这，你要相信我，知道吗！

附件下载：Flag.docx

<br/>

#### 牛年大吉(37s,871p)

> 要相信自己，他就是flag！

附件下载：starsnow.zip

<br/>

#### 网络深处(28s,928p)

> 网络深处! 千万不要一个人大晚上做哦！！！

附件下载：网络深处.rar

<br/>

#### 拼图(15s,981p)

> 你也喜欢鬼刀吗？

附件下载：拼图.zip

题目生成源码：拼图生成.zip

<br/>

#### Very very easy hex(12s,988p)

> Very very easy hex!! Enjoy it!!!

附件下载：img.zip

<br/>

#### YLBNB(10s,992p)

> 你会喜欢他的! :)

附件下载：YLBNB.zip

<br/>

#### Love_it!(9s,994p)

> 文件较大，选择网盘下载(手动狗头)
> 蓝奏：https://wws.lanzous.com/iy5T6lf343g 密码:gbmf
> 百度云：链接: https://pan.baidu.com/s/1wT3bVls2X_5bOSBaxBK91A 提取码: ufrs 复制这段内容后打开百度网盘手机App，操作更方便哦
>
> 解压密码为：2021_jia_you!!
> flag 为 flag{后台名称_后台账号_后台密码_一句话木马名称_一句话密码_第三个马子执行的命令}
> 例如：
> 后台网址为:
> http://127.0.0.1/admin/index.php 后台名称就为: admin
> 账号为：2021 后台账号为: 2021
> 密码为：happy_new_year! 后台密码为: happy_new_year!
> 一句话木马路径为: http://127.0.0.1/mu.php 一句话木马名称为: mu
> 一句话木马 一句话密码为: starsnow
> 一句话执行的命令
> 连接马子 之后执行的第三条 命令
> 第一条 yingzi=phpinfo();
> 第二条 yingzi=system('whoami');
> 第三条 yingzi=system('ls'); 第三个马子执行的命令： system('ls');
>
> 例如：
> flag{admin_2021_happy_new_year!_starsnow_system('ls');}

附件下载：Love_It!.zip

<br/>

### 签到

#### 签到题(82s,350p)

> http://106.55.249.213:5002/
> 祝各位大佬，大大佬，新春快乐！
> 2021 更加牛13！！！

附件下载：签到.zip