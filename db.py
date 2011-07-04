# reset the database

from betatest import *

db.drop_all()
db.create_all()


# create users
opatut = models.user.User("opatut", "test", "opatutlol@aol.com")
zetaron = models.user.User("zetaron", "test", "zetaron@live.com")
svenstaro = models.user.User("svenstaro", "test", "svenstaro@example.com")

db.session.add(opatut)
db.session.add(zetaron)
db.session.add(svenstaro)

# create projects
rgj_webapp = models.project.Project("RedditGameJam Webapp", 
	"A helper webapp for organising the reddit game jams (http://reddit.com/r/RedditGameJam).", 
	opatut)
betatest = models.project.Project("Betatest Backend", 
	"The betatest.net website really needs an analytics tool backend...", 
	zetaron)
spacegame = models.project.Project("Space game", 
	"Awesome game. Just a space shooter.", 
	opatut)
ducttape = models.project.Project("Ducttape Game Engine", 
	"The most awesome game engine. It's magic inside!", 
	svenstaro)
	
db.session.add(rgj_webapp)	
db.session.add(betatest)	
db.session.add(spacegame)	
db.session.add(ducttape)

# create sample messages
msg_1 = models.message.Message("Test 1", "BlaBla", opatut, zetaron)
msg_2 = models.message.Message("Test 2", "BlaBla", opatut, zetaron)
msg_3 = models.message.Message("Test 3", "BlaBla", zetaron, opatut)
msg_4 = models.message.Message("Test 4", "BlaBla", zetaron, opatut)

db.session.add(msg_1)
db.session.add(msg_2)
db.session.add(msg_3)
db.session.add(msg_4)

# close
db.session.commit()
