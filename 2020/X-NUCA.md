## 比赛信息

> 比赛名称：2020年全国高校网安联赛X-NUCA’2020
>
> 比赛时间：2020年10月30日9:30至2020年10月31日21:30
>
> 比赛网址：https://race.ichunqiu.com/2020xnuca

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1Rt3q31gZc1d6-j5c3-3NQA 提取码：5555

链接：https://share.weiyun.com/4fEOYIr9 密码：42zn1j

外链:https://t1m.lanzous.com/b0af9zg6h 密码:5555

<br/>

## 题目信息

### MISC

#### torch model(13sloved,313pt)

> Python==3.7.7
>
> torch==1.5.0
>
> Crack the torch model and get flag!
>
> Submission format: `flag{%s}`

附件下载：torchmodel.zip

<br/>

#### catchthecat(5sloved,417pt)

> Explore the maze and catch the cat. The cat may flash several times. Enjoy.
>
> nc 59.110.63.160 40001

附件下载：catchthecat_manual.zip

<br/>

#### 问卷调查(66sloved,24pt)

> https://www.wjx.cn/m/95796569.aspx

```
flag{thanks_to_your_feedback}
```

<br/>

### CRYPTO

#### imposter(14sloved,304pt)

> nc 123.57.4.93 45216

附件下载：imposter.tar.gz.zip

<br/>

#### weird(10sloved,345pt)

附件下载：weird.tar.gz.zip

<br/>

#### diamond(2sloved,477pt)

附件下载：diamond.tar.gz.zip

<br/>

### PWN

#### babyv8(2sloved,477pt)

> 这是真正的baby V8，你只需要知道那么一点点相关知识就能愉快地PWN了。
>
> nc 123.57.4.93 44228

附件下载：babyV8.zip

<br/>

#### defile(6sloved,400pt)

> It's a shame that such a beautiful shellcode has been defiled by a random patch. Try to write some robust code. Enjoy.
>
> nc 39.97.171.121 40001-40007 这7个端口任意一个端口同时只能接受一个连接，同一个队伍使用TOKEN只能在一定时间内连接一次（全局互斥，例如，在40001连接成功一次后，将不能在一定时间内连入任意一个端口）连接之间的间隔可能在比赛期间进行调整。建议本地能够相对稳定地打通再攻击远程。

附件下载：defile.tar.gz.zip

<br/>

#### rtos(2sloved,477pt)

> arm vexpress-a9 rt-thread rtos pwn stage 1 flag在sd.bin里面
>
> nc 123.57.4.93 45559
>
> 题目去除了pow.py
>
> hint: open: 600572F8 read: 6005741C scanf: 600746C0 ； 题目难度调整，已更新附件。

附件下载：rtos_new.zip

<br/>

#### vm(4sloved,435pt)

> ubuntu 18.04
>
> nc 123.57.4.93 8521

附件下载：vm.zip

<br/>

#### ParseC(20sloved,257pt)

> ParseC is a simple C interpreter `example` is a sample for this ParseC You will give your source code file in base64 to remote server
>
> nc 123.57.4.93 34007

附件下载：ParseC_lnew.zip

<br/>

#### cpp(9sloved,358pt)

> Heap exploiting is so boring.
>
> nc 123.57.4.93 12001

附件下载：cpp.zip

<br/>

#### ez_elf(9sloved,358pt)

> I think every CTFer is familiar with ELF structure.
>
> nc 123.57.4.93 23334

附件下载：ez_elf.zip

<br/>

### REVERSE

#### escapeme(3sloved,455pt)

> All work and no play makes Jack a dull boy. I have prepared you a game. If you complete the game, I will serve you the flag.
>
> nc 47.93.123.12 56184

附件下载：escapeme.zip

<br/>

#### I have no name!(0sloved,500pt)

> A very normal crackme, too normal to be named. Take your time.

附件下载：ihavenoname.zip

<br/>

#### cyclic(0sloved,500pt)

> It's so hard to understand and solve it, emmm...
>
> flag format: XNUCA2020{...}

附件下载：cyclic.zip

<br/>

#### babyarm(12sloved,323pt)

> qemu-arm -L . ./babyarm
>
> 只需要分析babyarm文件

附件下载：babyarm.zip

<br/>

#### repair(5sloved,417pt)

> 高版本qemu执行程序时会出现问题，请使用附带的qemu-arm

附件下载：repair.zip

<br/>

#### Unravel MFC(26sloved,223pt)

> Do you know the pain of reversing Microsoft Foundation Classes ?（本题没有flag格式）

附件下载：unravelmfc.zip

<br/>

#### Exception(7sloved,385pt)

> Nested expansion.（本题没有flag格式）

附件下载：exception.zip

<br/>

#### hellowasm(5sloved,417pt)

> Let's say hello to wasm.

附件下载：hellowasm.zip

