# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash, abort
from sqlalchemy import extract
from app import app, db
from app.models import *
from app.forms import *
from random import randint

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/branch')
def branch_page():
    name, city, minAsset, maxAsset = '', '', '', ''
    bs = branches.query
    if request.args.get('name'):
        name = request.args.get('name')
        bs = bs.filter(branches.branchName.like('%' + name + '%'))
    if request.args.get('city'):
        city = request.args.get('city')
        bs = bs.filter(branches.branchCity.like('%' + city + '%'))
    if request.args.get('minAsset'):
        minAsset = request.args.get('minAsset')
        bs = bs.filter(branches.branchAsset >= int(minAsset))
    if request.args.get('maxAsset'):
        maxAsset = request.args.get('maxAsset')
        bs = bs.filter(branches.branchAsset <= int(maxAsset))
    return render_template('branch.html', branches=bs.all() ,name=name, city=city, minAsset=minAsset, maxAsset=maxAsset)


@app.route('/branch/edit/<int:id>', methods=['POST', 'GET'])
def branch_edit(id):
    if request.method == 'POST':
        form = branchForm(request.form)
        if form.validate_on_submit():
            if id == 0:
                b = branches()
                if branches.query.filter(branches.branchName==form.branchName.data).all():
                    flash('该支行已存在')
                    return render_template('branch_edit.html', form=branchForm())
            else:
                b = branches.query.get(id)
            b.update(form)
            db.session.add(b)
            db.session.commit()
            return redirect(url_for('branch_page'))
    else:
        form = branchForm()
        b = branches.query.get(id)
        if id and b:
            form.branchName.data = b.branchName
            form.branchCity.data = b.branchCity
            form.branchAsset.data = b.branchAsset
        return render_template('branch_edit.html', form=form)


@app.route('/branch/delete/<int:id>')
def branch_delete(id):

    b = branches.query.get(id)
    if not b:
        flash('没有该支行的信息，无法删除。')
    else:
        s = staffs.query.filter(staffs.branchId == id).all()
        uda = user_depo_accounts.query.filter(user_depo_accounts.branchId == id).all()
        uca = user_check_accounts.query.filter(user_check_accounts.branchId == id).all()
        if s or uda or uca:
            flash('存在该支行的关联信息，无法删除。')
            return redirect(url_for('branch_page'))
        br = branch_records.query.filter(branch_records.branchId==id).first()
        if br:
            db.delete(br)
        db.session.delete(b)
        db.session.commit()
    return redirect(url_for('branch_page'))


@app.route('/staff')
def staff_page():
    name, idCard, branchName, managerId = '', '', '', ''
    ss = staffs.query
    if request.args.get('branchName'):
        branchName = request.args.get('branchName')
        b = branches.query.filter(branches.branchName == branchName).first()
        if not b:
            flash('支行名不存在')
            return render_template('staff.html', staffs=ss.all(), bnames=None, name=name,
                                   idCard='', branchName='', managerId='')
        ss = ss.filter(staffs.branchId == b.id)
    if request.args.get('name'):
        name = request.args.get('name')
        ss = ss.filter(staffs.staffName.like('%' + name + '%'))
    if request.args.get('idCard'):
        idCard = request.args.get('idCard')
        ss = ss.filter(staffs.staffId.like('%' + idCard + '%'))
    if request.args.get('managerId'):
        managerId = request.args.get('managerId')
        ss = ss.filter(staffs.managerId.like('%' + managerId + '%'))
    bnames = {each.branchId: branches.query.get(each.branchId).branchName for each in ss}
    return render_template('staff.html', staffs=ss.all(), bnames=bnames, name=name,
                           idCard=idCard, branchName=branchName, managerId=managerId)


