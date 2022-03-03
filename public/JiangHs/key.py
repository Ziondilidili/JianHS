import time
from mysql import UsingMysql
import base64
import random
import string


user_password = "JianHs"
salt = "zzy9007858"
seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
sa = []


def creat_key(point):
    com = 5
    off = 3
    key = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    new = base64.b64encode((user_password + salt).encode("utf-8"))
    new = new.decode("utf-8")
    if len(new) < com:
        new = new.ljust(com, "a")
    key = key.join(new[off: com + off])
    with UsingMysql(log_time=True) as um:
        sql = "insert into keyt(`key`, point, `use`, creat_time) values(%s,%s,%s,%s)"
        use = 0
        creat_time = int(time.time())
        params = (key, point, use, creat_time)
        um.cursor.execute(sql, params)


if __name__ == "__main__":
    for i in range(20):
        time.sleep(0.5)
        creat_key(100)
