# -*- coding: utf-8 -*- 
from app import db
import datetime

class ads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adName = db.Column(db.String(20))
    adContent = db.Column(db.String(60))
    adPrice= db.Column(db.Integer)
    endTime = db.Column(db.DateTime)

    def __init__(self, form):
        self.adName = form['adName'].data
        self.adContent = form['adContnt'].data
        self.adPrice = form['adPrice'].data
        self.endTime = form['endTime'].data

    def update(self, form):
        self.adName = form['adName'].data
        self.adContent = form['adContnt'].data
        self.adPrice = form['adPrice'].data
        self.endTime = form['endTime'].data


class offs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offName = db.Column(db.String(20))
    offType = db.Column(db.String(20))
    offRate = db.Column(db.Integer)
    offNum = db.Column(db.Integer)
    avaiNum = db.Column(db.Integer)
    endTime = db.Column(db.DateTime)

    def __init__(self, form):
        self.offName = form['offName'].data
        self.offType = form['offType'].data
        self.offRate = form['offRate'].data
        self.offNum = form['offNum'].data
        self.avaiNum = form['offNum'].data
        self.endTime = form['endTime'].data

    def update(self, form):
        self.offRate = form['offRate'].data
        self.offNum = form['offNum'].data
        self.endTime = form['endTime'].data

class marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), db.ForeignKey('customers.userName'), index=True)
    markSocre = db.Column(db.Float, default=4.0, index=True)
    markContent = db.Column(db.String(60))
    markType = db.Column(db.String(20))
    markName = db.Column(db.String(20))
    # customer = db.relationship('customers', backref=db.backref('marks'))

    def __init__(self, form):
        self.userName = form['userName'].data
        self.markSocre = form['markScore'].data
        self.markContent = form['markContent'].data
        self.markType = form['markType'].data
        self.markName = form['markName'].data


class flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flightId = db.Column(db.String(20), index=True)
    seatType = db.Column(db.String(20))
    price = db.Column(db.Integer, index=True)
    seatNum = db.Column(db.Integer)
    avaiNum = db.Column(db.Integer)
    fromTime = db.Column(db.DateTime, index=True)
    arivTime = db.Column(db.DateTime, index=True)
    fromCity = db.Column(db.String(20), index=True)
    arivCity = db.Column(db.String(20), index=True)

    # __table_args__ =(
    #     db.UniqueConstraint('flightId', 'seatType', name='flight_id_type'),''
    # )

    def __init__(self, form):
        self.flightId = form['flightId'].data
        self.seatType = form['seatType'].data
        self.price = form['price'].data
        self.seatNum = form['seatNum'].data
        self.avaiNum = form['seatNum'].data
        self.fromTime = form['fromTime'].data
        self.arivTime = form['arivTime'].data
        self.fromCity = form['fromCity'].data
        self.arivCity = form['arivCity'].data

    def update(self, form):
        self.price = form['price'].data
        self.avaiNum += form['seatNum'].data - self.seatNum
        self.seatNum = form['seatNum'].data
        self.fromTime = form['fromTime'].data
        self.arivTime = form['arivTime'].data

    def offs(self):
        allOffs = offs.query.filter(offs.offName==self.flightId).all()
        info = {}
        info['offType'] = [off.offType for off in allOffs]
        info['endTime'] = [off.endTime for off in allOffs]
        info['offRate'] = [off.offRate for off in allOffs]
        return info