@app.route('/staff/edit/<int:id>', methods=['POST', 'GET'])
def staff_edit(id):
    if request.method == 'POST':
        form = staffForm(request.form)
        if form.validate_on_submit():
            if id == 0:
                s = staffs()
                if staffs.query.filter(staffs.staffId==form.staffId.data).all():
                    flash('该身份证对应员工已存在')
                    return render_template('staff_edit.html', form=form)
            else:
                s = staffs.query.get(id)
            b = branches.query.filter(branches.branchName == form.branchName.data).first()
            if not b:
                flash('支行名不存在')
                return render_template('staff_edit.html', form=form)
            s.update(form, b.id)
            db.session.add(s)
            db.session.commit()
        return redirect(url_for('staff_page'))

    else:
        form = staffForm()
        s = staffs.query.get(id)
        if id and s:
            form.staffId.data = s.staffId
            form.staffName.data = s.staffName
            b = branches.query.get(s.branchId)
            form.branchName.data = b.branchName
            form.staffPhone.data = s.staffPhone
            form.staffAddr.data = s.staffAddr
            form.managerId.data = s.managerId
        return render_template('staff_edit.html', form=form)


@app.route('/staff/delete/<int:id>')
def staff_delete(id):
    s = staffs.query.get(id)
    if not s:
        flash('没有该员工的信息，无法删除。')
    else:
        l = loans.query.filter(loans.staffId == id).all()
        da = depo_accounts.query.filter(depo_accounts.staffId == id).all()
        ca = check_accounts.query.filter(check_accounts.staffId == id).all()
        if l or da or ca:
            flash('存在该员工的关联信息，无法删除。')
        db.session.delete(l)
        db.session.commit()
    return redirect(url_for('staff_page'))


@app.route('/user')
def user_page():
    name, idCard, linkName = '', '', ''
    us = users.query
    if request.args.get('name'):
        name = request.args.get('name')
        us = us.filter(users.userName.like('%' + name + '%'))
    if request.args.get('linkName'):
        linkName = request.args.get('linkName')
        us = us.filter(users.userName.like('%' + linkName + '%'))
    if request.args.get('idCard'):
        idCard = request.args.get('idCard')
        us = us.filter(users.userId.like('%' + idCard + '%'))
    return render_template('user.html', users=us.all(), name=name,
                           idCard=idCard, linkName=linkName)


@app.route('/user/edit/<int:id>', methods=['POST', 'GET'])
def user_edit(id):
    if request.method == 'POST':
        form = userForm(request.form)
        if form.validate_on_submit():
            if id == 0:
                u = users()
                if users.query.filter(users.userId==form.userId.data).all():
                    flash('该身份证对应客户已存在')
                    return render_template('user_edit.html', form=form)
            else:
                u = users.query.get(id)
            u.update(form)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('user_page'))

    else:
        form = userForm()
        u = users.query.get(id)
        if id and u:
            form.userId.data = u.userId
            form.userName.data = u.userName
            form.userPhone.data = u.userPhone
            form.userAddr.data = u.userAddr
            form.linkRelation.data = u.linkRelation
            form.linkName.data = u.linkName
            form.linkPhone.data = u.linkPhone
            form.linkMail.data = u.linkMail
        return render_template('user_edit.html', form=form)


@app.route('/user/delete/<int:id>')
def user_delete(id):
    u = users.query.get(id)
    if not u:
        flash('没有该客户的信息，无法删除。')
    else:
        ul = userLoans.query.filter(userLoans.userId == id).all()
        uda = user_depo_accounts.query.filter(user_depo_accounts.userId == id).all()
        uca = user_check_accounts.query.filter(user_check_accounts.userId == id).all()
        if ul or uda or uca:
            flash('存在该客户的关联信息，无法删除。')
        db.session.delete(u)
        db.session.commit()
    return redirect(url_for('user_page'))


