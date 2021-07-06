## 比赛信息

> 比赛时间：2020年10月17日 08:00~19日 08:00
>
> 比赛网址：https://ctf2020.nu1l.com/

<br/>

### writeup

[N1CTF 2020 Crypto Write-Ups](https://rkm0959.tistory.com/167?s=09)

网盘文档（链接见README.md）：

2020-N1CTF-Writeup By Nu1L.pdf

2020-N1CTF-WriteUp By Venom.pdf

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1V17t8na4pcFrBOFAfExc2Q 提取码：xing

链接：https://pan.xunlei.com/s/VMduF55-_a0PBZxGEUCHAHdnA1 提取码：678g

链接：https://ctf.lanzoui.com/b02c7sh9g 密码:xing

[官方题目源码](https://github.com/Nu1LCTF/n1ctf-2020)

<br/>

## 题目信息

### WEB

#### SignIn(78solved,116pt)

> http://101.32.205.189/

源码下载：SignIn.zip

```
database: n1ip、n1key
table n1key: id、key
key: n1ctf20205bf75ab0a30dfc0c
```

<br/>

#### GinDriver(3solved,833pt)

> The backend service will restart every minute but user data will be retained.
>
> https://web.c7466953fb.nu1lctf.com/

附件下载：c2415febb698ba47ed447aa42c1e6a6f.zip

<br/>

#### The King Of Phish (Victim Bot)(35solved,227pt)

> Find a way to get your shell. The flag is on the victim's desktop.
>
> http://101.32.189.101:5000/

源码下载：VictimBot.zip

<br/>

#### The King Of Phish (UserA-PC)(4solved,769pt)

> The flag's location is C:/flag.txt.
>
> http://101.32.189.101:5000/
>
> hint1: userA has some special priviledge.

源码下载：VictimBot.zip

<br/>

#### The King Of Phish (DC)(1solved,1000pt)

> The flag's location is C:/flag.txt.
>
> http://101.32.189.101:5000/

源码下载：VictimBot.zip

<br/>

#### Easy_tp5(11solved,499pt)

> Changed some code of `/thinkphp/library/think/Loader.php`.
>
> `chown -R root:root /var/www/html`
>
> `chmod -R 755 /var/www/html`
>
> `chmod 777 /var/www/html/public`
>
> The challenge environment is restarted every 10 minutes.
>
> Please execute `tac /flag` to get flag
>
> http://101.32.184.39/
>
> hint1: The challenge has nothing to do with MySQL. 
>
> hint2: Please check the security configuration on the phpinfo page carefully.

附件下载：f242832431765611a5739e12616a87e0.zip

<br/>

#### Zabbix_fun(6solved,666pt)

> Please download the attachment to build the local environment yourself. Please note that you can only access http://127.0.0.1:8080/ to attack. If you can get the flag from secret_agent, describe the attack process in detail, and finally send it to my mail: iamstudy@126.com, I will give you the URL of the real online environment, and you can reproduce the attack again to obtain the real flag. Writeup must be described in detail. Finally, please don’t damage the environment. Thank you.
>
> hint1: url: http://101.32.204.150 The challenge environment is restarted every 10 minutes.

附件下载：3945b466579baa3c46ee787ee30b7c9d.zip

<br/>

#### Docker_manager(0solved,1000pt)

> The challenge environment is restarted every 10 minutes.
>
> http://119.28.105.118/

附件下载：734e3f68793a3bb58cfa3a1f8d7d6b03.zip

<br/>

### PWN

#### EasyWrite(27solved,278pt)

> write? what? where?
>
> nc 124.156.183.246 20000

附件下载：38487d6aafac87273aaf671b8e423457.zip

<br/>

#### SignIn(60solved,146pt)

> nc 47.242.161.199 9990
>
> Due to network reasons, the remote server may be slow, please test locally before attacking the remote

附件下载：e06c4f7b2b1c66e609b6f6e5118af7f1.zip

<br/>

#### Babyrouter(4solved,769pt)

> Please attack remotely after a successful local test
>
> http://8.210.119.59:9990/
>
> hint1: The method my exp used is Stack Overflow.

附件下载：12d313be010f3c6fe9dd7bf617fcc8ac.zip

<br/>

#### Escape(2solved,909pt)

> Seems that browser exploitation is becoming an essential skill for pwners lately. Let's see if you meet the standards.
>
> http://47.242.33.101:13337/

附件下载：033868cf6ff18a1d9d903d92bf658e41.tgz.zip

<br/>

#### Kemu(1solved,1000pt)

> Have you learned pci device?
>
> ssh pwn:pwn 8.210.166.195

附件下载：4391528d9c6dca9441918d5927253d23.tar.gz

<br/>

#### Echoserver(6solved,666pt)

> Which architecture do you hate most?
>
> nc 150.158.156.120 23333
>
> Notice: There are no `/bin/sh` or `/bin/cat` in remote server , please use `orw` to get the flag
>
> hint1: there is no need to bruteforce, try to move your eyes out of the stack

附件下载：338320ea08f14c7b2afb6a9581c9bdf7.zip

<br/>

#### W2L(3solved,833pt)

> Let's exploit the 2017 bug in 2020.
>
> nc 47.242.143.220 6969

附件下载：93bb92c3433926a88c271572c9335ee8.tar.gz

<br/>

### CRYPTO

#### VSS(38solved,212pt)

> Just a simple visual threshold scheme.

附件下载：4c2493e0504e6f8e4e044fd8c313aadd.zip

<br/>

#### BabyProof(8solved,587pt)

> An easy non-interactive zero-knowledge proof.
>
> nc 101.32.203.233 23333

附件下载：aa99a69fe535aa3d2747e60840d84e01.zip

<br/>

#### Curve(22solved,322pt)

> I need some special curves for my project. Can you do me a favor?
>
> nc 47.242.140.57 9998

附件下载：f40a64dcc2489a09b010dbba81475042.zip

<br/>

#### Easy RSA?(5solved,714pt)

> Oh my god, how linear it is

附件下载：5a4361724d5d2ff3e2ce8789b5b798ad.zip

<br/>

#### FlagBot(23solved,312pt)

> A simple bot for broadcasting flags.

附件下载：10c98b6259b3106189b5d22203a8b745.zip

<br/>

### REVERSE

#### Oflo(92solved,102pt)

附件下载：8e29204565c44a402d280791f54659b1.zip

<br/>

#### Oh My Julia(8solved,587pt)

附件下载：43bd298957c1b89c4fad9c0bf55024cc.zip

<br/>

#### EasyAPK(10solved,525pt)

> Stay positive and be patient (with this challenge).

附件下载：27b981aa7ffa16eedfb9ce5c60416ac8.apk

<br/>

#### Fixed Camera(11solved,499pt)

> Arrow keys to operate the lens

附件下载：e62e946640f508573c571a41d5cef93b.7z

<br/>

#### N1vault(2solved,909pt)

> We provide you with the ultimate security solution: n1vault.

附件下载：80f32c0476290dbd8a7440bb2a2874fb.zip

<br/>

#### EasyRE(6solved,666pt)

附件下载：1775f94da8b71fac02839312a8687cbd.zip

<br/>

#### Auth(1solved,1000pt)

> This must be the most contrived challenge I've ever created...
>
> nc 8.210.115.106 13337
>
> nc 47.57.188.114 13337
>
> hint1: You don't need to bypass the sandbox, you can get the flag by interacting with auth.exe .

附件下载：48801c9610ab191043e450017957f282.tgz.zip

<br/>

#### BabyCompiler(2solved,909pt)

> hint1: tokens: YACC LEX CTF FUN + - * / ^ numbers

附件下载：4cd3684118081d38f529c45539c25d76.zip

<br/>

#### BabyOS(2solved,909pt)

> ./n1ctf
>
> hint1: ELF / XOR

附件下载：0eeb145e3a66028cd200bfcb6198c8dc.zip

<br/>

#### Rrr(1solved,1000pt)

> Maybe you need a powerful tool

附件下载：ad53b84b1b0adab2aad7040dba313e9f.zip

<br/>

#### N1egg In Fixed Camera(37solved,217pt)

> Arrow keys to operate the lens

<br/>

### MISC

#### SignIn(835solved,69pt)

> Welcome to N1CTF 2020.
>
> n1ctf{welc0m3_to_n1ctf2020_ctfers}

<br/>

#### N1egg-AllSignIn(17solved,383pt)

> flags = misc_signin_flag + web_signin_flag + pwn_signin_flag + re_oflo_flag + crypto_vss_flag
>
> flag = "n1egg{" + MD5.new(flags.encode()).hexdigest() + "}"
>
> print(flag)

<br/>

#### Filters(10solved,525pt)

> http://101.32.188.147:23333/
>
> hint1: This challenge has an unintended solution. You could solve this challenge with ease. Additionally, you could also try to solve this challenge in the right way which is more interesting. Enjoy your game! Sorry for my bad.

附件下载：e9806d5a92c8fbb754c5119d5b093b5f.zip

<br/>

#### GinDriver Revenge(1solved,1000pt)

> Maybe you should get a shell?
>
> P.S. Challenge address is identical to GinDriver,
>
> P.P.S. Backend services will restart every minute, user data will be kept.
>
> https://web.c7466953fb.nu1lctf.com/
>
> hint1: SSH service in the container is maped to 22 port of the host
>
> hint2: Backend service is launched by www-data, pay attention to /etc/passwd file.
>
> hint3: This challenge can be solved after gaining file uploading.
>
> Hint4: pam