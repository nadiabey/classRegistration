import sqlite3


def getdb(file):
    conn = sqlite3.connect(file)
    cur = conn.cursor()
    cur.execute(""" SELECT tbl_name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'""")
    depts = [x[0] for x in cur.fetchall()]
    lines = ["SELECT * FROM {}".format(x) for x in depts]
    ret = []
    for x in lines:
        if x is not lines[-1]:
            ret.append(x)
            ret.append('UNION ALL')
        else:
            ret.append(x + ';')
    return ret


def out(listy, name):
    o = '.open ' + name + '.db\n'
    hed = '.headers on\n'
    mod = '.mode csv\n'
    f = '.output ' + name + '.csv\n'
    file = open(name + '.sql', 'w')
    file.write(o)
    file.write(hed)
    file.write(mod)
    file.write(f)
    for x in listy:
        file.write(x + '\n')
    file.close()


if __name__ == '__main__':
    q = getdb('/Users/nadiabey/PycharmProjects/classRegistration/fall21.db')
    out(q,'fall21')