class trains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainId = db.Column(db.String(20), index=True)
    seatType = db.Column(db.String(20))
    price = db.Column(db.Integer, index=True)
    seatNum = db.Column(db.Integer)
    avaiNum = db.Column(db.Integer)
    fromTime = db.Column(db.DateTime, index=True)
    arivTime = db.Column(db.DateTime, index=True)
    fromCity = db.Column(db.String(20), index=True)
    arivCity = db.Column(db.String(20), index=True)

    # __table_args__ =(
    #     db.UniqueConstraint('trainId', 'seatType', name='train_id_type'),''
    # )

    def __init__(self, form):
        self.trainId = form['trainId'].data
        self.seatType = form['seatType'].data
        self.price = form['price'].data
        self.seatNum = form['seatNum'].data
        self.avaiNum = form['seatNum'].data
        self.fromTime = form['fromTime'].data
        self.arivTime = form['arivTime'].data
        self.fromCity = form['fromCity'].data
        self.arivCity = form['arivCity'].data

    def update(self, form):
        self.price = form['price'].data
        self.avaiNum += form['seatNum'].data - self.seatNum
        self.seatNum = form['seatNum'].data
        self.fromTime = form['fromTime'].data
        self.arivTime = form['arivTime'].data

    def offs(self):
        allOffs = offs.query.filter(offs.offName==self.trainId).all()
        info = {}
        info['offType'] = [off.offType for off in allOffs]
        info['endTime'] = [off.endTime for off in allOffs]
        info['offRate'] = [off.offRate for off in allOffs]
        return info


class hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotelName = db.Column(db.String(20))
    hotelLoca = db.Column(db.String(20), index=True)
    roomType = db.Column(db.String(20))
    price = db.Column(db.Integer, index=True)
    roomNum = db.Column(db.Integer)
    avaiNum = db.Column(db.Integer)
    hotelSocre = db.Column(db.Float, index=True)

    # __table_args__ =(
    #     db.UniqueConstraint('hotelName', 'roomType', name='hotel_name_type'), ''
    # )

    def __init__(self, form):
        self.hotelName = form['hotelName'].data
        self.hotelLoca = form['hotelLoca'].data
        self.roomType = form['roomType'].data
        self.price = form['price'].data
        self.roomNum = form['roomNum'].data
        self.avaiNum = form['roomNum'].data
        self.hotelSocre = 4.0

    def update(self, form):
        self.price = form['price'].data
        self.avaiNum += form['roomNum'].data - self.roomNum
        self.roomNum = form['roomNum'].data

    def contents(self):
        hotelMarks = marks.query.filter(marks.markName==self.hotelName, marks.markType=='hotel').all()
        return [mark.markContent for mark in hotelMarks]

    def offs(self):
        allOffs = offs.query.filter(offs.offName==self.hotelName).all()
        info = {}
        info['offType'] = [off.offType for off in allOffs]
        info['endTime'] = [off.endTime for off in allOffs]
        info['offRate'] = [off.offRate for off in allOffs]
        return info


class attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attrName = db.Column(db.String(20))
    attrLoca = db.Column(db.String(20), index=True)
    features = db.Column(db.String(40))
    ticType = db.Column(db.String(20))
    endTime = db.Column(db.DateTime, index=True)
    price = db.Column(db.Integer, index=True)
    attrSocre = db.Column(db.Float, default=0.0, index=True)

    # __table_args__ =(
    #     db.UniqueConstraint('attrName', 'ticType', name='attr_name_type'), ''
    # )

    def __init__(self, form):
        self.attrName = form['attrName'].data
        self.attrLoca = form['attrLoca'].data
        self.features = form['features'].data
        self.ticType = form['ticType'].data
        self.endTime = form['endTime'].data
        self.price = form['price'].data
        self.attrSocre = 4.0

    def update(self, form):
        self.features = form['features'].data
        self.endTime = form['endTime'].data
        self.price = form['price'].data

    def contents(self):
        attrMarks = marks.query.filter(marks.markName==self.attrName, marks.markType=='attractions').all()
        return [mark.markContent for mark in attrMarks]

    def offs(self):
        allOffs = offs.query.filter(offs.offName==self.attrName).all()
        info = {}
        info['offType'] = [off.offType for off in allOffs]
        info['endTime'] = [off.endTime for off in allOffs]
        info['offRate'] = [off.offRate for off in allOffs]
        return info


class customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, index=True)
    passWd = db.Column(db.String(20))
    custName = db.Column(db.String(20), unique=True)
    custSex = db.Column(db.String(4))
    custAge = db.Column(db.Integer)
    custPhone = db.Column(db.String(20))
    custAddr = db.Column(db.String(40))

    def __init__(self, form):
        self.userName = form['userName'].data
        self.passWd = form['passWd'].data
        self.custName = form['custName'].data
        self.custSex = form['custSex'].data
        self.custAge = form['custAge'].data
        self.custPhone = form['custPhone'].data
        self.custAddr = form['custAddr'].data

    def totalNum(self):
        rs = reservations.query.filter(reservations.custId==self.id).all()
        return len(rs)
    def totalCost(self):
        rs = reservations.query.filter(reservations.custId==self.id).all()
        return sum([r.price() for r in rs])

class myoffs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custId = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    offId = db.Column(db.Integer, db.ForeignKey('offs.id'), index=True)
    customer = db.relationship('customers', backref=db.backref('myoffs'))

    def __init__(self, custId, offId):
        self.custId = custId
        self.offId = offId


class reservations(db.Model):
    resvKey = db.Column(db.Integer, primary_key=True)
    custId = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    resvType = db.Column(db.Enum('flight', 'hotel', 'train', 'attraction'))
    resvId = db.Column(db.Integer)
    resvNum = db.Column(db.Integer, default=0)
    customer = db.relationship('customers', backref=db.backref('reservations'))

    # __table_args__ =(
    #     db.UniqueConstraint('custId', 'resvId', 'resvType', name='cust_resv_Id'), ''
    # )

    def __init__(self, custId, resvId, resvType):
        self.custId = custId
        self.resvType = resvType
        self.resvId = resvId
        self.resvNum = 1

    def type(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            return f.seatType
        elif self.resvType == 'train':
            t = trains.query.get(self.resvId)
            return t.seatType
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvId)
            return h.roomType
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            return a.ticType

    def name(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            return f.flightId
        elif self.resvType == 'train':
            t = trains.query.get(self.resvId)
            return t.trainId
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvId)
            return h.hotelName
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            return a.attrName

    def location(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            return f.fromCity + '->' + f.arivCity
        elif self.resvType == 'train':
            t = trains.query.get(self.resvId)
            return t.fromCity + '->' + t.arivCity
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvId)
            return h.hotelLoca
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            return a.attrLoca
        # elif self.resvType == 'car':
        #     c = cars.query.get(self.resvid)
        #     return c.location

    def time(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            return f.fromTime.strftime("%Y-%m-%d %H:%M") + '~' + f.arivTime.strftime("%Y-%m-%d %H:%M")
        elif self.resvType == 'train':
            t = trains.query.get(self.resvId)
            return t.fromTime.strftime("%Y-%m-%d %H:%M") + '~' + t.arivTime.strftime("%Y-%m-%d %H:%M")
        elif self.resvType == 'hotel':
            return "Any time accessed."
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            return 'now ~' + a.endTime.strftime("%Y-%m-%d %H:%M")

    def price(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            return f.price
        elif self.resvType == 'train':
            t = trains.query.get(self.resvId)
            return t.price
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvId)
            return h.price
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            return a.price
        # elif self.resvType == 'car':
        #     c = cars.query.get(self.resvid)
        #     return c.price

        # def type(self):
        # return {'flight': '航班', 'hotel': '宾馆', 'train': '火车', 'attraction': '景点'}[self.resvType]

    def delete(self):
        if self.resvType == 'flight':
            f = flights.query.get(self.resvId)
            f.avaiNum += self.resvNum
            db.session.add(f)
        elif self.resvType == 'train':
            h = trains.query.get(self.resvId)
            h.avaiNum += self.resvNum
            db.session.add(h)
        elif self.resvType == 'hotel':
            h = hotels.query.get(self.resvId)
            h.avaiNum += self.resvNum
            db.session.add(h)
        elif self.resvType == 'attraction':
            a = attractions.query.get(self.resvId)
            db.session.add(a)
        # elif self.resvType == 'car':
        #     c = cars.query.get(self.resvid)
        #     c.numAvail += 1
        #     db.session.add(c)
        db.session.delete(self)
