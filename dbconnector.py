import MySQLdb


def connectdb():
   return MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="$ftp$erver",  # your password
                         db="sftp")        # name of the data base

def saveuser(idtoupdate,headermail,fromuser,increment,dateofmail,isnew):
    done = 9999999;
    if(isnew):
        connection = connectdb();
        try:
            cursor = connection.cursor()
                # Create a new record
            sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
            cursor.execute(sql, (headermail, fromuser, increment, dateofmail))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            done = cursor.lastrowid

            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        finally:
            connection.close()
    else:
        connection = connectdb();
        try:
            cursor = connection.cursor()
            # Create a new record
            sql = "update is_old set nboftries = %s,time =%s where id=%s "
            cursor.execute(sql, (int(increment)+1,dateofmail, int(idtoupdate)))
            # sql = "update is_old set time = %s where id=%s "
            # cursor.execute(sql, (dateofmail, int(idtoupdate)))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            done = cursor.execute('SELECT LAST_INSERT_ID()')
            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        finally:
            connection.close()
    return done;
def checkuser(header,fromuser):
    connection = connectdb()
    try:
       # with connection.cursor() as cursor:
            # Create a new record
            # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
            # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
       # connection.commit()

            cursor = connection.cursor()
            # Read a single record
            sql = "SELECT `*` FROM `is_old` where header = %s and email = %s"
            cursor.execute(sql,(header,fromuser))
            result = cursor.fetchall()
        #    print "resulttttttt"
       #     print result
            return result
    finally:
        connection.close()
def checkuserwaiting(header,fromuser,dateofmail):
    connection = connectdb()
    try:
       # with connection.cursor() as cursor:
            # Create a new record
            # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
            # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
       # connection.commit()

            cursor = connection.cursor()
            # Read a single record
            sql = "SELECT * FROM `is_old` where header = %s and email = %s and `time` = %s"
            cursor.execute(sql,(header,fromuser,dateofmail))
            result = cursor.fetchall()
            return result
        #    print "resulttttttt"
       #     print result
    finally:
        connection.close()

def getuserbyid(id):
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "SELECT `*` FROM `is_old` where `id` = %s "
        cursor.execute(sql,id)
        result = cursor.fetchall()
        #    print "resulttttttt"
        #     print result
        return result
    finally:
        connection.close()
def generateauth(id,name,password):
    connection = connectdb();
    authenticationid = 9999999;
    try:
        cursor = connection.cursor()
        # Create a new record
        sql = "insert into authentication (user_id,username,password) VALUES(%s,%s,%s)"
        cursor.execute(sql, (id,name,password))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        authenticationid = cursor.lastrowid
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()
    return authenticationid
def authenticateuer(user,password):
    authen = False
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "SELECT count(*) FROM `authentication` where username = %s and password = %s"
        cursor.execute(sql,(user,password))
        result = cursor.fetchall()
        if (result[0][0] !=0):
            authen = True
        #    print "resulttttttt"
        #     print result
    finally:
        connection.close()
    return authen

def markaswaitingnew(lastid):
    done = 9999999;
    connection = connectdb();
    try:
        cursor = connection.cursor()
        # Create a new record
        sql = "INSERT INTO `waiting` (`user_id`,`status`) VALUES (%s,%s)"
        cursor.execute(sql, (lastid,0))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        done = cursor.lastrowid

        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()
    return done


def checkwaitinglist(lastid):
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "SELECT * FROM `waiting` where user_id=%s"
        cursor.execute(sql, (lastid,))
        result = cursor.fetchall()
        return result
        # print "resulttttttt"
        #     print result
    finally:
        connection.close()
def getallwaiting():
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "SELECT * FROM `waiting` INNER JOIN is_old on user_id = id where status = 0 limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
        # print "resulttttttt"
        #     print result
    finally:
        connection.close()


def updatewaiting(updatelist):
    updatedone = False
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "UPDATE `waiting` SET `status` = 1 where `waiting_id`=%s"
        cursor.execute(sql,(updatelist,))
        connection.commit()
        updatedone = True
        # print "resulttttttt"
        #     print result
    finally:
        connection.close()
    return updatedone


def removeauth(user, password):
    removepass = False
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "delete FROM `authentication` where `username`=%s and password=%s"
        cursor.execute(sql, (user,password))
        connection.commit()
        removepass = True
        # print "resulttttttt"
        #     print result
    finally:
        connection.close()
    return removepass
def removewaiting(lastid):
    removepass = False
    connection = connectdb()
    try:
        # with connection.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `is_old` (`header`, `email`,`nboftries`, `time`) VALUES (%s, %s,%s, %s)"
        # cursor.execute(sql, (headermail, fromuser, increment, dateofmail))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()

        cursor = connection.cursor()
        # Read a single record
        sql = "delete FROM `waiting` where `user_id`=%s"
        cursor.execute(sql,(lastid,))
        connection.commit()
        removepass = True
    except Exception as  e:
        print e
        # print "resulttttttt"
        #     print result
    finally:
        connection.close()
    return removepass
