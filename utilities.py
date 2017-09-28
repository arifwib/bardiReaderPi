import psycopg2
import psycopg2.extras

def dbi():
    dbi = psycopg2.connect("dbname=pswjl host=localhost\
    user=postgres password=masterkey")
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
    cur.execute("select * from jobs where id = %s" %(id))
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
    c.execute("update jobs \
    set jobdate='%s', nosalesorder='%s', jenisjob='%s',statusjob='%s'\
     where id = %s"
    % (parms['jobdate'],parms['nosalesorder'],parms['jenisjob'],
    parms['statusjob'],id))
    con.commit()

def enterjob(parms):
    con = dbi()
    c = con.cursor()
    c.execute("insert into jobs(nosalesorder,jobdate,statusjob,jenisjob)\
       values ('%s', '%s', '%s', '%s')" % (parms['nosalesorder'],
       parms['jobdate'],parms['statusjob'],parms['jenisjob']))
    con.commit()