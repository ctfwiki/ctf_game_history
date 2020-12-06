## 比赛信息

> 比赛名称：
>
> 比赛网址：https://ctf.4hou.com/
>
> 比赛时间：
>
> 积分规则变动公告：
>
> 2020RoarCTF赛事已顺利进行12小时，比赛过程中我们发现目前的平台动态记分算法存在着一定的不公平性，最主要的影响在于取得一血的战队积分与后续答题战队差距过大。
>
> 尽管在记分规则中答题速度是一项重要的参考标准，但是我们认为答题速度这一因素在目前的积分规则中占据的比重过大，会影响最终记分排名的公平性。
>
> 所以我们将在比赛结束后使用以下算法对所有队伍得分重新计算并在平台上进行公布：
>
> ```php
> <?php
> function calculate($solvedCount, $baseScore = 1000, $minimumScore = 10){
>         if ($solvedCount === 1){
>             return $baseScore;
>         }
>         $score = ($baseScore / 1000) * (-28730 * pow($solvedCount, 0.007236) + 29840);
>         if ($score <= $minimumScore){
>             return $minimumScore;
>         }
>         return round($score, 0);
> }
> echo calculate((int)$argv[1]);
> ```
>
> 一切为了呈现给大家一场公平公正的比赛。
>
> 特别鸣谢：
>
> 赛事平台的进步离不开每支参赛战队及队员的支持和建议，在此感谢大家为赛事组提供的建议和意见，再次预祝各位取得好的成绩！！！
>
> RoarCTF赛事组

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1pNxk1JzvY-SjKV8_y9sj8Q 提取码：5555

链接：https://share.weiyun.com/Qxrl2f2x 密码：555555

链接：https://t1m.lanzous.com/b0afd45kd 密码:5555

<br/>

## 题目信息

### MISC

#### 签到题(210p)

> 题目描述:简单的签到题

```php
<?php
echo "<!-- /?url= -->";
if ($_GET['url']) {
  if (preg_match("/flag/i", $_GET['url'])) {
    die();
  }
  $curl = curl_init();

  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl, CURLOPT_TIMEOUT, 500);
  curl_setopt($curl, CURLOPT_URL, $_GET['url']);

  $res = curl_exec($curl);
  curl_close($curl);
  echo $res;
}
```

<br/>

#### Hi_433MHz(317p)

> 小李同学刚刚学会了使用HackRF对无线电信号进行抓取，这天他抓到了一个奇怪的信号，你能帮他看看是怎么回事么？

附件下载：4250411002de8b62f6f05a523ff6d5e0.zip

<br/>

#### FM(627p)

> 小王同学刚刚入门了无线电安全领域，这天他用瀑布图软件录制了87-108MHz某一频点上的一段信号，你能找找看他听到了什么么？

附件下载：FM.zip（203M）

<br/>

### WEB

#### ezsql(344p)

> Find the flag! 场景地址：http://139.129.98.9:30003

<br/>

#### Calc(1000p)

> 需要注册的在线计算器 场景地址：http://139.129.98.9:30000

<br/>

#### User Info(1000p)

> Golang VUE MongoDB redis demo

<br/>

#### badhack(820p)

> 好烦啊，我辛辛苦苦搭建的网站居然被黑了，我ssh口令还忘掉了，有没有带黑阔帮我把站黑回来呢。

<br/>

#### 你能登陆成功吗(367p)

> 登陆成功就给flag,你能登陆成功吗？ 场景地址：http://139.129.98.9:30005

<br/>

#### HTML在线代码编辑器(442p)

> ps:flag在环境变量里 场景地址：http://139.129.98.9:30004

<br/>

#### 快乐圣诞cei叮壳(881p)

> 场景地址：http://139.129.98.9:30006

<br/>

#### 你能登陆成功吗-Revenge(367p)

> 登陆成功就给flag，你能登陆成功吗？出题人刚刚犯了弱智错误导致出了非预期，正在暴打出题人。 场景地址：http://139.129.98.9:30007

<br/>

### CRYPTO

#### Crypto_System(491p)

> 场景地址：nc 139.129.98.9 30001

附件下载：0bc15cdcb46bcf011876fcd6720c75b7.zip

<br/>

#### EASYRSA(491p)

附件下载：EasyR5A_7580a4f9758718b878e44015393413e7.zip

<br/>

#### ECDSA(674p)

> 场景地址：nc 139.129.98.9 30002

<br/>

#### Reverse(515p)

附件下载：Reverse_67f115c1fddc4ce1aeb1c754001585bc.zip

<br/>

### REVERSE

#### steGO(966p)

> Recover the hidden message

附件下载：73282eb54ffdd632288234ca20eda543.zip

<br/>

#### slime_war(572p)

附件下载：674fae4dff3fe15f21e6540651f5868b.zip

<br/>

#### singularDLP(966p)

> tianst最近在入坑密码学，但是只会C语言，所以只好用C手挫了一个加密算法。

附件下载：d5f6a2b69cc6a8e09adcef05c07e0dc3.zip

<br/>

#### WaO(820p)

> 逆向反调试、花指令、套壳什么的都好无聊，来试试这个OldSchool。

附件下载：002622cdd5b68cf5c36bebb816e1eb73.zip

<br/>

### PWN

#### qtar(735p)

> do u like tar?

附件下载：qtar.zip

<br/>

#### 2a1(541p)

> easy like 2+1

附件下载：520045ae2a00c141903761cb5095673f.zip

<br/>

#### easy_pwn(820p)

> 简单的求FIRST集合代码...

附件下载：04ec409c43f07db893ee569067a987ca.zip