# 账户类型 账户号码 负责员工姓名 余额 开户时间 最近访问时间 开户支行
# 查询：账户类型，开户支行，负责员工。。。。。
# 操作：增加用户，删除，存取款操作，编辑(账户号不能更改) （共有客户 no账户记录）
@app.route('/account')
def account_page():
    if request.args.get('Id') and request.args.get('Name'):
        # get的输入不能为空
        aid = request.args.get('aid')
        userId = request.args.get('Id')
        userName = request.args.get('Name')

        u = users.query.filter(users.userId == userId).first()
        aType = aid[0]
        if aType == '0':
            aid = int(str(aid)[1:])
            ua = user_depo_accounts.query.filter(user_depo_accounts.userId == u.id,
                                                 user_depo_accounts.accountId == aid).first()
            a = depo_accounts.query.get(aid)
        else:
            aid = int(str(aid)[1:])
            ua = user_check_accounts.query.filter(user_check_accounts.userId == u.id,
                                                  user_check_accounts.accountId == aid).first()
            a = check_accounts.query.get(aid)

        if not u or not a or u.userName != userName:
            flash('没有找到该客户的信息，请先在客户管理中注册' if not u else '该账户不存在' if not a
            else '客户姓名与身份证不匹配，请姓名检查是否为' + u.userName)
            return redirect(url_for('account_page'))
        if ua:
            flash('该客户已经存在该账户中')
            return redirect(url_for('account_page'))

        if aType == '0':
            bid = user_depo_accounts.query.filter(user_depo_accounts.accountId==aid).first().branchId
            ua = user_depo_accounts(aid, u.id, bid)
            flag = user_depo_accounts.query.filter(user_depo_accounts.userId==u.id and
                                                   user_depo_accounts.branchId==bid).first()
        else:
            bid = user_check_accounts.query.filter(user_check_accounts.accountId==aid).first().branchId
            ua = user_check_accounts(aid, u.id, bid)
            flag = user_check_accounts.query.filter(user_check_accounts.userId==u.id and
                                                   user_check_accounts.branchId==bid).first()
        if flag:
            flash('一个支行仅允许用户开设一个账户')
            return redirect(url_for('account_page'))
        db.session.add(ua)
        db.session.commit()
        return redirect(url_for('account_page'))



    account_dict = {'accountId': '', 'branchame': '', 'staffName': '', 'userName': '', 'balance': '',
                    'accountType': '', 'depoRate':'', 'depoType':'', 'checkLimit':''}
    das = depo_accounts.query
    cas = check_accounts.query
    error = False

    if request.args.get('branchName'):
        account_dict['branchName'] = request.args.get('branchName')
        # 可以改为模糊查询
        b = branches.query.filter(branches.branchName == account_dict['branchName']).first()
        if not b:
            flash('支行名不存在')
            error = True
        else:
            aids = [uda.accountId for uda in user_depo_accounts.query.filter(user_depo_accounts.branchId==b.id).all()]
            das = das.filter(depo_accounts.id.in_(aids))
            cas = cas.filter(check_accounts.id.in_(aids))

    if request.args.get('accountId') and not error:
        account_dict['accountId'] = request.args.get('accountId')
        das = das.filter(depo_accounts.accountId.like('%' + account_dict['accountId'] + '%'))
        cas = cas.filter(check_accounts.accountId.like('%' + account_dict['accountId'] + '%'))

    if request.args.get('staffName') and not error:
        account_dict['staffName'] = request.args.get('staffName')
        # 可改为模糊查询
        s = staffs.query.filter(staffs.staffName == account_dict['staffName']).first()
        if not s:
            flash('员工不存在')
            error = True
        else:
            das = das.filter(depo_accounts.staffId == s.id)
            cas = cas.filter(check_accounts.staffId == s.id)

    if request.args.get('userName') and not error:
        account_dict['userName'] = request.args.get('userName')
        uns = account_dict['userName'].split()
        # 可改为模糊查询
        us = users.query.filter(users.userName.in_(uns)).all()
        if not us:
            flash('客户不存在')
            error =True
        else:
            uids = [u.id for u in us]
            l1, l2 = [], []
            for uid in uids:
                l1.append(set([uda.accountId for uda in user_depo_accounts.query.filter(user_depo_accounts.userId == uid).all()]))
                l2.append(set([uca.accountId for uca in user_check_accounts.query.filter(user_check_accounts.userId == uid).all()]))
            daids = l1[0] if l1 != [] else None
            caids = l2[0] if l2 != [] else None
            for i in range(1, len(l1)):
                daids = daids & l1[i]
            for i in range(1, len(l2)):
                caids = caids & l2[i]
            if daids:
                das = das.filter(depo_accounts.id.in_(list(daids)))
            if caids:
                cas = cas.filter(check_accounts.id.in_(list(caids)))

    tag = 0
    if request.args.get('accountType') and not error:
        account_dict['accountType'] = request.args.get('accountType')
        if account_dict['accountType'] == 'depo':
            tag = 1
        elif account_dict['accountType'] == 'check':
            tag = 2

    if request.args.get('balance') and not error:
        account_dict['balance'] = request.args.get('balance')
        das = das.filter(depo_accounts.balance >= float(account_dict['balance']))
        cas = cas.filter(check_accounts.balance >= float(account_dict['balance']))

    if request.args.get('depoRate') and not error:
        account_dict['depoRate'] = request.args.get('depoRate')
        das = das.filter(depo_accounts.depoRate >= float(account_dict['depoRate']))

    if request.args.get('depoType') and not error:
        account_dict['depoType'] = request.args.get('depoType')
        das = das.filter(depo_accounts.depoType == account_dict['depoType'])

    if request.args.get('checkLimit') and not error:
        account_dict['checkLimit'] = request.args.get('checkLimit')
        das = das.filter(check_accounts.checkLimit >= int(account_dict['checkLimit']))

    unames_da = {da.id: ','.join(
        [users.query.get(u.userId).userName for u in
         user_depo_accounts.query.filter(user_depo_accounts.accountId == da.id).all()])
        for da in das}
    unames_ca = {ca.id: ','.join(
        [users.query.get(u.userId).userName for u in
         user_check_accounts.query.filter(user_check_accounts.accountId == ca.id).all()])
        for ca in cas}

    bnames_da = {da.id: branches.query.get
    (user_depo_accounts.query.filter(user_depo_accounts.accountId == da.id).first().branchId).branchName for da in das}
    bnames_ca = {ca.id: branches.query.get
    (user_check_accounts.query.filter(user_check_accounts.accountId == ca.id).first().branchId).branchName for ca in cas}
    snames_da = {da.id: staffs.query.get(da.staffId).staffName for da in das}
    snames_ca = {ca.id: staffs.query.get(ca.staffId).staffName for ca in cas}

    return render_template('account.html', cas=cas.all() if tag != 1 else [], das=das.all() if tag != 2 else [], unames_ca=unames_ca, bnames_ca=bnames_ca,
                           snames_ca=snames_ca,
                           unames_da=unames_da, bnames_da=bnames_da, snames_da=snames_da, account_dict=account_dict)



