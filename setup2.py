
from app import db
db.create_all()
from app import User, Task, List

#schauspieler
Keanu = User(name="Keanu", email="Keanu@hotmail.com", password="asdf1234")
Jason = User(name="Jason", email="Jason@hotmail.com", password="asdf1234")
Twain = User(name="Twain", email="Twain@hotmail.com", password="asdf1234")

db.session.add(Keanu)
db.session.add(Jason)
db.session.add(Twain)
db.session.commit()

u = User.query.all()

k = u[0]
j = u[1]
t = u[2]

print(f"{k.name}{k.email}{k.password}{k.time_created}")
print(f"{j.name}{j.email}{j.password}{j.time_created}")
print(f"{t.name}{t.email}{t.password}{t.time_created}")

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

print(f"{fr.title}{fr.time_created}")
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