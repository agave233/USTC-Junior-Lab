# -*- coding: utf-8 -*- 
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, NumberRange


class AdForm(FlaskForm):
    adName = StringField('活动名称', validators=[DataRequired()])
    adContnt = StringField('内容信息', validators=[DataRequired()])
    # adContent = StringField('内容信息', validators=[DataRequired()])
    adPrice = IntegerField('活动价格', validators=[DataRequired(), NumberRange(1)])
    endTime = DateTimeField("结束时间", validators=[DataRequired()])
    submit_btn = SubmitField('发布')


class OffForm(FlaskForm):
    offName = StringField('折扣商家', validators=[DataRequired()])
    offType = StringField('类型', validators=[DataRequired()])
    offRate= IntegerField('折扣', validators=[DataRequired(), NumberRange(1)])
    offNum = IntegerField('优惠券数量', validators=[DataRequired(), NumberRange(1)])
    endTime = DateTimeField("使用期限", validators=[DataRequired()])
    submit_btn = SubmitField('发布')


class MarkForm(FlaskForm):
    userName = StringField('评论者用户名', validators=[DataRequired()])
    markName= StringField('商家', validators=[DataRequired()])
    markType = StringField('类型', validators=[DataRequired()])
    markScore = FloatField('评分', validators=[DataRequired()])
    markContent = StringField('评价内容', validators=[DataRequired()])
    submit_btn = SubmitField('发表')


class FlightForm(FlaskForm):
    flightId = StringField('航班号', validators=[DataRequired()])
    seatType = StringField('舱位', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    seatNum = IntegerField('座位数', validators=[DataRequired(), NumberRange(1)])
    fromTime = DateTimeField("起飞时间", validators=[DataRequired()])
    arivTime = DateTimeField("到达时间", validators=[DataRequired()])
    fromCity = StringField('出发城市', validators=[DataRequired()])
    arivCity = StringField('目的城市', validators=[DataRequired()])
    submit_btn = SubmitField('提交')


class TrainForm(FlaskForm):
    trainId = StringField('火车班次', validators=[DataRequired()])
    seatType = StringField('座位类型', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    seatNum = IntegerField('座位数', validators=[DataRequired(), NumberRange(1)])
    fromTime = DateTimeField("出发时间", validators=[DataRequired()])
    arivTime = DateTimeField("到达时间", validators=[DataRequired()])
    fromCity = StringField('出发城市', validators=[DataRequired()])
    arivCity = StringField('目的城市', validators=[DataRequired()])
    submit_btn = SubmitField('提交')


class HotelForm(FlaskForm):
    hotelName= StringField('酒店名', validators=[DataRequired()])
    hotelLoca = StringField('位置', validators=[DataRequired()])
    roomType = StringField('房间类型', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    roomNum = IntegerField('房间数', validators=[DataRequired(), NumberRange(1)])
    submit_btn = SubmitField('提交')


class AtttactionForm(FlaskForm):
    attrName= StringField('景点名', validators=[DataRequired()])
    attrLoca = StringField('位置', validators=[DataRequired()])
    features = StringField('景点特色', validators=[DataRequired()])
    ticType = StringField('门票类型', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired(), NumberRange(1)])
    endTime = DateTimeField("使用期限", validators=[DataRequired()])
    submit_btn = SubmitField('提交')


class CustomerForm(FlaskForm):
    userName = StringField('用户名', validators=[DataRequired()])
    passWd = StringField('密码', validators=[DataRequired()])
    passWd_ = StringField('确认密码', validators=[DataRequired()])
    custName = StringField('姓名', validators=[DataRequired()])
    custSex = StringField('性别', validators=[DataRequired()])
    custAge = IntegerField('年龄', validators=[DataRequired(), NumberRange(1)])
    custPhone = StringField('手机号', validators=[DataRequired()])
    custAddr = StringField('地址', validators=[DataRequired()])
    submit_btn = SubmitField('注册')