@app.route('/account/edit/<int:id>/<int:atype>', methods=['POST', 'GET'])
def account_edit(id, atype):
    if request.method == 'POST':
        accountType = request.form['accountType']
        if accountType == '0':
            depoRate = request.form['depoRate']
            depoType = request.form['depoType']
            checkLimit = ''
        else:
            depoRate = ''
            depoType = ''
            checkLimit = request.form['checkLimit']

        if id == 0:
            branchName = request.form['branchName']
            staffName = request.form['staffName']
            userName = request.form['userName']
            accountId = ''

            while True:
                for i in range(6):
                    accountId += str(randint(0, 9))
                if (accountType == '0' and not depo_accounts.query.filter(depo_accounts.accountId == accountId).all())\
                    or (accountType == '1' and not check_accounts.query.filter(check_accounts.accountId == accountId).all()):
                    break
                accountId = ''

            b = branches.query.filter(branches.branchName == branchName).first()
            s = staffs.query.filter(staffs.staffName == staffName).first()
            u = users.query.filter(users.userName == userName).first()
            uca = user_check_accounts.query.filter(user_check_accounts.branchId == b.id and user_check_accounts.userId == u.id).first()

            if not b or not s or not u or b.id != s.branchId:
                flash('支行名不存在' if not b else '员工不存在' if not s else '客户不存在' if not u else '该支行中没有该员工')
                return render_template('account_edit.html', branchName=branchName, staffName=staffName, accountType='2',
                                       depoRate=depoRate, depoType=depoType, checkLimit=checkLimit, aid=id, atype=atype)
            if accountType == '0':
                a = depo_accounts(accountId, s.id)
                a.update_info(float(depoRate), depoType)
                if user_depo_accounts.query.filter(user_depo_accounts.branchId == b.id and user_depo_accounts.userId == u.id).first():
                    flash('一个支行仅允许每个用户有一个储蓄账户！')
                    return render_template('account_edit.html', branchName=branchName, staffName=staffName, accountType='2',
                                            depoRate=depoRate, depoType=depoType, checkLimit=checkLimit, aid=id, atype=atype)
                db.session.add(a)
                db.session.commit()
                ua = user_depo_accounts(depo_accounts.query.filter(depo_accounts.accountId==accountId).first().id, u.id, b.id)
                db.session.add(ua)
                db.session.commit()

            else:
                a = check_accounts(accountId, s.id)
                a.update_info(int(checkLimit))
                if user_check_accounts.query.filter(user_check_accounts.branchId == b.id and user_check_accounts.userId == u.id).first():
                    flash('一个支行仅允许每个用户有一个支票账户！')
                    return render_template('account_edit.html', branchName=branchName, staffName=staffName, accountType='2',
                                            depoRate=depoRate, depoType=depoType, checkLimit=checkLimit, aid=id, atype=atype)
                db.session.add(a)
                db.session.commit()
                ua = user_check_accounts(check_accounts.query.filter(check_accounts.accountId==accountId).first().id, u.id, b.id)
                db.session.add(ua)
                db.session.commit()

        else:
            if accountType == '0':
                a = depo_accounts.query.get(id)
                a.update_info(depoRate, depoType)
            else:
                a = check_accounts.query.get(id)
                a.update_info(checkLimit)

            db.session.add(a)
            db.session.commit()
        return redirect(url_for('account_page'))

    else:
        a = depo_accounts.query.get(id) if atype == 0 else check_accounts.query.get(id)
        depoRate, depoType, checkLimit = '', '', ''
        if atype == 0:
            depoRate = a.depoRate
            depoType = a.depoType
        elif atype == 1:
            checkLimit = a.checkLimit
        return render_template('account_edit.html', branchName='', staffName='', accountType=str(atype),
                               depoRate=depoRate, depoType=depoType, checkLimit=checkLimit, aid=id, atype=atype)



