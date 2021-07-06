## 比赛信息

> 比赛名称：**中北大学第二届网络和信息安全知识技能竞赛**
>
> 比赛网址：http://www.dasctf.com/
>
> 比赛时间：2021年06月07日 09:00~18:30

<br/>

## writeup

官方wp鸽了

[【中北大学第二届NUCTF】misc yusa的音乐](https://www.cnblogs.com/CNdate/p/14867390.html)

[NUCTF-部分逆向wp](https://s1lenc3-chenmo.github.io/2021/06/09/NUCTF-%E9%83%A8%E5%88%86wp/)

[[NUCTF] NUCTF 个人writeup](https://zhuanlan.zhihu.com/p/379154268)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1KV-avq_VAKF6wyaqBnRHrw 提取码：xing

链接：https://pan.xunlei.com/s/VMdv3VTWbmNNpIWbWYxHBmi1A1 提取码：9d2d

链接：https://ctf.lanzoui.com/b02c7tfzg 密码:xing

<br/>

## 题目信息

### WEB

#### EasyUnser(100p)

> EasyUnser.本题flag 格式为DASCTF{}，提交时只需要提交括号中间的字符。

```php
<?php
    include_once 'flag.php';
    highlight_file(__FILE__);
    // Security filtering function
    function filter($str){
        return str_replace('secure', 'secured', $str);
    }
    class Hacker{
        public $username = 'margin';
        public $password = 'margin123';
    }
    $h = new Hacker();
    if (isset($_POST['username']) && isset($_POST['password'])){
        // Security filtering
        $h->username = $_POST['username'];
        $c = unserialize(filter(serialize($h)));
        if ($c->password === 'hacker'){
            echo $flag;
        }
    }
```

<br/>

#### JustSerial(100p)

```php
<?php

highlight_file(__FILE__);
include 'flag.php'; // $flag = "DASCTF{xxxxx}"
$obj = $_GET['obj'];
if (preg_match('/flag/i', $obj)) {
    die("?");
}
$obj = @unserialize($obj);
if ($obj->flag === 'flag') {
    $obj->flag = $flag;
}
foreach ($obj as $k => $v) {
    if ($k !== "flag") {
        echo $v;
    }
}
```

<br/>

#### crackme(200p)

> 想拿flag?来闯关吧！

```php
<?php
//what you want to see is in ssssrf.php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_POST['crack_me.com']))
{
    $filename=$_POST['crack_me.com'];
    if(stripos($filename, 'bingbing')>0){ 
        echo file_get_contents($filename); 
    }
    else{
        die("you don't like  bingbing ???");
    }
}
else
{
    die("can't pass the level?hai xiang kai junjian?");
}
```

<br/>

#### ezssrf(300p)

> ssrf me

源码下载：ezssrf.zip

<br/>

#### medium_calc(300p)

> 这次不是easy了，不过他还是个计算器
>
> hint: 直接使用 constructor 获得 Object

源码下载：source.zip

<br/>

#### 抽象画廊(200p)

> 来上传你们的抽象画吧.本题flag 格式为DASCTF{}，提交时只需要提交括号中间的字符。
>
> hint: https://nodejs.org/api/esm.html#esm_data_imports

源码下载：index.zip

<br/>

#### 文件上传(200p)

> 只是文件上传么？



<br/>

### MISC

#### funnygame(100p)

> snake is so fun!
>
> hint: stegosaurus

附件下载：funnygame的附件.zip

<br/>

#### Yusa'sMussic(200p)

附件下载：Yusa'sMussic的附件.zip

<br/>

#### 艾斯的信仰(100p)

> 提交最终结果的md5值

附件下载：艾斯的信仰的附件.zip

<br/>

#### verylow(200p)

> 神奇的bmp

附件下载：verylow的附件.zip

<br/>

#### noobflutter(300p)

> 最高明的黑客往往采用最朴素的方式
>
> hint: codemoji

附件下载：noobflutter的附件.zip

<br/>

### CRYPTO

#### backdoor_lcg(200p)

> nc 117.21.200.166 41912（本题flag 格式为 flag{}/DASCTF{}，提交时只需要提交括号中间的字符。）

附件下载：backdoor_lcg的附件.zip

<br/>

#### math_rsa(200p)

> how is your math（本题flag 格式为 flag{}，提交时只需要提交括号中间的字符。）

附件下载：math_rsa的附件.rar

<br/>

#### rsa12(200p)

附件下载：rsa12的附件.zip

<br/>

#### CFB(300p)

> nc 117.21.200.166 49988（本题flag 格式为 flag{}，提交时只需要提交括号中间的字符。）

附件下载：CFB的附件.zip

<br/>

### REVERSE

#### anbug(200p)

> 写的不是代码，而是bug。注：flag请小写md5之后提交

附件下载：anbug的附件.zip

<br/>

#### encryption(200p)

> Can you recover the encryted function?

附件下载：encryption的附件.zip

<br/>

#### vvm(300p)

> 本题flag{}也需提交

附件下载：vvm的附件.zip

<br/>

#### regVM(200p)

> 写的不是代码，而是历史遗留问题。注：flag请进行32位小写md5之后提交
>
> hint: 翻译虚拟机指令集

附件下载：regVM的附件.zip

<br/>

### PWN

#### Weapon(200p)

> Welcome to Weapon System!

附件下载：weapon.zip

<br/>

#### soeasyheap(200p)

> hint: unlink + double free

附件下载：soeasyheap.rar.zip

<br/>

#### rabbit(300p)

> 狡兔三窟,flag在哪嘞
>
> hint: lagebin_attack劫持tcache_max_bins

附件下载：rabbit.zip

<br/>

#### vpwn(300p)

> 你写过虚拟机吗？

附件下载：vpwn.zip

