const https = require('https');
const axios = require('axios');
const base64 = require('base64-url');
const cipher = require('eroad-oauth2-encryption');

// 忽略签名安全性的ajax实例
const instanceAjax = axios.create({
  httpsAgent: new https.Agent({
    rejectUnauthorized: false
  })
});

// appid 常量 作为公司id可以在系统中查看
const appid = '5628278295749946';

let appidString = JSON.stringify({"appid" : appid}),
    appidBase64 = base64.encode(appidString);

instanceAjax({
    method: 'post',
    url: 'https://localhost:4431/api/oauth2/oauth2_token',
    headers: {
        'identification': appidBase64
    }
})
.then((res) => {
    // 取得token和linkid
    start(res.data.data.token, res.data.data.linkid);
})

function start(token, linkid){
    // 加密将要发送的数据
    let data = {"name": "测试数据"},
        enData = cipher.encrypt(data, token, appid);

    console.log('传入的数据')
    console.log(data)

    let linkidString = JSON.stringify({"linkid" : linkid}),
        linkidBase64 = base64.encode(linkidString);
    
    // 访问测试接口，该接口返回值是传入的data
    instanceAjax({
        method: 'post',
        url: 'https://localhost:4431/api/oauth2/decrypt_test',
        headers: {
            'identification': linkidBase64
        },
        data: enData
    })
    .then((res) => {
        // 对返回的数据进行解密
        let dedata = cipher.decrypt(res.data, token, appid)
        // dedata === data 证明解密成功
        console.log('返回的数据')
        console.log(dedata.data)
    })
}