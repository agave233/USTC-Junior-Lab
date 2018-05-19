# -*- coding: utf-8 -*- 
from flask import render_template, redirect, url_for, request, flash, abort, session
from app import app, db
from app.models import *
from app.forms import *

@app.route('/')
def index():
    userId = 0
    name = ''
    allads = ads.query.all()
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
    return render_template('index.html', ads=allads, userId=userId, name=name)

@app.route('/about')
def about():
    userId = 0
    name = ''
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
    return render_template('about.html', userId=userId, name=name)

@app.route('/ad/edit/<int:id>',methods=['POST', 'GET'])
def ad_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = AdForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                ad = ads(form)
            else:
                ad = ads.query.get(id)
                ad.update(form)
            db.session.add(ad)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('ad_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/ad/delete/<int:id>')
def ad_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    ad = ads.query.get(id)
    if ad:
        db.session.delete(ad)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = customers.query.filter_by(userName = username).first()

        if user is None:
            error = 'User ' + username + 'doesn\'t exist.'
        elif password != user.passWd:
            error = 'Password Wrong.'
        else:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = username
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error, userId=0, name=None)


@app.route('/signup',methods=['GET','POST'])
def signup():
    if session.get('logged_in'):
        return redirect(url_for('index'))

    error = None
    form = CustomerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form['userName']
            custName = form['custName']
            password = request.form['passWd']
            password_ = request.form['passWd_']
            user1 = customers.query.filter_by(userName = username).first()
            user2 = customers.query.filter_by(userName=custName).first()
            if user1 is not None:
                error = username + ' has existed,please try another.'
            if user2 is not None:
                error = custName + ' has existed,please try another.'
            elif password != password_:
                error = 'Password Inconsistent,please check.'
            else:
                c = customers(form)
                db.session.add(c)
                db.session.commit()
                flash('You have signed up successfully.')
                return redirect(url_for('login'))
    return render_template('signup.html', error=error, form=form, name='', userId=0)

@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        abort(404)

    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('user_name',None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/coupon')
def coupon_page():
    userId = 0
    name = ''
    offIds = []
    if session.get('logged_in'):
        name = session['user_name']
        userId = session['user_id']
        offIds = [off.offId for off in myoffs.query.filter(myoffs.custId==userId).all()]
    if request.args.get('name'):
        searchName = request.args.get('name')
        coupons = offs.query.filter(offs.offName == searchName).all()
    else:
        coupons = offs.query.all()
    return render_template('coupon.html', offIds=offIds, coupons=coupons, userId=userId, name=name)


@app.route('/coupon/add/<int:id>')
def coupon_add(id):
    if not session.get('logged_in'):
        abort(401)
    userId = session['user_id']
    if myoffs.query.filter(myoffs.custId==userId, myoffs.offId==id).first():
        flash("您已经领取过了。")
        return redirect(url_for('coupon_page'))
    off=offs.query.get(id)
    if off.avaiNum <= 0:
        flash("优惠券没了。")
        return redirect(url_for('coupon_page'))
    off.avaiNum -= 1
    mf = myoffs(userId, id)
    db.session.add(mf)
    db.session.commit()
    return redirect(url_for('coupon_page'))

@app.route('/coupon/edit/<int:id>', methods=['POST', 'GET'])
def coupon_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = OffForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                off = offs(form)
            else:
                off = offs.query.get(id)
                delta = form['offNum'].data - (off.offNum - off.avaiNum)
                if delta < 0:
                    flash('优惠券数小于已领取数')
                    return render_template('coupon_edit.html', form=form, userId=session['user_id'], name=session['user_name'])
                off.update(form)
            db.session.add(off)
            db.session.commit()
            return redirect(url_for('coupon_page'))
    return render_template('coupon_edit.html', form=form, userId=session['user_id'], name=session['user_name'])

@app.route('/coupon/delete/<int:id>')
def coupon_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    off = offs.query.get(id)
    for myof in myoffs.query.filter(myoffs.offId == id).all():
        db.session.delete(myof)
    db.session.delete(off)
    db.session.commit()
    return redirect(url_for('coupon_page'))

@app.route('/flight')
def flight_page():
    userId = 0
    name = ''
    resvNums = {}
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
        rs = reservations.query.filter(reservations.custId == userId, reservations.resvType == 'flight').all()
        resvNums = {r.resvId: r.resvNum for r in rs}
    if request.args.get('from') and request.args.get('to'):
        fromCity = request.args.get('from')
        toCity = request.args.get('to')
        f = flights.query.filter(flights.fromCity == fromCity).filter(
            flights.arivCity == toCity).all()
    else:
        fromCity = ''
        toCity = ''
        f = flights.query.all()
    return render_template('flight.html', flights=f, resvNums=resvNums, userId=userId, name=name, fromCity=fromCity, toCity=toCity)


@app.route('/flight/delete/<int:id>')
def flight_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    f = flights.query.get(id)
    reservations.query.filter(reservations.resvType == 'flight').filter(
        reservations.resvId == f.id).delete()
    db.session.delete(f)
    db.session.commit()
    return redirect(url_for('flight_page'))


@app.route('/flight/edit/<int:id>', methods=['POST', 'GET'])
def flight_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = FlightForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                f = flights(form)
            else:
                f = flights.query.get(id)
                delta = form['seatNum'].data - (f.seatNum - f.avaiNum)
                if delta < 0:
                    flash('座位数小于已预订数')
                    return render_template('flight_edit.html', form=form, userId=session['user_id'], name=session['user_name'])
                f.update(form)
            db.session.add(f)
            db.session.commit()
            return redirect(url_for('flight_page'))
    return render_template('flight_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/train')
def train_page():
    userId = 0
    name = ''
    resvNums = {}
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
        rs = reservations.query.filter(reservations.custId == userId, reservations.resvType == 'train').all()
        resvNums = {r.resvId: r.resvNum for r in rs}
    if request.args.get('from') and request.args.get('to'):
        fromCity = request.args.get('from')
        toCity = request.args.get('to')
        t = trains.query.filter(trains.fromCity == fromCity).filter(
            trains.arivCity == toCity).all()
    else:
        fromCity = ''
        toCity = ''
        t = trains.query.all()
    return render_template('train.html', trains=t, resvNums=resvNums, userId=userId, fromCity=fromCity, toCity=toCity, name=name)


@app.route('/train/delete/<int:id>')
def train_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    t = trains.query.get(id)
    reservations.query.filter(reservations.resvType == 'train').filter(
        reservations.resvId == t.id).delete()
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('train_page'))


