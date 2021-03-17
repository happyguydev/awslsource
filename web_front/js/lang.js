var arrLang = {
    "en": {
        "INDEX": "Home",
        "DOWNLOAD": "Download",
        "HELP": "Help",
        "PERSONAL":"Personal",
        "READ MORE":"READ MORE",
        "COMPANY PROFILE":"COMPANY PROFILE",
        "company profile":"Company Profile",
        "CONTACT US":"CONTACT US",
        "COMPANY":"Zhuhai Hongye Technology Development Co., Ltd",
        "CUSTOMER":"customer service:",
        "PHONE":"phone:",
        "EMAIL":"email:",
        "WEBSITE":"website:",
        "Y-C-L":"Your current location",
        "L-R":"Login & Register",
        "REGISTER":"No account? To register",
        "ACCOUNT":"Account:",
        "ACCOUNT TEXT":"please input Account",
        "PASSWORD":"Password:",
        "PASSWORD PWD":"please input Password",
        "SIGN IN":"Sign in",
        "PASSWORD1":"Old Password:",
        "PASSWORD1 PWD":"please input Old Password",
        "PASSWORD2":"New Password:",
        "PASSWORD2 PWD":"please input New Password",
        "PASSWORD3":"Confirm New Password:",
        "PASSWORD3 PWD":"please input Confirm New Password",
        "REGISTER BTN":"register",
        "LOGIN":"Already have an account? To log in",
        "PUBLISH TIME":"publish time:",
        "AUTHOR":"author:",
        "CONFIRM PASSWORD":"Confirm Password:",
        "PASSWORD0 PWD":"please input Confirm Password:",
        "EMAIL1":"Email:",
        "RECHARGE RECORD":"Recharge record",
        "MEMBER RECHARGE":"Member recharge",
        "MODIFY PASSWORD":"Modify password",
        "MODIFY EMAIL":"Modify email",
        "YUAN":"Yuan",
        "DAY":"day",
        "IP_COUNT":"Number of IP calls per day:",
        "PAYABLE":"Amount payable:",
        "JUMP-TO-ALIPAY":"Jump to Alipay",
        "SIGN OUT":"sign out",
        "FUNCTION":"function:",
        "START TIME":"start time",
        "END TIME":"end time",
        "PAYMENT METHOD":"payment method",
        "ALIPAY":"Alipay",
        "WECHAT":"WeChat",
        "PAYPAL":"Paypal",
        "ORDER STATUS":"order status",
        "UNPAID":"Unpaid",
        "PAID":"Paid",
        "ORDER NUMBER":"order number",
        "SEARCH":"search",
        "AMOUNT":"amount",
        "OPERATION TIME":"operation time",
        "TRADE NUMBER":"trade number",
        "EMAIL TEXT":"please input Email",
        "SAVE":"save",
        "LINKS":"Links",
        "BAIDU STATISTICS":"Baidu statistics",
        "GOOGLE STATISTICS":"Google statistics",
        "WEBSITE STATISTICS":"Website statistics",
        "LOVE STATION KIT":"Love Station Kit",
        "GOOGLE KEYWORD MINING":"Google keyword mining",
        "ALEXA INTERNATIONAL RANKINGS":"Alexa international rankings",
        "ALEXA CHINA RANKINGS":"Alexa China rankings",
        "IP_ALL":"Total IP",
    },
    "zh": {
        "INDEX": "首页",
        "DOWNLOAD": "下载中心",
        "HELP": "帮助中心",
        "PERSONAL":"个人中心",
        "READ MORE":"阅读全文",
        "COMPANY PROFILE":"公司简介",
        "company profile":"公司简介",
        "CONTACT US":"联系我们",
        "COMPANY":"珠海红叶科技发展有限公司",
        "CUSTOMER":"客服：",
        "PHONE":"电话：",
        "EMAIL":"邮箱：",
        "WEBSITE":"网址：",
        "Y-C-L":"您当前所在位置",
        "L-R":"登录注册",
        "REGISTER":"没有账号？去注册",
        "ACCOUNT":"账号：",
        "ACCOUNT TEXT":"请输入账号",
        "PASSWORD":"密码：",
        "PASSWORD PWD":"请输入密码",
        "SIGN IN":"登录",
        "PASSWORD1":"原密码：",
        "PASSWORD1 PWD":"请输入原密码",
        "PASSWORD2":"新密码：",
        "PASSWORD2 PWD":"请输入新密码",
        "PASSWORD3":"确认新密码：",
        "PASSWORD3 PWD":"请输入确认新密码",
        "REGISTER BTN":"注册",
        "LOGIN":"已有账号？去登录",
        "PUBLISH TIME":"发布时间：",
        "AUTHOR":"作者：",
        "CONFIRM PASSWORD":"确认密码：",
        "PASSWORD0 PWD":"请输入确认密码",
        "EMAIL1":"邮箱：",
        "RECHARGE RECORD":"充值记录",
        "MEMBER RECHARGE":"会员充值",
        "MODIFY PASSWORD":"修改密码",
        "MODIFY EMAIL":"修改邮箱",
        "YUAN":"元",
        "DAY":"天",
        "IP_COUNT":"每天可以调用IP个数：",
        "PAYABLE":"应支付金额：",
        "JUMP-TO-ALIPAY":"跳转支付宝",
        "SIGN OUT":"退出",
        "FUNCTION":"功能：",
        "START TIME":"开始时间",
        "END TIME":"结束时间",
        "PAYMENT METHOD":"支付方式",
        "ALIPAY":"支付宝",
        "WECHAT":"微信",
        "PAYPAL":"Paypal",
        "ORDER STATUS":"订单状态",
        "UNPAID":"未支付",
        "PAID":"已支付",
        "ORDER NUMBER":"订单号",
        "SEARCH":"查询",
        "AMOUNT":"金额",
        "OPERATION TIME":"操作时间",
        "TRADE NUMBER":"交易单号",
        "EMAIL TEXT":"请输入邮箱",
        "SAVE":"保存",
        "LINKS":"友情链接",
        "BAIDU STATISTICS":"百度统计",
        "GOOGLE STATISTICS":"谷歌统计",
        "WEBSITE STATISTICS":"网站统计",
        "LOVE STATION KIT":"爱站工具包",
        "GOOGLE KEYWORD MINING":"Google关键字挖掘",
        "ALEXA INTERNATIONAL RANKINGS":"Alexa国际排名",
        "ALEXA CHINA RANKINGS":"Alexa中国排名",
        "IP_ALL":"IP总数",
    }
};

// The default language is English
var lang = "en";
// Check for localStorage support
if('localStorage' in window){
    var lang = localStorage.getItem('lang') || navigator.language.slice(0, 2);
    if (!Object.keys(arrLang).includes(lang)) lang = 'en';
}

$(document).ready(function() {
    $(".lang").each(function(index, element) {
        $(this).text(arrLang[lang][$(this).attr("key")]);
        if($(this)[0].tagName=='INPUT'){
           console.log($(this).attr("type"));
           if ($(this).attr("type")=='text'||$(this).attr("type")=='password'){
               $(this).attr("placeholder",arrLang[lang][$(this).attr("key")])
           }
           if ($(this).attr("type")=='button'){
               $(this).attr("value",arrLang[lang][$(this).attr("key")])
           }
        }
    });
});

// get/set the selected language
$(".translate").click(function() {
    var lang = $(this).attr("id");

    // update localStorage key
    if('localStorage' in window){
        localStorage.setItem('lang', lang);
        console.log( localStorage.getItem('lang') );
    }

    $(".lang").each(function(index, element) {
        $(this).text(arrLang[lang][$(this).attr("key")]);
    });
});