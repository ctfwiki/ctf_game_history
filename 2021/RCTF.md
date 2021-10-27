## 比赛信息

> 比赛名称：2021-RCTF
>
> 比赛时间：2021-09-11 09:00:00——2021-09-13 09:00:00
>
> 比赛网址：https://adworld.xctf.org.cn/match/guide?event=153&hash=d068dfd5-afdf-47c7-92a3-1d833b2d90a8.event

<br/>

## writeup

网盘文档

[2021-RCTF-WriteUp-By-Nu1L.pdf](../writeup/2021-RCTF-WriteUp-By-Nu1L.pdf)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1PX9QNBnsmCVInR-hzJlk3g 提取码：xing

链接：https://pan.xunlei.com/s/VMjTuP5fk2YQq8AQquxPeZwTA1 提取码：2zpt

链接：https://ctf.lanzoui.com/b02cfqoyj 密码:xing

<br/>

## 题目信息

### MISC

#### Monopoly(28s,425p)

> Just find the bug of rule , win the game!
> nc 123.60.25.24 20031

附件下载：dd54dc4f950540579ca8ddd9bf1709c7.zip

<br/>

#### coolcat(26s,444p)

> Can you help me to decrypt the image?
> (This is misc , so please do not try to upload a webshell or scan my website!)
> http://124.70.137.88:5000

附件下载：e99aa4e9b7fc4ed5a74a590a63b131e6.zip

<br/>

#### CheckIn(133s,131p)

> Just a easy challenge.
> https://github.com/CheckInChallenge/CheckIn
>
> hint: why flag so short and only have number

<br/>

#### ezshell(23s,476p)

> you will watch flag by the Behinder(There is an agent to filter memshell and ProcessImpl)(The Outbound traffic is closed)
> http://124.70.137.88:60080/
>
> hint: find flag in Behinder Basicinfo 在冰蝎Basicinfo里找找flag
>
> hint2: If you don't know how to use BehinderClient because it's Chinese, maybe the Code about BasicInfo in BehinderClient is useful.

附件下载：ROOT.zip

<br/>

#### welcome_to_rctf(478s,40p)

> hack for fun,enjoy it
>
> http://124.71.132.232:60180/
> https://rois.io/

```
RCTF{welcome_to_rctf2021}
```

<br/>

#### FeedBack(81s,200p)

> Thank you for participating our game. Hope you enjoy it!
> And We need your FeedBack!
>
> https://docs.google.com/forms/d/e/1FAIpQLScUAe-Q5kdEKwqp375PW8QTxdmjQzmD2Ib8lD1tk6Uwygfg0w/viewform?usp=sf_link

<br/>

### PWN

#### ezheap(23s,476p)

> There seems to be a problem with this heap manager.
> nc 123.60.25.24 20077

附件下载：4a0b8b631ede4ab4a40a297da6de06e1.zip

<br/>

#### game(5s,833p)

> nc 123.60.25.24 20000

附件下载：2b34a60ead004cf78dec1612c6275883.zip

<br/>

#### Pokemon(3s,909p)

> nc 123.60.25.24 8888

附件下载：d1b7f4a74c50445cac5b87933004c10a.zip

<br/>

#### musl(15s,588p)

> easy musl-libc challenge flag is in /home/ctf/flag/, but there seems to be something wrong with its filename
>
> nc 123.60.25.24 12345

附件下载：6f6a79d555bc4d7283d401acff88dd2f.zip

<br/>

#### sharing(22s,487p)

> nc 124.70.137.88 30000

附件下载：00fcf15fc5a543ffb03a88d702ce2a2f.zip

<br/>

#### warmnote(4s,869p)

> nc 124.70.137.88 20000

附件下载：9b1a620e6e43471084eb622e7c4d988c.zip

<br/>

#### catch_the_frog(6s,800p)

> nc 124.70.137.88 10000

附件下载：65c1499d604c48e1a9900425f1a1e92a.zip

<br/>

#### unistruct(11s,666p)

> nc 124.70.137.88 40000

附件下载：6668156101534d4f9f3c7f936b102b07.zip

<br/>

### WEB

#### Easyphp(43s,322p)

> Just a common and simple php service
> http://124.71.132.232:60080

附件下载：c5c06ee7394f4f21aa2d66223c7d8859.zip

<br/>

#### VerySafe(16s,571p)

> I think it’s very safe
> http://123.60.21.23:54120

附件下载：3e27bf526b33409a8a64984a7a42783c.zip

<br/>

#### xss it?(6s,800p)

> Pay attention to asoul，http://123.60.21.23:60001/，http://172.28.1.120/?asoul={“jiaran”:“672328094”,“xiangwan”:“672346917”,“beila”:“672353429”,“jiale”:“351609538”,“nailin”:“672342685”}
>
> http://123.60.21.23:60001
>
> hint1: URLs cannot be encoded to contain "/"
>
> hint2: 验证码为纯数字/The captcha is a pure number

附件下载：87cd260a3f7f4e02a84b1119f8b5bb40.zip

