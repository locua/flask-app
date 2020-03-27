from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session, flash, abort
from vs_url_for import vs_url_for
from forms import addPostForm, editPostForm, loginForm, registrationForm
from dbhelper import DBHelper
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from user import User
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from flask import jsonify

login_manager = LoginManager()

app = Flask(__name__)
db = DBHelper()
login_manager.init_app(app)
api = Api(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

resource_fields = {
    'post_id': fields.Integer,
    'post': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.DateTime(dt_format='rfc822')
}

parser = reqparse.RequestParser()
parser.add_argument('post', type=str, help='the text of the post; must be a string')
parser.add_argument('post_id', type=int, help='the id of the post; must be an integer')
parser.add_argument('user_id', type=int, help='the id of the user; must be an integer')

#----instantiating the resource; the main part of the flask-restful api
class PostsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return  db.get_all_posts()

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        post = args['post']
        user_id = args['user_id']
        db.add_post(post,user_id)
        return  db.get_all_posts()

class PostsIdApi(Resource):

    @marshal_with(resource_fields)
    def get(self, post_id):
        if  db.get_post(post_id):
            return db.get_post(post_id)
        abort(404)

    @marshal_with(resource_fields)
    def put(self,post_id):
        args = parser.parse_args()
        post = args['post']
        db.update_post(post,post_id)
        return  db.get_all_posts()

    @marshal_with(resource_fields)
    def delete(self, post_id):
        db.delete_post(post_id)
        return  db.get_all_posts()

#----assigning a route for the api
api.add_resource(PostsApi,'/api')
api.add_resource(PostsIdApi,'/api/<int:post_id>')



@login_manager.user_loader
def load_user(user_id):
    result = db.get_user(user_id)
    if result:
        return User(user_id)

@app.route('/')
def index():
    posts = db.get_all_posts()
    numreplys = db.howmanyreplys()[0]
    replys = db.get_all_replys()
    try:
        currentuser = db.get_user(session['user_id'])
        uname = currentuser[1]
        print(session['user_id'])
        print(db.poster_id(14))
    except:
        uname = 'why dont you sign up'
    ##print(replys)
    appip = request.remote_addr
    remaddr = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template("myforum_mysql.html", posts=posts,replys=replys, remaddr=remaddr, appip=appip,uname=uname)

@app.route('/add_post', methods = ['GET', 'POST'])
@login_required
def add_post():
    form = addPostForm()
    if form.validate_on_submit():
        post = form.post.data
        db.add_post(post,session['user_id'])
        return redirect(vs_url_for('index'))
    return render_template('add_post.html',form=form)

@app.route('/add_reply/<postid>', methods = ['GET', 'POST'])
@login_required
def add_reply(postid):
    form = addPostForm()
    if form.validate_on_submit():
        pid = int(postid)
        reply = form.post.data
        db.add_reply(pid,reply,session['user_id'])
        return redirect(vs_url_for('index'))
    return render_template('add_reply.html',form=form, postid=postid)

@app.route('/edit_post', methods = ['GET', 'POST'])
@login_required
def edit_post():
    form = editPostForm()
    if request.args.get('id'):
        post_id = request.args.get('id')
        post = db.get_post(post_id)
        form.post.data = post[0]
        form.post_id.data = post_id
        return render_template('edit_post.html',form=form,post=post)
    if form.validate_on_submit():
        post = form.post.data
        post_id = form.post_id.data
        db.update_post(post,post_id)
        return redirect(vs_url_for('index'))
    return render_template('edit_post.html',form=form)

@app.route('/delete_post', methods = ['GET', 'POST'])
@login_required
def delete_post():
    if request.args.get('id'):
            post_id = request.args.get('id')
            post_user_id = db.poster_id(post_id)
            if (session['user_id'] == post_user_id[0]):
                post = db.delete_post(post_id)
            else:
                flash('cannot delete another users post')
    return redirect(vs_url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user_id = db.check_password(username,password)
        if user_id:
            user = User(user_id)
            login_user(user)
            flash('login successful!')
            return redirect(vs_url_for('index'))
        else:
            flash('login unsuccessful!')
    return render_template('login.html',form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = registrationForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        db.sign_up(username, password)
        flash('You are now a member')
        return redirect(vs_url_for('index'))
    return render_template('signup.html', form=form)
        

@app.route('/forumapi')
@app.route('/forumapi/<username>')
def forumapi(username=None):
    if username:
        posts = db.get_user_posts(username)
        return jsonify({'posts':posts})
    else:
        posts = db.get_all_posts()
        return jsonify({'posts':posts})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    flash('you are now logged out')
    return redirect(vs_url_for('index'))

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
