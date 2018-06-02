# -*- coding: utf-8 -*-
from app import db
import datetime

class branches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branchName = db.Column(db.String(40), unique=True)
    branchCity = db.Column(db.String(20))
    branchAsset = db.Column(db.Integer)

    def update(self, form):
        self.branchName = form['branchName'].data
        self.branchCity = form['branchCity'].data
        self.branchAsset = form['branchAsset'].data


class staffs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffId = db.Column(db.String(20), unique=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branches.id'), index=True)
    staffName = db.Column(db.String(20))
    staffPhone = db.Column(db.String(20))
    staffAddr = db.Column(db.String(40))
    EnterTime = db.Column(db.Date)
    managerId = db.Column(db.String(20))

    def update(self, form, branchId):
        self.staffId = form['staffId'].data
        self.branchId = branchId
        self.staffName = form['staffName'].data
        self.staffPhone = form['staffPhone'].data
        self.staffAddr = form['staffAddr'].data
        self.EnterTime = form['enterTime'].data
        self.managerId = form['managerId'].data


class depo_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.String(20), unique=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staffs.id'), index=True)
    balance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    visitTime = db.Column(db.DateTime)
    depoRate = db.Column(db.Float)
    depoType = db.Column(db.String(10))

    def __init__(self, accountId, staffId):
        # 不允许修改
        self.accountId = accountId
        self.staffId = staffId
        self.balance = 0.00
        self.openTime = datetime.datetime.now()
        self.visitTime = None

    def update_balance(self, add, money):
        self.balance += add * money
        self.visitTime = datetime.datetime.now()

    def update_info(self, depoRate, depoType):
        self.depoRate = depoRate
        self.depoType = depoType


class user_depo_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, db.ForeignKey('depo_accounts.id'), index=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branches.id'), index=True)

    __table_args__ =(
        db.UniqueConstraint('accountId', 'userId', name='con1'),
        db.UniqueConstraint('branchId', 'userId', name='con2'),
    )

    def __init__(self, accountId, userId, branchId):
        self.accountId = accountId
        self.userId = userId
        self.branchId = branchId


class check_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.String(20), unique=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staffs.id'), index=True)
    balance = db.Column(db.Float)
    openTime = db.Column(db.DateTime)
    visitTime = db.Column(db.DateTime)
    checkLimit = db.Column(db.Integer)

    def __init__(self, accountId, staffId):
        # 不允许修改
        self.accountId = accountId
        self.staffId = staffId
        self.balance = 0.00
        self.openTime = datetime.datetime.now()
        self.visitTime = None

    def update_balance(self, add, money):
        self.balance += add * money
        self.visitTime = datetime.datetime.now()

    def update_info(self, checkLimit):
        self.checkLimit = checkLimit


class user_check_accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, db.ForeignKey('check_accounts.id'), index=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branches.id'), index=True)

    __table_args__ =(
        db.UniqueConstraint('accountId', 'userId', name='con1'),
        db.UniqueConstraint('branchId', 'userId', name='con2'),
    )

    def __init__(self, accountId, userId, branchId):
        self.accountId = accountId
        self.userId = userId
        self.branchId = branchId


# class userCheckAcounts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     acountId = db.Column(db.Integer, db.ForeignKey('acounts.id'), index=True)
#     userId = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
#     openBranch = db.Column(db.String(20))
#     checkLimit = db.Column(db.Integer)
#
#     __table_args__ =(
#         db.UniqueConstraint('accountId', 'userId', name='con1'),
#         db.UniqueConstraint('openBranch', 'userId', name='con2'),
#     )
#
#     def update(self, form):
#         self.acountId = form['accountId'].data
#         self.userId = form['userId'].data
#         self.openBranch = form['openBranch'].data
#         self.checkLimit = form['checkLimit'].data


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(20), unique=True)
    userPhone = db.Column(db.String(20))
    userName = db.Column(db.String(20))
    userAddr = db.Column(db.String(40))
    linkRelation = db.Column(db.String(10))
    linkName = db.Column(db.String(20))
    linkPhone = db.Column(db.String(20))
    linkMail = db.Column(db.String(40))

    def update(self, form):
        self.userId = form['userId'].data
        self.userName = form['userName'].data
        self.userPhone = form['userPhone'].data
        self.userAddr = form['userAddr'].data
        self.linkRelation = form['linkRelation'].data
        self.linkName = form['linkName'].data
        self.linkPhone = form['linkPhone'].data
        self.linkMail = form['linkMail'].data


# 不允许修改
class loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branches.id'), index=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staffs.id'), index=True)
    loanId = db.Column(db.String(6), unique=True)
    loanStatus = db.Column(db.String(20))
    loanMoney = db.Column(db.Float)
    payMoney = db.Column(db.Float)

    def __init__(self, brachId, staffId, loanId, money):
        self.branchId = brachId
        self.staffId = staffId
        self.loanId = loanId
        self.loanMoney = money
        self.loanStatus = '未开始发放'
        self.payMoney = 0.0


class userLoans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loanId = db.Column(db.Integer, db.ForeignKey('loans.id'), index=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    __table_args__ =(
        db.UniqueConstraint('loanId', 'userId', name='con1'),
    )

    def __init__(self, loanId, userId):
        self.loanId = loanId
        self.userId = userId


class payLoans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loanId = db.Column(db.Integer, db.ForeignKey('loans.id'), index=True)
    payTime = db.Column(db.DateTime)
    payMoney = db.Column(db.Integer)

    def __init__(self, loanId, money):
        self.loanId = loanId
        self.payMoney = money
        self.payTime = datetime.datetime.now()


class branch_records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branches.id'))
    opType = db.Column(db.String(4))
    opTime = db.Column(db.Date)
    opMoney = db.Column(db.Float)

    def __init__(self, branchId, opMoney, opType):
        self.branchId = branchId
        self.opType = opType
        self.opTime = datetime.date.today()
        self.opMoney = opMoney

