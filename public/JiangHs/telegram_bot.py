import configparser
from pyrogram import Client, filters, emoji
from mysql import UsingMysql
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import logging.handlers
import tornado.web
import tornado.ioloop
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import json
import tqdm

define('port', default=8044, type=int)
# 账号日志
config = configparser.ConfigParser()  # 类实例化
zion_logger = logging.getLogger("JianHs-zion")
zion_logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(filename='zion.log', when='M', backupCount=10, encoding='utf-8')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
zion_logger.addHandler(handler)
# bot日志
bot_logger = logging.getLogger("JianHs-bot")
bot_logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(filename='bot.log', when='M', backupCount=10, encoding='utf-8')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
bot_logger.addHandler(handler)
# 配置文件
config_path = "config.ini"
config.read(config_path, encoding="UTF-8")
# 日志等级
logging.basicConfig(level=logging.INFO)
# 脚本配置
zy_group_id = config.get('pyrogram', 'zy_group_id')
my_group_id = config.get('pyrogram', 'my_group_id')
me_id = config.get('pyrogram', 'me_id')
no_group_title = config.get('pyrogram', 'no_group_title')
group_url = config.get('pyrogram', 'group_url')
bot_app = Client(
    "Douyinnn_bot",
    bot_token=config.get('pyrogram', 'bot_token'),
    # bot_token='5111025743:AAH-pAHXppygEAdVq_ugk9g7LoEKkrcdlyw',
)
zion_app = Client(
    "Zion2",
    api_id=config.get('pyrogram', "api_id"),
    api_hash=config.get('pyrogram', 'api_hash'),
    proxy=dict(
        hostname="127.0.0.1",
        port=1080,
    )
)


def select_one(cursor):
    cursor.execute("select * from video")
    data = cursor.fetchone()
    # print("-- 单条记录: {0} ".format(data))


def fetch_user(id):
    with UsingMysql(log_time=False) as um:
        sql = 'select * from user where id = %d' % id
        um.cursor.execute(sql)
        data_list = um.cursor.fetchall()
        # print('-- 总数: %d' % len(data_list))
        if len(data_list) != 0:
            return True
        else:
            return False
        # return data_list


def fetch_point(id):
    with UsingMysql(log_time=False) as um:
        sql = 'select * from user where id = %d' % id
        um.cursor.execute(sql)
        data_list = um.cursor.fetchall()
        # print('-- 总数: %d' % len(data_list))
        if len(data_list) != 0:
            return data_list[0]['point']
        else:
            return 0
        # return data_list


def fetch_video(id):
    with UsingMysql(log_time=False) as um:
        sql = 'select * from video where file_id = "%s"' % id
        um.cursor.execute(sql)
        data_list = um.cursor.fetchall()
        # print('-- 总数: %d' % len(data_list))
        if len(data_list) != 0:
            return True
        else:
            return False
        # return data_list


def update_point(id, point):
    with UsingMysql(log_time=False) as um:
        sql = "UPDATE user SET point = %d WHERE id = %d" % (point, id)
        um.cursor.execute(sql)
        # 查看结果
        # select_one(um.cursor)


# 查找
# def fetch_list():
#     with UsingMysql(log_time=True) as um:
#         # 查找id 大于800的记录
#         data_list = fetch_list_by_filter(um.cursor, 0)


# 新增单条记录
def create_one_video(i):
    with UsingMysql(log_time=False) as um:
        sql = "insert into video(file_id,file_unique_id,file_name,width,height,duration,mime_type,file_size," \
              "supports_streaming,thumbs_file_id,thumbs_file_unique_id,thumbs_width,thumbs_height," \
              "thumbs_file_size,type,from_user_id,message_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
              ", %s, %s, %s, %s)"
        file_id = i['video']['file_id']
        file_unique_id = i['video']['file_unique_id']
        file_name = i['video']['file_name']
        width = i['video']['width']
        height = i['video']['height']
        duration = i['video']['duration']
        mime_type = i['video']['mime_type']
        file_size = i['video']['file_size']
        supports_streaming = i['video']['supports_streaming']
        thumbs_file_id = i['video']['thumbs'][0]['file_id']
        thumbs_file_unique_id = i['video']['thumbs'][0]['file_unique_id']
        thumbs_width = i['video']['thumbs'][0]['width']
        thumbs_height = i['video']['thumbs'][0]['height']
        thumbs_file_size = i['video']['thumbs'][0]['file_size']
        type = i['media']
        from_user_id = i['from_user']['id']
        message_id = i['message_id']
        params = (file_id, file_unique_id, file_name, width, height, duration, mime_type, file_size, supports_streaming,
                  thumbs_file_id, thumbs_file_unique_id, thumbs_width, thumbs_height, thumbs_file_size, type,
                  from_user_id, message_id)
        um.cursor.execute(sql, params)
        # 查看结果
        select_one(um.cursor)