<br/>

#### dga(0sloved,500pt)

附件下载：dga.zip

<br/>

### WEB

#### easyjava(0sloved,500pt)

> hint: something interest in /download and it’s response

<br/>

#### oooooooldjs(4sloved,435pt)

> no intranet, try to rce, have fun!
>
> hint: `npm audit` may miss something, be careful of the version of `lodash`. There is prototype pollution in `express-validator`, limited but powerful。

附件下载：oooooooldjs.zip

<br/>

#### workdeep(0sloved,500pt)

> flag in /root/flag
>
> 提示1：try to read source code 
>
> 提示2：dompurify is safe,read source code carefully 
>
> 提示3：/client

<br/>

#### easyphp_revenge(0sloved,500pt)

> http://39.97.167.132/notice.txt
>
> windows is powerful

```
disable_functions = chdir,imagecreatefromgd2part,fclose,imagecreatefromgd2,sqlite_popen,fwrite,chgrp,xml_parser_create_ns,ini_get,pcntl_wifexited,openlog,linkinfo,apache_child_terminate,copy,zip_open,socket_bind,proc_get_status,stream_socket_accept,pcntl_get_last_error,pcntl_wtermsig,parse_ini_file,shell_exec,apache_get_modules,readdir,sqlite_open,syslog,pcntl_strerror,imap_open,error_log,passthru,fopen,pcntl_wexitstatus,dir,pcntl_wifstopped,ignore_user_abort,pcntl_wait,link,xml_parse,pcntl_getpriority,ini_set,imagecreatefromxpm,imagecreatefromwbmp,pcntl_wifsignaled,pcntl_sigwaitinfo,curl_init,socket_create,rename,pcntl_signal_get_handler,apache_setenv,sleep,ini_get_all,parse_ini_string,realpath,apache_reset_timeout,curl_exec,pcntl_signal_dispatch,putenv,ftp_exec,pcntl_exec,imagecreatetruecolor,get_cfg_var,dl,stream_socket_server,popen,pcntl_waitpid,chown,ini_restore,ini_alter,pcntl_signal,glob,pcntl_sigtimedwait,zend_version,imagecreatefrompng,set_time_limit,pcntl_fork,mb_send_mail,system,pcntl_setpriority,pcntl_async_signals,imap_mail,pfsockopen,imagecreatefromwebp,pcntl_alarm,pcntl_wstopsig,exec,virtual,ftp_connect,stream_socket_client,fsockopen,imagecreatefromstring,apache_get_version,readlink,pcntl_wifcontinued,xml_parser_create,imagecreatefromxbm,proc_open,pcntl_sigprocmask,curl_multi_exec,mail,chmod,apache_getenv,chroot,bindtextdomain,ld,symlink
flag is in /flag
navigate / to init your env
```

```php
<?php
$userHome = md5($_SERVER['REMOTE_ADDR']);
$arr = explode('\\', getcwd());
$num = count($arr);
if($arr[$num - 1] !== $userHome) {
    echo "no access to this challenge";
    die();
}
if(!isset($_GET['content']) || !isset($_GET['filename']) || !isset($_GET['teamtoken'])){
    highlight_file(__FILE__);
    die();
}

include($_SERVER['DOCUMENT_ROOT'] . "/function.php");

$content = $_GET['content'];
$filename = $_GET['filename'];
$token = $_GET['teamtoken'];

if(!is_string($content) || strlen($content)>125) {
    echo "Hacker";
    die();
}
if(!is_string($filename) || strlen($filename)>10) {
    echo "Hacker";
    die();
}
if(!is_string($token) || strlen($token)!==32) {
    echo "Hacker";
    die();
}
for($i=0;$i<31;$i++) {
    if($i !== 10 && stristr($content, chr($i))) {
        echo "Hacker";
        die();
    }
}
for($i=127;$i<256;$i++) {
    if(stristr($content, chr($i))) {
        echo "Hacker";
        die();
    }
}
$content_blacklist = array("session", "html", "type", "upload", "append", "prepend", "log", "script", "error", "include", "zend", "htaccess", "pcre", "\\", "#");
foreach($content_blacklist as $keywords) {
    if(stristr($content, $keywords)) {
        echo "Hacker";
        die();
    }
}
$filename_whitelist = array(".htaccess");
$append_string = "\nhope no unintended\nhope no unintended\nhope no unintended\n";
if(preg_match("/icq[0-9a-f]{29}/", $token) === 1) {
    if (checkToken($token, $content) === true) {
        if(array_search($filename, $filename_whitelist) !== FALSE){
            file_put_contents(getcwd() . '/' . $filename, $content . $append_string);
        } else {
            echo $filename;
        }
    } else {
        echo "use your valid teamtoken in icq, and you only have 30 times submit your payload.";
        die();
    }
} else {
    echo "Hacker";
    die();
}
?>
```