@app.route('/account/op/<int:id>/<int:atype>/', methods=['POST', 'GET'])
def account_op(id, atype):
    if request.method == 'POST':
        a = depo_accounts.query.get(id) if atype == 0 else check_accounts.query.get(id)
        add = int(request.form['add'])
        money = float(request.form['money'])
        if add < 0 and money > a.balance:
            flash('余额不足，取款失败')
            return render_template('account_op.html', id=id, atype=atype)
        if atype == 0:
            opType = '存款' if add > 0 else '取款'
            branchId = user_depo_accounts.query.filter(user_depo_accounts.accountId==id).first().branchId
            br = branch_records(branchId, money, opType)
            db.session.add(br)
        a.update_balance(add, money)
        a.visitTime = datetime.datetime.now()
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('account_page'))

    return render_template('account_op.html', id=id, atype=atype)


@app.route('/account/delete/<int:id>/<int:atype>')
def account_delete(id, atype):
    a = depo_accounts.query.get(id) if atype == 0 else check_accounts.query.get(id)
    if not a:
        flash('没有该账户的信息，无法删除。')
    else:
        if atype == 0:
            uas = user_depo_accounts.query.filter(user_depo_accounts.accountId==id)
        else:
            uas = user_check_accounts.query.filter(user_check_accounts.accountId==id)
        for ua in uas:
            db.session.delete(ua)
        db.session.delete(a)
        db.session.commit()
        flash('删除成功')
    return redirect(url_for('account_page'))














