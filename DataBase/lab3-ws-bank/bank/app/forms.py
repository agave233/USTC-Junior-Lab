# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

# name = StringField(validators=[Required()],render_kw={"placeholder": "your name","style":"width:300px"})

# {% block content %}
# <form method='post'>
#   {{ wtf.form_field(form.title) }}
#   {{ wtf.form_field(form.author) }}
# </form>
# {% endblock %}

class branchForm(FlaskForm):
    branchName = StringField('支行名', validators=[InputRequired(message="支行名不能为空")])
    # InputRequired(message="no kong"), NumberRange(min=1, max=9999)]
    branchCity = StringField('所在城市', validators=[InputRequired(message="城市不能为空")])
    branchAsset= IntegerField('资产', validators=[InputRequired(message="资产不能为空"), NumberRange(1)])
    submit_btn = SubmitField('提交')

class staffForm(FlaskForm):
    staffId = StringField('员工身份证', validators=[DataRequired(message="身份证不能为空")])
    staffName = StringField('员工姓名', validators=[DataRequired(message="姓名不能为空")])
    branchName = StringField('所在支行', validators=[DataRequired(message="支行名不能为空")])
    staffPhone = StringField('手机号', validators=[DataRequired(message="手机号不能为空")])
    staffAddr = StringField('地址', validators=[DataRequired(message="地址不能为空")])
    enterTime = DateField('入职时间', validators=[DataRequired(message="时间不能为空")])
    managerId = StringField('经理身份证', validators=[DataRequired(message="身份证不能为空")])
    submit_btn = SubmitField('提交')

# class depoAccountForm(FlaskForm):
#     staffName = StringField('账户负责员工姓名', validators=[InputRequired(message="姓名不能为空")])
#     branchName = StringField('开户支行名', validators=[InputRequired(message="支行名不能为空")])
#     depoRate =

# 开新卡：账户负责员工姓名，开户支行名，开户人身份证（可能有多个），类型<choice>，2 or 1
# 增加用户到老卡：账户类型<choice>，账户卡号，身份证
# 存取钱：卡号，选择<choice>，钱多少
# 更新：类型<choice>，卡号，2 or 1

class userForm(FlaskForm):
    userId = StringField('客户身份证', validators=[InputRequired(message="身份证不能为空"), Length(18, 18)])
    userName = StringField('客户姓名', validators=[InputRequired(message="姓名不能为空")])
    userPhone = StringField('客户手机号', validators=[InputRequired(message="手机号不能为空"), Length(11, 11)])
    userAddr = StringField('客户地址', validators=[InputRequired(message="地址不能为空")])
    linkName = StringField('联系人姓名')
    linkRelation = StringField('与客户的关系')
    linkPhone = StringField('联系人手机号', validators=[Length(0, 11)])
    linkMail = StringField('联系人邮箱', validators=[Email(message="请输入正确格式的邮箱")])
    submit_btn = SubmitField('提交')


class loanForm(FlaskForm):
    branchName = StringField('发放贷款支行名', validators=[InputRequired(message="支行名不能为空")])
    staffName = StringField('负责员工姓名', validators=[InputRequired(message="姓名不能为空")])
    loanMoney = FloatField('贷款金额', validators=[InputRequired(message="金额不能为空"), NumberRange(1)])
    submit_btn = SubmitField('提交')
