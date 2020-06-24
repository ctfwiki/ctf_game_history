### Writeup

大部分引用网络连接，小部分题目有详细信息为原创内容，自己整理的也会尽量附上引用链接



### 附件下载链接

文档中所有附件均为相对路径，具体文件下载请在下面分享的网盘中查找

- 百度网盘：链接：https://pan.baidu.com/s/1oxokSnY9rVd5go0QkPpVIw 提取码：5ej0
- 腾讯微云：链接：https://share.weiyun.com/5zyHn0l 密码：z6724j
- 蓝奏云：https://t1m.lanzous.com/b0aesxbif 密码:8bri

### 特殊说明

目前以下所有网盘的上传账号都没有开通会员，配置均为普通用户级别，受限较大

#### 百度网盘（非会员下载限速，单文件限制小于4G）

开通了百度网盘会员的用户，建议优先使用百度网盘下载



#### 腾讯微云（非会员上传限速，总容量较小）

由于未开会员，容量只有10G，所以大于1G的附件不会保存到微云。



#### 蓝奏云（限制文件类型和单文件大小）

由于蓝奏云限制单个文件最大为100M，经过测试连续上传大于50M单文件会有20%的文件上传失败，所以对于蓝奏网盘大于100M的附件进行了切割，切分成48M的单个文件。

切分方式是直接截取连续的字节，切分和拼接工具在filesplit.py（python3环境），或可或自行按照编号顺序将文件的字节直接拼接。切分后的文件命名方式为origin_name_[1-n].zip。

例如：

```bash
# 原文件 = file.7z = 276M

python3 filesplit.py -s /mnt/file.7z

# 经过切分后得到
file_1.7z = 48M
file_2.7z = 48M
file_3.7z = 48M
file_4.7z = 48M
file_5.7z = 48M
file_6.7z = 36.7M

# 还原文件
python3 filesplit.py -c /mnt/file.7z

# 会自动按顺序搜寻/mnt/路径下file_[1-n].7z命名方式的文件，，并自动拼接成file.7z保存到/mnt/路径下
```

为了防止切分成过多子文件，大于1G的附件不会存到蓝奏云。



### 捐赠

如有疑问或提供相关资源请联系QQ909712710（备注来源：github-ctf_game_history）

如果本仓库对您有帮助或者您愿意支持本仓库的更新，欢迎扫码捐助（捐后不退，谨慎操作）

<p>
<img src="./img/donate/wechatpay.png" width="300"  />
<img src="./img/donate/alipay.jpg" width="300" />
</p>