# 展示：贷款号，发放支行，负责员工，贷款金额，发放状态，（共有客户，支付详情）
# 查询：贷款号，发放支行名，负责员工姓名，客户所有，3种状态，金额范围？
# 增加用户。 删除 状态更改 共有客户详情(loan_page)。 支付详情(loan_pay)
@app.route('/loan')
def loan_page():

    if request.args.get('Id') and request.args.get('Name'):
        # get的输入不能为空
        id = request.args.get('lid')
        userId = request.args.get('Id')
        userName = request.args.get('Name')
        u = users.query.filter(users.userId == userId).first()
        l = loans.query.get(id)
        if not u or not l or u.userName != userName:
            flash('没有找到该客户的信息，请先在客户管理中注册' if not u else '该贷款项不存在' if not l
            else '客户姓名与身份证不匹配，请姓名检查是否为' + u.userName)
            return redirect(url_for('loan_page'))
        if userLoans.query.filter(userLoans.userId==u.id, userLoans.loanId==id).all():
            flash('该客户已经存在该贷款项中')
            return redirect(url_for('loan_page'))
        print 'ojbk'
        ul = userLoans(id, u.id)
        db.session.add(ul)
        db.session.commit()
        return redirect(url_for('loan_page'))

    loan_dict = {'loanId':'', 'branchame':'', 'staffName':'', 'userName':'', 'loanMoney':'', 'loanStatus':''}
    ls = loans.query

    if request.args.get('branchName'):
        loan_dict['branchName'] = request.args.get('branchName')
        # 可以改为模糊查询
        b = branches.query.filter(branches.branchName == loan_dict['branchName']).first()
        if not b:
            flash('支行名不存在')
            unames = {l.id: ','.join(
                [users.query.get(u.userId).userName for u in userLoans.query.filter(userLoans.loanId == l.id).all()])
                      for l in ls}
            bnames = {l.id: branches.query.get(l.branchId).branchName for l in ls}
            snames = {l.id: staffs.query.get(l.staffId).staffName for l in ls}
            return render_template('loan.html', loans=ls.all(), unames=unames, bnames=bnames, snames=snames,
                                   loan_dict=loan_dict)
        ls = ls.filter(loans.branchId == b.id)

    if request.args.get('loanId'):
        loan_dict['loanId'] = request.args.get('loanId')
        ls = ls.filter(loans.loanId.like('%' + loan_dict['loanId'] + '%'))

    if request.args.get('staffName'):
        loan_dict['staffName'] = request.args.get('staffName')
        # 可改为模糊查询
        s = staffs.query.filter(staffs.staffName == loan_dict['staffName']).first()
        if not s:
            flash('员工不存在')
            unames = {l.id: ','.join(
                [users.query.get(u.userId).userName for u in userLoans.query.filter(userLoans.loanId == l.id).all()])
                      for l in ls}
            bnames = {l.id: branches.query.get(l.branchId).branchName for l in ls}
            snames = {l.id: staffs.query.get(l.staffId).staffName for l in ls}
            return render_template('loan.html', loans=ls.all(), unames=unames, bnames=bnames, snames=snames,
                                   loan_dict=loan_dict)
        ls = ls.filter(loans.staffId == s.id)

    if request.args.get('userName'):
        loan_dict['userName'] = request.args.get('userName')
        uns = loan_dict['userName'].split()
        # 可改为模糊查询
        us = users.query.filter(users.userName.in_(uns)).all()
        if not us:
            flash('客户不存在')
            unames = {l.id: ','.join(
                [users.query.get(u.userId).userName for u in userLoans.query.filter(userLoans.loanId == l.id).all()])
                      for l in ls}
            bnames = {l.id: branches.query.get(l.branchId).branchName for l in ls}
            snames = {l.id: staffs.query.get(l.staffId).staffName for l in ls}
            return render_template('loan.html', loans=ls.all(), unames=unames, bnames=bnames, snames=snames,
                                   loan_dict=loan_dict)
        uids = [u.id for u in us]
        l = []
        for uid in uids:
          l.append(set([ul.loanId for ul in userLoans.query.filter(userLoans.userId == uid).all()]))
        lids = l[0]
        for i in range(1, len(l)):
            lids = lids & l[i]
        ls = ls.filter(loans.id.in_(list(lids)))
    if request.args.get('loanStatus'):
        loan_dict['loanStatus'] = request.args.get('loanStatus')
        if loan_dict['loanStatus'] != 'all':
            ls = ls.filter(loans.loanStatus == loan_dict['loanStatus'])

    if request.args.get('loanMoney'):
        loan_dict['loanMoney'] = request.args.get('loanMoney')
        ls = ls.filter(loans.loanMoney >= float(loan_dict['loanMoney']))

    unames = {l.id:','.join([users.query.get(u.userId).userName for u in userLoans.query.filter(userLoans.loanId==l.id).all()]) for l in ls}
    bnames = {l.id:branches.query.get(l.branchId).branchName for l in ls}
    snames = {l.id:staffs.query.get(l.staffId).staffName for l in ls}
    return render_template('loan.html', loans=ls.all(), unames=unames, bnames=bnames, snames=snames, loan_dict=loan_dict)