<br/>

#### CandyShop(47s,303p)

> Buy some sweet candies online?
> 环境每10分钟重启一次/The container will be restarted every 10 minutes
> http://123.60.21.23:23333

附件下载：dda6eaf3c5ad4091b174623e32a927f7.zip

<br/>

#### ns_shaft_sql(2s,952p)

> http://124.71.132.232:23334/
> Go to the buttom of newest SQL chasm , and get your flag.
>
> hint1: We add docker-compose.yml attatchment for mysql

附件下载：2ed71dfde69f4aa3a2b972c3a8ab4cf9.zip

<br/>

#### EasySQLi(2s,952p)

> Everyone Knows SQLi in “ORDER BY”
>
> http://124.71.132.232:11002
>
> ps: mysql server is 8.0.21
>
> hint: time-based

```php
<?php
require_once('db.php');
highlight_file(__FILE__);

set_time_limit(1);
$s = floatval(microtime());

$order = $_GET['order'] ?? 1;
$sql = "SELECT CONCAT('RCTF{',USER(),'}') AS FLAG WHERE '🍬关注嘉然🍬' = '🍬顿顿解馋🍬' OR '🍬Watch Diana a day🍬' = '🍬Keep hunger away🍬' OR '🍬嘉然に注目して🍬' = '🍬食欲をそそる🍬' ORDER BY $order;";

$stm = $pdo->prepare($sql);
$stm->execute();
echo "Count {$stm->rowCount()}.";

usleep((1 + floatval(microtime()) - $s) * 1e6);
```

<br/>

#### hiphop(7s,769p)

> R U DJ?
> http://124.71.132.232:58080

```
<?hh
<<__EntryPoint>>
function main(): void {
	$sandbox = '/var/www/html/sandbox/' . md5($_SERVER['REMOTE_ADDR']) . '/';
	@mkdir($sandbox);
	$s = file_get_contents(__FILE__);
	ini_set('open_basedir', $sandbox);
	if (!isset($_GET['url'])) {
		echo $s;
		echo "\n\n";
		echo "// Your sandbox: $sandbox";
	} else {
		$url = $_GET['url'] ?? 'http://127.0.0.1/hello.html';
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HEADER, 0);
		$output = curl_exec($ch);
		curl_close($ch);
		echo $output;
	}
}
// Hint:
// Do not use any scanner / 不要使用任何扫描器
// No internal network / 没有内网


// Your sandbox: /var/www/html/sandbox/********************************/
```

<br/>

### REVERSE

#### Hi!Harmony!(28s,425p)

> Hello, hackers! Have you ever heard of pangu, the creator of the world in Chinese mythology?

附件下载：fdc3c361090043f888b5f811889156d5.zip

<br/>

#### Valgrind(17s,555p)

> Hello, brave men from all over the world! I have heard that there is a technique called symbolic execution. We have captured the running process of an encryption program in symbolic execution. Can you tell me its encryption result?

附件下载：bf6384aee7064ec4af124a6e4b0c7457.zip

<br/>

#### sakuretsu(6s,800p)

> 链接：https://pan.baidu.com/s/1r1RXm5JQSldukjXVkZ-VQA
> 提取码：RCTF
> Or download by the following link : https://mega.nz/file/YtgWxDxA#tBG_1uvlm5vMGlwyWiQF4g1B_ER7KexmwnMlQlSuUNc

附件下载：re.zip

<br/>

#### LoongArch(37s,357p)

> help find valid input in stack

附件下载：3d05b37b23074a2ea63baafcc94ac68f.zip

<br/>

#### dht(6s,800p)

> flag is like flag{[a-z0-9]*}

附件下载：38cae3539a554272bce2d9ef81ce9817.zip

<br/>

#### two_shortest(7s,769p)

> get some old code related to SGU Online Judge, and just find it’s pwnable lol
>
> nc 124.70.137.88 60000

附件下载：5c1288738a6d4e0092dec40e59a902e7.zip

<br/>

### CRYPTO

#### Uncommon Factors I(14s,606p)

> link：https://pan.baidu.com/s/1EfvkU5gQIzqBsENxJfyRUA (authcode: RCTF)
> or you can download by https://mega.nz/file/sthiWIiS#0yois8vZo0-CEQdBFFyeTiRsiqV7E-qbCKrVq4bWewI
>
> flag begin with flag(not RCTF

附件下载：uncommon.7z(256M)

<br/>

#### Uncommon Factors II(29s,416p)

> flag begin with flag(not RCTF

附件下载：4827b6edfb794d0ab91d190b51fac592.zip

<br/>

### BLOCKCHAIN

#### HackChain(6s,800p)

> Your goal is to emit ForFlag(address addr) event
> nc 121.36.221.84 10001

附件下载：a3ea172520bb4d3cb052a2d78d0f26d2.zip

<br/>

#### EasyFJump(6s,800p)

> Your goal is to emit ForFlag(address addr) event
> nc 121.37.179.71 10001

