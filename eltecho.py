# -*- coding: utf-8 -*-
import os
import re
import random
import webapp2
import jinja2
import hashlib
import hmac
from string import letters
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'hormigassomostodos'
clave = 'comienzo'
lpreg = ['¿Cuál es la capital de Argentina?', #1
         '¿Cuál es la capital de Uruguay?', #2
         '¿En qué ciudad de Venezuela nacio tu novio?', #3
         '¿Y en qué año nació él?', #4
         'Bien, sencillo. Vamos a aumentar la dificultad ahora, no hay tiempo que perder. Dime "ya" cuando estés lista', #5
         '¿El Real Madrid jugó la final de la Champions del 2014 contra que equipo?', #6
         '¿En qué país se va a realizar la Copa America del 2015?', #7
         'Y el estadio del Boca Juniors que queremos visitar en Buenos Aires, ¿cómo se lllama?', #8
         'Bieeeen, bien mi amor. Vamos a empezar con unos chocolaticos pues. Anda, anda a buscarlos. Te diria donde están, pero eso ya tu lo sabes. Dime "ya" cuando los tengas.', #9
         'Y ahora, ¿estas lita? Bueno, pasemos a la programación. En Python, cuando se habla de slicing se habla de procesar un string. ¿Cual es resultado de ejecutar: "Tu sabes, riquiti"[10:0]', #10
         'Puedo definir una lista de la siguiente manera: la_nena = ["goza", "rie", "vuela", "goza", "vibra", "goza"]. ¿Cierto o falso?', #11
         'Y entonces, utilizando la lista anterior, ¿cuantos "goza" quedarian despues de ejecutar: [i for i in la_nena if i == "goza"]', #12
         'Ayy nena, ay nena. ¿Te gustan las sopresas, no? ¿Te gusta gozar? Dime cuantos juguetes hay en la ultima cesta de donde ponemos la luz, los celulares, etc', #13
         'Ay si mi nena, feliz cumpleaños. Dime que me amas'] #14 y ultima
lresp = ['buenos aires', #1
         'montevideo', #2
         'maturin', #3
         '1990', #4
         'ya', #5
         'atletico de madrid', #6
         'chile', #7
         'bombonera', #8
         'ya', #9
         'riquiti', #10
         'cierto', #11
         '3', #12
         '2', #13
         'te amo'] #ultima
lmens = ['Te la sabes, vamos para alla el miercoles :)', #1
         'Tambien de la sabes, piensa en un video de un monte', #2
         'Es la capital de Monagas', #3
         'Debes escribir el año en numeros', #4
         'Escribe simplemente "ya"', #5
         'Son de la misma ciudad, Simeone es el coach', #6
         'Queda cerca de Argentia, no vamos a estar muy lejos de alli el miercoles', #7 
         'Dimelo sin articulo, una sola palabra, mi bombom', #8
         'Escribe simplemente "ya"', #9
         '¿Necesitas una pista? Si abres un terminal y empiezas Python, puedes escribir la linea de codigo exactamente y ejecutarla. ¿Ves que mucho te ayudo? Debes escribir la respuesta sin comillas', #10
         'Si necesitas combrobarlo, puedes hacerlo en el temrinal. La respuesta aqui es simplemente "cierto" o "falso"', #11
         'Ejecuta esa linea, ¿se ve rara no? La respuesta aqui es un numero simplemente, mayor que 2 y menor que 5', #12
         'Me refieron a la mesita de noche improvisada, donde tenemos cestas encima de otras cestas. No tengas miedo, que no te tiemble o vibre la mano, revisa la ultima de abajo. La respuesta aqui es simplemente un numero, mayor que 1 y menor que 3',
         'No seas mala nena, dime que me amas con un "te amo"'] #Ultima

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def mensaje():
    print 'In mensaje()'
    if clave == 'comienzo':
        print 'mensaje() - clave es comienzo, mensaje listo'
        mensaje = lmens[0]
    elif clave == 'segunda':
        print 'mensaje() - clave es segunda, mensaje listo'
        #print 'segunda'
        mensaje = lmens[1]
    elif clave == 'tercera':
        print 'mensaje() - clave es tercera, mensaje listo'
        #print 'segunda'
        mensaje = lmens[2]
    elif clave == 'cuarta':
        mensaje = lmens[3]
    elif clave == 'quinta':
        mensaje = lmens[4]
    elif clave == 'sexta':
        mensaje = lmens[5]
    elif clave == 'septima':
        mensaje = lmens[6]
    elif clave == 'octava':
        mensaje = lmens[7]
    elif clave == 'novena':
        mensaje = lmens[8]
    elif clave == 'decima':
        mensaje = lmens[9]
    elif clave == 'decimaprimera':
        mensaje = lmens[10]
    elif clave == 'decimasegunda':
        mensaje = lmens[11]
    elif clave == 'decimatercera':
        mensaje = lmens[12]
    elif clave == 'decimacuarta':
        mensaje = lmens[13]

    return mensaje


