## 比赛信息

> 比赛名称：UNCTF2020 - 公开赛
>
> 比赛网址：https://unctf.hackingfor.fun/#/match/join/a54d0938-1b2c-48a7-876c-6acebc347643
>
> 比赛时间：2020-11-07 08:00~2020-11-14 18:00

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1cIPonhL_u_YYhR_UJqKMEw 提取码：5555

链接：https://share.weiyun.com/EQ9o0i7K 密码：ftnk2p

外链: https://t1m.lanzous.com/b0afb8zgb 密码:5555

<br/>

## 题目信息

### WEB

#### easy_ssrf(109s,10p)

题目源码，flag在/flag

```php
<?php
echo'<center><strong>welc0me to 2020UNCTF!!</strong></center>';
highlight_file(__FILE__);
$url = $_GET['url'];
if(preg_match('/unctf\.com/',$url)){
    if(!preg_match('/php|file|zip|bzip|zlib|base|data/i',$url)){
        $url=file_get_contents($url);
        echo($url);
    }else{
        echo('error!!');
    }
}else{
    echo("error");
}
?>
```

<br/>

#### easyunserialize(89s,29p)

题目源码

```php
<?php
error_reporting(0);
highlight_file(__FILE__);

class a
{
    public $uname;
    public $password;
    public function __construct($uname,$password)
    {
        $this->uname=$uname;
        $this->password=$password;
    }
    public function __wakeup()
    {
            if($this->password==='easy')
            {
                include('flag.php');
                echo $flag;    
            }
            else
            {
                echo 'wrong password';
            }
        }
    }

function filter($string){
    return str_replace('challenge','easychallenge',$string);
}

$uname=$_GET[1];
$password=1;
$ser=filter(serialize(new a($uname,$password)));
$test=unserialize($ser);
?>
```

<br/>

#### babyeval(76s,48p)

题目源码

```php
<?php
    // flag在flag.php
    if(isset($_GET['a'])){
        if(preg_match('/\(.*\)/', $_GET['a']))
            die('hacker!!!');
        ob_start(function($data){
                 if (strpos($data, 'flag') !== false)
                 return 'ByeBye hacker';
                 return false;
                 });
        eval($_GET['a']);
    } else {
        highlight_file(__FILE__);
    }
    ?>
```

<br/>

#### ezphp(73s,52p)

题目源码

```php
<?php
show_source(__FILE__);
$username  = "admin";
$password  = "password";
include("flag.php");
$data = isset($_POST['data'])? $_POST['data']: "" ;
$data_unserialize = unserialize($data);
if ($data_unserialize['username']==$username&&$data_unserialize['password']==$password){
    echo $flag;
}else{
    echo "username or password error!";
}
```

<br/>

#### easyflask(49s,78p)

源码下载：easyflask.zip

<br/>

#### easy_upload(52s,76p)

> 随便上传

源码下载：easy_upload.zip

<br/>

#### UN's_online_tools(39s,86p)

> 一个很好用的工具

开始是sql注入，后来改成命令执行绕过了，下面是改过后的源码

源码下载：UN's_online_tools.zip

<br/>

#### L0vephp(27s,93p)

> 简单的php

源码下载：L0vephp.zip

<br/>

#### checkin-sql(28s,93p)

> 非常简单的sql 0.0
>
> 提示1：flag不在数据库中。。

源码下载：checkin-sql.zip

<br/>

#### easyphp(23s,95p)

> 提示1：/?source

flag在环境变量中

源码下载：easyphp.zip

<br/>

#### ezfind(31s,91p)

> 提示1：if(!(is_file($name)===false)){flag}else{no flag}

```
能不能长点心?                       文件不存在
你怎么能拿谁都知道的东西来骗我!         关键词过滤
你找到我了！UNCTF{xxx}
```

源码下载（静态文件）：ezfind.zip

<br/>

#### 俄罗斯方块人大战奥特曼(18s,97p)

> wasm

源码下载：俄罗斯方块人大战奥特曼.zip

<br/>

#### easy_flask2(9s,99p)

> flask&&pickle

源码下载：easy_flask2.zip

<br/>

### PWN

#### YLBNB(104s,10p)

> 守护世界上最好的YLB
>
> nc 45.158.33.12 8000

<br/>

#### fan(56s,72p)

