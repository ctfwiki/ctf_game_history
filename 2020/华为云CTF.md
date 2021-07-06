## 比赛信息

> 比赛名称：xctf高校网络安全挑战赛-华为云专场
>
> 比赛网址：https://huaweictf.xctf.org.cn/
>
> 报名网址：https://huaweictf2020.xctf.org.cn/
>
> 比赛时间：2020-12-20 08:00~2020-12-21 00:00

注：本次比赛没有crypto题目，不是丢失

<br/>

### writeup

[XCTF华为云专题赛 官方Writeup](https://www.xctf.org.cn/library/details/b69108559ccd6ff0fa3ec79e3f2f198f121e90a8/)

网盘文档：

2020-华为云专场-Writeup-Venom.pdf

2020-华为CTF-1-WP-Nu1L.pdf

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1lHk4Cc3KtjXD2V67Q74mAw 提取码：xing

链接：https://pan.xunlei.com/s/VMdulVOCmiISmYScJtOOOqDXA1 提取码：6usd

链接：https://ctf.lanzoui.com/b02c7t1uh 密码:xing

[官方题目源码](https://github.com/huaweictf/xctf_huaweicloud-qualifier-2020)

<br/>

## 题目信息

### WEB

#### hids(28s,434p)

> 启动场景后，访问赛题可能需要1-3分钟左右，等待服务启动，可尝试多次刷新题目url。
>
> hint: readflag运行90秒后才会打印出flag

源码下载：hids.zip

<br/>

#### cloud(5s,833p)

> 提交flag1的答案

```
"login success, /static/tools.zip, /wsproxy"
```

部分附件下载：tools.zip

<br/>

#### mine2(53s,277p)

源码下载：暂无

<br/>

#### mine1_1(80s,202p)

源码下载：mine1_1.zip

<br/>

#### pyer(416s,29p)

源码下载：pyer.zip

<br/>

#### webshell_1(105s,161p)

> 启动场景后，访问赛题可能需要1-3分钟左右，等待服务启动，可尝试多次刷新题目url。
>
> hint: flag必须通过执行命令cat /flag的方式才能获取到

源码下载：webshell_1.zip

<br/>

#### 签到(439s,43p)

> http://119.3.228.61:8080/

```
flag{w3lc0m3_t0_huAw3iXCTF}
```

源码下载：签到.zip

<br/>

### REVERSE

#### weird_lua(2s,952p)

附件下载：task_1.zip

<br/>

#### divination(7s,769p)

附件下载：task_divination.zip

<br/>

### PWN

#### cpp(32s,392p)

> nc 124.70.12.210 10002

附件下载：task_attachment.zip

<br/>

#### game(8s,740p)

> nc 121.36.21.113 10004
> 本题没附件，emmm

```bash
----------Welcome to  GEG!!!----------
------------------data info------------------
f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAwAVAAAAAAABAA.....................................
..................................................................................
AAAAAAAAAAAAAAAAjRAAAAAAAAD8AAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA==
Hi, input code:
bad input
```

数据下载：code.zip

<br/>

#### fastexec(1s,1000p)

> nc 124.70.14.0 10006
>
> hint: 无需泄漏，Shellcode直接注入，请调试好偏移

附件下载：task_attachment_RaCCoDH.zip

<br/>

#### fastga(0s,1000p)

> nc 124.70.12.65 10007 10006 两个端口
>
> hint: 客户机guest agent可以被替换，请检查进程，查看qemu手册进行突破

附件下载：task_attachment_g1YmcID.zip

<br/>

#### mysqli(0s,1000p)

> http://121.36.12.116:10008/
>
> hint: qop技术~~~

附件下载：task_attachment_L64jCmy_dyEfjeN.zip

<br/>

#### miniobs(0s,1000p)

> flag在/home/pwn/flag；
>
> 给的二进制附件中的ak/sk只有下载文件权限没有上传权限，服务器端的程序有上传权限
>
> nc 121.36.28.133 60001
>
> hint1: 栈溢出
>
> hint2: 题目内容描述有更新，请详细阅读！

附件下载：task_main.zip

<br/>

#### nday_container_escape(0s,1000p)

> 本题目要求选手先使用本地环境验证成功后，发送队伍名称及writeup至hwc_qualifier_2020@126.com，出题人审核有效后，提供在线环境，选手获取flag后提交。
>
> 本地环境如下，使用docker-compose up -d 启动后，等待约3分钟直到容器内服务启动，以ctf/ctf用户通过ssh登录，即可进入容器内，选手需要通过容器逃逸至宿主机，获取flag
>
> hint1: 1. cve-2020-8558 2. cve-2020-15257
>
> hint2: 1. 与特权容器无关 2. 有完整利用思路的，但暂时没有利用成功的，可以发送writeup试试
>
> hint3: k8s=1.18.3-00
>
> hint4: containerd=1.3.3-0ubuntu2

附件下载：task_docker-compose.zip

<br/>

#### qemuzzz_1(9s,714p)

> nc 124.70.28.14 9999

附件下载：task_attachment_7mfbXgk_X1c7px4.zip

<br/>

### MISC

#### ethenc(2s,952p)

> nc 124.70.31.199 10001

```bash
[+] sha256(PALIoOqQ+?).binary.endswith('00000000000000000000')
[-] ?=c218
[+] passed

We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Game environment: Ropsten testnet

Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after emit OhSendFlag(address addr) event.
You can finish this challenge in a lot of connections.

[-]input your choice: 1
[+]Your game account:0x5A173c16576D0EA55e22d0630857f22B0E78bdb3
[+]token: EbIIKKxa1GC......
[+]Deploy will cost 565486 gas
[+]Make sure that you have enough ether to deploy!!!!!!

[+]new token: EVgQPuk......
[+]Your goal is to emit OhSendFlag(address addr) event in the game contract
[+]Transaction hash: 0x46c404e0ec6380c198955b5d54518d45d0ada57d36fc6d51d97717b676d14cf2
```

<br/>

#### Who Moved My Flag(11s,666p)

> 此题flag格式为 ctf{}

附件下载：task_flow.zip