def formula():
    print 'In formula()'
    #Formula cual es la pregunta del momento
    if clave == 'comienzo':
        print 'forumla() - clave es comienzo, primera formulada'
        pregunta = lpreg[0]
    elif clave == 'segunda':
        print 'forumla() - clave es segunda, segunda formulada'
        #print 'segunda'
        pregunta = lpreg[1]
    elif clave == 'tercera':
        print 'forumla() - clave es tercera, tercera forumulada'
        #print 'segunda'
        pregunta = lpreg[2]
    elif clave == 'cuarta':
        pregunta = lpreg[3]
    elif clave == 'quinta':
        pregunta = lpreg[4]
    elif clave == 'sexta':
        pregunta = lpreg[5]
    elif clave == 'septima':
        pregunta = lpreg[6]
    elif clave == 'octava':
        pregunta = lpreg[7]
    elif clave == 'novena':
        pregunta = lpreg[8]
    elif clave == 'decima':
        pregunta = lpreg[9]
    elif clave == 'decimaprimera':
        pregunta = lpreg[10]
    elif clave == 'decimasegunda':
        pregunta = lpreg[11]
    elif clave == 'decimatercera':
        pregunta = lpreg[12]
    elif clave == 'decimacuarta':
        pregunta = lpreg[13]

    return pregunta

