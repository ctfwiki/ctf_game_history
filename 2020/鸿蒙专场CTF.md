## 比赛信息

> 比赛名称：xctf高校网络安全挑战赛-鸿蒙专场
>
> 比赛链接：https://huaweictf.xctf.org.cn/event_jeopardy/contest_challenge/1ae67194-26a0-4c27-bfa0-02e7f470c15d/
>
> 比赛时间：2020-12-27 08:00~2020-12-28 00:00

<br/>

## writeup

[XCTF高校网络安全专题挑战赛-HarmonyOS和HMS专场 官方Writeup](https://www.xctf.org.cn/library/details/5acdc1c31cf4935ac38fce445978888a5710cf11/)

网盘文档：2020-华为CTF-3-WP-Nu1L.pdf

<br/>

## 附件链接

链接：https://pan.baidu.com/s/11H_SU0IF1yz6TlU8FYwXTA 提取码：xing

链接：https://pan.xunlei.com/s/VMdujNB1NORneS_vzmFhljy8A1 提取码：pdt8

链接：https://ctf.lanzoui.com/b02c7t07i 密码:xing

<br/>

## 题目信息

### REALWORLD

#### harmofs01(11s,666p)

> 这道题不计一二三血分值，比赛结束后会由裁判确认调整一二三血分值。

附件下载：task_attachment_for_player_g279gBq.zip

<br/>

#### v8(2s,952p)

> nc 124.71.31.233 1338

附件下载：task_give_to_players.zip

<br/>

#### honormap01(6s,800p)

附件下载：task_attachment_for_player_ITansRi.zip

<br/>

#### ez_ohos01(0s,1000p)

附件下载：task_attachments_x5PUaYL.zip

<br/>

#### luaplayground01(15s,588p)

> Have you ever try to run Lua on HarmoneyOS?
> Run `/bin/flag_app` to get your flag

附件下载：task_for_player.tar_YMuLXOR.gz

<br/>

#### harmodriver(0s,1000p)

> nc 139.9.71.245 9999

附件下载：task_harmodriver.zip

<br/>

#### luaplayground02(9s,714p)

> Just do it. To get flag check app, you need to connect to server, the flag path is under `/etc/flag2.lua`
>
> 本题需要基于 luaplayground01的环境，继续获得flag2.lua

<br/>

#### FHWH(2s,952p)

附件下载：task_attachment_KxfoWE6.zip

<br/>

### WEB

#### 华为HCIE的第一课(24s,465p)

源码下载：华为HCIE的第一课.zip

<br/>

#### 签到啦(268s,69p)

> 冲鸭！！！
>
> http://119.3.228.61:8080/

源码下载：签到啦.zip

<br/>

#### ezlogin(3s,909p)

> http://121.37.196.163:8080

静态文件：ezlogin.zip

<br/>

### MISC

#### ContractGame(1s,1000p)

> nc 124.71.41.121 10001

```bash
[+] sha256(7Bkrm0C9+?).binary.endswith('00000000000000000000')
[-] ?=3584951
[+] passed

We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
Game environment: Ropsten testnet

Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after emit SendFlag(msg.sender) event.
You can finish this challenge in a lot of connections.

[-]input your choice: 1
[+]Your game account:0xbEEb4f9C20339D1CA084916D59C7067c9c2DDdaD
[+]token: Dc5bXz4Sjsgcu+z2AaNJDN6hBV5sGv......
[+]Deploy will cost 889130 gas
[+]Make sure that you have enough ether to deploy!!!!!!(at least > 1 ether)

[-]input your choice: 2
[-]input your token: Dc5bXz4Sjsgcu+z2AaNJDN6hBV5sGv......
[+]new token: 1f+tASzkzaZx9r/5uprxIhbHYn......
[+]Your goal is to emit SendFlag(msg.sender) event in the game contract
[+]Transaction hash: 0xbb12f502efe557a8890dea84a8385356d04cbc84769fb72101683533f58dfde8
```

<br/>

#### RSP(1s,1000p)

>139.159.187.82 7777
>
>不是nc连接，请使用gdb远程调试,flag在flag.txt中

<br/>

### PWN

#### harmoshell(14s,606p)

> nc 121.37.222.236 9999

附件下载：task_attachment_Hwj7Ah7.zip

<br/>

#### harmoshell2(12s,645p)

> nc 139.159.132.55 9999

附件下载：task_attachment_BnJN4BQ.zip

<br/>

#### pwn1(21s,500p)

> nc 139.159.210.220 9999

附件下载：task_attachment_cRrWS7K.zip

<br/>

### REVERSE

#### crash(29s,416p)

附件下载：task_attachment_k7eBhSA.zip

<br/>

#### re123(26s,444p)

附件下载：task_re123.zip

<br/>

#### aRm(17s,555p)

> easy aRm

附件下载：task_attachments.zip

<br/>

#### puzzle(18s,540p)

> solve this MIPS puzzle

附件下载：task_puzzle.zip

<br/>

#### pe(12s,645p)

> Can you run this ARM PE?

附件下载：task_arm_pe.zip