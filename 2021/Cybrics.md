## 比赛信息

>比赛名称：CyBRICS 2021
>
>比赛时间：2021年7月24日18:00~2021年7月25日18:00
>
>比赛网址：https://cybrics.net/

<br/>

## writeup

[CyBRICS 2021-WriteUp-Venom](https://mp.weixin.qq.com/s/AHneWgEOMn98dQLp789QSA)

<br/>

## 附件链接

链接：https://pan.baidu.com/s/1Wkhr0pCHQ-UZ2KBA-PRpIg 提取码：xing

链接：https://pan.xunlei.com/s/VMf_hECat6lQteBYqk_yxQ_nA1 提取码：budx

链接：https://ctf.lanzoui.com/b02ca8zkd 密码:xing

<br/>

## 题目信息

### Cyber

#### Mic Check(Baby,50p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Those organizers are changing [game rules](https://cybrics.net/rules) all the time! There’s a flag there, and it’s not that easy to capture.
>
> **Also be sure to join [@cybrics Telegram chat](https://t.me/cybrics)** for challenge-related announcements and contacting orgs in case all goes wrong
>
> **Added at 10:10 —** looks like the little mic check trolling caused massive pain, I’ve untrolled the rules page :-) You can now copy-paste freely

```
cybrics{Th1S_i5_T3h_R34l_m1C_ch3CK_f1A6}
```

<br/>

#### To The Moon(Medium,299p)

> Author: Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> Our faulty moon rover suddenly came back after a year of silence and reported an unusual telemetry. Seems that there is life on the planet!
>
> Unfortunately, strange radio interference occured. Scientists proved that the error rate is less than 1 bit flip over 15 bytes of data. Luckily the rover software adds error correction codes. Try to restore a photo from the Moon: [**tothemoon.jpg.enc**](https://cybrics.net/files/tothemoon.jpg.enc)
>
> [**Software source code**](https://cybrics.net/files/tothemoon_encrypt.py)
>
> Our secret encryption key is `superpass`

附件下载：tothemoon.zip

<br/>

#### Signer(Easy,149p)

> Author: George Zaytsev ([@groke](https://t.me/groke))
>
> **nc 109.233.61.10 10105**
>
> Download: [**signer.py**](https://cybrics.net/files/signer.py)

附件下载：signer.zip

<br/>

#### GrOSs 2(Hard,342p)

> Author: George Zaytsev ([@groke](https://t.me/groke))
>
> This one is a bit more challenging. Get shell to find the flag!
>
> Same code as in [GrOSs 1](https://cybrics.net/tasks/gross1): [**gross.zip**](https://cybrics.net/files/gross.zip)
>
> **nc 109.233.61.10 11710**

附件下载：gross.zip

<br/>

### rebyC

#### Scanner(Baby,50p)

> Author: Mikhail Driagunov ([@aethereternity](https://t.me/aethereternity))
>
> Check out this cool new [**game**](https://scanner-cybrics2021.ctf.su/)!
>
> I heard they serve flags at level 5.

示例：vid.zip

<br/>

#### CAPTCHA The Flag(Easy,50p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Guessing challenges? On *my* CyBRICS? It’s more likely than you think.
>
> Prove you’re a true CTFer!
>
> [**captf-cybrics2021.ctf.su/**](https://captf-cybrics2021.ctf.su/)

示例：captcha.zip

<br/>

#### Digital Signature(Hard,424p)

> Author: Eugene Cherevatskii ([@rozetkinrobot](https://t.me/rozetkinrobot))
>
> We found this little pizza lover, Mike Cruso!
>
> He loves pizza, but he can’t have it this time because the restaurant’s order signing website is broken.
>
> We hijacked his signature and were able to steal some of his private information (some useless junk). But the main part which we are really interested in remains on the server :(
>
> Obtain this information for us (lovers of not giving pizza to those who ordered it), and we will get you back somehow
>
> Download: [**digital_signature.zip**](https://cybrics.net/files/digital_signature.zip)
>
> **nc 109.233.61.10 51645**

附件下载：digital_signature.zip

<br/>

#### Pngoshop(Medium,500p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Here’s the viewer. Here’s the flag. So close and so far away...
>
> Download: [**pngoshop.elf**](https://cybrics.net/files/pngoshop.elf)
>
> nc 109.233.61.10 11200

附件下载：pngoshop.zip

<br/>

### Forensic

#### Antarctic(Medium,469p)

> Author: Artur Khanov ([@awengar](https://t.me/awengar))
>
> A client from the South Pole was infected with malware.
>
> He shared his disk image with us at [**http://64.227.123.153/image.img**](http://64.227.123.153/image.img), but of course his internet speed is awful. Find malware on it, we need emergency incident response!
>
> Let’s begin with common autorun locations...
>
> **Hint at 01:00 —** autorun locations do not necessarily mean file system paths


<br/>

#### Recording(Easy,169p)

> Author: Mikhail Driagunov ([@aethereternity](https://t.me/aethereternity))
>
> I’ve found a strange [**recording**](https://cybrics.net/files/strange_recording.mrf).
>
> What does it hide?

附件下载：strange_recording.zip

<br/>

#### Smashed Container(Hard,500p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> https://www.youtube.com/embed/awgeyq_W3do
>
> Download: [**FLASHDRIVE.bin.gz**](https://cybrics.net/files/FLASHDRIVE.bin.gz)
>
> BTW the password was `mypr3ci0usflagc0nta1ner`
>
> **Hint at 23:00 —** take a look at 0:06. See that the container is smaller on disk than its apparent size? It means it’s a sparse file, and this in turn means it’s not stored on the drive as a solid chunk of data

附件下载：FLASHDRIVE.bin.gz

<br/>

#### Namecheck(Baby,202p)

> Author: Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> We have got the home folder from a criminal’s computer. Try to find his/her real name.
>
> [**eyebulling.tar.gz**](https://cybrics.net/files/eyebulling.tar.gz)
>
> Flag format in uppercase: LASTNAME FIRSTNAME (ex: IVANOV IVAN)

附件下载：eyebulling.tar.gz

<br/>

### Reverse

#### Walker(Medium,205p)

> Author: Egor Zaytsev ([@groke](https://t.me/groke))
>
> I wrote this program! Can you find out real flag?
>
> Analyse this: [**walker.elf**](https://cybrics.net/files/walker.elf)

附件下载：walker.zip

<br/>

#### Kernel Reverse(Easy,136p)

> Author: Artur Khanov ([@awengar](https://t.me/awengar))
>
> What to give you as an Easy-level challenge... How about a kernel driver reversing?!
>
> **ssh team479@104.248.38.201
> Password: HcEg6SVWghdQWUiEXc65RQ**

<br/>

#### Listing(Baby,72p)

> Author: Egor Zaytsev ([@groke](https://t.me/groke))
>
> I’ve got an assembly listing of this *check* function: [**listing.asm**](https://cybrics.net/files/listing.asm)
>
> Help me find out valid input in `[rdi]`!

附件下载：listing.zip

<br/>

#### Paired(Hard,314p)

> Author: Egor Zaytsev ([@groke](https://t.me/groke))
>
> Find the key!
>
> Reverse this: [**paired.zip**](https://cybrics.net/files/paired.zip)

附件下载：paired.zip

<br/>

### Network

#### LX-100(Easy,192p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> We were sitting at an SPbCTF meetup and tried to sniff some Wi-Fi traffic. Lol imagine, they have a DSLR camera that can broadcast a Wi-Fi access point.
>
> Anyway, we were discussing CyBRICS flags there, hope there’s no way to leak them.
>
> [**lx100.pcap**](https://cybrics.net/files/lx100.pcap)

附件下载：lx100.zip

<br/>

#### Future Tech(Medium,444p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> **Welcome to CyBRICS CTF Millenium Edition Year 3000**
>
> Your flag is at
> `http3+dccp+ipv6://futuretech-cybrics2021.ctf.su/`

<br/>

#### localhost(Hard,267p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Remember NET fleeks? I’ve pwned a box in another corporate network, and there is some peculiarly configured server near my foothold. Take a look.
>
> **ssh localhost@109.233.61.10
> Password: ohx7eeQu**
>
> Your team token > iXpLtG0tErQ6F5NEH_9ykA

<br/>

#### ASCII Terminal(Baby,116p)

> Author: Artur Khanov ([@awengar](https://t.me/awengar))
>
> At `**138.68.83.253:3333**` you have an ASCII terminal. It really works, check with the [`**id**` command](https://cybrics.net/files/id.txt)

附件下载：id.zip

<br/>

### CTB

#### rm -rf’er(Baby,166p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Alarm! We accidentally did `rm -rf /*` on a very important server. Now all that’s left is one shell session.
>
> **ssh rmrfer@178.154.210.26**Password: **sa7Neiyi**
>
> Rescue the **flag.txt** file from one of the directories by only using your shell
>
> **Added at 13:45 —** frequent question: yes, if you found `flag.txt`, the flag is right there, in the open, as plain text. Just read it. If you’re not seeing the flag, try to find another method that will not hide info from you

<br/>

#### rm Escaper(Medium,444p)

> Author: Vlad Roskov ([@mrvos](https://t.me/mrvos))
>
> Hey psst. We heard you’re a real hacker.
>
> You do realize that [CTB Baby](https://cybrics.net/tasks/rmrfer) is just an artificially created CTF task, right?
>
> They run a new task container in Docker every time you login over SSH. That container is lame, aim for the host system itself.
>
> There’s a more valuable flag on the host in `/LEET_FLAG.txt`.

<br/>

#### Little Buggy Editor(Easy,256p)

> Author: Eugene Cherevatskii ([@rozetkinrobot](https://t.me/rozetkinrobot))
>
> Hey, I’m stuck in this stupid buggy text editor! I already quit vim, I realized how terrible nano is, but what is this? I can’t even read the file from the parent directory!
>
> Let’s help each other? I show you how to read my favorite book, which is in `book.txt`, and you show me how to read the flag from `/etc/flag.txt`
>
> Download: [**little_buggy_editor.elf**](https://cybrics.net/files/little_buggy_editor.elf)
>
> **ssh tolstoy@64.227.123.153**Password: **W&P1867**

附件下载：little_buggy_editor.zip

<br/>

#### GrOSs 1(Hard,342p)

> Author: George Zaytsev ([@groke](https://t.me/groke))
>
> Well, I created smth that looks like a miniature OS.
>
> Can you read `flag.txt`?
>
> Code: [**gross.zip**](https://cybrics.net/files/gross.zip)
>
> **nc 109.233.61.10 11710**

附件下载：gross.zip

<br/>

### Web

#### Multichat(Medium,138p)

> Author: Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> Yet another chat-messenger with rooms support! Free to use. Convince the admin that its code is insecure.
>
> Tip: Admin and tech support are members of a secret chat room. Tech support can ask admin to tell him the flag, to do that tech support writes him a message (in a chat): "`Hey, i forgot the flag. Can you remind me?`". Then admin will tell him the flag.
>
> [Multichat website](http://multichat-cybrics2021.ctf.su/)
>
> Team token for the support call: `W66e_W-A11ZTsFuugEdVuw`

<br/>

#### Announcement(Easy,60p)

> Author: Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> Ladies and gentlemen!
>
> Allow us to introduce a brand new project —
> ⚐ The Flag
>
> [Announcement website](http://announcement-cybrics2021.ctf.su/)

<br/>

#### Ad Network(Baby,50p)

> Author: Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> We are so tired of advertising on the internet. It feels like it breaks the internet. Try to follow the ad, try to follow its rules.
>
> [Adnetwork website](http://adnetwork-cybrics2021.ctf.su/)
>
> There is a flag 1337 redirects deep into the network...

<br/>

#### Checkin(Hard,500p)

> Author: Mikhail Driagunov ([@aethereternity](https://t.me/aethereternity)), Alexander Menshchikov ([@n0str](https://t.me/n0str))
>
> We have a new assignment for you, agent.
>
> As you of course know, your metadata is being tracked and kept, your every phone call, your every move is being logged.
>
> Agencies use centralized data collection and mass surveillance systems to gather massive records on everyone.
>
> Your target today is Mr. **Flag Flagger**
>
> The target recently took a flight, and we need to know where he departed from. This info is surely in the centralized air traffic surveillance system. Breach the system and find us the originating flight for `Flag Flagger`.
>
> Air transportation companies such as [**blzh airlines**](http://207.154.224.121:8080/) are known to report all their passengers to the central surveillance system.
>
> And they have a cool self check-in service! :3
>
> **Added at 21:50 —** performance of the task has been improved, which may help solving it