def revisa(respuesta):
    print 'In revisa()'
    #Revisa cual es la respuesta y decide si es correcto o no
    #medidor = (False,0)
    global clave
    if clave == 'comienzo':
        print 'In revisa() - clave es comienzo'
        medidor = (False,0)
        if clave == 'comienzo' and respuesta == lresp[0]:
            print 'In revisa() - clave es comienzo y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,0)
            print 'In revisa() - medidor: ', medidor
            clave = 'segunda'
            print 'In revisa() - clave: ', clave
            return medidor
    if clave == 'segunda':
        print 'In revisa() - clave es segunda'
        medidor = (False,1)
        if clave == 'segunda' and respuesta == lresp[1]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,1)
            clave = 'tercera'
            return medidor
    if clave == 'tercera':
        print 'In revisa() - clave es segunda'
        medidor = (False,2)
        if clave == 'tercera' and respuesta == lresp[2]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,2)
            clave = 'cuarta'
            return medidor
    if clave == 'cuarta':
        print 'In revisa() - clave es segunda'
        medidor = (False,3)
        if clave == 'cuarta' and respuesta == lresp[3]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,3)
            clave = 'quinta'
            return medidor
    if clave == 'quinta':
        print 'In revisa() - clave es segunda'
        medidor = (False,4)
        if clave == 'quinta' and respuesta == lresp[4]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,4)
            clave = 'sexta'
            return medidor
    if clave == 'sexta':
        print 'In revisa() - clave es segunda'
        medidor = (False,5)
        if clave == 'sexta' and respuesta == lresp[5]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,5)
            clave = 'septima'
            return medidor
    if clave == 'septima':
        print 'In revisa() - clave es segunda'
        medidor = (False,6)
        if clave == 'septima' and respuesta == lresp[6]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,6)
            clave = 'octava'
            return medidor
    if clave == 'octava':
        print 'In revisa() - clave es segunda'
        medidor = (False,7)
        if clave == 'octava' and respuesta == lresp[7]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,7)
            clave = 'novena'
            return medidor
    if clave == 'novena':
        print 'In revisa() - clave es segunda'
        medidor = (False,8)
        if clave == 'novena' and respuesta == lresp[8]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,8)
            clave = 'decima'
            return medidor
    if clave == 'decima':
        print 'In revisa() - clave es segunda'
        medidor = (False,9)
        if clave == 'decima' and respuesta == lresp[9]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,9)
            clave = 'decimaprimera'
            return medidor
    if clave == 'decimaprimera':
        #print 'In revisa() - clave es segunda'
        medidor = (False,10)
        if clave == 'decimaprimera' and respuesta == lresp[10]:
            print 'In revisa() - clave es segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,10)
            clave = 'decimasegunda'
            return medidor
    if clave == 'decimasegunda':
        print 'In revisa() - clave es d_segunda'
        medidor = (False,11)
        if clave == 'decimasegunda' and respuesta == lresp[11]:
            print 'In revisa() - clave es d_segunda y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,11)
            clave = 'decimatercera'
            return medidor  
    if clave == 'decimatercera':
        print 'In revisa() - clave es d_tercera'
        medidor = (False,12)
        if clave == 'decimatercera' and respuesta == lresp[12]:
            print 'In revisa() - clave es d_tercera y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,12)
            clave = 'decimacuarta'     
            return medidor
    if clave == 'decimacuarta':
        print 'In revisa() - clave es d_tercera'
        medidor = (False,13)
        if clave == 'decimacuarta' and respuesta == lresp[13]:
            print 'In revisa() - clave es d_tercera y la respuesta es correcta'
            #medidor = 'primera correcta'
            medidor = (True,'ultima')
            clave = 'comienzo'     
            return medidor


    return medidor

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class LaNena(BlogHandler):
    def get(self):
        print 'In get()'
        pregunta = formula()
        d_pregunta = pregunta.decode('utf-8')
        #msg = mensaje()
        print 'get() - pregunta formulada: ', pregunta
        #print d_pregunta
        #print 'get() - mensaje: ', msg
        self.render('lanena.html', pregunta = d_pregunta)

    def post(self):
        print 'In post()'
        respuesta = (self.request.get('respuesta')).lower()
        #pregunta =  self.request.get('pregunta')
        print respuesta
        
        el_medidor = revisa(respuesta)
        print 'post() - el_medidor: ', el_medidor
        
        
        if el_medidor[1] == 'ultima': #si fue la ultima, vete para /teamo
            self.redirect("/teamo")
        elif el_medidor[0] == True: #si la respuesta es correcta, siguiente pregunta, actualiza la clave
            print 'post() - respuesta correcta'
            self.redirect("/lanena")
        else: #si no, muestra el mensaje y vuelve a preguntar la misma
            print 'post() - respuesta incorrecta'
            msg = mensaje()
            pregunta = formula()
            d_pregunta = pregunta.decode('utf-8')
            d_msg = msg.decode('utf-8')
            print 'post() - pregunta formulada: ', pregunta
            print 'post() - mensaje: ', msg
            self.render("lanena.html", pregunta = d_pregunta, msg = d_msg)

class TeAmo(BlogHandler):
    def get(self):
        self.render('teamo.html')

class Post(db.Model):
    image = db.StringProperty(required = False)
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        #if self.request.path == "/":
        return render_str("post.html", p = self)

class BlogFront(BlogHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('front.html', posts = posts)

class PostPage(BlogHandler):
    def get(self, post_name):
        key = db.Key.from_path('Post', post_name, parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/')

        subject = self.request.get('subject')
        content = self.request.get('content')
        image = self.request.get('image')
        path_name = self.request.get('path_name')
        
        if subject and content and path_name:
            p = Post(parent = blog_key(), subject = subject, content = content, key_name = path_name, image = image)
            p.put()
            self.redirect('/%s' % str(p.key().name()))
        else:
            error = "subject and content and path_name, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class Acerca(BlogHandler):
    def get(self):
        self.render('acerca.html')



class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            
            u = User.register(self.username, self.password, self.email)
            u.put()
            #self.error(404)
            self.login(u)
            self.redirect('/')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/newpost')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u



app = webapp2.WSGIApplication([('/', BlogFront),
                               ('/(eltecho-[a-zA-Z0-9_-]+)', PostPage),
                               ('/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/acerca', Acerca),
                               ('/lanena', LaNena),
                               ('/teamo', TeAmo),
                               ],
                              debug=True)



