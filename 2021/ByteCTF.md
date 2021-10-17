## 比赛信息

> 比赛名称：2021字节跳动安全范儿高校挑战赛
>
> 比赛时间：2021-10-16 10:00:00 —— 2021-10-17 18:00:00
>
> 比赛网址：[https://2021bytectf-g.xctf.org.cn/competition](https://2021bytectf-g.xctf.org.cn/ad5/match/jeopardy/contest_challenge?event=88&hash=0eb40615-7e39-4a76-80b9-ceeac26be59f.event)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1r_hCcPY7yIhCcf9tEcaIdQ 提取码：xing

链接：https://pan.xunlei.com/s/VMmAliAW0ZBXV1_HTwadrXDTA1 提取码：za7b

链接：https://ctf.lanzoui.com/b02cjfxtg 密码:xing

<br/>

## 题目信息

### PWN

#### bytezoom(s,p)

> nc 39.105.37.172 30012
> nc 39.105.103.24 30012
> nc 39.105.63.142 30012

附件下载：abd6fcb6fc0947088d4422898dc3d2de.zip

<br/>

#### ByteCSMS(s,p)

> Bytectf admin will use the system to manage your score, hacker it.
> nc 39.105.37.172 30011
> nc 39.105.103.24 30011
> nc 39.105.63.142 30011

附件下载：bde8669be18944dda399f552a0cb796c.zip

<br/>

#### babydroid(s,p)

> Have you watched the live sharing on 10.12?
> nc 39.107.138.253 30001

附件下载：4abf817432f04b35805de5b4aa08846b.zip

<br/>

#### easydroid(s,p)

> Have you watched the live sharing on 10.12?
> nc 39.107.138.253 30002
>
> hint: The principle of the vulnerability is introduced at https://bytedance.feishu.cn/file/boxcnWibqpknk3S708qerqHoxiP
>
> And some tips: 1. You should get the flag through local vulnerability first, and then transmit it through the network(You should add `<uses-permission android:name="android.permission.INTERNET"/>` and `android:usesCleartextTraffic="true"` in AndroidManifest.xml). 2. You should use the avd simulator to test locally, so you can better debug the exploit, please pay attention to the Android SDK version matching. 3. You should create a new android project, the package name matches the one in server.py, such as com.bytectf.pwneasydroid .

附件下载：2ad6e34cee194a79b04e024ccca5a29e.zip

<br/>

#### mediumdroid(s,p)

> It looks like a weird permission has been granted
> nc 39.107.138.253 30003

附件下载：f8c966f94dcf495cb1267b34238aae47.zip

<br/>

#### chatroom(s,p)

> Exploit my chatroom
>
> [http://39.105.37.172:30013](http://39.105.37.172:30013/)
> [http://39.105.103.24:30013](http://39.105.103.24:30013/)
> [http://39.105.63.142:30013](http://39.105.63.142:30013/)
>
> hint: Where is the entry of Headless Chrome?

<br/>

### REVERSE

#### moderncpp(s,p)

> flag格式为bytectf{}

附件下载：991ec95d3924419a9bf96b99b6a99a68.zip

<br/>

#### bytecert(s,p)

> Cannot connect without a bytecert
> nc 39.107.138.253 30021
>
> hint: To build a qualified bytecert, OpenSSL is your friend, and -utf8 option may help.

附件下载：721391e1e5ba405ba79f4c4a735c5dc1.zip

<br/>

#### 0x6d21(s,p)

> Never give up！！！

附件下载：db25b3c1efb14226b425356a3c8a169e.zip

<br/>

#### languages binding(s,p)

> 2 program languages binding , enjoy it
>
> hint: new_lang_script.out is a compiled luac script ,but encrypted.

附件下载：6931aec18dcb45b2826f3f0864a218d4.zip

<br/>

#### Baby Bytal(s,p)

> Can y0u re@d my 50uRc3 cod3 and ge7 the f1a9?
>
> hint1: Try to read the source code to achieve text flashing effect
>
> hint2: The algorithm achieving text flashing effect is running on GPU with a custom compute shader
>
> hint3: The flag is in the compute shader itself; the image contains no flag. The source code of the compute shader is needed for this problem, while decompiled shader from GPU byte code may not work.

附件下载：175ba50801cd481c96cc5420e48dbbbb.zip

<br/>

#### Mother Bytal(s,p)

> Can y0u f1nd c0rrec7 1nput im@93?

附件下载：3454cb9acb3c46a6952b081d7967e32c.zip

<br/>

### MISC

#### BabyShark(s,p)

附件下载：cb5a835747374f52920e5878de657406.zip

<br/>

#### Lost Excel(s,p)

> Please find out who leaked this document asap
>
> hint: Block size = 8. Notice repeating patterns.

附件下载：41f3f4157b1a43ebb7baf662fc9b5604.zip

<br/>

#### frequently(s,p)

> Someone wants to send secret information through a surreptitious channel. Could you intercept their communications?

附件下载：27bf98ffacef41d6b605fe2534b0a2ab.zip

<br/>

#### HearingNotBelieving(s,p)

> Hearing is not believing

附件下载：a1fe791c76c245279317da2230fdc639.zip

<br/>

#### Checkin(s,p)

> 字节跳动安全系列活动主题名字是什么？你造吗？关注【字节跳动安全中心】公众号并回复本次大赛主题（4字），会有意外惊喜！

```
ByteCTF{Empower_Security_Enrich_Life}
```

<br/>

### WEB

#### double sqli(s,p)

> easy sqli
>
> http://39.105.175.150:30001/?id=1
> http://39.105.116.246:30001/?id=1
> http://39.105.189.250:30001/?id=1

<br/>

#### Unsecure Blog(s,p)

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

#### Aginx(s,p)

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

#### easy_extract(s,p)

> I learn nodejs by building this website in August. There shouldn't be any security issue since there is just one function...
>
> [http://39.107.98.218:30090](http://39.107.98.218:30090/)
> [http://39.105.118.216:30090](http://39.105.118.216:30090/)
> [http://39.105.31.50:30090](http://39.105.31.50:30090/)

<br/>

#### sp-oauth(s,p)

> To get flag, you need a rce.
>
> [http://39.105.175.150:30003](http://39.105.175.150:30003/)
> [http://39.105.116.246:30003](http://39.105.116.246:30003/)
>
> hint1: spring-oauth
>
> hint2: hint: https://bytectf.feishu.cn/file/boxcnfs5Ymw5x3gke6ZkVPyvtbg

```java
//sp-oauth_hint1.txt
@RequestMapping("/zwo/callback")
    public String getToken(@RequestParam String code, HttpServletRequest request) throws Exception{
        
        ...
        
        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("grant_type","authorization_code");
        params.add("code",code);
        params.add("client_id","62608e08adc29a8d6dbc9754e659f125");
        params.add("client_secret","9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx9");
        params.add("redirect_uri",java.net.URLDecoder.decode(new String(request.getRequestURL()), "UTF-8"));
        HttpEntity<MultiValueMap<String, String>> requestEntity = new HttpEntity<>(params,headers);
        ResponseEntity<String> response = restTemplate.postForEntity("http://"+ idpsocket +"/oauth/token", requestEntity, String.class);
        String resp  = response.getBody();
        
        ...

    }
```

<br/>

### CRYPTO

#### abusedkey(s,p)

> A weak key is used in two insecure cryptographic protocol instance.
>
> http://39.105.181.182:30000/
> http://39.105.115.244:30000/
>
> hint: Document revision 2: https://bytectf.feishu.cn/file/boxcnqmxm83Ph2vI0E0T2e9683d , fixes typos and clarifies some ambiguity.

附件下载：49fc99e2472c46898759fbf681c7f344.zip

<br/>

#### JustDecrypt(s,p)

> It's just a decryption system. And I heard that only the Bytedancers can get secret.
>
> nc 39.105.181.182 30001
> nc 39.105.115.244 30001

附件下载：aca681ba2d5c408097e516a65b633416.zip

<br/>

#### Overheard(s,p)

> nc 39.105.38.192 30000
> nc 47.95.109.47 30000

附件下载：a7b6c253e0a94c95ba3d5d8beb395510.zip

<br/>

#### easyxor(s,p)

> Block cipher is used frequently.

附件下载：2e2e330cebff4716820e9046f8f88e39.zip

