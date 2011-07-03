# reset the database

from betatest import *

db.drop_all()
db.create_all()


# create users
opatut = models.user.User("opatut", "test", "opatut@example.com")
zetaron = models.user.User("zetaron", "test", "zetaron@example.com")
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

# close
db.session.commit()