def creat_one_user(i):
    with UsingMysql(log_time=False) as um:
        sql = "insert into user(id, first_name, last_name, last_online_date, next_offline_date, username, language_code, " \
              "dc_id, phone_number,point) values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        id = i['id']
        first_name = i['first_name']
        if i['last_name']:
            last_name = i['last_name']
        else:
            last_name = "null"
        if i['last_online_date']:
            last_online_date = i['last_online_date']
        else:
            last_online_date = "null"
        if i['next_offline_date']:
            next_offline_date = i['next_offline_date']
        else:
            next_offline_date = "null"
        if i['username']:
            username = i['username']
        else:
            username = "null"
        if i['language_code']:
            language_code = i['language_code']
        else:
            language_code = "null"
        if i['dc_id']:
            dc_id = i['dc_id']
        else:
            dc_id = "null"
        if i['phone_number']:
            phone_number = i['phone_number']
        else:
            phone_number = "null"
        point = 10
        params = (id, first_name, last_name, last_online_date, next_offline_date, username, language_code, dc_id,
                  phone_number, point)
        um.cursor.execute(sql, params)
        # 查看结果
        select_one(um.cursor)


def rand_get_video():
    with UsingMysql(log_time=False) as um:
        # sql = 'SELECT * FROM `video` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(file_id) FROM `video`)-(SELECT MIN(file_id) ' \
        #       'FROM `video`))+(SELECT MIN(file_id) FROM `video`)) AS file_id) AS t2 WHERE t1.file_id >= t2.file_id ORDER BY t1.file_id LIMIT 1;'
        sql = "SELECT file_id FROM video ORDER BY RAND() limit 1;"
        um.cursor.execute(sql)
        data_list = um.cursor.fetchall()
        return data_list[0]['file_id']
        # print('-- 总数: %d' % len(data_list))
        # print('-- 数据: {0}'.format(data_list[0]['file_id']))


def use_key(key):
    with UsingMysql(log_time=False) as um:
        sql = "UPDATE keyt SET `use` = %d WHERE `key` = '%s'" % (1, key)
        um.cursor.execute(sql)


def validate_key(key):
    with UsingMysql(log_time=False) as um:
        sql = 'select * from keyt where `key` = "%s"' % key
        um.cursor.execute(sql)
        data_list = um.cursor.fetchall()
        # print('-- 总数: %d' % len(data_list))
        if len(data_list) != 0:
            if data_list[0]['use'] == 0:
                return data_list[0]['point']
            else:
                return 1
        else:
            return 0
        # return data_list


#         0:卡密不存在1:卡密失效 other:充值成功的面额


def forward_messages():
    with zion_app:
        for l in config.sections():
            try:
                if l == "pyrogram":
                    continue
                if config.get(l, "title") in no_group_title or l[0] != "-":
                    continue
                if config.get(l, 'limit') == config.get(l, 'count'):
                    continue
                zy_group_id = l
                chat = zion_app.get_chat(zy_group_id)
                config.set(zy_group_id, "title", chat['title'])
                limit = int(config.get(zy_group_id, "limit"))
                count = zion_app.get_history_count(zy_group_id)
                config.set(zy_group_id, 'count', str(count))
                for j in range(limit, int(count), 100):
                    logging.info(l + ":" + "Forward messages:(" + str(j) + "/" + str(count) + ")")
                    history = zion_app.get_history(zy_group_id, offset=j, reverse=True)
                    for i in tqdm(history):
                        if 'video' in i['media']:
                            zion_app.forward_messages(my_group_id, zy_group_id, i['message_id'],
                                                      disable_notification=True)
                        else:
                            continue
                    config.set(zy_group_id, 'limit', str(j))
                    config.write(open(config_path, "w+"))
                    zion_logger.info(l + ": " + str(limit) + " over")
            except:
                zion_logger.debug(l + "have a error: except")
                continue
        zion_logger.info("Forward messages over!")


