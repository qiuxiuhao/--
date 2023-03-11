import pymysql


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
        sql = """ SELECT  A.userId,A.password,A.phone,A.gender,A.schoolName, B.name,B.geXin 
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
        cursor.close()
        self.close()
        return str(data[0])

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
        self.commit()
        cursor.close()
        self.close()

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


if __name__ == "__main__":
    A = OpDB()
    if A.exist_user("10001010"):
        C = A.get_password("10001010")
        print(C)

    B = OpDB()
    D = B.get_userinfo("10001000")
    print(D)

    # E = OpDB()
    # E.create_user("12345672839", "hcuihiuchaiu", "schoolname3", "男", "bxhsudu", 123456)

    T = OpDB()
    T.exist_phonenumber("15717217249")

    # R = OpDB()
    # R.change_info1("password", "bxhgcdy", "10001019")

    # S = OpDB()
    # S.change_payment("nopayCode", "1", "10001020")

    # W = OpDB()
    # W.change_money("150", "10001020")

    N = OpDB()
    M = N.get_payment("10001020")
    print(M)

    L = OpDB()
    P = L.get_school()
    print(P)

    K = OpDB()
    WW = K.get_userid('15717217249')
    # KK = K.get_userinfo(str(WW))
    print(WW)

    HH = OpDB()
    LL = HH.get_payinfo("10001020")
    print(LL)
