import tornado.escape
import tornado.web

from wechat_sdk import WechatConf
conf = WechatConf(
    token='veronica', # 你的公众号Token
    appid='wxb6e1256edec94cba', # 你的公众号的AppID
    appsecret='575b4a50b98132fc7bbbe8168ef76b37', # 你的公众号的AppSecret
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='6aAAVnUa6xDgqRTNrHWX6leqZQnrtfzQV3yE3t0QLy9'  # 如果传入此值则必须保证同时传入 token, appid
)

from wechat_sdk import WechatBasic
wechat = WechatBasic(conf=conf)

class WX(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and echostr != 'default' \
                and wechat.check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('Not Open')