def get_config():
    with zion_app:
        for dialog in tqdm(zion_app.iter_dialogs()):
            id = str(dialog['chat']['id'])
            title = str(dialog['chat']['title'])
            limit = "1"
            if id not in config.sections():
                config.add_section(id)
                config.set(id, 'limit', limit)
            config.set(id, 'title', title)
            config.set(id, 'count', str(zion_app.get_history_count(dialog['chat']['id'])))
            config.set(id, 'username', str(dialog['chat']['username']))
            config.set(id, 'first_name', str(dialog['chat']['first_name']))
            config.write(open(config_path, "w+"))


def fetch_list_by_filter(cursor, pk):
    sql = 'select * from video where width > %d' % pk
    cursor.execute(sql)
    data_list = cursor.fetchall()
    print('-- 总数: %d' % len(data_list))
    return data_list


# 查找
def fetch_list():
    with UsingMysql(log_time=True) as um:
        # 查找id 大于800的记录
        data_list = fetch_list_by_filter(um.cursor, 0)


# 新增单条记录
def create_one(i):
    with UsingMysql(log_time=False) as um:
        sql = "insert into video(file_id,file_unique_id,file_name,width,height,duration,mime_type,file_size," \
              "supports_streaming,thumbs_file_id,thumbs_file_unique_id,thumbs_width,thumbs_height," \
              "thumbs_file_size,type,from_user_id,message_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
              ", %s, %s, %s, %s)"
        file_id = i['video']['file_id']
        file_unique_id = i['video']['file_unique_id']
        file_name = i['video']['file_name']
        width = i['video']['width']
        height = i['video']['height']
        duration = i['video']['duration']
        mime_type = i['video']['mime_type']
        file_size = i['video']['file_size']
        supports_streaming = i['video']['supports_streaming']
        thumbs_file_id = i['video']['thumbs'][0]['file_id']
        thumbs_file_unique_id = i['video']['thumbs'][0]['file_unique_id']
        thumbs_width = i['video']['thumbs'][0]['width']
        thumbs_height = i['video']['thumbs'][0]['height']
        thumbs_file_size = i['video']['thumbs'][0]['file_size']
        type = i['media']
        from_user_id = i['from_user']['id']
        message_id = i['message_id']
        params = (file_id, file_unique_id, file_name, width, height, duration, mime_type, file_size, supports_streaming,
                  thumbs_file_id, thumbs_file_unique_id, thumbs_width, thumbs_height, thumbs_file_size, type,
                  from_user_id, message_id)
        um.cursor.execute(sql, params)
        # 查看结果
        select_one(um.cursor)


@bot_app.on_message(filters.group)
def get_video(client, message):
    # message.reply(message.text)
    # print(message)
    user_id = message['from_user']['id']
    if message['media'] == "video":
        try:
            create_one_video(message)
            message.reply("上传成功,成功获得1积分")
            update_point(user_id, fetch_point(user_id) + 1)
        except:
            message.reply("您上传的视频已经有了哟，不能给您积分啦！")

    else:
        message.reply('notok')


