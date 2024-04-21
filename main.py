from flask import Flask, render_template, redirect, make_response, jsonify, request
from sqlalchemy import delete

from data import db_session
from data.api import jobs_api, users_resource
from data.forms.login import LoginForm
from data.forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user
from data.jobs import Jobs
from data.order import Orders
from data.users import User
from data.cart import Cart
from data.forms.set_order import SetOrderForm
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/site_st.db")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).all()
    return render_template('index.html', **context)


@app.route('/cart/<u>')
def cart(u):
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        return redirect('/')
    context["cart"] = db_sess.query(Cart).filter(Cart.user == u)
    context["user"] = db_sess.query(User).filter(User.email == u)
    return render_template('cart.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    q = request.args.get('q')
    if q:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            total=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    q = request.args.get('q')
    if q:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add/<u>/<int:i>/<n>/<int:p>/<im>')
def add(i, n, p, im, u):
    db_sess = db_session.create_session()
    cart = db_sess.query(Cart).filter(Cart.user == u, Cart.id == i).first()
    user = db_sess.query(User).filter(User.email == u).first()
    if cart:
        cart.quantity += 1
        cart.tprice += cart.price
        user.total += cart.price
    else:
        user.total += p
        cart = Cart(id=i,
                    name=n,
                    price=p,
                    img=im,
                    user=u,
                    quantity=1,
                    tprice=p)
        db_sess.add(cart)
    db_sess.commit()
    return redirect("/")


@app.route('/quantity/<u>/<int:i>/<s>')
def quantity(u, i, s):
    db_sess = db_session.create_session()
    cart = db_sess.query(Cart).filter(Cart.user == u, Cart.id == i).first()
    user = db_sess.query(User).filter(User.email == u).first()
    if cart:
        if s == '+':
            cart.quantity += 1
            cart.tprice += cart.price
            user.total += cart.price
        else:
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.tprice -= cart.price
                user.total -= cart.price
            elif cart.quantity == 1:
                user.total -= cart.price
                db_sess.delete(cart)
    db_sess.commit()
    return redirect(f"/cart/{u}")


@app.route('/set_order/<u>/<int:t>', methods=['GET', 'POST'])
def order(u, t):
    q = request.args.get('q')
    if q:
        return redirect('/')
    form = SetOrderForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cart = db_sess.query(Cart).filter(Cart.user == u).all()
        goo = []
        for i in range(len(cart)):
            for j in range(cart[i].quantity):
                goo.append(str(cart[i].id))
        order = Orders(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            comment=form.comment.data,
            user=u,
            goods=' '.join(goo),
            total=t
        )
        user = db_sess.query(Cart).filter_by(user=u).first()
        while user:
            db_sess.delete(user)
            user = db_sess.query(Cart).filter_by(user=u).first()
        db_sess.add(order)
        user = db_sess.query(User).filter(User.email == u).first()
        user.total = 0
        db_sess.commit()
        return redirect(f'/orders/{u}')
    return render_template('set_order.html', title='Оформление заказа', form=form)


@app.route('/orders/<u>')
def orders(u):
    q = request.args.get('q')
    if q:
        return redirect('/')
    db_sess = db_session.create_session()
    context = {}
    context["orders"] = db_sess.query(Orders).filter(Orders.user == u)
    return render_template('order.html', **context)


@app.route('/catalog')
def catalog():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(
            Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.type == 'самый лучший товар в мире')
    return render_template('catalog.html', **context)


@app.route('/catalog_up')
def catalog_up():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(
            Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.type == 'верхняя одежда')
    return render_template('catalog.html', **context)


@app.route('/catalog_hat')
def catalog_hat():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(
            Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.type == 'головные уборы')
    return render_template('catalog.html', **context)


@app.route('/catalog_acc')
def catalog_acc():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(
            Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.type == 'аксессуары')
    return render_template('catalog.html', **context)


@app.route('/catalog_food')
def catalog_food():
    db_sess = db_session.create_session()
    context = {}
    q = request.args.get('q')
    if q:
        context["jobs"] = db_sess.query(Jobs).filter(
            Jobs.name.contains(q) | Jobs.desc.contains(q) | Jobs.type.contains(q))
    else:
        context["jobs"] = db_sess.query(Jobs).filter(Jobs.type == 'еда')
    return render_template('catalog.html', **context)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    app.run(port=8001, host='127.0.0.1')