@app.route('/train/edit/<int:id>', methods=['POST', 'GET'])
def train_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = TrainForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                t = trains(form)
            else:
                t = trains.query.get(id)
                delta = form['seatNum'].data - (t.seatNum - t.avaiNum)
                if delta < 0:
                    flash('座位数小于已预订数')
                    return render_template('train_edit.html', form=form, userId=session['user_id'], name=session['user_name'])
                t.update(form)
            db.session.add(t)
            db.session.commit()
            return redirect(url_for('train_page'))
    return render_template('train_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/hotel')
def hotel_page():
    userId = 0
    name = ''
    resvNums = {}
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
        rs = reservations.query.filter(reservations.custId == userId, reservations.resvType == 'hotel').all()
        resvNums = {r.resvId: r.resvNum for r in rs}
    if request.args.get('location'):
        loc = request.args.get('location')
        h = hotels.query.filter(hotels.hotelLoca.like('%' + loc + '%')).all()
    else:
        loc = ''
        h = hotels.query.all()
    return render_template('hotel.html', hotels=h, resvNums=resvNums, userId=userId, name=name, loc=loc)



@app.route('/hotel/delete/<int:id>')
def hotel_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    h = hotels.query.get(id)
    reservations.query.filter(reservations.resvType == 'hotel').filter(
        reservations.resvId == h.id).delete()
    db.session.delete(h)
    db.session.commit()
    return redirect(url_for('hotel_page'))


@app.route('/hotel/edit/<int:id>', methods=['POST', 'GET'])
def hotel_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = HotelForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                h = hotels(form)
            else:
                h = hotels.query.get(id)
                delta = form['roomNum'].data - (h.roomNum - h.avaiNum)
                if delta < 0:
                    flash('座位数小于已预订数')
                    return render_template('hotel_edit.html', form=form, userId=session['user_id'], name=session['user_name'])
                h.update(form)
            db.session.add(h)
            db.session.commit()
            return redirect(url_for('hotel_page'))
    return render_template('hotel_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/attraction')
def attraction_page():
    userId = 0
    name = ''
    resvNums = {}
    if session.get('logged_in'):
        userId = session['user_id']
        name = session['user_name']
        rs = reservations.query.filter(reservations.custId == userId, reservations.resvType == 'attraction').all()
        resvNums = {r.resvId: r.resvNum for r in rs}
    if request.args.get('location'):
        loc = request.args.get('location')
        a = attractions.query.filter(attractions.hotelLoca.like('%' + loc + '%')).all()
    else:
        loc = ''
        a = attractions.query.all()
    return render_template('attraction.html', attractions=a, resvNums=resvNums, userId=userId, name=name, loc=loc)



