import minigraf, subprocess, sys, tempfile, os
p=os.path.join(tempfile.mkdtemp(),'a.graph')
db=minigraf.MiniGrafDb.open(p); db.execute('(transact [[:a :b "c"]])')
r=subprocess.run([sys.executable,'-I','-c',f'import minigraf;db=minigraf.MiniGrafDb.open({p!r});print(db.execute("(query [:find ?v :where [:a :b ?v]])"))'],capture_output=True,text=True)
print('child:', r.stdout.strip(), r.stderr.strip()[-200:])
# repeat #371 check with fresh file, read before and after reopen
p2=os.path.join(tempfile.mkdtemp(),'b.graph'); d=minigraf.MiniGrafDb.open(p2)
d.execute('(transact [[:e :tag :x] [:e :tag :y] [:e :tag :z]])')
print('same session:', d.execute('(query [:find ?t :where [:e :tag ?t]])'))
d.checkpoint(); del d
d=minigraf.MiniGrafDb.open(p2); print('after reopen:', d.execute('(query [:find ?t :where [:e :tag ?t]])'))
print('count:', d.execute('(query [:find (count ?t) :where [:e :tag ?t]])'))
