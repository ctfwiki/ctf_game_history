## 比赛信息

> <b>比赛时间：</b>2019年10月19日09:00:00~2019年10月19日15:00:00
>
> <b>比赛平台：</b>[360攻防演练创新竞赛平台](https://cp.cup.360.cn/)
>
> <b>参赛形式：</b>个人赛
>
> <b>题目类型：</b>初赛通过线上选择题和CTF夺旗进行，选择题主要涉及计算机网络、协议分析、Web安全、中间件安全、系统安全、主机防护等题目类型，CTF夺旗主要涉及Web安全、数据包分析、取证分析、隐写、加解密编码等试题类型，主要考核参赛人员理论知识掌握和实际分析能力。
>
> <b>计分原则：</b>选择题100道共计400分，CTF夺旗共计1600分，总分前500名晋级复赛。



## 附件链接

链接：https://pan.baidu.com/s/1kSy1uHpXpe8BhNvIdgIrlQ 提取码：hdxw

链接：https://share.weiyun.com/Ih6eWYzy 密码：f8lrtj

外链:https://t1m.lanzous.com/b0aesxoni 密码:hdxw



## 题目信息

### **第一题 签到题！**

> 分值：50 分
> 试题类型：Crypto
> 
> ZmxhZ3tXZWxjb21lIHRvIDNDVEYhfQ%3D%3D
> (1). flag格式为：flag{xxxxxx}

```
flag{Welcome to 3CTF!}
```



### **第二题 漏洞与函数的绕过**

> 分值：100 分
>
> 试题类型：Web
>
> 题目：真实的环境中，充满了未知，漏洞与函数的拼接，能否绕过？
>
> 链接：http://examination.cup.360.cn:9004
>
> (1). flag格式：flag{xxxxxx}
>
> tips：用户名admin，密码为键盘密码
>
> tips：ImageMagic



官方writeup：https://mp.weixin.qq.com/s/aYh5M38vTuUcUrTUMa_asg



### **第三题 立誓要成为admin的男人！**

> 分值：150 分
>
> 试题类型：Web
>
> 链接：http://examination.cup.360.cn:9001
>
> (1). flag格式为：flag{xxxxxx}
>
> tips：控制服务器Session



官方writeup：https://mp.weixin.qq.com/s/WSfUbIIdpam7ALuxI1Y31g



### **第四题 python没写完的网站**

> 分值：200 分
>
> 试题类型：Web
>
> 题目：用Python写的一个网站，好像还没有写完？
>
> 链接：http://examination.cup.360.cn:9002
>
> (1). flag格式为：flag{xxxxxx}



官方writeup：https://mp.weixin.qq.com/s/S1DNwNlt_Imytt9SVOywBA



### **第五题 刚开发的博客**

> 分值：250 分
>
> 试题类型：Web
>
> 题目：最近在学习编程，这是我刚开发的博客，你能找到问题么？
>
> 链接：http://examination.cup.360.cn:9003
>
> 附件：https://yunpan.360.cn/surl_yuqVCcY2geT （提取码：e38a）
>
> (1). flag格式为：flag{xxxxxx}
>



附件下载：6ed9a0b2.jar

官方writeup：https://mp.weixin.qq.com/s/-k-9oagAKxqtOBpmGi9Q0A



### **第六题 你知道Alice的密码吗？**

> 分值：150 分
>
> 试题类型：Crypto
>
> 题目：Alice把一个秘密藏在了她最爱读的“4书”的文件末尾，但不幸的是这个文件被勒索病毒加密了。还好她还有一份“4书”未藏秘密前的备份，不然就连“4书”都没得看了。但这个备份是未藏秘密之前做的，你能帮Alice找回她的秘密吗？
>
> 附件：http://resource.cup.360.cn/5b810dc6/22a0a6.zip
>
> (1). flag格式为：=&360CTF{xxxxxx}

这是Alice的朋友帮她逆向得到的勒索病毒的加密部分代码：

```c
#define R(a,b) (((a) << (b)) | ((a) >> (32 - (b))))
void crypt(uint32 out[16],uint32 in[16])
{
 int i;
 uint32 x[16];
 for (i = 0;i < 16;++i)
  x[i] = in[i];
 for (i = 20;i > 0;i -= 2) {
  x[ 4] ^= R(x[ 0]+x[12], 7);  x[ 8] ^= R(x[ 4]+x[ 0], 9);
  x[12] ^= R(x[ 8]+x[ 4],13);  x[ 0] ^= R(x[12]+x[ 8],18);
  x[ 9] ^= R(x[ 5]+x[ 1], 7);  x[13] ^= R(x[ 9]+x[ 5], 9);
  x[ 1] ^= R(x[13]+x[ 9],13);  x[ 5] ^= R(x[ 1]+x[13],18);
  x[14] ^= R(x[10]+x[ 6], 7);  x[ 2] ^= R(x[14]+x[10], 9);
  x[ 6] ^= R(x[ 2]+x[14],13);  x[10] ^= R(x[ 6]+x[ 2],18);
  x[ 3] ^= R(x[15]+x[11], 7);  x[ 7] ^= R(x[ 3]+x[15], 9);
  x[11] ^= R(x[ 7]+x[ 3],13);  x[15] ^= R(x[11]+x[ 7],18);
  x[ 1] ^= R(x[ 0]+x[ 3], 7);  x[ 2] ^= R(x[ 1]+x[ 0], 9);
  x[ 3] ^= R(x[ 2]+x[ 1],13);  x[ 0] ^= R(x[ 3]+x[ 2],18);
  x[ 6] ^= R(x[ 5]+x[ 4], 7);  x[ 7] ^= R(x[ 6]+x[ 5], 9);
  x[ 4] ^= R(x[ 7]+x[ 6],13);  x[ 5] ^= R(x[ 4]+x[ 7],18);
  x[11] ^= R(x[10]+x[ 9], 7);  x[ 8] ^= R(x[11]+x[10], 9);
  x[ 9] ^= R(x[ 8]+x[11],13);  x[10] ^= R(x[ 9]+x[ 8],18);
  x[12] ^= R(x[15]+x[14], 7);  x[13] ^= R(x[12]+x[15], 9);
  x[14] ^= R(x[13]+x[12],13);  x[15] ^= R(x[14]+x[13],18);
 }
 for (i = 0;i < 16;++i)
  out[i] = x[i] + in[i];
}
```



附件下载：22a0a6.zip

官方writeup：https://mp.weixin.qq.com/s/EIwQrvFY2QGObaWE-ibJBg



### **第七题 注入真的好难!!!**

> 分值：150 分
>
> 试题类型：Misc
>
> 附件：http://resource.cup.360.cn/6a1ab4b9/1.pcap
>
> (1). flag格式为：flag{xxxxxx} 



附件下载：1.zip

解题过程中网盘附件：flag.zip

官方writeup：https://mp.weixin.qq.com/s/5vIFfavLdbsEaiPn4y5N7w



### **第八题 google语法真不错！！！**

> 分值：200 分
>
> 试题类型：Misc
>
> 附件：https://yunpan.360.cn/surl_yuqVRCSrf7d （提取码：3f26）
>
> (1). flag格式：flag{xxxxxx} (200 分)
>
> tips：volatility->隐写



附件下载：xp.zip

官方writeup：https://mp.weixin.qq.com/s/VIwL6d9qCiMBYgPHqj-ubg



### **第九题 Here are some big nums.**

> 分值：150 分
>
> 试题类型：Reverse
>
> 附件：http://resource.cup.360.cn/f31be108/c33f4cdd3a9a78f313a425b16b5644b1.exe
>
> (1). flag格式：flag{xxxxxx} (150 分)



附件下载：c33f4cdd3a9a78f313a425b16b5644b1.exe

官方writeup：https://mp.weixin.qq.com/s/38FoJ_GQOh8Ey8CVBKHh9g



### **第十题 I believe you can solve it.**

> 分值：100 分
>
> 试题类型：Pwn
>
> nc 180.153.183.102 10001
>
> 附件：http://resource.cup.360.cn/38ff70b1/7631454338ff70b1a6b1262f5f36beac
>
> (1). flag格式为：flag{xxxxxx}
>
> 



附件下载：7631454338ff70b1a6b1262f5f36beac.zip

官方writeup：https://mp.weixin.qq.com/s/MCyEyhbDdDoVHmYmwyA8MA



### **第十一题 你会360内的加减乘除吗？**

> 分值：100 分
>
> 试题类型：Pwn
>
> nc 180.153.183.102 10002
>
> 附件：http://resource.cup.360.cn/bcdc1da8/5b7420a5bcdc1da85bccc62dcea4c7b8
>
> (1). flag格式为：flag{xxxxxx}



附件下载：5b7420a5bcdc1da85bccc62dcea4c7b8.zip

官方writeup：https://mp.weixin.qq.com/s/_1lnDNeZKKw-OcM64iUl2A

