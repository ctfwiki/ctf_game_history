## 比赛信息

> 比赛名称：2021“红明谷”杯数据安全大赛
>
> 比赛时间：2021年04月02日 10:00~18:00
>
> 比赛网址：https://race.ichunqiu.com/hmgctf

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1vKGx3eaRqmR1uzGIkUBaag 提取码：5555

链接：https://t1m.lanzous.com/b0afph0tc 密码:5555

阿里云盘：暂无

<br/>

## 题目信息

### MISC

#### InputMonitor

> Akira在某次取证的过程中，在桌面找到了一个奇怪的文件，但是除此之外好像没有找到什么有价值的情报，很多的数据都被抹干净了，而且这个用户似乎根本就没装什么第三方的软件。Akira还粗心的只拷贝了C盘下的User目录，这下还有机会解开可疑文件吗？

附件下载：Dump_6e7e51d82aa230fe12d1fbc145da6441.7z（146M）

<br/>

#### 歪比歪比

> 戴夫发送了一些信息给僵尸，但是被我截获到了。看看能从里边发现什么?好像是一个Surprise，你来翻译翻译?

附件下载：data_71d06302156e5bfc15c2e61a9899e462.zip

<br/>

#### babytraffic

> 攻击者A在某次渗透测试过程中，通过枚举弱口令的方式拿下了机器B的登录权限。他的部分操作被系统捕捉并记录了下来，请分析他的操作并获取flag。答案加flag{}格式。

附件下载：babytraffic.zip

<br/>

#### 我的心是冰冰的

> 似乎有信息被隐藏了。

附件下载：bingbing_93171aa9233c6751e3ca3346fa920657.rar

<br/>

#### 签到

> 一起来参与数据安全知识小竞赛。

源码下载：签到.zip

<br/>

### CRYPTO

#### babyForgery

> **nc 8.140.179.11 39254**
>
> XE vs XEX

附件下载：babyForgery_7e5017da73f530ad9bfe991ade0794a6.zip

<br/>

#### RSA attack

> 天呀，一个重要的工业数据被截获了，但是被RSA加密了，万幸的是加密规则和一部分数据 也被截获了，你可以通过给出的线索，找到那个重要的数据吗?

附件下载：task_ea8fa233a5d461f6b7f56fd20e51689d.zip

<br/>

#### ezCRT

> Chinese Remainder Theorem is fantastic

附件下载：ezCRT_9e515e8903cf42186c89fe152d584085.zip

<br/>

### PWN

#### 双边协议1.0

> **nc 8.140.179.11 13452**
>
> 获得权限后，执行pwn文件同目录下的"getflag"，并输入队伍token，即可获取flag。

附件下载：Maybe_fun_game.zip

<br/>

### REVERSE

#### gogogo

> gogogo

附件下载：gogogo.zip

<br/>

#### g0

> Gooo...ooo

附件下载：g0.zip

<br/>

### WEB

#### javaweb

> **try to rce.**
>
> http://8.140.152.226:9999/login

<br/>

#### happysql

静态文件：happysql.zip

<br/>

#### easytp

thinkphp3.2.3

静态文件：easytp.zip

<br/>

#### write_shell

> 万无一失的waf。

```php
# /var/www/html/index.php
<?php
error_reporting(0);
highlight_file(__FILE__);
function check($input){
    if(preg_match("/'| |_|php|;|~|\\^|\\+|eval|{|}/i",$input)){
        // if(preg_match("/'| |_|=|php/",$input)){
        die('hacker!!!');
    }else{
        return $input;
    }
}

function waf($input){
  if(is_array($input)){
      foreach($input as $key=>$output){
          $input[$key] = waf($output);
      }
  }else{
      $input = check($input);
  }
}

$dir = 'sandbox/' . md5($_SERVER['REMOTE_ADDR']) . '/';
if(!file_exists($dir)){
    mkdir($dir);
}
switch($_GET["action"] ?? "") {
    case 'pwd':
        echo $dir;
        break;
    case 'upload':
        $data = $_GET["data"] ?? "";
        waf($data);
        file_put_contents("$dir" . "index.php", $data);
}
?>
# /!whatyouwantggggggg401.php
<?php $flag = 'flag{f38235f7-cf63-40d1-9dc1-3625315c7e76}';?>
```

