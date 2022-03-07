import logging
import configparser
from tqdm import tqdm
from pyrogram import Client, filters, emoji
from mysql import UsingMysql
import time
from flask import Flask
from gevent import pywsgi
import logging
import logging.handlers
import time

# flask框架
flaskapp = Flask(__name__)
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
zion_app = Client(
    "Zion2",
    api_id=config.get('pyrogram', "api_id"),
    api_hash=config.get('pyrogram', 'api_hash'),
    proxy=dict(
        hostname="127.0.0.1",
        port=1080,
    )
)
bot_app = Client(
    "douyinn_bot",
    bot_token="5169188658:AAGU1cBxF35c9QwxloT8WKeZOq9kXoCEVBg",
    # bot_token='5111025743:AAH-pAHXppygEAdVq_ugk9g7LoEKkrcdlyw',
    proxy=dict(
        hostname="127.0.0.1",
        port=1080,
    )
)


def forward_messages():
    with zion_app:
        try:
            zion_app.run(get_config())
        except:
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
                                time.sleep(1)
                                zion_app.forward_messages(my_group_id, zy_group_id, i['message_id'],
                                                          disable_notification=True)
                            else:
                                continue
                        config.set(zy_group_id, 'limit', str(j))
                        config.write(open(config_path, "w+"))
                        zion_logger.info(l + ": " + str(limit) + " over")
                except:
                    zion_logger.debug(l + " have a error: except")
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


def select_one(cursor):
    cursor.execute("select * from video")
    data = cursor.fetchone()
    # print("-- 单条记录: {0} ".format(data))


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


if __name__ == "__main__":
    zion_app.run(forward_messages())
