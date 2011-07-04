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

# add some testers
ducttape.testers.append(zetaron)
ducttape.testers.append(opatut)
betatest.testers.append(opatut)
betatest.testers.append(svenstaro)
spacegame.testers.append(svenstaro)
spacegame.testers.append(zetaron)
rgj_webapp.testers.append(zetaron)

# create sample messages
msg_1 = models.message.Message("Message 1", "Hi what's up?", opatut, zetaron)
msg_2 = models.message.Message("Message 2", "Omg is this really you?", opatut, zetaron)
msg_3 = models.message.Message("Message 3", "How are you?", zetaron, opatut)
msg_4 = models.message.Message("Message 4", "Good morning!", zetaron, opatut)

reply_3_1 = models.message.Message(msg_3, "Hello you!", zetaron, opatut)
reply_3_2 = models.message.Message(msg_3, "I got your message.", zetaron, opatut)
reply_3_3 = models.message.Message(msg_3, "What are you up to?", zetaron, opatut)
reply_3_4 = models.message.Message(msg_3, "Can you please reply?!", zetaron, opatut)

db.session.add(msg_1)
db.session.add(msg_2)
db.session.add(msg_3)
db.session.add(msg_4)
db.session.add(reply_3_1)
db.session.add(reply_3_2)
db.session.add(reply_3_3)
db.session.add(reply_3_4)

msg_3.reply = reply_3_1
reply_3_1.reply = reply_3_2
reply_3_2.reply = reply_3_3
reply_3_3.reply = reply_3_4

# close
db.session.commit()
