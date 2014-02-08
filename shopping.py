import web
from passlib.hash import bcrypt

# this line included for using session
web.config.debug = False

# initialize a database connection
db = web.database(dbn='mysql', user='test', pw='test123', db='recipe_shopping')

# list of app urls
urls = (
    '/(\d*)', 'index',
    '/add', 'add',
    '/login', 'login',
    '/logout', 'logout',
    '/register', 'register',
    '/new_recipe', 'new_recipe'
)

# create application 
app = web.application(urls, locals())
# initialize session
session = web.session.Session(app, web.session.DiskStore('sessions'))

# rendering ?
render = web.template.render('templates/', base='base',globals={'session': session})
render_plain = web.template.render('templates/', globals={'session': session})

# home page 
class index:
    def GET(self, userid):
        if hasattr(session, 'user_id'):
            where = "users.id = %s" % session.user_id
        else:
            where = None
            raise web.seeother('/login')
        users = db.select('users', where=where)
        return render.index(users)

# insert new user into database
class add:
    def POST(self):
        i = web.input()
        user_email = i.email
        # hash users passwords to store them in the database
        hashed_password = bcrypt.encrypt(i.password)
        n = db.insert('users', email=user_email, password=hashed_password)
        raise web.seeother('/')

# handle user logins
class login:
    def GET(self):
        return render_plain.login()

    def POST(self):
        credentials = web.input()
        q = web.SQLQuery(["SELECT * FROM users WHERE email=", 
            web.SQLParam(credentials.email)])
        user = db.query(q)
        if len(user) > 0:
            this_user = user[0]
            # verify login with bcrypt
            if bcrypt.verify(credentials.password, this_user.password):
                session['user_id'] = str(this_user.id)
                raise web.seeother('/' + session.user_id)
            else:
                return render_plain.login()
        else:
            return render_plain.login()

# logout the user and destroy the session
class logout:
    def GET(self):
        session.kill()
        return render_plain.login()

# registration page for new users
class register:
    def GET(self):
        return render_plain.register()

# form for adding new recipes to the recipe book
class new_recipe:
    def GET(self):
        return render.new_recipe()

# actually inserting the recipe into the database
class add_recipe:
    def POST(self):
        i = web.input()
        recipe_name = i.recipe_name
        # hash users passwords to store them in the database
        #n = db.insert('users', email=user_email, password=hashed_password)
        recipe = db.inser('recipes', name=recipe_name) 
        raise web.seeother('/')


if __name__ == "__main__":
    app.run()
