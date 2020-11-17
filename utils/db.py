class LongTengServer(object):
    """该项目数据库的常用业务操作封装"""
    def __init__(self, db):
        self.db = db

    def check_data_source_id(self, data_source_id):
        sql = f'SELECT dataSourceId FROM datasource WHERE dataSourceId="{data_source_id}"'
        result = self.db.query(sql)
        return True if result else False

    def del_card_if_exist(self, card_number):
        if self.check_card(card_number):
            sql = f'DELETE FROM cardInfo WHERE cardNumber="{card_number}"'
            self.db.change_db(sql)
            return True
        return False

    def check_card(self, card_number):
        sql = f'SELECT cardNumber FROM cardInfo WHERE cardNumber="{card_number}"'
        result = self.db.query(sql)
        return True if result else False  # 如果result为真(非()),返回True, 否则返回False

    def add_card_if_not_exist(self, card_number):
        if not self.check_card(card_number):
            sql = f'INSERT INTO cardInfo (`cardNumber`) VALUES ("{card_number}")'
            self.db.change_db(sql)
            return True
        return False

    def reset_card(self, card_number):
        if self.check_card(card_number):
            sql = f'UPDATE cardInfo SET cardstatus=0, userId=null WHERE cardNumber="{card_number}";'
            self.db.change_db(sql)
            return True
        return self.add_card_if_not_exist(card_number)

    def bind_card(self, card_number, user_name):
        self.add_card_if_not_exist(card_number)
        sql = f'UPDATE cardInfo SET cardstatus=5010, userId=(SELECT userId FROM carduser WHERE userName="{user_name}" LIMIT 1) WHERE cardNumber="{card_number}";'
        self.db.change_db(sql)
        return True

    def reset_user(self, user_name):  # todo check_user
        sql = f'UPDATE cardInfo SET cardstatus=0, userId=null WHERE userId in (SELECT userId FROM carduser WHERE userName="{user_name}");'
        self.db.change_db(sql)
        return True

    def get_balance(self, card_number):
        sql = f'select cardBalance from cardInfo where cardNumber="{card_number}" '
        result, = self.db.query(sql) or [{}]
        balance = result.get('cardBalance', None)
        return balance

    def get_recharge_details(self, card_number):
        sql = f'SELECT cardBalance, createTime FROM rechargedetails WHERE cardNumber="{card_number}" ORDER BY createTime DESC;'
        result = self.db.query(sql)
        if not result:
            return []

        return [f"充值金额:{line['cardBalance']},时间:{line['createTime']}" for line in result]

    def get_consume_details(self, card_number):
        sql = f'SELECT cardBalance, createTime FROM consumptiondetails WHERE cardNumber="{card_number}" ORDER BY createTime DESC;'
        result = self.db.query(sql)
        if not result:
            return []
        return [f"消费金额:{line['cardBalance']},时间:{line['createTime']}" for line in result]

    def get_user_id(self, user_name):
        sql = f'SELECT userId FROM carduser WHERE userName="{user_name}"'
        result, = self.db.query(sql) or [{}]
        user_id = result.get('userId', None)
        return user_id
