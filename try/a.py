import pymysql

passwd = '1606721192wyh@'
# CVEs = []
# def load_CVEs():
#     H = os.walk("../dataset/cvss_dataset")
#     t = open("./cvss.csv","w")
#     for path, dir_list, file_list in H:
#         for file_name in file_list:
#             file = open(path+'/'+file_name,"r")
#             lines = csv.reader(file)
#             next(lines)
#             for line in lines:
#                 CVEs.append(line[0])
#                 t.write(line[0]+','+line[4]+'\n')
#     t.close()


def load_CVEs():
    # t = open(inputpath+"cvss.csv", "r")
    # lines = csv.reader(t)
    # for line in lines:
    #     CVE_scores[line[0]]=line[1]
    # t.close()
    conn = pymysql.connect(
        host = 'winhost',
        user = 'root',
        passwd = passwd,
        port = 3306,
        db = 'iscomp',
        charset = 'utf8'
    )
    cur = conn.cursor()
    sql = "select * from `cve` "
    cur.execute(sql)
    data = cur.fetchall()
    CVE_scores = {}
    for i in data:
        CVE_scores[i[0]]=i[1]
    print(CVE_scores)
    cur.close()
    conn.close()

load_CVEs()