import psycopg2
import psycopg2.extras
from ConfigParser import SafeConfigParser

def dbi():
    config = SafeConfigParser()
    config.read('config.ini')

    host = config.get('DB', 'host')
    dbname = config.get('DB', 'dbname')
    user =  config.get('DB', 'user')
    password = config.get('DB', 'password')

    dbi = psycopg2.connect("dbname="+dbname+' host='+host+'\
    user='+user+' password='+password+'key')
    return dbi


def duplic(nosalesorder,jobdate,msg,ok):
    dup = False
    db = dbi()
    curs = db.cursor()
    curs.execute("select * from tjobmachinereader where nosalesorder = '%s'\
                and jobdate='%s'" % (nosalesorder,jobdate))
    row = curs.fetchone()
    if row:
        ok = False
        msg += "Duplicate Entry: %s" %(item)
    return msg, ok


def duplicedit(nosalesorder,jobdate,id,msg,ok):
    dup = False
    db = dbi()
    curs = db.cursor()
    curs.execute("select * from tjobmachinereader where nosalesorder = '%s'\
                and jobdate='%s' and id != %s" % (nosalesorder,jobdate,id))
    row = curs.fetchone()
    if row:
        ok = False
        msg += "Duplicate Entry: %s" %(item)
    return msg, ok

def getjobparms(id):
    db = dbi()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from tjobmachinereader where id = %s" %(id))
    k = cur.fetchone() #cur.dictfetchone()
    return k

def getjobs():
    db = dbi()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from tjobmachinereader order by jobdate,nosalesorder")
    li = cur.fetchall()    #cur.dictfetchall()
    return li

def getname(id):
    res = ''
    db = dbi()
    try:
        cur = db.cursor()
        cur.execute("select nosalesorder from tjobmachinereader\
                 where id = %s" %(id))
        res = cur.fetchone()[0]
    except:
        pass
    return res

def getid(nosalesorder,jobdate):
    res = ''
    db = dbi()
    cur = db.cursor()
    try:
        cur.execute("select id from tjobmachinereader\
                     where nosalesorder = '%s' and jobdate='%s'" %(nosalesorder,jobdate))
        res = cur.fetchone()[0]
    except:
        pass
    return res

def deletejob(id):
    con = dbi()
    c = con.cursor()
    delete = 0
    try:
        c.execute("delete from tjobmachinereader\
        where id = %s" % (int(id)))
        con.commit()
    except:
        delete = 1
    return delete

def updatejob(parms,id):
    con = dbi()
    c = con.cursor()
    c.execute("update tjobmachinereader \
    set jobdate='%s', nosalesorder='%s', jenisjob='%s',statusjob='%s',\
    makereadytime='%s', makereadyoutput=%s, productivetime='%s',productiveoutput=%s,\
    finishtime='%s', finishoutput=%s\
     where id = %s"
    % (parms['jobdate'],parms['nosalesorder'],parms['jenisjob'], parms['statusjob'],\
       parms['makereadytime'], parms['makereadyoutput'], parms['productivetime'],\
       parms['productiveoutput'], parms['finishtime'], parms['finishoutput'],\
       id))
    con.commit()

def enterjob(parms):
    con = dbi()
    c = con.cursor()
    c.execute("insert into tjobmachinereader(nosalesorder,machine_id,jobdate,statusjob,jenisjob,\
              makereadytime, makereadyoutput, productivetime, productiveoutput, finishtime, finishoutput\
              ) values ('%s', %s, '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', %s)"
              % (parms['nosalesorder'], parms['machine_id'],
                parms['jobdate'],parms['statusjob'],parms['jenisjob'],
                parms['makereadytime'],parms['makereadyoutput'],parms['productivetime'],
                parms['productiveoutput'], parms['finishtime'], parms['finishoutput'])
        )
    con.commit()