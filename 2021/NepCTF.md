## 比赛信息

> 比赛名称：NepCTF欢乐个人赛
>
> 比赛网址：https://camp.hackingfor.fun/
>
> 比赛时间：2021年03月20日 10:00~2021年03月22日 00:00

<br/>

## 附件连接

链接：https://pan.baidu.com/s/1OSQT6ExUoQTp6kWEmUtOfg 提取码：5555

链接：https://t1m.lanzous.com/b0afobfbc 密码:5555

阿里云盘：暂无

<br/>

## 题目信息

### WEB

#### little_trick(151s,10p)

> This only requires a little trick！！！ just enjoy it

```php
# index.php
<?php
    error_reporting(0);
    highlight_file(__FILE__);
    $nep = $_GET['nep'];
    $len = $_GET['len'];
    if(intval($len)<8 && strlen($nep)<13){
        eval(substr($nep,0,$len));
    }else{
        die('too long!');
    }
?>
# nepctf.php
<?php
$flag = 'NepCTF{n3pn3p_l1ttle_tr1ck_c0me_bAck}';
?>
```

<br/>

#### 梦里花开牡丹亭(38s,87p)

> 简单的PHP序列化

<br/>

#### bbxhh_revenge(35s,89p)

> 小红花又双叒叕遇到黑页了，不过这个黑页好像有点奇怪 让小红花回忆起来了刚学CTF的那段时光...
>
> 提示1：shell_exec 用不了，就试试别的吧，让自己的 ip 动起来~

<br/>

#### faka_revenge(10s,99p)

> 张三的发卡网站去年被一群禽兽给~~了，不甘心的他留下了没有技术的泪水。
>
> a few months later，faka2.0 is back full of anger。

附件下载：faka.zip

<br/>

#### gamejs(6s,100p)

> 好好玩游戏不香吗

<br/>

#### easy_tomcat(6s,100p)

> 简单的Tomcat
>
> 请访问 /Easy_Tomcat
>
> please interview /Easy_Tomcat

<br/>

#### 画皮(0s,100p)

> 简单题，直接莽就行

<br/>

### PWN

#### [签到] 送你一朵小红花(70s,56p)

> 小红花一朵(๑•̀ㅂ•́)و✧

附件下载：xhh.zip

<br/>

#### easystack(35s,89p)

> 这么简单的栈溢出？！

附件下载：easystack.zip

<br/>

#### scmt(35s,89p)

附件下载：scmt.zip

<br/>

#### sooooeasy(11s,99p)

> 难得有如此easy的题了，快来签到吧

附件下载：sooooeasy.zip

<br/>

#### easypwn(5s,100p)

> Libc 2.27

附件下载：easypwn.zip

<br/>

#### superpowers(5s,100p)

> 拥有超能力的你会看些什么呢？ 怎么开心怎么来 gogogo！

附件下载：superpower__.zip

<br/>

#### NULL_FXCK(1s,100p)

> hook,hook啊,你怎么就不能用了呢,呜呜呜呜呜呜呜

附件下载：attachment.tar

<br/>

#### escape(0s,100p)

> qemu escape 成功弹出计算器，请录制视频连同exp打包发邮箱 tina2114@outlook.com
>
> 链接：https://pan.baidu.com/s/1JH-jwoAWw0QN7tkNERwTXg 提取码：jtc9
>
> hint:注意一下启动命令

附件下载：escape.7z（690.5M）

<br/>

### MISC

#### 签到(96s,17p)

> sharun：这题有很多解啊

附件下载：签到.zip

<br/>

#### 冰峰历险记(41s,85p)

> 冒险者小张在迷宫里意外发现了坏女人留下的宝箱，你能帮他解开秘密么？

附件下载：Adventure of 1cepeak.zip

<br/>

#### 出题人日记(26s,94p)

> 我把茶包的出题日记找到了，里面居然有！！！

附件下载：出题人日记.zip

<br/>

#### 我是间谍2nd(15s,98p)

> 坏女人往我的u盘里偷偷放了一个程序，你能找出她干了什么吗？remember: try to forgery ip,but not to reverse it.

附件下载：imspy2_packed.zip

<br/>

#### 我没有py(11s,99p)

