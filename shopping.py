import web

db = web.database(dbn='mysql', user='test', pw='test123', db='recipe_shopping')

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/add', 'add'
)


class index:
    def GET(self):
        users = db.select('users')
        return render.index(users)

class add:
    def POST(self):
        i = web.input()
        n = db.insert('users', email=i.email, password=i.password)
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
