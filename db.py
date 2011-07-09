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
rgj_webapp = models.project.Project("RedditGameJam Web Application",
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

# add some tags
betatest.tags.append(models.tag.Tag.getTag("webapp"))
betatest.tags.append(models.tag.Tag.getTag("python"))

ducttape.tags.append(models.tag.Tag.getTag("game"))
ducttape.tags.append(models.tag.Tag.getTag("engine"))

spacegame.tags.append(models.tag.Tag.getTag("sfml"))
spacegame.tags.append(models.tag.Tag.getTag("c++"))
spacegame.tags.append(models.tag.Tag.getTag("GAME"))

opatut.tags.append(models.tag.Tag.getTag("GAME"))
opatut.tags.append(models.tag.Tag.getTag("engine"))
opatut.tags.append(models.tag.Tag.getTag("webapp"))
opatut.tags.append(models.tag.Tag.getTag("internet"))
opatut.tags.append(models.tag.Tag.getTag("c++"))

zetaron.tags.append(models.tag.Tag.getTag("c++"))
zetaron.tags.append(models.tag.Tag.getTag("game"))
zetaron.tags.append(models.tag.Tag.getTag("webapp"))
zetaron.tags.append(models.tag.Tag.getTag("desktop"))
zetaron.tags.append(models.tag.Tag.getTag("internet"))


# add some testers
ducttape.testers.append(zetaron)
ducttape.testers.append(opatut)
betatest.testers.append(opatut)
betatest.testers.append(svenstaro)
spacegame.testers.append(svenstaro)
spacegame.testers.append(zetaron)
rgj_webapp.testers.append(zetaron)

# create sample messages
thread_1 = models.messagethread.MessageThread("Thread #1", [opatut, zetaron, svenstaro])

msg_1 = models.message.Message(thread_1, "Hi what's up?", opatut)
msg_2 = models.message.Message(thread_1, '''
# What is this

I think its a headline.

## Is it really?

Yes it is!
''', zetaron)
msg_3 = models.message.Message(thread_1, '''
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

Have fun with it!''', opatut)
msg_4 = models.message.Message(thread_1, "That is a nice Markdown!", svenstaro)

db.session.add(thread_1)
db.session.add(msg_1)
db.session.add(msg_2)
db.session.add(msg_3)
db.session.add(msg_4)

# add some applications
application1 = models.application.Application(rgj_webapp, "I'd like to do this kind of stupid test job.")
application1.user = zetaron
db.session.add(application1)

application2 = models.application.Application(rgj_webapp, "I'd like to do this kind of stupid test job.")
application2.user = opatut
db.session.add(application2)

application3 = models.application.Application(betatest, "I'd like to do this kind of stupid test job.")
application3.user = opatut
db.session.add(application3)

application4 = models.application.Application(betatest, "I'd like to do this kind of stupid test job.")
application4.user = svenstaro
db.session.add(application4)

# some notifications
status = models.notification.ApplicationStatus("declined", application3)
n1 = models.notification.Notification(opatut, status)
db.session.add(n1)

# add some bugs
bug1 = models.bug.Bug("This is a real bug report you should realy think about writing your own... I mean __realy__", "First real bug report", betatest)
bug1.user = opatut

bug2 = models.bug.Bug("This is a real bug report you should realy think about writing your own... I mean __realy__. Not like me I just copied the first one.", "Second real bug report", betatest)
bug2.user = svenstaro

bug3 = models.bug.Bug("This is a real bug report you should realy think about writing your own... I mean __realy__. Not like me I just copied the first one. Thats bad I know but I did not know what to write as a sample bug report.", "Third real bug report", betatest)
bug3.user = zetaron

db.session.add(bug1)
db.session.add(bug2)
db.session.add(bug3)

# add some replies to the bugs
reply1 = models.bugreply.BugReply("Wow thats an awsome bug report you should write more like this one.", bug1)
reply1.user = zetaron

reply2 = models.bugreply.BugReply("Wow thats an awsome bug report you should write more like this one. Ok I did it again... I copied the previous comment. Sry.", bug1)
reply2.user = svenstaro

reply3 = models.bugreply.BugReply("Wow thats an awsome bug report you should write more like this one. Ok I did it again... I copied the previous comment. Sry. Hehe you cant blame me :). Right thats my first time I copied something __on this page__ :P.", bug1)
reply3.user = opatut

db.session.add(reply1)
db.session.add(reply2)
db.session.add(reply3)
# close
db.session.commit()

