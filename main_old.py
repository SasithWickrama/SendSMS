import multiprocessing
import random
import time
import db
from log import getLogger
from sendsms import Sendsms
import sendsms
import sys

logger = getLogger('smslog', 'logs/smslog')

text = """
ඉස්කෝලෙ නැතත් O/L විභාගයට සූදානම් වෙන ඔබේ දරුවා වෙනුවෙන් PEOTVGO වෙතින් විශේෂ අධ්‍යාපනික නාලිකාවක්. 10 සහ 11 ශ්‍රේණි සදහා දැන් ‘විදැස 10-11’.
PEOTVGO Mobile APP එක ඔස්සේ ඕනෑම වේලාවක අධ්‍යාපන කටයුතු නොනැවතී කර ගැනීමට, පැය 48 ක Rewind පහසුකමද සහිතව. ජූලි මාසය පුරාවටම නොමිලේ!
අදම www.peotvgo.com වෙත පිවිස ලියාපදිංචි වී PEOTVGO App එක Download කරගන්න.
"""


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


def sendSmsAuto(x):
    ref = specific_string(15)
    logger.info("Request : %s" % ref + " - " + str(x))
    conn = db.DbConnection.dbconnSmsPrg(self="")
    c = conn.cursor()
    #sql = 'select SEND_TPNO,SEND_MSG,SENT_OWNER,SMS_ID from SMSMSGS1 WHERE SEND_SUCS=0   AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SMSMSGS1.ROWID), 10) = ' + str(x)
    sql = 'SELECT CUSTOMER_CONTACT FROM TEST_CUS_MOB WHERE STATUS IS NULL and CUSTOMER_CONTACT = :CUSTOMER_CONTACT AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(TEST_CUS_MOB.ROWID), 10) = ' + str(x)    
    c.execute(sql,["0710959907"])

    for row in c:

        TPNO, = row
        
        print(TPNO)
        
        SEND_MSG ="""Dear Valued Customer,
        
Due to the current situation in the country, your SLT-MOBITEL<Insert Telephone number> 
Home bill will be sent as a SMS to your this registered mobile number instead of the printed bill with immediate effect. 
Please dial 1212 for more details.

SLTMobitel -The Connection.

        
        
 හිතවත් පාරිභෝගිකයිනි,
 
රටෙහි පවතින වර්තමාන තත්වය හමුවේ මුද්‍රිත බිල්පත වෙනුවට ඔබගේ  SLT-MOBITEL ගෘහස්ත බිල්පත 
 ඔබගේ ලියාපදිංචි ජංගම දුරකතන අංකයට  එකක් ලෙස එවනු ලැබේ. වැඩි විස්තර සඳහා 1212 අමතන්න.

SLT MOBITEL-එකම එක සබැදියාව

"""

        try:
            # create a cursor
            Sendsms.sendSms(TPNO, SEND_MSG, 'OSS',TPNO)
            print("msgid " + sendsms.msgid)
            print("smsmsgid " + sendsms.smsmsgid)
            print("msgid_id " + sendsms.msgid_id)
            

            sql = "update TEST_CUS_MOB set STATUS = : sms_rtn where  CUSTOMER_CONTACT= :sms_id"
            #print("sql "+ sql)
            with conn.cursor() as cursor:
                cursor.execute(sql, [sendsms.response, TPNO])
                # cursor.execute(sql)
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))



def sendSmsManual(x):

    ref = specific_string(15)
    logger.info("Request : %s" % ref + " - " + str(x))
    conn = db.DbConnection.dbconnSmsPrg(self="")
    c = conn.cursor()
    sql = 'select MOBILE,SMSID from SMS_SLT_CUS WHERE STAT=0   AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SMS_SLT_CUS.ROWID), 5) = ' + str(x)
    c.execute(sql)

    for row in c:

        SEND_TPNO, SMSID = row
        
        print(SEND_TPNO)
        

        try:
            # create a cursor
            Sendsms.sendSms(SEND_TPNO, text, 'OSS',SMSID)

           
            sql = "update SMS_SLT_CUS set STAT=1,DATE_UPDATE=sysdate,SMSID_RETURN = : sms_rtn where  SMSID= :sms_id"

            with conn.cursor() as cursor:
                cursor.execute(sql, [sendsms.response, SMSID])
                # cursor.execute(sql)
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))

def sendSmsManual2(x):

          
    ref = specific_string(15)
    logger.info("Request : %s" % ref + " - " + str(x))
    conn = db.DbConnection.dbconnSmsPrg(self="")
    c = conn.cursor()
    sql = 'select MOBILE,SMSID from SMS_SLT_CUS2 WHERE STAT=0   AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SMS_SLT_CUS2.ROWID), 5) = ' + str(x)
    c.execute(sql)

    for row in c:

        SEND_TPNO, SMSID = row
        
        print(SEND_TPNO)
        
        try:
            # create a cursor
            Sendsms.sendSmsTwo(SEND_TPNO, text, 'OSS',SMSID)

           
            sql = "update SMS_SLT_CUS2 set STAT=1,DATE_UPDATE=sysdate,SMSID_RETURN = : sms_rtn where  SMSID= :sms_id"

            with conn.cursor() as cursor:
                cursor.execute(sql, [sendsms.response, SMSID])
                # cursor.execute(sql)
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))

def sendSmsManual3(x):
   
          
    ref = specific_string(15)
    logger.info("Request : %s" % ref + " - " + str(x))
    conn = db.DbConnection.dbconnSmsPrg(self="")
    c = conn.cursor()
    sql = 'select MOBILE,SMSID from SMS_SLT_CUS3 WHERE STAT=0   AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(SMS_SLT_CUS3.ROWID), 5) = ' + str(x)
    c.execute(sql)

    for row in c:

        SEND_TPNO, SMSID = row
        
        print(SEND_TPNO)
        
        try:
            # create a cursor
            Sendsms.sendSmsThree(SEND_TPNO, text, 'OSS',SMSID)

            sql = "update SMS_SLT_CUS3 set STAT=1,DATE_UPDATE=sysdate,SMSID_RETURN = : sms_rtn where  SMSID= :sms_id"

            with conn.cursor() as cursor:
                cursor.execute(sql, [sendsms.response, SMSID])
                # cursor.execute(sql)
                conn.commit()
        except conn.Error as error:
            print('Error occurred:' + str(error))



if __name__ == '__main__':
    
    if sys.argv[1] == 'AUTO':
        processes = []
        for i in range(0, 10):
            p = multiprocessing.Process(target=sendSmsAuto, args=(i,))
            processes.append(p)
            p.start()
           # multiprocessing_func(i)
        for process in processes:
            process.join()
            
    if sys.argv[1] == 'MANUAL':
        processes = []
        for i in range(0, 10):
            p = multiprocessing.Process(target=sendSmsManual, args=(i,))
            processes.append(p)
            p.start()
            
            p2 = multiprocessing.Process(target=sendSmsManual2, args=(i,))
            processes.append(p2)
            p2.start()
            
            p3 = multiprocessing.Process(target=sendSmsManual3, args=(i,))
            processes.append(p3)
            p3.start()
            
           # multiprocessing_func(i)
        for process in processes:
            process.join()    

