# reset the database

from betatest import *

db.drop_all()
db.create_all()


# create users
opatut = models.user.User("opatut", "test", "opatutlol@aol.com", "Paul Bienkowski", "Germany")
zetaron = models.user.User("zetaron", "test", "zetaron@live.com", "Fabian Stegemann", "Germany", "http://zetaron.de")
svenstaro = models.user.User("svenstaro", "test", "svenstaro@example.com", "Svensven", "Germany")

db.session.add(opatut)
db.session.add(zetaron)
db.session.add(svenstaro)

# create projects
rgj_webapp = models.project.Project("RedditGameJam Webapp", 
	"A helper webapp for organising the [reddit game jams](http://reddit.com/r/RedditGameJam).", 
	opatut,
	"http://redditgamejam.org")
betatest = models.project.Project("Betatest Backend", 
	"The betatest.net website really needs an analytics tool backend...", 
	zetaron,
	"http://betatest.net")
spacegame = models.project.Project("Space game", 
	"Awesome game. Just a space shooter.", 
	opatut)
ducttape = models.project.Project("Ducttape Game Engine", 
	"The most awesome game engine. It's magic inside!", 
	svenstaro,
	"http://ducttape.org")
	
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
msg_2 = models.message.Message("Message 2", '''
# What is this

I think its a headline.

## Is it really?

Yes it is!
''', opatut, zetaron)
msg_3 = models.message.Message("Message 3", '''
# Headline

## Second Headline

### Third Headline
#### Fourth Headline
##### Fifth Headline
###### Sixth Headline

This is a paragraph. It contains a [link](http://google.de) and also some escaped <html>. Furthermore, 
there is some ```inline-code```, some **bold** and *italic* text.

1. This is a numbered list.

3. It is numbered in order.
    
    You can have paragraphs within it.

6. It doesn't matter if you order it correct.

---

* This is one of them.
* This is another item.
    - This is a subitem.
    - This one too.
* And again back.

> Blockquotes are used to quote a text someone else said. They are displayed with a blue bar on the left.
>
> > You can also have blockquotes within blockquotes.
>
> That one above is a "living example".

    @app.route("/")
    def awesome():
        return "Markdown + Flask"

Have fun with it!''', opatut, zetaron)
msg_4 = models.message.Message("Message 4", "Good morning!", zetaron, opatut)

reply_3_1 = models.message.Message(msg_3, "Hello you!", zetaron, opatut)
reply_3_2 = models.message.Message(msg_3, "I got your message.", opatut, zetaron)
reply_3_3 = models.message.Message(msg_3, "What are you up to?", zetaron, opatut)
reply_3_4 = models.message.Message(msg_3, "Can you please reply?!", opatut, zetaron)

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