@app.route('/loan/edit/<int:id>', methods=['POST', 'GET'])
def loan_edit(id):
    if request.method == 'POST':
        form = loanForm(request.form)
        if form.validate_on_submit():
            if id == 0:
                loanId = ''
                while True:
                    for i in range(6):
                        loanId += str(randint(0, 9))
                    if not loans.query.filter(loans.loanId == loanId).all():
                        break
                    loanId = ''
                b = branches.query.filter(branches.branchName == form.branchName.data).first()
                s = staffs.query.filter(staffs.staffName == form.staffName.data).first()
                if not b or not s or b.id != s.branchId:
                    flash('支行名不存在' if not b else '员工不存在' if not s else '该支行中没有该员工')
                    return render_template('loan_edit.html', form=form)
                l = loans(b.id, s.id, loanId, form.loanMoney.data)
            else:
                flash('不允许修改贷款信息')
                return redirect(url_for('loan_page'))
            br = branch_records(b.id, form.loanMoney.data, '放贷')
            db.session.add(br)
            db.session.add(l)
            db.session.commit()
        return redirect(url_for('loan_page'))

    else:
        form = loanForm()
        return render_template('loan_edit.html', form=form)


@app.route('/loan/status/<int:id>')
def loan_status(id):
    l = loans.query.get(id)
    if not l:
        flash('该贷款项不存在')
        return redirect(url_for('loan_page'))
    if l.loanStatus == '未开始发放':
        l.loanStatus = '发放中'
    elif l.loanStatus == '发放中':
        l.loanStatus = '已全部发放'
    db.session.add(l)
    db.session.commit()
    return redirect(url_for('loan_page'))


@app.route('/loan/pay/<int:id>')
def loan_pay(id):
    l = loans.query.get(id)
    if not l:
        flash('该贷款项不存在')
        return redirect(url_for('loan_page'))
    if request.args.get('payMoney'):
        payMoney = min(l.loanMoney - l.payMoney, int(request.args.get('payMoney')))
        pl = payLoans(id, payMoney)
        l.payMoney += payMoney
        br = branch_records(l.branchId, payMoney, '还款')
        db.session.add(br)
        db.session.add(pl)
        db.session.add(l)
        db.session.commit()
        flash('成功还款￥' + str(payMoney))
    pls = payLoans.query.filter(payLoans.loanId == id).all()
    return render_template('loan_pay.html', pls=pls)