> 简单栈溢出

附件下载：fan.zip

<br/>

#### do_you_like_me?(52s,76p)

附件下载：do_you_like_me.zip

<br/>

#### 你真的会pwn嘛？(35s,89p)

附件下载：do_you_really_know_pwn.zip

<br/>

#### baby_heap(19s,97p)

附件下载：baby_heap.zip

<br/>

#### pwngirl(16s,98p)

附件下载：pwngirl.zip

<br/>

#### 原神(13s,98p)

> 219.152.60.100 54232

附件下载：原神.zip

<br/>

#### keer's bug(15s,98p)

附件下载：keer_s_bug.zip

<br/>

#### ezheapy!(5s,100p)

> heap？heap。heap！

附件下载：ezheapy!.zip

<br/>

### REVERSE

#### re_checkin(103s,10p)

> 二进制手做不出来这个就考虑退役吧

附件下载：occasionally.zip

<br/>

#### 反编译(56s,72p)

附件下载：run.rar

<br/>

#### babypy(51s,77p)

> Babypy.That's really easy!!!

附件下载：babypy.zip

<br/>

#### easyMaze(46s,81p)

> 别迷路了

附件下载：easyMaze.zip

<br/>

#### ezRust(17s,97p)

> 基于Rust的安全编程

附件下载：ezRust.zip

<br/>

#### ICU(17s,97p)

> I see you! 别想做坏事

附件下载：ICU.zip

<br/>

#### base_on_rust(12s,99p)

> 基于Rust的编码程序

附件下载：base_on_rust.zip

<br/>

#### ezre(10s,99p)

> 小学二年级数学了解一下？

附件下载：ezre.zip

<br/>

#### Trap(11s,99p)

> You Find libc.so?

附件下载：Trap.zip

<br/>

#### ezvm(9s,99p)

> 可能要了解一下密码学？

附件下载：ezvm.zip

<br/>

#### CTFilter(7s,100p)

> 假如你是李华，你的好友学习委员无意之间看到了一串flag！ 
>
> 这串flag极有可能是解开谜题的关键。 
>
> 他立刻在一台装有Windows10 1903 x64操作系统的虚拟机中使用记事本写下了这串flag并保存。 
>
> 然而，令他没想到的是，这个系统却另有玄机！ 
>
> 任何人都无法在这个系统中写下正确的flag？ 请你以好友的身份对他伸出援手，帮助学习委员找到真正的flag。 
>
> 学习委员：那你能帮帮我吗？ 
>
> 李华：瞧谁不起呢？

附件下载：CTFilter.zip

<br/>

#### BetterCPU(4s,100p)

> 手搓虚拟机了解一下

附件下载：BetterCpu.zip

<br/>

### CRYPTO

#### easy_rsa(94s,20p)

附件下载：RSA1.zip

<br/>

#### 鞍山大法官开庭之缺的营养这一块怎么补(77s,47p)

> 某日，鞍山大法官在点外卖时点了2个韭菜盒子，商家只送了1个，大法官给了该商家一个差评
>
> 次日，该大法官又在该商家点了1个韭菜盒子，希望商家能补上上次的韭菜盒子，而商家又只发了一个韭菜盒子
>
> 这名大法官一天正常要吃2个韭菜盒子，而该商家每天只给他1个韭菜盒子，请问该名大法官缺的营养这一块怎么补 ottttootoootooooottoootooottotootttootooottotttooootttototoottooootoooottotoottottooooooooottotootto
>
> flag格式：unctf{}

<br/>

#### 简单的RSA(70s,56p)

> 你们都不会百度的吗

附件下载：RSA.zip

<br/>

#### wing(43s,83p)

> 你过office二级了吗

附件下载：wing.zip

<br/>

#### signin(25s,94p)

> Really baby problem about block cipher
>
> flag 格式： flag{}

附件下载：signIn.zip

<br/>

#### 快乐数学_0x00(17s,97p)