> 他说他没有py，他可是不是没有py的。啪的一下，就解出了1cePeak的压轴题，很快啊。
>
> 链接：https://pan.baidu.com/s/1ds8L-NIJWWkXO88FRiqvdg 
> 提取码：ft1e 

附件下载：我没有py.zip（966.5M）

<br/>

#### make_hsy_great_again(8s,99p)

> Q师傅是韩商言的粉丝，前段日子他刚组装了台新电脑，并且要求我帮他装系统，我在他电脑里发现了这个。

附件下载：make hsy great again_.rar

<br/>

#### 我没有py-新(1s,100p)

> 昨天下午，出题人本人公开发表了过激的言论，在此向大家致歉。当然，我所说的更多是因为对这种现象的气愤，最近CTF圈的乱象愈演愈烈，有的队伍频频闹出笑话，相信大家也都有目共睹。我相信每一个热爱CTF的人都不希望CTF圈再这样腐烂下去。我出这道题的初衷，也是想嘲讽这种现象。在此，希望借以此题，能与大家共勉，一起维护CTF圈的纯净！最后，祝大家玩得开心！ 
>
> 由于一天时间没有人用正解做出此题，所以附上提示:微信版本是:3.0.0.57
>
> 链接：https://pan.baidu.com/s/1qh-Vi5Xo8sUrHjBnI6AKcQ 提取码：itww

附件下载：py3.zip（1.15G）

<br/>

#### DoYouKnowVmess(0s,100p)

> 傅总在翻墙浏览网页的时候下载了一份文件，打开后没多久电脑就上线了，你能帮他找出这个文件请求了什么api站点吗？ 
>
> 请在虚拟机下运行！！
>
> 请在虚拟机下运行！！ 
>
> 请在虚拟机下运行！！

附件下载：DoYouKnowVmess.zip

<br/>

#### 简单取证(0s,100p)

> 傻润的数据库崩了，你可以他恢复吗
>
> 链接：https://pan.baidu.com/s/1NCzeeeYc8KMBT-SyJvTVrA 提取码：cjl3

附件下载：sharun.tar（525.9M）

<br/>

### REVERSE

#### hardcsharp(131s,10p)

> 我觉得很hard，你觉得呢（doge

附件下载：hardcsharp.rar

<br/>

#### 二十六进制(60s,68p)

> 提交格式：Nep{md5(输入的数字)}（32位小写MD5） fix：第一位key是5 9位最小解

附件下载：二十六进制.zip

<br/>

#### easy_mips(60s,68p)

> 听说solar大神竟然会mips！？

附件下载：easymips1.zip

<br/>

#### password(48s,79p)

> 简单粗暴

附件下载：password.zip

<br/>

#### worrrrms(25s,94p)

> go go go ghost
>
> 报毒请忽略即可

附件下载：worrrrms.7z

<br/>

#### 勇士打恶龙(6s,100p)

> 长路漫漫
>
> 提交格式：Nep{md5(flag)}（32位小写MD5）

附件下载：re__.zip

<br/>

#### Qriver(5s,100p)

> 看我熟练的IDA->Select Debugger->Local Windows Debugger->F9 咦？

附件下载：Qriver.rar

<br/>

#### Spy-woman(1s,100p)

> 关闭windows强制签名，使用inf安装，使用sc start scanner启动驱动，并以管理员权限运行user.exe

附件下载：BadWoman is spying on your file.zip

<br/>

### CRYPTO

#### Real_Base(82s,39p)

> base64？林北不太确定

附件下载：Real_base.zip

<br/>

#### 你们一天天的不写代码，难道是在等爱情吗(55s,73p)

> 打南边来了一群奇奇怪怪的人，他说他们是小银、小盲、小精、小跳。。。。但是他们七嘴八舌的，剩下的就听不清了，他们将要去北边见凯撒，后来他们过了三个畸形的栅栏后终于见到了凯撒大帝（粉红色笔记如不需要可以当无

附件下载：你们一天天的不写代码难道是在等爱情吗.zip

<br/>

#### ChildRSA(8s,99p)

> 这题林北都会做啦

附件下载：rsa.zip

<br/>

#### easyEncryption(6s,100p)

> flag格式为flag{}

附件下载：easy_encryption.zip

<br/>

#### lowExponent(3s,100p)

> hint:You may need to know Hastad attack and lattice reduction algorithm

附件下载：lowExponent.zip