@app.route('/loan/delete/<int:id>')
def loan_delete(id):
    l = loans.query.get(id)
    if not l:
        flash('没有该贷款的信息，无法删除。')
    elif l.loanStatus == '发放中':
        flash('该贷款正在发放中，无法删除。')
    elif l.loanMoney - l.payMoney > 1e-2 and l.loanStatus == '已全部发放':
        flash('该贷款未还清，无法删除。')
    else:
        uls = userLoans.query.filter(userLoans.loanId == id)
        pls = payLoans.query.filter(payLoans.loanId == id)
        for ul in uls:
            db.session.delete(ul)
        for pl in pls:
            db.session.delete(pl)
        db.session.delete(l)
        db.session.commit()
        flash('删除成功')
    return redirect(url_for('loan_page'))


@app.route('/census/<int:id>')
def census_page(id):

    year = 0
    if request.args.get('year'):
        year = int(request.args.get('year'))

    if id == 0:
        userNums = {}
        totalMoneyIn1 = {}
        totalMoneyIn2 = {}
        totalMoneyOut1 = {}
        totalMoneyOut2 = {}

        bs = branches.query.all()
        for b in bs:
            ls = loans.query.filter(loans.branchId==b.id).all()
            temp = []
            for l in ls:
                temp += [ul.userId for ul in userLoans.query.filter(userLoans.loanId==l.id).all()]
            temp += [uda.userId for uda in user_depo_accounts.query.filter(user_depo_accounts.branchId==b.id).all()]
            userNums[b.id] = len(set(temp))

            brs = branch_records.query
            if year != 0:
                brs = brs.filter(extract('year', branch_records.opTime) == year)
            brs = brs.filter(branch_records.branchId==b.id)
            totalMoneyIn1[b.id] = sum([br.opMoney for br in brs.filter(branch_records.opType=='存款').all()])
            totalMoneyOut1[b.id] = sum([br.opMoney for br in brs.filter(branch_records.opType=='取款').all()])
            totalMoneyIn2[b.id] = sum([br.opMoney for br in brs.filter(branch_records.opType=='还款').all()])
            totalMoneyOut2[b.id] = sum([br.opMoney for br in brs.filter(branch_records.opType=='放贷').all()])

        return render_template('census.html',bs=bs, uns=userNums, mi1=totalMoneyIn1, mi2=totalMoneyIn2,
                               mo1=totalMoneyOut1, mo2=totalMoneyOut2, year = '')

    else:
        yearMoneyIn1 = [0] * 12
        yearMoneyIn2 = [0] * 12
        yearMoneyOut1 = [0] * 12
        yearMoneyOut2 = [0] * 12

        if year == 0:
            year = datetime.date.today().year
        b = branches.query.get(id)
        if not b:
            flash('没有该支行的信息！')
            return redirect(url_for('census_page',id=0))
        brs = branch_records.query.filter(branch_records.branchId == id).filter(extract('year', branch_records.opTime) == year)
        for month in range(1, 13):
            brs1 = brs.filter(extract('month', branch_records.opTime) == month)
            yearMoneyIn1[month - 1] = sum([br.opMoney for br in brs1.filter(branch_records.opType=='存款').all()])
            yearMoneyOut1[month - 1] = sum([br.opMoney for br in brs1.filter(branch_records.opType == '取款').all()])
            yearMoneyIn2[month - 1] = sum([br.opMoney for br in brs1.filter(branch_records.opType == '还款').all()])
            yearMoneyOut2[month - 1] = sum([br.opMoney for br in brs1.filter(branch_records.opType == '放贷').all()])

        return render_template('census.html', uns=0, bs=b, mi1=yearMoneyIn1, mi2=yearMoneyIn2,
                               mo1=yearMoneyOut1, mo2=yearMoneyOut2, year = str(year))