@app.route('/attraction/delete/<int:id>')
def attraction_delete(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    a = attractions.query.get(id)
    reservations.query.filter(reservations.resvType == 'attraction').filter(
        reservations.resvId == a.id).delete()
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('attraction_page'))


@app.route('/attraction/edit/<int:id>', methods=['POST', 'GET'])
def attraction_edit(id):
    if not session.get('logged_in'):
        abort(404)
    if session['user_id'] > 1:
        abort(401)

    form = AtttactionForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if id == 0:
                a = attractions(form)
            else:
                a = attractions.query.get(id)
                a.update(form)
            db.session.add(a)
            db.session.commit()
            return redirect(url_for('attraction_page'))
    return render_template('attraction_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/reservation/<int:id>')
def reservation_page(id):
    if not session.get('logged_in'):
        flash('请登录后查看~')
        return redirect(url_for('login'))

    userId = session['user_id']
    name = session['user_name']
    if userId > 1:
        r = reservations.query.filter(reservations.custId == userId).all()
    else:
        if id > 0:
            r = reservations.query.filter(reservations.custId == id).all()
        else:
            r = reservations.query.all()
    return render_template('reservation.html', reservations=r, userId=userId, name=name)


@app.route('/reservation/add/<int:type>/<int:id>/<int:add>/', methods=['POST', 'GET'])
def reservation_add(type, id, add):
    add = 1 - add
    if not session.get('logged_in'):
        flash('请登录后查看~')
        return redirect(url_for('login'))

    # if request.method == 'POST':
    custId = session['user_id']

    if type == 0:
        resvType = 'flight'
        f = flights.query.get(id)
        if not f:
            abort(404)

        f.avaiNum -= add
        db.session.add(f)
    elif type == 1:
        resvType = 'train'
        t = trains.query.get(id)
        if not t:
            abort(404)
        t.avaiNum -= add
        db.session.add(t)
    elif type == 2:
        resvType = 'hotel'
        h = hotels.query.get(id)
        if not h:
            abort(404)
        h.avaiNum -= add
        db.session.add(h)
    elif type == 3:
        resvType = 'attraction'
        a = attractions.query.get(id)
        if not a:
            abort(404)
    else:
        return abort(404)

    r = reservations.query.filter(reservations.custId == custId,
                                  reservations.resvId == id,
                                  reservations.resvType == resvType).first()

    if r == None and add == 1:
        r = reservations(custId, id, resvType)
    elif r:
        r.resvNum += add
    else:
        abort(404)

    # db.session.commit()
    if r.resvNum == 0:
        db.session.delete(r)
    else:
        db.session.add(r)
    db.session.commit()
    return redirect(url_for(resvType + '_page'))


@app.route('/reservation/delete/<int:id>')
def reservation_delete(id):
    if not session.get('logged_in'):
        abort(404)

    r = reservations.query.get(id)
    if r:
        if r.custId == session['user_id']:
            r.delete()
            db.session.commit()
    return redirect(url_for('reservation_page',id=0))


@app.route('/customer')
def customer_page():
    if not session.get('logged_in'):
        flash('请登录后查看~')
        return redirect(url_for('login'))

    userId = session['user_id']
    name = session['user_name']
    if userId == 1:
        if request.args.get('sname'):
            sname = request.args.get('sname')
            c = customers.query.filter(customers.custName.like('%' + sname + '%')).all()
        else:
            sname = ''
            c = customers.query.all()
        return render_template('customer.html', customers=c, sname=sname, name=name, userId=1)
    c = customers.query.get(userId)
    return render_template('customer.html', customers=c, name=name,userId=userId)



@app.route('/customer/edit/<int:id>', methods=['POST', 'GET'])
def customer_edit(id):
    if not session.get('logged_in'):
        flash('您还没有登录，请先登录帐号！')
        abort(401)
    c = customers.query.get(id)
    form = CustomerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            c.custName = form['custName'].data
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('customer_page'))
    return render_template('customer_edit.html', form=form, userId=session['user_id'], name=session['user_name'])


@app.route('/customer/delete/<int:id>')
def customer_delete(id):
    if not session.get('logged_in'):
        flash('您还没有登录，请登录管理员帐号删除！')
        abort(401)
    if session['user_id'] != 1:
        abort(404)
    c = customers.query.get(id)
    for r in reservations.query.filter(reservations.custid == id).all():
        r.delete()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('customer_page'))
