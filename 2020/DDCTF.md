## 比赛信息

比赛名称：DDCTF（滴滴CTF）

比赛类型：校园赛

比赛网址：https://ddctf.didichuxing.com/

比赛时间：2020年09月04日 11:00~2020年09月06日 11:00

### 附件下载

链接：https://pan.baidu.com/s/1LY4y3vNWCZ5QEclgUJriLw 提取码：hdxw

外链:https://t1m.lanzous.com/b0af5ovef 密码:hdxw

链接：https://share.weiyun.com/vGjnfisN 密码：jhnlrn



## 题目信息

### WEB

#### Web签到题(150)

> 请从服务端获取client，利用client获取flag
> server url:http://117.51.136.197/hint/1.txt

```
Interface documentation
- login interface
[-][Safet Reminder]The Private key cannot use request parameter
Request
Method | POST
URL    | http://117.51.136.197/admin/login
Param  | username str | pwd str
Response
token str | auth(Certification information)

- auth interface
Request
Method | POST
URL    | http://117.51.136.197/admin/auth
Param  | username str | pwd str | token str
Response
url str | client download link

+------------------+                +----------------------+                +--------------------+
|                  |                |                      |                |                    |
|                  +---------------->                      +---------------->                    |
|  Client(Linux)   |                |     Auth/Command     |                |       minion       |
|                  <----------------+                      +<---------------+                    |
|                  |                |                      |                |                    |
+------------------+                +----------------------+                +--------------------+
```



#### 卡片商店(200)

> 题目链接：
> http://116.85.37.131/11b67e5088cef9b1c97bd5a30eb3b760/



#### Easy Web(350)

> 题目链接：
> http://116.85.37.131/34867ccfda85234382210155be32525c/web/index



#### Overwrite Me(400)

> http://117.51.137.166/EOf9uk3nSsVFK1LQ.php

```php
<?php
error_reporting(0);

class MyClass
{
    var $kw0ng;
    var $flag;

    public function __wakeup()
    {
        $this->kw0ng = 1;
    }

    public function get_flag()
    {
        return system('find /FlagNeverFall ' . escapeshellcmd($this->flag));
    }
}

class Prompter
{   
    protected  $hint;
    public function execute($value)
    {
        include($value);
    }

    public function __invoke()
    {
        if(preg_match("/gopher|http|file|ftp|https|dict|zlib|zip|bzip2|data|glob|phar|ssh2|rar|ogg|expect|\.\.|\.\//i", $this->hint))
        {
            die("Don't Do That!");
        }
        $this->execute($this->hint);
    }
}

class Display
{
    public $contents;
    public $page;
    public function __construct($file='/hint/hint.php')
    {
        $this->contents = $file;
        echo "Welcome to DDCTF 2020, Have fun!<br/><br/>";
    }
    public function __toString()
    {
        return $this->contents();
    }

    public function __wakeup()
    {
        $this->page->contents = "POP me! I can give you some hints!";
        unset($this->page->cont);
    }
}

class Repeater
{
    private $cont;
    public $content;
    public function __construct()
    {
        $this->content = array();
    }

    public function __unset($key)
    {
        $func = $this->content;
        return $func();
    }
}

class Info
{
    function __construct()
    {
        eval('phpinfo();');
    }

}

$show = new Display();
$bullet = $_GET['bullet'];

if(!isset($bullet))
{
    highlight_file(__FILE__);
    die("Give Me Something!");
}else if($bullet == 'phpinfo')
{
    $infos = new Info();
}else
{
    $obstacle = new stdClass;
    $mc = new MyClass();
    $mc->flag = "MyClass's flag said, Overwrite Me If You Can!";
    @unserialize($bullet);
    echo $mc->get_flag();
}
```



### Reverse

#### Android Reverse 1(100)

> 以此提示为准！！！
> 最后一次MD5前的输入为：
>
> 0xf4,0x75,0xef,0x15,0x7a,0x7b,0x27,0xc4,0x2d,0x41,0xf4,0xe7,0x45,0x83,0xe7,0x78,0xe2,0x6d,0xf1,0xec,0x77,0x94,0xd2,0xd5,0xa0,0xb3,0x69,0x21,0xaa,0x5b,0x68,0x2a

附件下载：reverse1_17i2sde0ev3275y2.apk



#### Android Reverse 2(300)

> 【提示】MD5计算之前的32字节：
> {0x60,0x1d,0x81,0x9a,0x38,0x4d,0x96,0x1b,0xf3,0x3c,0x33,0xcc,0xf9,0xc8,0xee,0xe8,0xaa,0x63,0xa0,0x74,0xb9,0x37,0x1a,0x1c,0x61,0x8c,0xac,0xbb,0x25,0x76,0x48,0x22};
> flag:DDCTF{P++++y W++++$} +为打码

附件下载：reverse2_bc364da.apk



#### Android Reverse 3(400)

> 提示：
> ollvm混淆和整体加壳
> 另外尝试获取密钥时需要有网环境
>
> 更新：
> 去除DDCTF{}标识符，flag是9位字符
>
> 更新：
> DDCTF{s++++++dI}，+为打码

附件下载：ddctf2020-android_reverse3.apk



### PWN

#### we love free(200)

> 1.题目采用c++编写；
> 2.使用了vector库，需要了解vector的机制；
> 3.117.51.143.25:5005
>
> 拿到题目中的flag后，需要将其填入至DDCTF{}中。
> !!!!正确答案格式均为DDCTF{xxxxxx}

附件下载：pwn1.zip



### MISC

#### 真·签到题(1)

flag在公告

```
DDCTF{he1l0_ddctf_2o2o_*\^o^/*=3=33!!!}
```



#### 一起拼图吗(200)

> http://116.85.51.117/d0wn_ctf_2o20.html

附件下载：file_d0wnl0ad.zip、demo.zip



#### decrypt(300)

> try to decrypt：
> 8ed251b18692697cd9697276478b631848b4fc6604dcf48fae471b7f62e47f656c57fb7498e0bff01dcf
>
> 算法见附件

附件下载：differentech_cipher.zip