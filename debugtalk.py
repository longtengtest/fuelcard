import os

import pymysql

DB_CONF = {
    'host': os.getenv('MYSQL_HOST'),
    'port': 3306,
    'db': os.getenv('MYSQL_DB'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PWD'),
    'charset': 'utf8',
    'autocommit': True
}


def do_sql(sql):
    connect = pymysql.connect(**DB_CONF)
    cur = connect.cursor()
    cur.execute(sql)
    return cur.fetchall()


def check_data_source_id(data_source_id):
    """验证data_source_id是否存在"""
    sql = f'SELECT dataSourceId FROM datasource WHERE dataSourceId="{data_source_id}"'
    result = do_sql(sql)
    return True if result else False


def check_card(card_number):
    """检查卡是否存在"""
    sql = f'SELECT cardNumber FROM cardInfo WHERE cardNumber="{card_number}"'
    result = do_sql(sql)
    return True if result else False  # 如果result为真(非()),返回True, 否则返回False


def del_card_if_exist(card_number):
    """存在则删除指定卡-确保为新卡"""
    if check_card(card_number):
        sql = f'DELETE FROM cardInfo WHERE cardNumber="{card_number}"'
        do_sql(sql)
        return True
    return False


def add_card_if_not_exist(card_number):
    """如果卡不存在则添加卡"""
    if not check_card(card_number):
        sql = f'INSERT INTO cardInfo (`cardNumber`) VALUES ("{card_number}")'
        do_sql(sql)
        return True
    return False


def reset_card(card_number):
    """重置卡状态"""
    if check_card(card_number):
        sql = f'UPDATE cardInfo SET cardstatus=0, userId=null WHERE cardNumber="{card_number}";'
        do_sql(sql)
        return True
    return add_card_if_not_exist(card_number)


def bind_card(card_number, user_name):
    """添加并绑定卡"""
    add_card_if_not_exist(card_number)
    sql = f'UPDATE cardInfo SET cardstatus=5010, userId=(SELECT userId FROM carduser WHERE userName="{user_name}" LIMIT 1) WHERE cardNumber="{card_number}";'
    do_sql(sql)
    return True


def reset_user(user_name):  # todo check_user
    """重置用户"""
    sql = f'UPDATE cardInfo SET cardstatus=0, userId=null WHERE userId in (SELECT userId FROM carduser WHERE userName="{user_name}");'
    do_sql(sql)
    return True


def get_balance(card_number):
    """查询数据库余额"""
    sql = f'select cardBalance from cardInfo where cardNumber="{card_number}" '
    result, = do_sql(sql) or [{}]
    balance = result.get('cardBalance', None)
    return balance


def get_recharge_details(card_number):
    """查询充值记录"""
    sql = f'SELECT cardBalance, createTime FROM rechargedetails WHERE cardNumber="{card_number}" ORDER BY createTime DESC;'
    result = do_sql(sql)
    if not result:
        return []

    return [f"充值金额:{line['cardBalance']},时间:{line['createTime']}" for line in result]


def get_consume_details(card_number):
    """查询消费记录"""
    sql = f'SELECT cardBalance, createTime FROM consumptiondetails WHERE cardNumber="{card_number}" ORDER BY createTime DESC;'
    result = do_sql(sql)
    if not result:
        return []
    return [f"消费金额:{line['cardBalance']},时间:{line['createTime']}" for line in result]


def get_user_id(user_name):
    """查询用户id"""
    sql = f'SELECT userId FROM carduser WHERE userName="{user_name}"'
    result, = do_sql(sql) or [{}]
    user_id = result.get('userId', None)
    return user_id
