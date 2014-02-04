import web
web.config.debug = False

db = web.database(dbn='mysql', user='test', pw='test123', db='recipe_shopping')


urls = (
    '/(\d*)', 'index',
    '/add', 'add',
    '/login', 'login'
)

app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

render = web.template.render('templates/', globals={'session': session})

class index:
    def GET(self, user_id):
        if user_id:
            where = "users.id = %s" % user_id
        else:
            where = None
            raise web.seeother('/login')
        users = db.select('users', where=where)
        return render.index(users)

class add:
    def POST(self):
        i = web.input()
        n = db.insert('users', email=i.email, password=i.password)
        raise web.seeother('/')

class login:
    def GET(self):
        return render.login()

    def POST(self):
        credentials = web.input()
        q = web.SQLQuery(["SELECT * FROM users WHERE email=", 
            web.SQLParam(credentials.email), " AND password=", 
            web.SQLParam(credentials.password)])
        user = db.query(q)
        if len(user) > 0:
            session['user_id'] = str(user[0].id)
            raise web.seeother('/' + session.user_id)
        else:
            return render.login()

if __name__ == "__main__":
    app.run()
