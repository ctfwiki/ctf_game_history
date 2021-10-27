## 比赛信息

> 比赛名称：2021字节跳动安全范儿高校挑战赛
>
> 比赛时间：2021-10-16 10:00:00 —— 2021-10-17 18:00:00
>
> 比赛网址：[https://2021bytectf-g.xctf.org.cn/competition](https://2021bytectf-g.xctf.org.cn/ad5/match/jeopardy/contest_challenge?event=88&hash=0eb40615-7e39-4a76-80b9-ceeac26be59f.event)

<br/>

## writeup

[2021 ByteCTF 初赛部分题目官方Writeup](https://bytectf.feishu.cn/docs/doccnq7Z5hqRBMvrmpRQMAGEK4e)

[ByteCTF-WriteUp-Venom](https://mp.weixin.qq.com/s/k8wrSSra_NO165RLM_CrUw)

[ByteCTF 2021 By W&M（PWN）部分](https://mp.weixin.qq.com/s/fqX-ICojKhe-FBGCLhWB0A)

[ByteCTF 2021 By W&M（REVERSE）部分](https://mp.weixin.qq.com/s/h-wTnquhBTB8EzU5pYmPDg)

[ByteCTF 2021 By W&M（MISC）部分](https://mp.weixin.qq.com/s/_A3TjeAZ0yAnpvxyn0wWCA)

[ByteCTF 2021 By W&M（WEB）部分](https://mp.weixin.qq.com/s/s59xN-QI9oNPrkjhuXtPyw)

[ByteCTF 2021 By W&M（Crypto）部分](https://mp.weixin.qq.com/s/LpFb9qlrazb7o-zZFuZufw)

网盘文档

[2021-ByteCTF-初赛部分题目官方Writeup.pdf](../writeup/2021-ByteCTF-初赛部分题目官方Writeup.pdf)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1r_hCcPY7yIhCcf9tEcaIdQ 提取码：xing

链接：https://pan.xunlei.com/s/VMmAliAW0ZBXV1_HTwadrXDTA1 提取码：za7b

链接：https://ctf.lanzoui.com/b02cjfxtg 密码:xing

<br/>

## 题目信息

### PWN

#### bytezoom(39s,344p)

> nc 39.105.37.172 30012
> nc 39.105.103.24 30012
> nc 39.105.63.142 30012

附件下载：abd6fcb6fc0947088d4422898dc3d2de.zip

<br/>

#### ByteCSMS(11s,666p)

> Bytectf admin will use the system to manage your score, hacker it.
> nc 39.105.37.172 30011
> nc 39.105.103.24 30011
> nc 39.105.63.142 30011

附件下载：bde8669be18944dda399f552a0cb796c.zip

<br/>

#### babydroid(19s,526p)

> Have you watched the live sharing on 10.12?
> nc 39.107.138.253 30001

附件下载：4abf817432f04b35805de5b4aa08846b.zip

<br/>

#### easydroid(14s,606p)

> Have you watched the live sharing on 10.12?
> nc 39.107.138.253 30002
>
> hint: The principle of the vulnerability is introduced at https://bytedance.feishu.cn/file/boxcnWibqpknk3S708qerqHoxiP
>
> And some tips: 1. You should get the flag through local vulnerability first, and then transmit it through the network(You should add `<uses-permission android:name="android.permission.INTERNET"/>` and `android:usesCleartextTraffic="true"` in AndroidManifest.xml). 2. You should use the avd simulator to test locally, so you can better debug the exploit, please pay attention to the Android SDK version matching. 3. You should create a new android project, the package name matches the one in server.py, such as com.bytectf.pwneasydroid .

附件下载：2ad6e34cee194a79b04e024ccca5a29e.zip

<br/>

#### mediumdroid(4s,869p)

> It looks like a weird permission has been granted
> nc 39.107.138.253 30003

附件下载：f8c966f94dcf495cb1267b34238aae47.zip

<br/>

#### chatroom(4s,869p)

> Exploit my chatroom
>
> [http://39.105.37.172:30013](http://39.105.37.172:30013/)
> [http://39.105.103.24:30013](http://39.105.103.24:30013/)
> [http://39.105.63.142:30013](http://39.105.63.142:30013/)
>
> hint: Where is the entry of Headless Chrome?

<br/>

### REVERSE

#### moderncpp(19s,526p)

> flag格式为bytectf{}

附件下载：991ec95d3924419a9bf96b99b6a99a68.zip

<br/>

#### bytecert(4s,869p)

> Cannot connect without a bytecert
> nc 39.107.138.253 30021
>
> hint: To build a qualified bytecert, OpenSSL is your friend, and -utf8 option may help.

附件下载：721391e1e5ba405ba79f4c4a735c5dc1.zip

<br/>

#### 0x6d21(16s,571p)

> Never give up！！！

附件下载：db25b3c1efb14226b425356a3c8a169e.zip

<br/>

#### languages binding(13s,625p)

> 2 program languages binding , enjoy it
>
> hint: new_lang_script.out is a compiled luac script ,but encrypted.

附件下载：6931aec18dcb45b2826f3f0864a218d4.zip

<br/>

#### Baby Bytal(4s,869p)

> Can y0u re@d my 50uRc3 cod3 and ge7 the f1a9?
>
> hint1: Try to read the source code to achieve text flashing effect
>
> hint2: The algorithm achieving text flashing effect is running on GPU with a custom compute shader
>
> hint3: The flag is in the compute shader itself; the image contains no flag. The source code of the compute shader is needed for this problem, while decompiled shader from GPU byte code may not work.

附件下载：175ba50801cd481c96cc5420e48dbbbb.zip

<br/>

#### Mother Bytal(1s,1000p)

> Can y0u f1nd c0rrec7 1nput im@93?
>
> hint: The algorithm running on GPU is a custom 2d image filter

附件下载：3454cb9acb3c46a6952b081d7967e32c.zip

<br/>

### MISC

#### BabyShark(8s,740p)

附件下载：cb5a835747374f52920e5878de657406.zip

<br/>

#### Lost Excel(6s,800p)

> Please find out who leaked this document asap
>
> hint: Block size = 8. Notice repeating patterns.

附件下载：41f3f4157b1a43ebb7baf662fc9b5604.zip

<br/>

#### frequently(25s,454p)

> Someone wants to send secret information through a surreptitious channel. Could you intercept their communications?

附件下载：27bf98ffacef41d6b605fe2534b0a2ab.zip

<br/>

#### HearingNotBelieving(107s,158p)

> Hearing is not believing

附件下载：a1fe791c76c245279317da2230fdc639.zip

<br/>

#### Survey(129s,135p)

> Thank you for playing ByteCTF!
> Visit https://www.wjx.cn/vj/eywKU3d.aspx and get the flag!

```
ByteCTF{h0p3_y0u_Enjoy_our_ch4ll3n9es!}
```

<br/>

#### Checkin(433s,44p)

> 字节跳动安全系列活动主题名字是什么？你造吗？关注【字节跳动安全中心】公众号并回复本次大赛主题（4字），会有意外惊喜！

```
ByteCTF{Empower_Security_Enrich_Life}
```

<br/>

### WEB

#### double sqli(57s,263p)

> easy sqli
>
> http://39.105.175.150:30001/?id=1
> http://39.105.116.246:30001/?id=1
> http://39.105.189.250:30001/?id=1

<br/>

#### Unsecure Blog(10s,689p)

> jdk(x64)：java version "1.8.0_301"
> flag is in：HKEY_CURRENT_USER\ByteCTF\flag
>
> http://39.105.169.140:30000/
> http://39.105.189.155:30000/
>
> 请不要更改jfinal用户的密码
>
> 完整虚拟机镜像，请访问 https://cloud.189.cn/web/share?code=jMNRfemUNnYn 下载
>
> hint1: Update jfinal_blog.sql: https://bytectf.feishu.cn/file/boxcnIu4ezQPdmPGQuoAAAhDWfc ;The full system image will be released soon for you to debug locally
>
> hint2: you need to bypass SSTI's sandbox to get code execution

附件下载：b4b5c689fab74b74b0293ef35b0957e9.zip

<br/>

#### Aginx(1s,1000p)

> A platform can show your essays to express your love for [A-SOUL](https://space.bilibili.com/703007996)!!!
>
> [https://39.105.189.132:30443](https://39.105.189.132:30443/)
> bot nc 39.105.189.132 30000
>
> [https://39.105.56.120:30443](https://39.105.56.120:30443/)
> bot nc 39.105.56.120 30000
>
> [https://39.105.13.40:30443](https://39.105.13.40:30443/)
> bot nc 39.105.13.40 30000
>
> [https://39.105.153.197:30443](https://39.105.153.197:30443/)
> bot nc 39.105.153.197 30000
>
> Note: Please don't use scanner
>
> hint1: Environment: https://bytectf.feishu.cn/file/boxcnEgg8wORkydhrVdSHnpZdDb 请不要扫描目录，flag需要管理员访问/flag获取
>
> hint2: init.sql: https://bytectf.feishu.cn/file/boxcnXZaup2iOONRCW1rQ1zCSLc ; And notice the difference of each response

附件下载：Aginx-d7bd132e16f0de31d97ee072a53037d65bbfc29c.tar.gz、init.sql-209cf88ed3a14e30e74453c835a02cfea622a386.zip

<br/>

#### easy_extract(3s,909p)

> I learn nodejs by building this website in August. There shouldn't be any security issue since there is just one function...
>
> [http://39.107.98.218:30090](http://39.107.98.218:30090/)
> [http://39.105.118.216:30090](http://39.105.118.216:30090/)
> [http://39.105.31.50:30090](http://39.105.31.50:30090/)
>
> hint1: It is important to figure out how the website is started.
>
> hint2: 1. require('tar@6.1.6'); 2.The file size limit is 1024 bytes, which is sufficient to complete the chall.

<br/>

#### sp-oauth(0s,1000p)

> To get flag, you need a rce.
>
> [http://39.105.175.150:30003](http://39.105.175.150:30003/)
> [http://39.105.116.246:30003](http://39.105.116.246:30003/)
>
> hint1: spring-oauth
>
> hint2: hint: https://bytectf.feishu.cn/file/boxcnfs5Ymw5x3gke6ZkVPyvtbg
>
> hint3: The flag is in IdP(30002) and the pom.xml of IdP(30002) may be useful for you. https://bytectf.feishu.cn/file/boxcn5zlv53KGo2fsRqNSLwRSTf
>
> hint4: Admin user will check your link after submit

附件下载：sp-oauth.zip

<br/>

### CRYPTO

#### abusedkey(16s,571p)

> A weak key is used in two insecure cryptographic protocol instance.
>
> http://39.105.181.182:30000/
> http://39.105.115.244:30000/
>
> hint: Document revision 2: https://bytectf.feishu.cn/file/boxcnqmxm83Ph2vI0E0T2e9683d , fixes typos and clarifies some ambiguity.

附件下载：49fc99e2472c46898759fbf681c7f344.zip

<br/>

#### JustDecrypt(22s,487p)

> It's just a decryption system. And I heard that only the Bytedancers can get secret.
>
> nc 39.105.181.182 30001
> nc 39.105.115.244 30001

附件下载：aca681ba2d5c408097e516a65b633416.zip

<br/>

#### Overheard(19s,526p)

> nc 39.105.38.192 30000
> nc 47.95.109.47 30000

附件下载：a7b6c253e0a94c95ba3d5d8beb395510.zip

<br/>

#### easyxor(50s,289p)

> Block cipher is used frequently.

附件下载：2e2e330cebff4716820e9046f8f88e39.zip

