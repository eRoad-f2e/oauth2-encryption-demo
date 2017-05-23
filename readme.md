易路开放平台oauth 加解密说明
作者：易路软件前端团队，sakura,sheely

> 接口：`api/oauth2/oauth2_token`


功能：获取token和linkid

参数：`appid`

将参数填入headers中identification字段，并且对参数进行base64编码

```
const $ = require('jquery');
const base64 = require('base64-url');

// 原始参数
let appid = JSON.stringify({"appid" : "5628278295749946"});

// base64编码
let base64Appid = base64.encode(appid);

// 写入headers并发起请求
$.ajax({
    url: '/api/oauth2/oauth2_token',
    type: 'POST',
    dataType: 'json',
    headers: {
        'identification': base64Appid
    },
    success: function (data) {
        console.log(data)
    },
    error: function (data) {
        console.log(data)
    }
});
``` 
返回值：
```
{
  "code": 0,
  "msg": "OK",
  "data": {
    "token": "95c97508fbbc4c1388d4812f32b4541e",
    "linkid": "673fe871-defb-416e-a995-bf29644ecc97"
  }
}
```

> 加密数据

 **加解密模块**  [eroad-oauth2-encryption](https://www.npmjs.com/package/eroad-oauth2-encryption)

```
const cipher = require('eroad-oauth2-encryption');

// 要发送的数据
let data = {
    "code": 0,
    "msg": "OK",
    "data": {
        "name": "测试数据"
    }
};
// api/oauth2/oauth2_token接口返回值中的token
let token = '95c97508fbbc4c1388d4812f32b4541e'; 
let appid = '5628278295749946';

// 对数据进行加密
let enData = cipher.encrypt(data, token, appid);

// 要解密的数据
let rdata = {
    "summary": "c287350f8cebd36ca26b343d8f6bcaae",
    "data": "s+wrANjtWJf5vemG4zHufv+vKRzxOFI75fp6wEG7CfdNxvjzIA/L2iYpOLW9F/eYZJ/5T7SEoDwWGL+zdGugY2hVZpziTdc7hFlFzuWvlTafbgrb/JwZOX+Iw7i2IcIY"
},
// 对数据进行解密
let deData = cipher.decrypt(rdata, token, appid)
```


> 接口：`api/oauth2/decrypt_test`


功能：加解密测试接口, 返回你传入的参数

参数：
- headers中的identification填入`api/oauth2/oauth2_token`接口返回的linkid
- body中放入已经加密过的数据
```
// linkid
let linkid = JSON.stringify({"linkid" : "673fe871-defb-416e-a995-bf29644ecc97"});
let base64Linkid = base64.encode(linkid);

// 要发送的数据
let data = {
    "code": 0,
    "msg": "OK",
    "data": {
        "name": "测试数据"
    }
};
// api/oauth2/oauth2_token接口返回值中的token
let token = '95c97508fbbc4c1388d4812f32b4541e'; 
let appid = '5628278295749946';

// 对数据进行加密
let enData = cipher.encrypt(data, token, appid);

// 传入加密后数据
$.ajax({
    url: '/api/oauth2/oauth2_token',
    type: 'POST',
    dataType: 'json',
    data: enData,
    headers: {
        'identification': base64Linkid
    },
    success: function (res) {
	    // 返回的数据是加密后的，需要进行解密
        console.log(res)
        let deData = cipher.decrypt(res, token, appid)
        console.log(deData)
    },
    error: function (data) {
        console.log(data)
    }
});
```







