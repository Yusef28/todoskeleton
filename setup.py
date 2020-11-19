
from app import db
db.create_all()
from app import User, Task, List

#schauspieler
Keanu = User(name="Keanu")
Jason = User(name="Jason")
Twain = User(name="Twain")

db.session.add(Keanu)
db.session.add(Jason)
db.session.add(Twain)
db.session.commit()

u = User.query.all()

k = u[0]
j = u[1]
t = u[2]

print(k.name)
print(j.name)
print(t.name)

#Keanu Listen
freund_list = List(title="Keanu's Freunden", eltern_user=k.id)
familie_list = List(title="Keanu's Filme", eltern_user=k.id)
kleidung_list = List(title="Keanu's Kleidung", eltern_user=k.id)

db.session.add(freund_list)
db.session.add(familie_list)
db.session.add(kleidung_list)
db.session.commit()

l = List.query.all()

fr = l[0]
fa = l[1]
kl = l[2]

print(fr.title)
print(fa.title)
print(kl.title)


#Keanu filme
matrix = Task(title="Die Matrix", eltern_list=fr.id)
matrixII = Task(title="Die Matrix II", eltern_list=fr.id)
matrixIII = Task(title="Die Matrix Neuegeladen", eltern_list=fr.id)

db.session.add(matrix)
db.session.add(matrixII)
db.session.add(matrixIII)
db.session.commit()

t = Task.query.all()

m = t[0]
mII = t[1]
mIII = t[2]

print(m.title)
print(mII.title)
print(mIII.title)