## 比赛信息

> 比赛名称：BMZCTF第一届网络安全公开赛
>
> 比赛链接：http://bmzclub.cn/challenges
>
> 比赛时间：2020年12月26日 09:00-2020年12月27日 21:00

<br/>

## writeup

[第一届BMZCTF公开赛-MISC-Writeup](https://mochu.blog.csdn.net/article/details/111306837)

[第一届BMZCTF公开赛-WEB-Writeup](https://mochu.blog.csdn.net/article/details/111916620)

[2020 BMZCTF Re&Pwn WriteUp](https://www.richar.top/2020/12/25/bmzctf-2020-wp/)

[BMZCTF -- WP-RE](https://www.cnblogs.com/pupububu/p/14218706.html)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1IZe6_cthnze9EcPU9DM0rA 提取码：xing

链接：https://pan.xunlei.com/s/VMdttqJwjZ6jbz2EvCZAeyCAA1 提取码：3t3k

链接：https://ctf.lanzoui.com/b02c7s3ve 密码:xing

<br/>

## 题目信息

### MISC

#### 签到题(417s,20p)

> 关注官方公众号:白帽子社区 回复：2020BMZCTF

```
BMZCTF{W3lc0me_T0_2020BMZCTF}
```

<br/>

#### 你猜猜flag(117s,30p)

附件下载：flag.zip

<br/>

#### Snake(6s,96p)

> 斯内克~斯内克~斯内克~斯内克~斯内克~斯内克~斯内克~

附件下载：snake.zip

<br/>

#### tiga(3s,100p)

> 迪迦奥特曼失去了光，又恢复到石像的模样，你能给迪迦光嘛？

附件下载：tiga.zip

<br/>

#### Hack K(0s,100p)

<br/>

### WEB

#### ezeval(38s,30p)

```php
<?php
highlight_file(__FILE__);
$cmd=$_POST['cmd'];
$cmd=htmlspecialchars($cmd);
$black_list=array('php','echo','`','preg','server','chr','decode','html','md5','post','get','file','session','ascii','eval','replace','assert','exec','cookie','$','include','var','print','scan','decode','system','func','ini_','passthru','pcntl','open','link','log','current','local','source','require','contents');
$cmd = str_ireplace($black_list,"BMZCTF",$cmd);
eval($cmd);

?>
```

<br/>

#### penetration(9s,89p)

```php
<?php
highlight_file(__FILE__);
if(isset($_GET['ip'])){
    $ip = $_GET['ip'];
    $_=array('b','d','e','-','q','f','g','i','p','j','+','k','m','n','\<','\>','o','w','x','\~','\:','\^','\@','\&','\'','\%','\"','\*','\(','\)','\!','\=','\.','\[','\]','\}','\{','\_');
    $blacklist = array_merge($_);
    foreach ($blacklist as $blacklisted) {
        if (strlen($ip) <= 18){
            if (preg_match ('/' . $blacklisted . '/im', $ip)) {
                die('nonono');
            }else{
            exec($ip);
            }
            
        }
        else{
        die("long");
        }
    }
    
}
?>
```

<br/>

#### ezphp(2s,100p)

源码下载：ezphp.zip

<br/>

### RE

#### RE1(50s,30p)

附件下载：re1.zip

<br/>

#### RE2(23s,30p)

附件下载：2re.zip

<br/>

#### RE3(16s,61p)

附件下载：attachment.rar

<br/>

### PWN

#### pwn1(34s,30p)

> nc 47.242.59.61 10000

附件下载：pwn1.zip

<br/>

#### pwn2(22s,30p)

> nc 47.242.59.61 10001

附件下载：pwn2.zip

<br/>

#### pwn3(7s,94p)

> nc 47.242.59.61 10002

附件下载：pwn3.zip

<br/>

#### pwn4(5s,98p)

> nc 47.242.59.61 10003

附件下载：pwn4.zip

<br/>

#### pwn5(3s,100p)

> nc 47.242.59.61 10004

附件下载：pwn5.zip

<br/>

### CRYPTO

#### easy_crypto(17s,56p)

附件下载：easy_crypto.zip

<br/>

#### xor(10s,86p)

> ['\x00', '\x00', '\x00'] at start of xored is the best hint you get

附件下载：xor.zip

<br/>

### 综合渗透

#### BMZ_Market(6s,96p)

源码下载：Market.zip

<br/>

#### hacker-Home(0s,100p)