@bot_app.on_message(filters.private)
def main(client, message):
    user_id = message['from_user']['id']
    if not fetch_user(user_id):
        creat_one_user(message['from_user'])
    if message.text == "来个视频":
        bot_app.send_cached_media(user_id, rand_get_video())
        update_point(user_id, fetch_point(user_id) - 1)
        message.reply("成功使用1积分")
    elif message.text == "我的积分":
        # update_point(user_id, 100)
        message.reply("您的剩余积分为" + str(fetch_point(user_id)))
    elif message['media'] == "video":
        try:
            create_one_video(message)
            message.reply("上传成功,成功获得1积分")
            update_point(user_id, fetch_point(user_id) + 1)
        except:
            message.reply("您上传的视频已经有了哟，不能给您积分啦！")
    elif message.text == "搜索":
        message.reply("暂未开放哦！")
    elif message.text[0] == "h" and message.text[-1] == "z":
        # try:
        if validate_key(message.text) == 0:
            message.reply("卡密不存在 如有问题请联系 https://t.me/Jiahsss")
        elif validate_key(message.text) == 1:
            message.reply("卡密失效 如有问题请联系 https://t.me/Jiahsss")
        else:
            update_point(user_id, fetch_point(user_id) + validate_key(message.text))
            message.reply("充值成功!增加" + str(validate_key(message.text)) + "积分")
            use_key(message.text)
    elif message.text == "充值":
        message.reply("https://www.jintbao.com/mall/?link=m61fdf74595627 购买后将卡密直接发送给我即可")
    # except:
    #     message.reply("充值失败！如有问题请联系 https://t.me/Jiahsss")
    else:
        bot_app.send_message(
            user_id,  # Edit this
            "欢迎来到抖阴，点击键盘上的指令开始！您可以向我发送视频上传获得积分，转发视频也可以哟！您也可以通过充值获得积分！",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["来个视频"],  # First row
                    ["搜索"],  # Second row
                    ["我的积分", "充值"],  # Third row
                ],
                resize_keyboard=False  # Make the keyboard smaller
            )
        )

        bot_app.send_message(
            user_id,  # Edit this
            "充值点此",
            reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        # InlineKeyboardButton(  # Generates a callback query when pressed
                        #     "Button",
                        #     callback_data="data"
                        # ),
                        InlineKeyboardButton(  # Opens a web URL
                            "充值网址",
                            url="https://www.jintbao.com/mall/?link=m61fdf74595627"
                        )
                    ]
                    # [  # Second row
                    #     InlineKeyboardButton(  # Opens the inline interface
                    #         "Choose chat",
                    #         switch_inline_query="pyrogram"
                    #     ),
                    #     InlineKeyboardButton(  # Opens the inline interface in the current chat
                    #         "Inline here",
                    #         switch_inline_query_current_chat="pyrogram"
                    #     )
                    # ]
                ]
            )
        )


class bot_start(tornado.web.RequestHandler):
    async def get(self):
        try:
            await bot_app.start()
            bot_logger.info("start ok")
            return_json = {"status": False, "data": None}
            self.write(json.dumps(return_json))
        except:
            bot_logger.debug("tornado: error")
            return_json = {"status": True, "data": None}
            self.write(json.dumps(return_json))


class bot_stop(tornado.web.RequestHandler):
    async def get(self):
        try:
            await bot_app.stop()
            bot_logger.info("stop ok")
            return_json = {"status": False, "data": None}
            self.write(json.dumps(return_json))
        except:
            bot_logger.debug("tornado: error")
            return_json = {"status": True, "data": None}
            self.write(json.dumps(return_json))


# class zion_start(tornado.web.RequestHandler):
#     def get(self):
#         try:
#             zion_app.run(forward_messages())
#             zion_logger.info("start ok")
#             return_json = {"status": False, "data": None}
#             self.write(json.dumps(return_json))
#         except:
#             zion_logger.debug("tornado: error")
#             return_json = {"status": True, "data": None}
#             self.write(json.dumps(return_json))
#
#
# class zion_stop(tornado.web.RequestHandler):
#     async def get(self):
#         try:
#             await zion_app.stop()
#             zion_logger.info("stop ok")
#             return_json = {"status": False, "data": None}
#             self.write(json.dumps(return_json))
#         except:
#             zion_logger.debug("tornado: error")
#             return_json = {"status": True, "data": None}
#             self.write(json.dumps(return_json))


if __name__ == "__main__":
    # 创建一个应用对象
    options.parse_command_line()
    app = tornado.web.Application([(r'/bot/start', bot_start), (r'/bot/stop', bot_stop)])
    # 绑定一个监听端口
    http_server = HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(1)
    # 启动web程序，开始监听端口的连接
    IOLoop.current().start()
