import pymysql
import datetime
import hashlib
import base64
import os

def gensalt():
    bytes = base64.b64encode(os.urandom(20))
    return bytes.decode("utf-8") 


class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='postforum_user',
            passwd='postforum_password',
            db='postforum')

    def howmanyreplys(self):
        query = "select count(*) from postreplys"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    def get_user(self, user_id):
        query = "select * from users where user_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,user_id)
            return  cursor.fetchone()

    def poster_id(self, post_id):
        query = "select p.user_id from posts p where p.post_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, post_id)
            return cursor.fetchone()

    def get_all_posts(self):
        query = "select u.username, p.post_id, p.post, p.created_at from posts p, users u where p.user_id=u.user_id order by p.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples

    def get_all_replys(self):
        query = "select u.username, r.reply_id, r.reply, r.created_at, r.post_id  from postreplys r, users u where r.user_id=u.user_id  order by r.created_at asc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples



    def get_user_posts(self,username):
        query = "select u.username, t.post, t.created_at from posts t,\
        users u where t.user_id=u.user_id and u.username=%s order by t.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query,(username))
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples

    def get_post(self,post_id):
        query = "select post from posts where post_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, post_id)
            return cursor.fetchone()  
            # more detals about cursor.fetchone at
            # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html

    def add_post(self,post,user_id):
        query = "insert into posts (post,user_id) values \
        (%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(query, (post,user_id))
            return self.db.commit()

    def add_reply(self,post_id,reply,user_id):
        query = "insert into postreplys (post_id,reply,user_id) values \
        (%s,%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(query, (post_id,reply,user_id))
            return self.db.commit()


    def update_post(self,post,post_id):
        query = "update posts set post=%s where post_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,(post,post_id))
            return self.db.commit()

    def delete_post(self,post_id):
        query = "delete from posts where post_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, post_id)
            return self.db.commit()

    def check_password(self,username,password):
        query = "select user_id, salt, hashed from users where username = %s;"
        with self.db.cursor() as cursor:
            cursor.execute(query,(username))
            user = cursor.fetchone()
            if user:
                user_id, salt, hashed = user
                if hashlib.sha512((salt + password).encode('utf-8')).hexdigest() == hashed:
                    return user_id
            return None

    def sign_up(self, username, password):
        retrievelastid = "select user_id from users order by user_id desc limit 1"        
        query = "insert into users (user_id,username,password,salt,hashed) values (%s,%s,%s,%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(retrievelastid)
            user_id = cursor.fetchone()[0] + 1
            salt = gensalt()
            hashed = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
            cursor.execute(query, (user_id, username, password, salt, hashed))
            return self.db.commit()


 
