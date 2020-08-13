## 其他wp

- [官方中文wp](https://blog.rois.io/2020/rctf-2020-official-writeup/)
- [官方英文wp](https://blog.rois.io/en/2020/rctf-2020-official-writeup-2/)
- [2020-RCTF-WP-Nu1L.pdf](../writeup/2020-RCTF-WP-Nu1L.pdf)
- [RCTF 2020 Writeup by Venom](https://mp.weixin.qq.com/s/0J9Omna8tmKWP9s4iSg10w)
- [RCTF2020 WriteUp By W&M](https://mp.weixin.qq.com/s/ppTD4uLAxa5VcOgZD70ZWw)
- [来自Timeline Sec CTF](https://mp.weixin.qq.com/s/3II5Etd2QpDqn5m0z7p88A)



## 附件链接

链接：https://pan.baidu.com/s/19qJHcHNWCu1S000Edw6VWQ 提取码：hdxw

链接：https://share.weiyun.com/igMsxq33 密码：w6nzjs

外链:https://t1m.lanzous.com/b0aewte3i 密码:hdxw



## WEB

### swoole

> Make unserialize great again
>
> https://swoole.rctf2020.rois.io
>
> hint1: https://github.com/swoole/library/issues/34 this might helpful

https://swoole.rctf2020.rois.io/?phpinfo
Version => 4.4.18

```php
#!/usr/bin/env php
<?php
Swoole\Runtime::enableCoroutine($flags = SWOOLE_HOOK_ALL);
$http = new Swoole\Http\Server("0.0.0.0", 9501);
$http->on("request",
    function (Swoole\Http\Request $request, Swoole\Http\Response $response) {
        Swoole\Runtime::enableCoroutine();
        $response->header('Content-Type', 'text/plain');
        // $response->sendfile('/flag');
        if (isset($request->get['phpinfo'])) {
            // Prevent racing condition
            // ob_start();phpinfo();
            // return $response->end(ob_get_clean());
            return $response->sendfile('phpinfo.txt');
        }
        if (isset($request->get['code'])) {
            try {
                $code = $request->get['code'];
                if (!preg_match('/\x00/', $code)) {
                    $a = unserialize($code);
                    $a();
                    $a = null;
                }
            } catch (\Throwable $e) {
                var_dump($code);
                var_dump($e->getMessage());
                // do nothing
            }
            return $response->end('Done');
        }
        $response->sendfile(__FILE__);
    }
);
$http->start();
```



### rBlog 2020

> https://rblog.rctf2020.rois.io
>
> The source deployed on the server has been slightly modified to ensure the isolation of every single payload.
>
> 题目附件：0d9cf2538f494e08af88aa980b943823.zip
>
> https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace



### chowder_cross

> try to bypass chowder filter to get flag
> http://124.156.139.238/
>
> you should bypass the csp at the first of all,try to find the difference from this web challenge's configuration and other challenge's configuration,maybe it can help you to bypass the csp.
>
> hint2:You can think about how the .htaccess of this web challenge is written, and think about a strange place in Content-Security-Policy, think about what function I implemented it on the back end of php,and find the relevant csp bypass method,I believe this is helpful for you.
>
> hint3: Try to visit the non-existent page and see what happens, pay attention to img-src to see what happens, please combine my previous hints.
>
> hint4: If you bypass the csp please leak nonce, if you use the best method you will only spend about ten seconds to leak admin's nonce,don't think too,I filter more in feedback than post.
>
> hint5: The bot is firefox74.0. And If you are trying leak nonce now and If you think you're doing the right thing but can't leak nonce out, I suggest you to find the difference between leak nonce and other values when there is csp.And if you are filtered in the feedback for no reason, it is recommended that you try to add one or more spaces to your payload.I believe these will be of great help to you.



### Calc

> nobody knows php better than me, So calc it
> http://124.156.140.90:8081

```php
<?php 
error_reporting(0); 
if(!isset($_GET['num'])){ 
    show_source(__FILE__); 
}else{ 
    $str = $_GET['num']; 
    $blacklist = ['[a-z]', '[\x7f-\xff]', '\s',"'", '"', '`', '\[', '\]','\$', '_', '\\\\','\^', ',']; 
    foreach ($blacklist as $blackitem) { 
        if (preg_match('/' . $blackitem . '/im', $str)) { 
            die("what are you want to do?"); 
        } 
    } 
    @eval('echo '.$str.';'); 
} 
?>
```

```bash
RCTF{NO60dy_kn0w5_PhP_6eTter_th4n_y0u}
```



### EasyBlog

> come and write something
> http://124.156.134.92:8081
>
> hint: zepto
>
> EasyBlog has now been fixed due to a CSP configuration issue that caused an error.Sorry about it.



## PWN

### no_write

> there are no write any more!
> This two container are the same, chose one you like.
> nc 124.156.135.103 6000 (HK)
> nc 129.211.134.166 6000 (ShangHai)
>
> 题目附件：e0fc595d04854cdba8e209a68c64383f.zip



### vm

> just simple vm.
> nc 124.156.135.103 6001
>
> 题目附件：43406f3cd1b14151b7748546a3706908.zip



### bf

> oh! brain f**k!
> nc 124.156.135.103 6002
>
> 题目附件：ec9c31bbf46a442f9ad6dc4eb4726978.zip



### note

> Welcome to NOTE shop!
> nc 124.156.135.103 6004
>
> 题目附件：959fac1f0ad7401aa1488f72a35e8502.zip



### golang_interface

> https://golang-interface.rctf2020.rois.io



### Best_php

> Have fun with php
> http://124.156.129.96:8081/
>
> 我们添加了多个端口 现在8080,8081,8082,8083,8084都可以连了
>
> We add some port, 8080,8081,8082,8083 and 8084 ports can be connected now.

Laravel

Hint: /file

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        return view('home');
    }

    public function file(Request $request)
    {
        $file = $request->get('file');

        if (!empty($file)) {
            if (stripos($file, 'storage') === false) {
                include $file;
            }
        } else {
            return highlight_file('../app/Http/Controllers/HomeController.php', true);
        }

    }

    public static function weak_func($code)
    {
        eval($code);
        // try try phpinfo();
        // scandir may help too
    }
}
```



### mginx

> A simple http server 😃
> nc 124.156.129.96 8888
>
> 题目附件：4ea3c3e83d724a2ca9ded15dfa8e4f4f.zip
>
> hint1: 远程环境开启了ASLR There are ASLR in the remote environment, you need to bypass it.
>
> hint2: 由于远程环境的问题，可能要多跑几次exp脚本才能拿到flag For the remote environment reason, maybe you need to run the exp script many times to get the flag. Sorry for it.
>
> hint3: 远程拿不了shell，用orw的方法来拿flag. For the remote environment reason, you can't getshell , use orw to get the flag instead.
>
> hint4: 由于远程环境的问题，如果你在本地用orw拿到了flag，打远程的时候可能多跑几次脚本（几百次左右） For the remote environment reason , if you use orw to get the flag in the local environment, try to run the exp script many times(about several hundred) to get the flag in the remote environment. Sorry for it.



### 0c

> Zero-featured TypeScript on JVM
> nc 124.156.133.68 5000
>
> 题目附件：d1efd6ae08774aabb05f25b4a7e8d27c.zip



## Reverse

### rust-flag

> a rusty flag.
>
> 题目附件：3d9f8fecfa3d4c58918a2d37482dfa00.zip



### go-flag

> I don’t believe that the code was written by a human.
>
> 题目附件：09401137be9541a3a6ebb3151a8b8638.zip



### My Switch Game

> Have fun in my interesting snake game 😃
>
> Relay bt traffic and capture by https://github.com/mart1nro/joycontrol.
>
> 题目附件：96885ee00f0a43369b656e0d1498a040.zip
>
> My switch game hint1: 即便你有switch，那可能也没什么帮助 To solve it, a switch or a swotch pro controller is not necessary. Even you have one, that may hardly helpful.
>
> Hint: If you feel almost arrive at the answer but still stuck in the last step, try to analyze the log.log carefully.



### cipher

> Decrypt it!
>
> 题目附件：b0d826c6af1e45a7b29949a2f1f65342.zip



### play_the _game

> play game!
>
> 题目附件：cb3f4ef2acd145beb3f5b671fda677a2.zip



### panda_trace

> Malware analysis 010，try find the flag：RCTF{****}
>
> The files provided by the two urls below are completely the same. Choose the one you like.
>
> link1: https://drive.google.com/open?id=1pdsk_wgmdf0uM0QRl_s7omC-E0DgtyFB
>
> link2: https://share.weiyun.com/eRXXgZAA
>
> 题目附件：panda_trace.zip



## Crypto

### infantECC

> nc 124.156.133.6 24351
>
> 题目附件：891f6d6b9b784517ae3a1e698d0a546f.zip
>
> hint1: coppersmith



### MultipleMultiply

> nc 124.156.133.6 22298
>
> 题目附件：9b59cd8cd2944803aba75bca4da40111.zip



### easy_f(x)

> Solve it again!
> nc 124.156.140.90 2333
>
> 题目附件：0da7289267504d978a77da96eaf7ea41.zip



## Blockchain

### roiscoin

> 124.156.133.6 10001
>
> Option 1, get an account which will be used to deploy the contract; 
>
> Before option 2, please transfer some eth to this account (for gas); 
>
> Option 2, the robot will use the account to deploy the contract for the problem; 
>
> Option 3, use this option to obtain the flag after the event is triggered. You can finish this challenge in a lot of connections.



## MISC

### bean

> count the PAC-MAN
> https://bean.rctf2020.rois.io



### mysql_interface

> https://mysql-interface.rctf2020.rois.io



### listen

> In 1804, there was such a piece of music
>
> b64eb9bd820d41dd9711fd9f87f52b95.zip



### Animal

> Tom Nook sent a telegram from the uninhabited island welcoming the new residents. It’s not fish sauce, it’s bass.
>
> 题目附件：bdadf07d1a2a423da227f6db745521fa.zip
>
> hint1: Please pay attention to the first phrase after the station is officially established



### Switch PRO Controller

> I bought a Switch PRO Controller!! It’s really cool!
>
> PS: Please replace ‘-’ to ‘_’ when you submit flag.
>
> 题目附件：4de4ce81eb3c4a878e66e8bbc4c6853c.zip



### Welcome to the RCTF 2020

> https://t.me/RCTF2020 for flag



```
RCTF{we1c0me_to_the_RCTF2020~}
```



### FeedBack

> We need your FeedBack!
> https://docs.google.com/forms/d/e/1FAIpQLSd8LfhSRNYpwelFp3VQUTrGkYkXpaxNDPY9cFgl5JVnao0Uww/viewform?usp=sf_link



```
RCTF{Thanks_for_your_FeedBack}
```

