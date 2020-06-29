## 0CTF/TCTF（Tencent CTF）

### 比赛信息

```
比赛类型：国际组队赛
比赛时间：48 Hours，27 June 2020, 02:00 UTC — 29 June 2020, 02:00 UTC
		（2020年06月27日 10:00-2020年06月29日 10:00）
IRC: #0ctf2020 on Freenode
```

## REVERSE

### flash-1（27solved,297pt）

> Another flag machine in 2020!

附件下载：flash.tar.gz



### Happy Tree（17solved,407pt）

附件下载：happy_tree_5afdfd58537ced7c61de957ea243dfa186448a6d.zip



### babymips（27solved,297pt）

附件下载：babymips.zip



### J（9solved,578pt）

> Just do it

附件下载：j.zip



### w（11solved,523pt）

> easy assembly without web.
>
> updated: file updated, pls re-download again. Only last step updated. `ww` also not affected

附件下载：ww.c66c281e1353bb5d8e08a560251ad262.tgz



## PWNABLE

### Duet（8solved,611pt）

> Duet on the Heap.
>
> 忽双声以动作，合六律之短长
>
> `pwnable.org:12356`

附件下载：duet.tar.gz



### flash-2（4solved,785pt）

> pwn me to get the second flag
>
> `$ nc pwnable.org 21387`

附件下载：flash.tar.gz



### Baby Bypass（5solved,733pt）

> There is no more 'fake web challenge', enjoy pwning PHP direcly! :D
>
> `nc pwnable.org 20202`

附件下载：babybypass.tar.gz



### One Line JS（1solved,1000pt）

> There is a backdoor in the strange JS interpreter, try to use it! :D
>
> `nc pwnable.org 23333`

附件下载：mujs-42fa6a11fa34d2267b7586f36226625e4ae34480.tar.gz



### Do It, Try It（0solved,1000pt）

> https://www.youtube.com/watch?v=ryh9rkIRGUs
>
> `nc pwnable.org 7000`
>
> Hint: http://111.186.59.7/poc.js

附件下载：DoItTryIt.tar.xz

```js
// poc.js
function f(o) {
    try { 
        o.constructor = function() {};
        o.constructor.prototype = Object.prototype;
        undefined;
    } catch(e) {};
    o.constructor = undefined;
    Object.prototype.toString = function() {};
    return 0;
}

for (var i = 0; i < 1000; i++) {
    f({});
}
```



### Chromium RCE（29solved,282pt）

> It's v8, but it's not a typical v8, it's CTF v8! Please enjoy pwning this d8 :)
>
> `nc pwnable.org 40404`
>
> Enviroment: Ubuntu18.04
>
> **Update:** If you want to build one for debugging, please
> `git checkout f7a1932ef928c190de32dd78246f75bd4ca8778b`

附件下载：chromium_rce.tar.gz



### simple echoserver（28solved,289pt）

> Have a try with my simple echoserver! But don't attack it.
> Your name and phone are logged in the background.
>
> `nc pwnable.org 12020`

附件下载：simple_echoserver.zip



### eeeeeemoji（12solved,500pt）

> Let's play more emoji!
>
> `nc pwnable.org 31323`

附件下载：eeeeeemoji_19f098c2f96d446db81d0363da464f5a406d9e84.zip



### Chromium SBX（7solved,647pt）

> Sandbox Gogogo!
>
> `nc pwnable.org 1337`
>
> Enviroment: Ubuntu18.04
>
> **NOTE:** The configuration of this challenge is copied from PlaidCTF 2020 - mojo. Thanks!

附件下载：https://drive.google.com/file/d/1bF2aRYjhy0nKTE3wG-NkfGlmGbylSKxV/view?usp=sharing



### Chromium Fullchain（2solved,916pt）

> RCE + SBX = Fullchain.
>
> No surprise, the bug is same as previous, but how about the exploits? :p
>
> `nc pwnable.org 2337`
>
> Enviroment: Ubuntu18.04
>
> **NOTE:** The configuration of this challenge is copied from PlaidCTF 2020 - mojo. Thanks!

附件下载：https://drive.google.com/file/d/1xD7mnET6ssuEgDYccvv2q17M2oHKC1cT/view?usp=sharing



### ww（0solved,1000pt）

> more flag without web pls.
>
> flag file is `flag`
>
> file of this challenge is same as the one in `w`
>
> `nc pwnable.org 20206`

附件下载：ww.tgz



## WEB

### amp2020（3solved,846pt）

> AMP is a web component framework to easily create user-first...what?
>
> http://pwnable.org:33000/

附件下载：amp2020.zip



### Wechat Generator（32solved,261pt）

> Come and check my latest innovation! It's normal to encounter some bugs and glitches since it is still in beta development.
>
> http://pwnable.org:5000/



### easyphp（175solved,59pt）

> My php have some problem that some functions are not working correctly or even disabled! Help me get the flag in the server: http://pwnable.org:19260/

部分源码：easyphp.zip



### lottery（21solved,354pt）

> http://pwnable.org:2333/



### noeasyphp（18solved,392pt）

> My php have some problem that some functions are not working correctly or even disabled! This time we have no idea about it... Help me get the flag in the server: http://pwnable.org:19261/



## CRYPTO

### babyring（47solved,192pt）

> Show me the signature
>
> nc pwnable.org 10001

附件下载：ring_1f0f741fcfdfc52519d7b09b78c97b43.tar.gz



### emmm（18solved,392pt）

> How simple can a block cipher be?

附件下载：emmm_aa99aba25254f6d6ef373ee48b99f8c8.tar.gz（288M）



### sham（5solved,733pt）

> Look at my new hash. You can try it here => http://pwnable.org:10002/

附件下载：sham_1abc55860e453619482de930fcf44562.tar.gz



### Simple Curve（16solved,423pt）

> Baby elliptic(?) curve challenge~

附件下载：chall_6e25fd5d004ec238b5b8489a13a5d32a.zip



### gene（5solved,733pt）

> baby crypto && baby re
> `nc pwnable.org 23334`

附件下载：gene_2462cb70b4f73102d2f0266cf0efea2c.tar.gz



## MISC

### Welcome（841solved,12pt）

> Welcome to 0CTF/TCTF 2020 Quals!
>
> What is the `format` of a flag?

```
flag{this_is_a_sample_flag}
```



### PyAuCalc（17solved,407pt）

> Use Python 3.8 audit hooks to protect my calculator!
> `nc pwnable.org 41337`
> (Docker: `FROM python:3.8`, environment resets periodically)



### Cloud Computing（42solved,211pt）

> Welcome to our new cloud function computing platform, enjoy here => http://pwnable.org:47780/.



### eeemoji（40solved,220pt）

> Let's play some emoji!
>
> `nc pwnable.org 31322`

附件下载：eeemoji_50248b15a8cc5ec43ee358d0c8cb4a5318e1b0f6.zip



### Cloud Computing v2（18solved,275pt）

> Welcome to our new cloud function computing platform, enjoy the more restrictive version here => http://pwnable.org:47781/.