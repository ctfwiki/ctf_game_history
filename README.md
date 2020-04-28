### 附件下载说明

文档中所有附件均为相对路径，具体文件下载请在下面分享的网盘中查找

- 百度网盘：链接：https://pan.baidu.com/s/1oxokSnY9rVd5go0QkPpVIw 提取码：5ej0
- 腾讯微云：链接：https://share.weiyun.com/5zyHn0l 密码：b9mag7
- 蓝奏云：https://t1m.lanzous.com/b0aesxbif 密码:8bri

#### 特殊说明

由于蓝奏云限制单个文件最大为100M，经过测试连续上传大于50M单文件会有20%的文件上传失败，所以对于蓝奏网盘大于100M的附件进行了切割，切分成48M的单个文件。

切分方式是直接截取连续的字节，切分和拼接工具在filesplit.py（python3环境），或可或自行按照编号顺序将文件的字节直接拼接。切分后的文件命名方式为origin_name_[1-n].zip。

例如：

```bash
原文件 = file.7z = 276M

python filesplit.py -s /mnt/file.7z

经过切分后得到
file_1.7z = 48M
file_2.7z = 48M
file_3.7z = 48M
file_4.7z = 48M
file_5.7z = 48M
file_6.7z = 36.7M

还原文件
python filesplit.py -c /mnt/file.7z

会自动按顺序搜寻/mnt/路径下file_[1-n].7z命名方式的文件，，并自动拼接成file.7z保存到/mnt/路径下
```

### 捐赠

如果本仓库对您有帮助或者您愿意支持本仓库的更新，欢迎扫码捐助（捐后不退，谨慎操作）

如有其他疑问或提供相关资源请联系QQ909712710（备注来源：github-ctf_game_history）

<p>
<img src="https://gitee.com/og/CDN/raw/master/blog/static/img/wechatpay.png" width="300"  />
<img src="https://gitee.com/og/CDN/raw/master/blog/static/img/alipay.jpg" width="300" />
</p>
