import pymysql
import datetime


# 打开数据库进行连接，host：主机名或IP ； user：用户名；password：密码； database：数据库名称
class OpDB:
    def __init__(self):

        try:
            self.db = pymysql.connect(host='rm-2ze4952cmw0q50t44ho.mysql.rds.aliyuncs.com',
                                      user='huangyi',
                                      password='@hy2010410201',
                                      database='cloudcampus',
                                      port=3306,
                                      charset='utf8')
        except Exception as e:
            print("数据库连接失败：%s" % e)

    def close(self):
        self.db.close()

    # 判断手机号是否注册
    def exist_phonenumber(self, phone):
        cursor = self.db.cursor()
        sql = "SELECT phone FROM user_info1 "
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            if phone == i[0]:
                return True
        return False

    # 判断用户ID是否存在
    def exist_user(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT userId FROM user_info1 "
        cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)
        for i in data:
            # print(i)
            if int(userid) == i[0]:
                # print(i[0])
                return True
        return False

    # 查找密码
    def get_password(self, userid):
        # 使用cursor()方法创建一个游标对象 cursor
        cursor = self.db.cursor()
        # sql语句
        sql = "SELECT password FROM user_info1 where userid = %s" % userid
        # print(sql)
        # 使用execute()方法执行SQL查询
        cursor.execute(sql)
        data = cursor.fetchone()  # 获取所有数据
        # print(data)
        cursor.close()
        self.close()
        return data[0]
        # 提交数据
        # db.commit()
        # 关闭数据库连接

    def get_userid(self, phonenumber):
        # 使用cursor()方法创建一个游标对象 cursor
        cursor = self.db.cursor()
        # sql语句
        sql = "SELECT userid FROM user_info1 where phone = %s" % phonenumber
        # print(sql)
        # 使用execute()方法执行SQL查询
        cursor.execute(sql)
        data = cursor.fetchone()  # 获取所有数据
        # print(data)
        return data[0]

    # 返回除用户密码及图片外所有数据（默认用户存在）
    def get_userinfo(self, userid):
        cursor = self.db.cursor()
        # sql语句
        sql = """ SELECT  A.userId,A.password,A.phone,A.gender,A.schoolName, B.name,B.autograph 
                  FROM user_info1 A, user_info2 B 
                  WHERE A.userId = %s AND B.userId = %s""" % (userid, userid)
        # print(sql)
        # 使用execute()方法执行SQL查询
        cursor.execute(sql)
        data = cursor.fetchone()  # 获取所有数据
        cursor.close()
        self.close()
        return data

    def get_payinfo(self, userid):
        cursor = self.db.cursor()
        sql = """ SELECT  payCode,nopayCode 
                  FROM payment_info 
                  WHERE userId = %s """ % userid
        cursor.execute(sql)
        data = cursor.fetchone()  # 获取所有数据
        cursor.close()
        self.close()
        return data

    # 创建用户数据(默认为新用户)
    def create_user(self, phone, password, schoolname, gender, name, paycode):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO user_info1(phone, password, schoolName, gender) 
                VALUES (%s,%s,%s,%s)
        """
        cursor.execute(sql, (phone, password, schoolname, gender))
        userid = cursor.lastrowid

        sql = """
                        INSERT INTO user_info2(userId, name) 
                        VALUES (%s, %s)
                """
        cursor.execute(sql, (userid, name))

        sql = """
                        INSERT INTO payment_info(userId, payCode) 
                        VALUES (%s, %s)
                """
        cursor.execute(sql, (userid, paycode))
        self.commit()
        cursor.close()
        self.close()

    def commit(self):
        self.db.commit()

    # 修改密码、手机号、学校名、性别
    def change_info1(self, typename, value, userid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                UPDATE user_info1
                SET %s = '%s'
                WHERE userId=%d;
                """ % (typename, value, int(userid))
        cursor.execute(sql)
        self.commit()

    # 修改昵称，个性签名
    def change_info2(self, typename, value, userid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                UPDATE user_info2
                SET %s = '%s'
                WHERE userId=%d;
                """ % (typename, value, int(userid))
        cursor.execute(sql)
        self.commit()

    # 修改支付密码、免密
    def change_payment(self, typename, value, userid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                UPDATE payment_info
                SET %s = '%s'
                WHERE userId=%d;
                """ % (typename, int(value), int(userid))
        cursor.execute(sql)
        self.commit()

    # 获取余额
    def get_payment(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT money FROM payment_info where userid = %s" % userid
        cursor.execute(sql)
        data = cursor.fetchone()
        return data[0]

    # 修改余额（传入余额值保证至多为两位小数)
    def change_money(self, value, userid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                    UPDATE payment_info
                    SET money = %.2f
                    WHERE userId=%d;
                    """ % (float(value), int(userid))
        cursor.execute(sql)

    # 获取所有学校
    def get_school(self):
        cursor = self.db.cursor()
        sql = "SELECT schoolName FROM school_info "
        cursor.execute(sql)
        data = cursor.fetchall()
        j = ()
        for i in data:
            j = j + i
        cursor.close()
        self.close()
        return j

    # 根据学校名查询所有未完成的失物招领订单
    def get_loss(self, school):
        cursor = self.db.cursor()
        sql = "SELECT lossId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,avatar from loss_info WHERE school " \
              "= '%s' and state = 0" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        # j = ()
        # for i in data:
        #     j = j + i
        return data

    # 根据学校名查询所有未出售的二手商品
    def get_commodity(self, school):
        cursor = self.db.cursor()
        sql = "SELECT commodityId, DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'), commodityName, type, avatar " \
              "from commodity_info WHERE school = '%s' and state = 0" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        return data

    # 根据学校名查询所有未出售的二手商品
    def get_commission(self, school):
        cursor = self.db.cursor()
        sql = "SELECT commissionId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,avatar from commission_info " \
              "WHERE school = '%s' and state = 0" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        return data

    # 默认商品id正确
    # 根据用户id和商品id(代办id、失物招领id)生成收藏信息
    def create_favorite(self, userid, type_, goodid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO favorite_info(userId, type, goodId) 
                VALUES (%s,%s,%s)
        """
        cursor.execute(sql, (userid, type_, goodid))
        self.commit()
        cursor.close()
        self.close()

    # 新增交易信息
    # 创建交易记录
    def create_trade(self, typename, userid, trademoney, remarks):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                    INSERT INTO trade_info(type, userId, tradeMoney, remarks)
                    VALUES (%s,%s,%s,%s)
            """
        cursor.execute(sql, (typename, userid, trademoney, remarks))
        money = float(self.get_payment(userid))
        if typename == "充值":
            money = str(money + float(trademoney))
        else:
            money = str(money - float(trademoney))
        self.change_money(money, userid)

    # 根据用户id、商品id、收货地址生成购物订单
    def create_shopping(self, userid, address, commodity):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO shopping_info(userId, commodityId, address) 
                VALUES (%s,%s,%s)
        """
        cursor.execute(sql, (userid, commodity, address))
        orderid = cursor.lastrowid
        sql = """
                update commodity_info
                set state = 1
                where commodityId = %s
                        """ % commodity
        cursor.execute(sql)
        sql = """
                    select price,userId
                    from commodity_info
                    where commodityId = %s
                """ % commodity
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        money = self.get_payment(userid)
        if money < data[0]:
            return False
        else:
            self.create_trade("付款", userid, data[0], "二手" + str(orderid))
            self.create_trade("充值", data[1], data[0], "二手" + str(orderid))
            self.commit()
            cursor.close()
            self.close()
            return True

    # 根据用户id、代办id生成代办订单
    def create_daiban(self, userid, commissionid):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO daiban_info(userId, commissionId) 
                VALUES (%s,%s)
        """
        cursor.execute(sql, (userid, commissionid))
        sql = """
                update commission_info
                set state = 1
                where commissionId = %s
                        """ % commissionid
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 新增失物/招领订单
    def create_lossinfo(self, userid, type_, name, address, detail, school, avatar):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO loss_info(userId, type, name, address, detail, school, avatar) 
                VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (userid, type_, name, address, detail, school, avatar))
        self.commit()
        cursor.close()
        self.close()

    # 新增发布代办
    def create_commissioninfo(self, userid, school, name, detail, price):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO commission_info(userId, school, name, detail, price) 
                VALUES (%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (userid, school, name, detail, price))
        self.create_trade("付款", userid, price, "代办")
        self.create_trade("充值", "0", price, "代办")
        self.commit()
        cursor.close()
        self.close()

    # 新增发布商品
    def create_commodityinfo(self, userid, school, name, detail, price, avatar):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO commodity_info(userId, school, commodityName, detail, price, avatar) 
                VALUES (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (userid, school, name, detail, price, avatar))
        self.commit()
        cursor.close()
        self.close()

    # 根据用户id查询发布二手订单
    def get_commodity_order(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId from commodity_info WHERE userId = '%s'" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        j = ()
        for i in data:
            sql = "SELECT orderId from shopping_info WHERE commodityId = '%s'" % int(i[0])
            cursor.execute(sql)
            j = j + cursor.fetchall()
        cursor.close()
        self.close()
        k = ()
        for i in j:
            k = k + i
        return k

    # 根据用户id查询发布代办订单
    def get_commission_order(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId from commission_info WHERE userId = '%s'" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        j = ()
        for i in data:
            sql = "SELECT orderId from daiban_info WHERE commissionId = '%s'" % int(i[0])
            cursor.execute(sql)
            j = j + cursor.fetchall()
        cursor.close()
        self.close()
        k = ()
        for i in j:
            k = k + i
        return k

    # 根据用户id查询接受代办订单
    def get_commission_order1(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT orderId from daiban_info WHERE userId = '%s'" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        k = ()
        for i in data:
            k = k + i
        return k

    # 根据用户id查询接受二手商品订单
    def get_commodity_order1(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT orderId from shopping_info WHERE userId = '%s'" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        k = ()
        for i in data:
            k = k + i
        return k

    # 查询对应代办订单id的订单信息（含评价信息)
    def get_daibaninfo(self, orderid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId,userId,state,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),DATE_FORMAT(time," \
              "'%%Y-%%m-%%d %%H:%%I:%%s'),commentId from daiban_info WHERE orderId = '%s'" % orderid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        # print(data)
        if data[5] != "Null":
            sql = "SELECT detail,replay from comment_info WHERE commentId = '%s'" % data[5]
            cursor.execute(sql)
            j = cursor.fetchall()
            for i in j:
                data = data + i
        cursor.close()
        self.close()
        return data

    # 查询对应购物订单id的订单信息（含评价信息)
    def get_shoppinginfo(self, orderid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId,userId,state,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),DATE_FORMAT(time," \
              "'%%Y-%%m-%%d %%H:%%I:%%s'),commentId,address from shopping_info WHERE orderId = '%s'" % orderid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        # print(data)
        if data[5] != "Null":
            sql = "SELECT detail,replay from comment_info WHERE commentId = '%s'" % data[5]
            cursor.execute(sql)
            j = cursor.fetchall()
            for i in j:
                data = data + i
        cursor.close()
        self.close()
        return data

    # 查询对应商品id的商品信息
    def get_commodityinfo(self, commodityid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId,userId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),commodityName,school,price," \
              "avatar,detail,state,type " \
              "from commodity_info WHERE commodityId = '%s'" % commodityid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        cursor.close()
        self.close()
        return data

    # 查询对应代办id的商品信息
    def get_commissioninfo(self, commissionid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId, userId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,school,price,avatar," \
              "detail,state,type " \
              "from commission_info WHERE commissionId = '%s'" % commissionid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        cursor.close()
        self.close()
        return data

    # 查询对应失物招领id的失物招领信息
    def get_lossinfo(self, lossid):
        cursor = self.db.cursor()
        sql = """
                SELECT lossId,userId, DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,school,avatar,detail,state,type,time,address
                from loss_info WHERE lossId = '%s'
         """ % lossid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        cursor.close()
        self.close()
        return data

    # 确认完成购物订单
    def commit_shoppingorder(self, orderid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql语句
        sql = """
                update shopping_info
                set state = '已完成' , time = %s
                where orderId = %s
        """
        cursor.execute(sql, (datatime, orderid))
        self.commit()
        cursor.close()
        self.close()

    # 确认完成失物招领
    def commit_lossorder(self, lossid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql语句
        sql = """
                update loss_info
                set state = 1 , time = %s
                where lossId = %s
        """
        cursor.execute(sql, (datatime, lossid))
        self.commit()
        cursor.close()
        self.close()

    # 确认完成代办订单
    def commit_daibanorder(self, orderid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql语句
        sql = """
                update daiban_info
                set state = '已完成' , time = %s
                where orderId = %s
        """
        cursor.execute(sql, (datatime, orderid))
        sql = """
                    select commissionId,userId
                    from daiban_info
                    where orderId = %s
            """ % orderid
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]
        sql = """
                                select price,userId
                                from commission_info
                                where commissionId = %s
                        """ % data1[0]
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        self.create_trade("充值", data1[1], data[0], "代办" + str(orderid))
        self.create_trade("付款", 0, data[0], "代办" + str(orderid))
        self.commit()
        cursor.close()
        self.close()

    # 取消代办订单
    def cancel_daibanorder(self, orderid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql语句
        sql = """
                update daiban_info
                set state = '已取消' , time = %s
                where orderId = %s
        """
        cursor.execute(sql, (datatime, orderid))
        sql = """
                    select commissionId
                    from daiban_info
                    where orderId = %s
                                """ % orderid
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]
        sql = """
                    update commission_info
                    set state = 0
                    where commissionId = %s
                """ % data1[0]
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 取消购物订单
    def cancel_shoppingorder(self, orderid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql语句
        sql = """
                update shopping_info
                set state = '已取消' , time = %s
                where orderId = %s
        """
        cursor.execute(sql, (datatime, orderid))
        sql = """
                select commodityId,userId
                from shopping_info
                where orderId = %s
                        """ % orderid
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]
        sql = """
                update commodity_info
                set state = 0
                where commodityId = %s
        """ % data1[0]
        cursor.execute(sql)
        sql = """
                    select price,userId
                    from commodity_info
                    where commodityId = %s
                        """ % data1[0]
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        self.create_trade("付款", data[1], data[0], "购物退款" + str(orderid))
        self.create_trade("充值", data1[1], data[0], "购物退款" + str(orderid))
        self.commit()
        cursor.close()
        self.close()

    # 发布评价
    def create_comment(self, detail, typename, id_):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                        INSERT INTO comment_info(detail) 
                        VALUES (%s)
                """
        cursor.execute(sql, detail)
        commentid = cursor.lastrowid
        if typename == '代办':
            sql = """
                    update daiban_info
                    set commentId = %s
                    where orderId = %s
            """
            cursor.execute(sql, (commentid, id_))
        else:
            sql = """
                    update shopping_info
                    set commentId = %s
                    where orderId = %s
            """
            cursor.execute(sql, (commentid, id_))
        self.commit()
        cursor.close()
        self.close()

    # 回复评价
    def create_comment_replay(self, replay, commentid):
        cursor = self.db.cursor()
        sql = """
                    update comment_info
                    set replay = %s
                    where commentId = %s
            """
        cursor.execute(sql, (replay, commentid))
        self.commit()
        cursor.close()
        self.close()


if __name__ == "__main__":
    A = OpDB()
    if A.exist_user("10001010"):
        C = A.get_password("10001010")
        print(C)
    #
    # B = OpDB()
    # D = B.get_userinfo("10001020")
    # print(D)

    # E = OpDB()
    # E.create_user("12345672839", "hcuihiuchaiu", "schoolname3", "男", "bxhsudu", 123456)

    # T = OpDB()
    # T.exist_phonenumber("15717217249")

    # R = OpDB()
    # R.change_info1("password", "bxhgcdy", "10001019")

    # S = OpDB()
    # S.change_payment("payCode", "111222", "10001020")

    # W = OpDB()
    # W.change_money("150", "10001020")

    # N = OpDB()
    # M = N.get_payment("10001020")
    # print(M)

    # L = OpDB()
    # P = L.get_school()
    # print(P)
    #
    # K = OpDB()
    # WW = K.get_userid('15717217249')
    # # KK = K.get_userinfo(str(WW))
    # print(WW)

    # HH = OpDB()
    # LL = HH.get_payinfo("10001020")
    # print(LL)
    #
    # Z = OpDB()
    # ZZ = Z.get_loss("中国矿业大学（北京）")
    # print(ZZ)

    # Z = OpDB()
    # ZZ = Z.get_commodity("清华大学")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commission("清华大学")
    # print(ZZ)

    # Z = OpDB()
    # Z.create_favorite("10001020", "二手", "2")
    #
    # Z = OpDB()
    # Z.create_shopping("10001020", "中国矿业学校（北京）学八", "2")

    # Z = OpDB()
    # Z.create_daiban("10001020", "4")

    # Z = OpDB()
    # Z.create_lossinfo("10001020", "失物", "饭卡", "教学楼南楼", "具体时间为今天早上到今天中午之间，仅在加血楼南楼一二三层活动过", "中国矿业大学（北京）", "nsahduuihw")

    # Z = OpDB()
    # Z.create_commissioninfo("10001020", "中国矿业大学（北京）", "取快递", "清真九号柜", "10", "xnauuwdu")

    # Z = OpDB()
    # Z.create_commodityinfo("10001020", "中国矿业大学（北京）", "书", "计算机专业大二书籍", "30", "cbhdgdv")

    # Z = OpDB()
    # ZZ = Z.get_commodity_order("10001020")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commission_order("10001020")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commission_order1("10001020")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commodity_order1("10001020")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_daibaninfo("2")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_shoppinginfo("3")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commodityinfo("21")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commissioninfo("21")
    # print(ZZ)
    #
    Z = OpDB()
    ZZ = Z.get_lossinfo("22")
    print(ZZ)

    # Z = OpDB()
    # Z.create_trade("充值", "10001020", "100", "支付宝")

    # Z = OpDB()
    # Z.commit_daibanorder("6")

    # Z = OpDB()
    # Z.cancel_shoppingorder("37")

    # Z = OpDB()
    # Z.create_comment_replay("3333", "3")
