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

    def rollback(self):
        self.db.rollback()

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
        sql = """ SELECT  A.userId,A.password,A.phone,A.gender,A.schoolName, B.name,B.autograph,B.avatar 
                  FROM user_info1 A, user_info2 B 
                  WHERE A.userId = %s AND B.userId = %s""" % (userid, userid)
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
    def create_user(self, phone, password, schoolname, gender, name, paycode, avatar):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO user_info1(phone, password, schoolName, gender) 
                VALUES (%s,%s,%s,%s)
        """
        cursor.execute(sql, (phone, password, schoolname, gender))
        userid = cursor.lastrowid

        sql = """
                        INSERT INTO user_info2(userId, name, avatar) 
                        VALUES (%s, %s, %s)
                """
        cursor.execute(sql, (userid, name, avatar))

        sql = """
                        INSERT INTO payment_info(userId, payCode) 
                        VALUES (%s, %s)
                """
        cursor.execute(sql, (userid, paycode))
        self.commit()
        cursor.close()
        self.close()
        return userid

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

    # 修改昵称，个性签名, 头像
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
              "= '%s' and state = 0 order by date desc" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        return data

    # 根据学校名查询所有未出售的二手商品
    def get_commodity(self, school):
        cursor = self.db.cursor()
        sql = "SELECT commodityId, DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'), commodityName, type, avatar " \
              "from commodity_info WHERE school = '%s' and state = 0 order by date desc" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        return data

    # 根据学校名查询所有未接取的代办
    def get_commission(self, school):
        cursor = self.db.cursor()
        sql = "SELECT commissionId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,avatar from commission_info " \
              "WHERE school = '%s' and state = 0 order by date desc" % school
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        self.close()
        return data

    # 默认商品id正确
    # 根据用户id和商品id(代办id、失物招领id)生成收藏信息
    def create_favorite(self, userid, type_, goodid, avatar):
        cursor = self.db.cursor()
        # sql语句
        sql = """
                INSERT INTO favorite_info(userId, type, goodId, avatar) 
                VALUES (%s,%s,%s,%s)
        """
        cursor.execute(sql, (userid, type_, goodid, avatar))
        self.commit()
        cursor.close()
        self.close()

    # 获取收藏信息
    def get_favorite(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT type, goodId  from " \
              "favorite_info WHERE userId = '%s' " % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        data1 = ()
        for i in data:
            if i[0] == "二手":
                sql = "SELECT commodityId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),commodityName,type,avatar  from " \
                       "commodity_info WHERE commodityId = '%s' " % i[1]
                cursor.execute(sql)
                data2 = cursor.fetchall()
            elif i[0] == "代办":
                sql = "SELECT commissionId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,avatar  from " \
                      "commission_info WHERE commissionId = '%s' " % i[1]
                cursor.execute(sql)
                data2 = cursor.fetchall()
            else:
                sql = "SELECT lossId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,avatar from loss_info WHERE " \
                        "lossId = '%s' " % i[1]
                cursor.execute(sql)
                data2 = cursor.fetchall()
            data1 = data1 + data2
        return data1

    # 删除收藏信息
    def delete_favorite(self, userid,  goodid, type):
        cursor = self.db.cursor()
        sql = "delete from favorite_info WHERE userId = '%s' and goodId = '%s' and type = '%s'" % (userid, goodid, type)
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 判定是否收藏
    def is_favorite(self, userid, goodid, type):
        cursor = self.db.cursor()
        sql = "SELECT type  from " \
              "favorite_info WHERE userId = '%s' and goodId = '%s' and type = '%s'" % (userid, goodid, type)
        cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)
        for i in data:
            if i[0] == type:
                return True
        return False

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
                            select state from commodity_info where commodityId = %s
                      """
        cursor.execute(sql, commodity)
        state = cursor.fetchall()
        state = state[0]
        if state[0] == 0:
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
                return 1
            else:
                self.create_trade("付款", userid, data[0], "二手" + str(orderid))
                self.create_trade("充值", data[1], data[0], "二手" + str(orderid))
                self.commit()
                cursor.close()
                self.close()
                return 0
        else:
            return 2

    # 根据用户id、代办id生成代办订单
    def create_daiban(self, userid, commissionid):
        cursor = self.db.cursor()
        sql = """
                    select state from commission_info where commissionId = %s
              """
        cursor.execute(sql, commissionid)
        data = cursor.fetchall()
        data = data[0]
        if data[0] == 0:
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
            return True
        else:
            return False

    # 新增失物/招领订单
    def create_lossinfo(self, userid, type_, name, address, detail, school, avatar):
        cursor = self.db.cursor()

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

    # 根据ID查询所有的失物招领订单
    def get_loss_order(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT lossId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,state,avatar from loss_info WHERE " \
              "userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    # 根据用户id查询发布的商品
    def get_commodity_(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),commodityName,type,state,avatar  from " \
              "commodity_info WHERE userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    # 根据用户id查询发布的代办
    def get_commission_(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,state,avatar  from " \
              "commission_info WHERE userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    # 根据用户id查询发布二手订单
    def get_commodity_order(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId from commodity_info WHERE userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        j = ()
        for i in data:
            sql = "SELECT commodityId, orderId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),state from " \
                  "shopping_info WHERE commodityId = '%s'" % int(i[0])
            cursor.execute(sql)
            j = j + cursor.fetchall()
        k = ()
        for i in j:
            sql = "SELECT commodityName,type,avatar from " \
                  "commodity_info WHERE commodityId = '%s'" % int(i[0])
            cursor.execute(sql)
            l = cursor.fetchall()
            l = i + l[0]
            k = k + ((l),)
        return k

    # 根据用户id查询发布代办订单
    def get_commission_order(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId from commission_info WHERE userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        j = ()
        for i in data:
            sql = "SELECT commissionId, orderId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),state from daiban_info " \
                  "WHERE commissionId = '%s'" % int(i[0])
            cursor.execute(sql)
            # print(cursor.fetchall())
            j = j + cursor.fetchall()
        k = ()
        for i in j:
            sql = "SELECT name,type, avatar from " \
                  "commission_info WHERE commissionId = '%s'" % int(i[0])
            cursor.execute(sql)
            l = cursor.fetchall()
            l = i + l[0]
            k = k + ((l),)
        return k

    # 根据用户id查询接受代办订单
    def get_commission_order1(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId, orderId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),state from daiban_info WHERE " \
              "userId = '%s'order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        k = ()
        for i in data:
            sql = "SELECT name,type,avatar from " \
                  "commission_info WHERE commissionId = '%s'" % int(i[0])
            cursor.execute(sql)
            l = cursor.fetchall()
            l = i + l[0]
            k = k + ((l),)
        return k

    # 根据用户id查询接受二手商品订单
    def get_commodity_order1(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT commodityId, orderId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),state from shopping_info WHERE " \
              "userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        k = ()
        for i in data:
            sql = "SELECT commodityName,type,avatar from " \
                  "commodity_info WHERE commodityId = '%s'" % int(i[0])
            cursor.execute(sql)
            l = cursor.fetchall()
            l = i + l[0]
            k = k + ((l),)
        return k

    # 查询对应代办订单id的订单信息（含评价信息)
    def get_daibaninfo(self, orderid):
        cursor = self.db.cursor()
        sql = "SELECT commissionId,userId,state,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),DATE_FORMAT(time," \
              "'%%Y-%%m-%%d %%H:%%I:%%s'),commentId from daiban_info WHERE orderId = '%s'" % orderid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]

        sql = "SELECT userId,name,price from commission_info WHERE commissionId = '%s'" % data[0]
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]

        sql = "SELECT phone from user_info1 WHERE userId = '%s'" % data1[0]
        cursor.execute(sql)
        data2 = cursor.fetchall()
        data2 = data2[0]

        sql = "SELECT name from user_info2 WHERE userId = '%s'" % data1[0]
        cursor.execute(sql)
        data3 = cursor.fetchall()
        data3 = data3[0]

        sql = "SELECT phone from user_info1 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data4 = cursor.fetchall()
        data4 = data4[0]

        sql = "SELECT name from user_info2 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data5 = cursor.fetchall()
        data5 = data5[0]

        data = data + data1 + data2 + data3 + data4 + data5

        return data

    # 查询评价信息
    def get_commentinfo(self, commentid):
        cursor = self.db.cursor()
        sql = "SELECT detail from comment_info WHERE commentId = '%s'" % commentid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
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
        print(data)
        data = data[0]
        sql = "SELECT userId,commodityName,price from commodity_info WHERE commodityId = '%s'" % data[0]
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]

        sql = "SELECT phone from user_info1 WHERE userId = '%s'" % data1[0]
        cursor.execute(sql)
        data2 = cursor.fetchall()
        data2 = data2[0]

        sql = "SELECT name from user_info2 WHERE userId = '%s'" % data1[0]
        cursor.execute(sql)
        data3 = cursor.fetchall()
        data3 = data3[0]

        sql = "SELECT phone from user_info1 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data4 = cursor.fetchall()
        data4 = data4[0]

        sql = "SELECT name from user_info2 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data5 = cursor.fetchall()
        data5 = data5[0]

        data = data + data1 + data2 + data3 + data4 + data5

        return data

    # 查询失物招领订单的详细信息
    def get_lossorder(self, lossid):
        cursor = self.db.cursor()
        sql = """
                SELECT lossId,userId, DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,state,time
                from loss_info WHERE lossId = '%s'
         """ % lossid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]

        sql = "SELECT phone from user_info1 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data2 = cursor.fetchall()
        data2 = data2[0]

        sql = "SELECT name from user_info2 WHERE userId = '%s'" % data[1]
        cursor.execute(sql)
        data3 = cursor.fetchall()
        data3 = data3[0]

        data = data + data2 + data3
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

    # 取消购物订单(退货)
    def cancel_shoppingorder(self, orderid):
        cursor = self.db.cursor()
        datatime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    # 删除失物招领
    def delete_loss(self, goodid):
        cursor = self.db.cursor()
        sql = "delete from loss_info WHERE lossId = '%s' " % goodid
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 删除商品
    def delete_commodity(self, goodid):
        cursor = self.db.cursor()
        sql = "delete from commodity_info WHERE commodityId = '%s' " % goodid
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 删除代办
    def delete_commission(self, goodid):
        cursor = self.db.cursor()
        sql = "delete from commission_info WHERE commissionId = '%s' " % goodid
        cursor.execute(sql)
        self.commit()
        cursor.close()
        self.close()

    # 发布评价
    def create_comment(self, detail, typename, id_):
        cursor = self.db.cursor()

        # sql语句
        sql = """
                        INSERT ignore INTO comment_info(detail) 
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

    # 查询所有的交易记录
    def get_trade(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT type,tradeMoney, DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'), remarks from trade_info WHERE " \
              "userId = '%s' order by date desc" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    # 查询聊天信息
    def get_user(self, userid):
        cursor = self.db.cursor()
        sql = "SELECT userId,name, avatar from user_info2 WHERE userId = '%s'" % userid
        cursor.execute(sql)
        data = cursor.fetchall()
        data = data[0]
        cursor.close()
        self.close()
        return data

    # 根据学校查询最新发布
    def get_new_(self, name):
        cursor = self.db.cursor()
        sql = """SELECT commissionId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,state,avatar,
                userId,price,detail ,school
                from commission_info
                where  state = 0 AND school = '%s' 
                order by date DESC""" % name
        cursor.execute(sql)
        data1 = cursor.fetchall()
        data1 = data1[0]
        print(data1)
        sql = """SELECT commodityId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),commodityName,type,state,avatar,
                userId,price,detail ,school
                from commodity_info
                where  state = 0 AND school = '%s' 
                order by date DESC""" % name
        cursor.execute(sql)
        data2 = cursor.fetchall()
        data2 = data2[0]
        print(data2)
        sql = """SELECT lossId,DATE_FORMAT(date,'%%Y-%%m-%%d %%H:%%I:%%s'),name,type,state,avatar,
                        userId,address,detail ,school
                        from loss_info
                        where  state = 0 AND school = '%s' 
                        order by date DESC""" % name
        cursor.execute(sql)
        data3 = cursor.fetchall()
        data3 = data3[0]
        print(data3)
        data = ()
        data = data + (( data1 ),)+ ((data2),) + ((data3),)
        cursor.close()
        self.close()
        print(data)
        return data


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
    # ZZ = Z.get_loss_order("10001020")
    # print(ZZ)
    # ZZ = Z.get_commodity_("10001020")
    # print(ZZ)
    # ZZ = Z.get_commodity_order("10001020")
    # print(ZZ)
    # ZZ = Z.get_commission_order("10001020")
    # print(ZZ)

    # Z = OpDB()
    # ZZ = Z.get_commodity_order("10001020")
    # print(ZZ)
    #
    # Z = OpDB()
    # ZZ = Z.get_commission_order("10001020")
    # print(ZZ)
    # #
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
    # Z = OpDB()
    # ZZ = Z.get_lossinfo("22")
    # print(ZZ)

    # Z = OpDB()
    # Z.create_trade("充值", "10001020", "100", "支付宝")

    # Z = OpDB()
    # Z.commit_daibanorder("6")

    # Z = OpDB()
    # Z.cancel_shoppingorder("37")

    # Z = OpDB()
    # Z.create_comment_replay("3333", "3")

    # Z = OpDB()
    # zz = Z.is_favorite("10001020", "22", "失物")
    # print(zz)
    #
    # Z = OpDB()
    # zz = Z.get_favorite("10001020")
    # print(zz)

    Z = OpDB()
    zz = Z.get_new_("中国矿业大学（北京）")
    print(zz)
    print(zz[1])
