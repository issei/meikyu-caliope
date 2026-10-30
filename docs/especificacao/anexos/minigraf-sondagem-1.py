import minigraf, os, tempfile, json
d=tempfile.mkdtemp(); p=os.path.join(d,'t.graph')
db=minigraf.MiniGrafDb.open(p)
def x(q):
    try: r=db.execute(q); print('OK', q[:70].replace('\n',' '), '=>', r[:300]); return r
    except Exception as e: print('ERR', q[:70], '=>', type(e).__name__, e)
x('(transact [[:r1 :resp/campo "rotina-1"] [:r1 :resp/texto "Assisto à noite"] [:ev1 :ev/resp :r1] [:ev1 :ev/code :c1] [:ev1 :ev/code :c2]])')
x('(query [:find ?c :where [:ev1 :ev/code ?c]])')
x('(transact [[:ev2 :ev/code :c1]])'); x('(transact [[:ev2 :ev/code :c2]])')
x('(query [:find ?c :where [:ev2 :ev/code ?c]])')
x('(query [:find (count ?e) :where [?e :ev/code :c1]])')
x('(query [:find ?t :where [?r :resp/texto ?t] [(str/includes? ?t "noite")]])')
x('(query [:find ?t :where [?r :resp/texto ?t] [(contains? ?t "noite")]])')
x('(retract [[:r1 :resp/texto "Assisto à noite"]])')
x('(query [:find ?t :as-of 1 :where [:r1 :resp/texto ?t]])')
x('(query [:find ?t :where [:r1 :resp/texto ?t]])')
x('(transact [[:bad :x/y "a"] [:bad :x/z ]])')
x('(query [:find ?e ?v :where [?e :x/y ?v]])')
x('(begin)')
db.checkpoint(); del db
db=minigraf.MiniGrafDb.open(p); x('(query [:find ?e ?c :where [?e :ev/code ?c]])')
try:
    db2=minigraf.MiniGrafDb.open(p); print('second open in same proc OK')
except Exception as e: print('second open', e)
print(os.listdir(d))
