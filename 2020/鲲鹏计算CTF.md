## 比赛信息

> 比赛名称：XCTF高校网络安全专题挑战赛鲲鹏计算专场
>
> 比赛网址：https://huaweictf.xctf.org.cn/event_jeopardy/contest_challenge/04d6dc22-6cbd-4a36-a298-5963b0638a14/
>
> 比赛时间：2020-12-23 08:00~2020-12-24 00:00

<br/>

## writeup

[XCTF高校网络安全专题挑战赛-鲲鹏计算专场 官方Writeup](https://www.xctf.org.cn/library/details/55599c9c17ea0e8ca0b094adbe075a03a7321599/)

网盘文档：

2020-华为CTF-2-WP-Nu1L.pdf

<br/>

### 附件链接

链接：https://pan.baidu.com/s/1tS3qDBkaX9sSrXvLVSTJqw 提取码：xing

链接：https://pan.xunlei.com/s/VMdun10WNORneS_vzmFhmbgrA1 提取码：6azx

链接：https://ctf.lanzoui.com/b02c7t3dc 密码:xing

<br/>

## 题目信息

### WEB

#### babyphp(44s,317p)

源码下载：babyphp.zip

<br/>

#### cloudstorage(20s,512p)

> 云存储！！！
> 由于node单线程容易阻塞，所以提供多个解题环境端口从8000到8015，flag都是相同的。
> [http://cloudstorage.xctf.org.cn:8000](http://cloudstorage.xctf.org.cn:8000/)
> [http://cloudstorage.xctf.org.cn:8001](http://cloudstorage.xctf.org.cn:8001/)
> [http://cloudstorage.xctf.org.cn:8002](http://cloudstorage.xctf.org.cn:8002/)
> [http://cloudstorage.xctf.org.cn:8003](http://cloudstorage.xctf.org.cn:8003/)
> 。。。
> [http://cloudstorage.xctf.org.cn:8015](http://cloudstorage.xctf.org.cn:8015/)
> 解压后请详细阅读`docker_build.zip`附件中的readme.md
> 下面的链接是docker save 导出的tar包，可使用docker load 命令导入。适用于docker build时网络不稳定，导致无法build的选手下载。
> [https://test-storage111v1.obs.cn-south-1.myhuaweicloud.com:443/clouddisk.tar?AccessKeyId=ES2PKF82MJ93YTSE673W&Expires=1608781380&response-content-disposition=inline&x-obs-security-token=gQpjbi1ub3J0aC00jJQiWuiM7ITkAMtI5Qc-ra7O3rTx5VSLL3pDF3nTfd43PvENOdi8bKzzzhthtnlrAzAhMOKSZ5yMKLe_znGDBNMb9lR2KPigeT8Zb8hTFVDzY1uLl1acWtZixyHPpjMVrosBGDd8wR1LcjtJiAq8Qvd44QU2kcgnYQXR4l4jSrQFO21Fs0LNECzbR6qdR-_vZcQBJjRPY47B-vUa3y1GE5qVCz1abrc19vrMlhXq0NV4XOKcsT-bDw311gpwI_ab2Rjtbjy89Kl54o3bZQhPMG4W_4rE8HZPFvte8kWQByakNw2B5JU0yZKcdVai4ELOy0QXZyGe8UNr0L7yACJBMhPt0iWf8yJA0_j4HV6uKiew-AUJSG_J2GZTPvXUngXPQbVCVvqhjcVbksvi9nVEAilUMO8jnpYdnjBe3J0vLWKfHgjdQuq1mx0IGQNZNpSbbJQmChux7LrMpbz7lRpspuQqOPE6cZLMs1a8RIfSpVp_lYwVFYGhmRfRNATmxLKE70_rNMhEDmMsilJpTXcSf5rwkHeXZGqA02eTfTzaB4w9NKOR04r46LEBX7SsMxf08re1KnZk07DDUAA06WOStpo6oRebCaLeJyl1DL0i0Pr2CAmSXbXcWYRDlvuX5aifGVSaM5lkkXSNaoUu2qG3c3oFc5CAzofexyyFCpnyJBWoGlyThvfnmW1y7WDEBodUBFNyrA3b6uvhspB7vk-BukE7ItxkrvgKlT_b2_ASGh00m1RbC0o2HiNhttUAsFZ2nMdIHpwXVNKf9Q8BdcZmZ0dJXLaJavuQ0PxLQUqbnhJo&Signature=1nUOMaVeP2l0dMR/XLnX6c7YRtA%3D](https://test-storage111v1.obs.cn-south-1.myhuaweicloud.com/clouddisk.tar?AccessKeyId=ES2PKF82MJ93YTSE673W&Expires=1608781380&response-content-disposition=inline&x-obs-security-token=gQpjbi1ub3J0aC00jJQiWuiM7ITkAMtI5Qc-ra7O3rTx5VSLL3pDF3nTfd43PvENOdi8bKzzzhthtnlrAzAhMOKSZ5yMKLe_znGDBNMb9lR2KPigeT8Zb8hTFVDzY1uLl1acWtZixyHPpjMVrosBGDd8wR1LcjtJiAq8Qvd44QU2kcgnYQXR4l4jSrQFO21Fs0LNECzbR6qdR-_vZcQBJjRPY47B-vUa3y1GE5qVCz1abrc19vrMlhXq0NV4XOKcsT-bDw311gpwI_ab2Rjtbjy89Kl54o3bZQhPMG4W_4rE8HZPFvte8kWQByakNw2B5JU0yZKcdVai4ELOy0QXZyGe8UNr0L7yACJBMhPt0iWf8yJA0_j4HV6uKiew-AUJSG_J2GZTPvXUngXPQbVCVvqhjcVbksvi9nVEAilUMO8jnpYdnjBe3J0vLWKfHgjdQuq1mx0IGQNZNpSbbJQmChux7LrMpbz7lRpspuQqOPE6cZLMs1a8RIfSpVp_lYwVFYGhmRfRNATmxLKE70_rNMhEDmMsilJpTXcSf5rwkHeXZGqA02eTfTzaB4w9NKOR04r46LEBX7SsMxf08re1KnZk07DDUAA06WOStpo6oRebCaLeJyl1DL0i0Pr2CAmSXbXcWYRDlvuX5aifGVSaM5lkkXSNaoUu2qG3c3oFc5CAzofexyyFCpnyJBWoGlyThvfnmW1y7WDEBodUBFNyrA3b6uvhspB7vk-BukE7ItxkrvgKlT_b2_ASGh00m1RbC0o2HiNhttUAsFZ2nMdIHpwXVNKf9Q8BdcZmZ0dJXLaJavuQ0PxLQUqbnhJo&Signature=1nUOMaVeP2l0dMR/XLnX6c7YRtA%3D)
>
> [http://cloudstorage.xctf.org.cn:8000](http://cloudstorage.xctf.org.cn:8000/)

附件下载：task_source.zip、clouddisk.tar（917M）

<br/>

#### 签到题(329s,57p)

> 不关注就没有flag
>
> ( •̀ ω •́ )✧

```
flag{Shifujiayou}
```

题目源码：签到题.zip

<br/>

### CRYPTO

#### backpack(16s,571p)

> 稍微算算就能接出来（逃

附件下载：task_attachment_0OMWkEy.zip

<br/>

#### combinelfsr(25s,454p)

> 一道简单的现代密码学赛题。

附件下载：task_task.zip

<br/>

#### rrssaa(24s,465p)

> 平平无奇的RSA

附件下载：task_task_gHXvFLV.zip

<br/>

### MISC

#### BoxGame(3s,909p)

> Your goal is to emit ForFlag(address addr) event
>
> nc 124.71.138.9 10001

```bash
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Game environment: Ropsten testnet

Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after emit ForFlag(address addr) event.
You can finish this challenge in a lot of connections.

[-]input your choice: 1
[+]Your game account:0xE7C4f303fA64EdBcB2C0D801adA1D9d7Eb3706F2
[+]token: 5ZUmEs1toe/ktUqdgEhd......
[+]Make sure that you have enough ether to deploy!!!!!!

[-]input your choice: 2
[-]input your token: 5ZUmEs1toe/ktUqdgEhd......
[+]new token: SBAqEBAuHoft0705vfBcX4QVoCl......
[+]Your goal is to emit ForFlag(address addr) event in the game contract
[+]Transaction hash: 0xa4933b574f3445224673a56b277c394b81c9cc949d1c0562cacc5e35cc1efdaa
```

源码下载：boxgame.zip

<br/>

#### s34hunka(15s,588p)

> 在excel中画画

附件下载：task_s34hunka.zip

<br/>

### PWN

#### honorbook(15s,588p)

> nc 121.36.192.114 9999

附件下载：task_attachment_DKoJ9wV.zip

<br/>

#### Schrodingerbox(0s,1000p)

> nc 121.37.196.163 52520
> 下载链接为无flag的在线环境镜像，可自行下载导入，格式为vmdk。
> 用户名root，密码huawei123！
> [https://test-storage111v1.obs.cn-south-1.myhuaweicloud.com:443/Schrodingerbox.vmdk?AccessKeyId=R6EMU4S8NYJT0HFFG240&Expires=1608778784&response-content-disposition=inline&x-obs-security-token=gQpjbi1ub3J0aC00jGyM7KsGshtz87EVwsqooxCYZ8cEo5c6Sat6pP3a_jdTzrYXAzPB_mOoABkooR5zYI11fdqEaHnEMgj5Ckvib2OgfEZtOPiqI5dXdp1cPl9NZyCY8_EptpMLLXwnqbeFFNyPkIO_FO8tQOxPIzMVjQe0zWJWzoIhlGEn3l5G4B8VEF3RZOBTR9Zh4wLHQUZ40jZBU1WsfIhPu9cGAJmAq5FQReIbVDKnz-7QrCYV-WWYqFpjwtmmzItczlYYeP8fzvEqUk87pQvTLtznHYCFGQUgtzFYdPthR9A1O9oSskx5n4XMMRbSZ0wSWgCPuA8fd2DmIfqtbZC9FjqDlJnkZHrBJuhLx1BrmRAxpQSlJib1wxs18UPsgUk_ARORcls0UjCvhT-EP6jvyopZA0fMV47kvB3Ox5UV2slQK1HEULqpZDRhcDIeIznR5jGKjvXrhZQqDuM7DIU8CQOeMPynExS09ZNxblMVrMKyNVDa3vdTHgiCMvW9X457Ytd6r9eTgRBTiXvZk7v3Vokm-9P_9EqZt9lFyNCmRj1kEEtAXh6Oo6kgEfhXs3zuY23cfVdkIgkY4uRhT4GTur0TDJiXDNl8zyBe7jq5vMrAqKJEjgs2yDz9R4F52nHdWu8QOunUYqD3UTmTFwJyKrQY9Bbxw5MJl7E2HYp41cYlFyEd6vDu6V14vnXUBsUpLSFTsoLfB_zwAhgtnNOOM7XVu3C5R7y6WY-pSRYpvAjy7SJaBikc8MJbDjz1HBorHCdBcrv2EOCAo99a5W38-LzH-Qqg8hZ59LIyA00E5JWpGVFjxqsY&Signature=XWHcc4Y6lchtwu5mhQ7Spfv7cP0%3D](https://test-storage111v1.obs.cn-south-1.myhuaweicloud.com/Schrodingerbox.vmdk?AccessKeyId=R6EMU4S8NYJT0HFFG240&Expires=1608778784&response-content-disposition=inline&x-obs-security-token=gQpjbi1ub3J0aC00jGyM7KsGshtz87EVwsqooxCYZ8cEo5c6Sat6pP3a_jdTzrYXAzPB_mOoABkooR5zYI11fdqEaHnEMgj5Ckvib2OgfEZtOPiqI5dXdp1cPl9NZyCY8_EptpMLLXwnqbeFFNyPkIO_FO8tQOxPIzMVjQe0zWJWzoIhlGEn3l5G4B8VEF3RZOBTR9Zh4wLHQUZ40jZBU1WsfIhPu9cGAJmAq5FQReIbVDKnz-7QrCYV-WWYqFpjwtmmzItczlYYeP8fzvEqUk87pQvTLtznHYCFGQUgtzFYdPthR9A1O9oSskx5n4XMMRbSZ0wSWgCPuA8fd2DmIfqtbZC9FjqDlJnkZHrBJuhLx1BrmRAxpQSlJib1wxs18UPsgUk_ARORcls0UjCvhT-EP6jvyopZA0fMV47kvB3Ox5UV2slQK1HEULqpZDRhcDIeIznR5jGKjvXrhZQqDuM7DIU8CQOeMPynExS09ZNxblMVrMKyNVDa3vdTHgiCMvW9X457Ytd6r9eTgRBTiXvZk7v3Vokm-9P_9EqZt9lFyNCmRj1kEEtAXh6Oo6kgEfhXs3zuY23cfVdkIgkY4uRhT4GTur0TDJiXDNl8zyBe7jq5vMrAqKJEjgs2yDz9R4F52nHdWu8QOunUYqD3UTmTFwJyKrQY9Bbxw5MJl7E2HYp41cYlFyEd6vDu6V14vnXUBsUpLSFTsoLfB_zwAhgtnNOOM7XVu3C5R7y6WY-pSRYpvAjy7SJaBikc8MJbDjz1HBorHCdBcrv2EOCAo99a5W38-LzH-Qqg8hZ59LIyA00E5JWpGVFjxqsY&Signature=XWHcc4Y6lchtwu5mhQ7Spfv7cP0%3D)
>
> hint1: Schrodingerbox离线虚拟机的用户名密码为root/huawei123!

附件下载：task_schrodingerbox.zip、Schrodingerbox.zip（2.06G）

<br/>

### REVERSE

#### mips(34s,377p)

> 找到正确的路径

附件下载：task_file.zip

<br/>

#### print(8s,740p)

> nc 121.37.182.111 6666

附件下载：task_print.zip

<br/>

#### pypy(30s,408p)

> 贪吃蛇

附件下载：task_main_6cKjEFN.zip

<br/>

### READLWORLD

#### riddle(0s,1000p)

> nc 124.71.21.14 11000

附件下载：task_riddle_iufJfbv.7z

<br/>

#### spec(1s,1000p)

> nc 139.159.190.149 11001

附件下载：task_spec_MEDUnEc.7z

<br/>

#### aes_baby(20s,512p)

> nc 139.159.190.149 10000

附件下载：task_aes_S8QRb7f.7z

<br/>

#### conv(2s,952p)

> nc 139.159.190.149 10001

附件下载：task_conv_EkZvwhe.7z

<br/>

#### hash_baby(6s,800p)

> nc 139.159.190.149 10002

附件下载：task_hash_1aFiBHH.7z

<br/>

#### mpi(9s,714p)

附件下载：task_mpi_P8WJIgB.7z

<br/>

#### omp(4s,869p)

附件下载：task_omp.7z

<br/>

#### sci(0s,1000p)

> nc 139.159.190.149 10003

附件下载：task_sci_vu44PCv.7z