> 刚才我问扎克利，扎总发生甚么事了。扎总说怎么回事。我给扎总发了几张截图。
>
> 扎总一看，噢，原来是昨天，几个大学生，二十多岁，他们说，哎~。
>
> 有一个说，我在 UNCTF 打比赛，头都做疼了，扎总，你能不能教教我怎么做题，哎，帮我分数弄高一点。
>
> 扎总说，可以，你在 UNCTF 死做题，不好用。他不服气。
>
> 扎总说，我说小朋友，你多长两个脑子来做我这新题。他做不动，他说你这个没用。
>
> 扎总说，我这个有用，他是数学，数学对计算机基础很重要，二百多个人做不出我这题。他非要和我试试。
>
> 扎总说，可以。扎总一说他啪站起来了，很快啊，然后上来一个左正蹬，一个右鞭腿，一个左刺拳。
>
> 扎总全部防出去了啊，防出去以后，自然是传统功夫以点到为止，右手把数学题摁在他鼻子上，没打他，扎总笑了一下，准备收拳。
>
> 后面我暂时编不下去了，你们来跟扎总打吧。
>
> 数学题，可能存在异议的，群里私聊 Hanser 的老公。
>
> 链接: https://pan.baidu.com/s/1nB8j4TN3HFe_SXvrwzyE2g 密码: ca04

附件下载：快乐数学_0x00.zip

<br/>

#### minisys(9s,99p)

> AES/CTR with controllable key

附件下载：minisys.zip

<br/>

### MISC

#### baba_is_you(184s,10p)

> 了解一下png文件格式

附件下载：baba_is_you.zip

<br/>

#### 爷的历险记(132s,10p)

> RPG小游戏
>
> 爷把flag弄丢了, 你可以帮他找回来吗

附件下载：file.zip（271M）

<br/>

#### 躲猫猫(98s,14p)

> 我躲好了，你来找我

附件下载：list.zip

<br/>

#### 阴阳人编码(102s,10p)

附件下载：就这就这不会吧.zip

<br/>

#### YLB's CAPTCHA - 签到题(72s,53p)

> YLB同款验证码

源码下载（静态文件）：YLB's CAPTCHA.zip

<br/>

#### 网络深处1(64s,63p)

> 好孩子不要上洋葱鸭

附件下载：网络深处1.zip

<br/>

#### 撕坏的二维码(71s,55p)

附件下载：qrcode.zip

<br/>

#### mouse_click(59s,69p)

> flag格式为unctf{*****}，******中的字母统一为大写

附件下载：mouse_click.zip

<br/>

#### 被删除的flag(58s,70p)

> flag被删除了，你能恢复它吗

附件下载：flag.zip

<br/>

#### 你能破解我的密码吗(54s,74p)

> flag内容为密码的32位小写的md5，请用unctf{}包裹字符串

附件下载：shadow.zip

<br/>

#### EZ_IMAGE(47s,80p)

附件下载：ez_image.zip

<br/>

#### YLB绝密文件(38s,87p)

> 提示1：需要提取出三个文件: \*.pyc,\*.py,\*.zip
>
> 提示2：zip文件可以以原始数据的形式导出Hex值，再导入Winhex/010 Editor然后删去非Zip数据部分（自行百度Zip格式

附件下载：YLBNB.zip

<br/>

#### 零(38s,87p)

> 我瞎了看不到flag了

附件下载：零.zip

<br/>

#### 倒影(30s,92p)

附件下载：倒影.zip

<br/>

#### ET-msg(7s,100p)

> 阿雷收到了ET回复的信息，不清楚它们想说什么
>
> 提示1：阿雷:Arecibo
>
> 提示2：30 80 7

附件下载：ET-msg.zip

<br/>

#### bashsecret(3s,100p)

附件下载：bashsecret.zip、secret.zip

<br/>

#### 太极八卦(2s,100p)

> 这可能是一道算法题
>
> *提示1：https://i.loli.net/2020/11/10/5s2hvAVUGmLQk36.jpg*
>
> 提示2：注意中间的字符，○没用
>
> 提示3：注意hint1中红色线头的走向和规律

附件下载：out.zip、5s2hvAVUGmLQk36.zip

<br/>

#### 调查问卷(119s,10p)

> 请大家认真填写哟~
>
> 只有几道，不多，最多占用大家两三分钟...
>
> 问卷地址：https://wj.qq.com/s2/7519766/6af6/
>
> 想要大家一起吐槽？
>
> 知乎链接：https://www.zhihu.com/question/429290669/answer/1564365629

```
unctf{b9b10385-a024-441b-bb77-679f56064d34}
```

