## writeup

#### 官方

https://github.com/SycloverSecurity/SCTF2020

/writeup/SCTF2020+官方Write-up.pdf

#### 其他

[星盟安全SCTF--WriteUp](https://mp.weixin.qq.com/s/au7wmC-JLapP5fxhen5qVw)

[SCTF2020 官方Write-up](https://mp.weixin.qq.com/s/nvSnGJ_GJ5LAY3t09KPXig)

## WEB

### pysandbox

> i love py!!(Each docker will reboot every 3 mins，so please launch the remote attack after successful exploitation in your own local environment)
> China：
> http://39.104.25.107:10000~10010
> Overseas：
> http://8.208.91.150:10000~10010

附件下载：pysandbox.zip



### CloudDisk

> http://120.79.1.217:7777/
>
> 1.【链接】Koa框架教程
> http://www.ruanyifeng.com/blog/2017/08/koa.html

附件下载：app.zip



### bestlanguage

> Best wish!
> China：
> http://39.104.93.188
> Overseas：
> http://8.208.85.45

附件下载：bestlanguage.zip



### UnsafeDefenseSystem

> don’t need to scan , flag is in /flag .The server is remade every 3 minutes. good luck to you
> if you get the flag, please don’t destory the environment.
> China:
> http://39.99.41.124/public/
> Overseas:
> http://8.208.102.48/public/



### Login Me

> Time is flag!
> 1.Please do not use the scanner, it will not work.
> 2.Please do not try to brute-force username and password, it will not work.
> 3.Please do not damage the application context with malicious intent.
> 4.The server reboots every two hour.
> China && Overseas:
> http://120.24.35.104:8888
> hint1:Not sql injection, non-default key, no access restrictions to the extranet, nginx front limit request frequency (16r/s)
> hint2: Compare the differences in encode or decode the execution methods between CAS 4.1.X-4.1.6 and CAS 4.1.7-4.2.X，you’ll find vuln.



### One step to get flag

> Try to bypass a mounted Rails engine WAF that rudely blocks all access to the /getflag.
>
> 8.208.89.219:8080/getflag
>
> Hint1:
> config/route.rb:
> Waf::Engine.routes.draw do
> get ‘*all’, to: ‘requests#block’
> end
>
> get ‘getflag’, to: ‘application#getflag’
>
> Hint2:
> RoR follows the “Convention Over Configuration” principle, e.g., there is some sort of routing convention between the high-level Rails apps



### pysandbox2

> Same as pysandbox，but must rce
> http://39.104.90.30:10000~10010



### Login Me Aagin

> Java is jar and war!
> 1.Please do not use the scanner, it will not work.
> 2.Please do not try to brute-force username and password, it will not work.
> 3.Please do not damage the application context with malicious intent.
> 4.The server cannot access the Internet.
> http://120.79.1.217/login
>
> Hint：
> step 1 : Establish proxy by register filter or servlet dynamically
> step 2 : https://gv7.me/articles/2020/how-to-detect-tomcat-ajp-lfi-more-accurately/ && https://issues.apache.org/jira/browse/SHIRO-760
>
> By the way,the server reset every 30 minutes

附件下载：SCTF2020_Login_Me_Aagin.zip（204M）



### Jsonhub

> I know my code is bad, but there should not be a lot of vulnerabilities
> China：
> http://39.104.19.182
> Overseas：
> http://8.208.80.172
> PS: This challenge differs from China to oversea, so make sure you have the right attachment according to your ip before you start the challenge.

附件下载：jsonhub-cn.zip、jsonhub-overseas.zip



## CRYPTO

### RSA

> 121.199.14.145 12345

附件下载：RSA.zip



### Lattice

附件下载：Lattice.zip



## MISC

### Can you hear

> Enjoy

附件下载：Can you hear.zip

```
SCTF{f78fsd1423fvsa}
```



### PassWord Lock

> Help me open the lock.

附件下载：PassWord Lock.zip



### sing-in

> welcome to sctf2020,here is your flag:
> t.me/SCTF2020

```
SCTF{welc0m3_t0_sctf2020_friends}
```



### AndroidDisplayBridge

> Finding his android phone’s touchscreen not working, he logged in his computer and painted something…

附件下载：attachment.zip



### Dou dizhu

> how to play:
> https://en.wikipedia.org/wiki/Dou_dizhu#Rules
> if somebody quit in an online game, the game will down,win to get the flag
> China&&Oversea:
> http://120.79.1.217:8877/

游戏源码：https://github.com/mailgyc/doudizhu

```
SCTF{Did-you-enj0y-1t?~~~~~~~~~!!~!!!~}
```



### EasyMisc

> galf_si_erehw

附件下载：b8f0ea44704f45eb800df8df0fb5be08.zip

```
SCTF{St@Y_@T_H0Me}
```



### PassWord Lock Plus

> Lock Plus.

附件下载：PassWord Lock Plus.zip



## Reverse

### flag_detector

> Log in and verify your flag.

附件下载：ac949ff033df44b888a91774e163b10c.zip



### get_up

> A good afternoon is always accompanied by a cup of reserve

附件下载：87f32158a2a34deca72a0788f2ea299b.zip



### signin

> SIGN

附件下载：signin.zip



### Orz

> !!!Orz

附件下载：2f055e8a399c40d09e0a5c86ba37f506.zip



### easyre

> find me

附件下载：easy.zip



### secret

> I have a secret,can you find it?（Please run it on DVM)

附件下载：app-release.zip



## PWN

### EasyWinHeap

> Easy Windows Heap Exploit
> China:
> nc 47.94.245.208 23333
> Overseas:
> nc 47.251.4.171 23333

附件下载：19f0ddc0acc44efb8b64420b7bea2bd7.zip



### coolcode

> easy code，hava fun.
> nc 39.107.119.192 9999

附件下载：058dc23d76854fab9c0ee77dd819c221.zip



### EasyMojo

> Chrome full chain exploit
> Chromium version: x64 release 85.0.4154.0
> OS : Windows Server 2019, build 17763.1282
>
> chrome.dll.pdb:
> https://yunpan.360.cn/surl_yYh5wP8rI2h （password：f056）
> https://mega.nz/file/AzABkIwC#UUrNfJc6S1IjeLwVZOlYV3dfb-rwboPg5eQCes0rfvo
>
> Before exploiting you need to send a string which length is 36 as your token.
> When you choose to upload a .zip, remember to put all .html and .js into the root of the .zip, and then name the webpage to be loaded as “exploit.html”.
> Once you exploit successfully, execute "C:\Users\pwnbox\EasyMojo\readflag.exe <token>" to get flag.
>
> If you don’t exploit once, try a few more times. And if the server is not responding immediately, it may be because the maximum number of connections has been reached, please be patient.
> China:
> nc 47.108.71.166 23333
> Overseas:
> nc 47.251.35.157 23333
>
> Attachment:
> https://yunpan.360.cn/surl_yYhWecUZhzQ （password：a76d）
> https://mega.nz/file/ZmIUgAZR#fZ4iiG_WGzkTpxMqWsHQVAzpazcBHa4t81QQMQ8OEcc
>
> hint1:
>
> ```python
> def POW(sample_hash):
> 	for c in itertools.product(string.printable[0:36], repeat=5):
> 		sample = f"SCTF{’’.join©}"
> 		if sha256(sample.encode(‘utf-8’)).hexdigest() == sample_hash:
> 			return sample
> ```
>
> hint2:
> ROP is very unstable 😃

附件太大了(2.5G+101M)，无备份



### snake

> Do you like to play snake
>
> ps:There is a problem with the remote operation, but if the exp is successful locally, the same exp will work for the remote. It will not affect the answer to the question
> nc 39.107.244.116 9999

附件下载：snake.zip



### MSRC Top 0xFFFFFFFF

> EoP after resolving EasyWinHeap.
> The binary files are located in c:\users\pwn\EoP, and flag.txt is located in the administrator’s desktop.
>
> EasyWinHeap server 47.94.245.208
>
> hint:
> Try to exploit logic bug instead of memory corruption