# -*- coding: utf-8 -*-
import re, time, math

def math_sign(sign, par_ans):
    if sign == 'cos':
        par_ans = str(math.cos(float(par_ans)))
    elif sign == 'sin':
        par_ans = str(math.sin(float(par_ans)))
    elif sign == 'tan':
        par_ans = str(math.tan(float(par_ans)))
    elif sign == 'log':
        par_ans = str(math.log(float(par_ans)) / math.log(10))
    elif sign == 'ln':
        par_ans = str(math.log(float(par_ans)))
    elif sign == 'sinh':
        par_ans = str(math.sinh(float(par_ans)))
    elif sign == 'cosh':
        par_ans = str(math.cosh(float(par_ans)))
    elif sign == 'tanh':
        par_ans = str(math.tanh(float(par_ans)))
    elif sign == 'atan':
        par_ans = str(math.atan(float(par_ans)))
    elif sign == 'asin':
        par_ans = str(math.asin(float(par_ans)))
    elif sign == 'acos':
        par_ans = str(math.acos(float(par_ans)))
    elif sign == 'abs':
        par_ans = str(abs(float(par_ans)))
    return par_ans


def clean(string):
    '''数据合法性'''
    b = 0
    for i in string:  # 判断
        if b < 0: break
        if i == "(":
            b += 1
        elif i == ")":
            b -= 1
    #    character = re.search("[a-zA-Z\=]", string)  # 没有字母为空
    kh = len(re.findall("\d+\.?\d*[\(]", string))  # 判断括号是否有  数字(的情况
    kh1 = len(re.findall("[()]", string))  # 判断括号
    #    dian = re.search("(\d+\.\.\d+)", string)  # 判断是否有 ..
    if kh1 % 2 == b == kh:
        return string.replace(" ", "")  # 去除空格
    return 0


def sign_replace(string):
    '''符号替换'''
    string = str(string)
    string = string.replace("++", "+")
    string = string.replace("+-", "-")
    string = string.replace("-+", "-")
    string = string.replace("--", "+")
    string = string.replace("*+", "*")
    string = string.replace("/+", "/")
    return string


def ccf(xx):
    '''乘除法'''
    if re.search("\(", xx): xx = xx[1:-1]  # 去括号
    while re.search("[\*\/\%]", xx):
        times = re.search("\d+\.?\d*[\*\/\%]{1}\-?\d+\.?\d*", xx)
        if times:
            times = times.group()
            if times.count("*") == 1:  # 一个乘法
                a, b = times.split("*")
                xx = xx.replace(times, str(float(a) * float(b)))
            #            elif times.count("**") == 1:
            #                a, b = times.split("**")
            #                xx = xx.replace(times, str(float(a) ** float(b)))
            elif times.count("/") == 1:
                a, b = times.split("/")
                xx = xx.replace(times, str(float(a) / float(b)))
            #            elif times.count("/") == 2:
            #                a, b = times.split("//")
            #                xx = re.sub(times, str(float(a) // float(b)), xx)
            elif times.count('%') == 1:
                a, b = times.split("%")
                xx = xx.replace(times, str(int(a) % int(b)))
        else:
            return xx
    return xx


def jjf(xx):
    '''加减法,按匹配顺序计算'''
    if "(" in xx: xx = xx[1:-1]  # 去括号
    while re.search("\d+\.?\d*[\+\-]\d+\.?\d*", xx):
        findret = re.search("[\-]?\d+\.?\d*[\+\-]\d+\.?\d*", xx)
        if findret:
            findret = findret.group()
            if re.search("\d+\.?\d*\+\d+\.?\d*", findret):  # 加法
                a, b = findret.split("+")
                xx = xx.replace(findret, str(float(a) + float(b)))
            elif re.search("\d+\.?\d*\-\d+\.?\d*", findret):  # 减法
                a, b = findret.split("-")
                xx = xx.replace(findret, str(float(a) - float(b)))
        else:
            return xx
    return xx


def parre(string):
    '''寻找括号'''
    string = re.search("[a-z]*(\([^()]+\))", string)
    if string: return string.group()  # 找到就返回找到结果
    return 0  # 没找到返回0


def expo(string):
    string = re.search("[a-z0-9\.]*(\{[^{}]+\})", string)
    if string: return string.group()  # 找到就返回找到结果
    return 0  # 没找到返回0


def iter(string):
    string = re.search("[0-9]*!", string)
    if string: return string.group()  # 找到就返回找到结果
    return 0  # 没找到返回0


def count(sample):
    #        sample = input("请输入公式，保留2位小数。\n绿色为正确,红色结果错误！\n>>>")
    sample = clean(sample)  # 合法性判断
    sample = sample.replace('mod', '%')
    sample = sample.replace('e', str(math.e))
    sample = sample.replace('pi', str(math.pi))
    if sample:  # 返回正确执行精算
        while sample.count('!') > 0:
            iters = iter(sample)
            num = iters[:-1]
            num = int(num)
            temp = 1
            for i in range(1, num + 1):
                temp *= i
            sample = sample.replace(iters, str(temp))
        while sample.count('{') > 0:  # 处理指数
            exp = expo(sample)
            exp_place = exp.find('{')
            x = exp[0:exp_place]
            exp_part = exp[exp_place:]
            exp_ans = float(x) ** float(exp_part[1:-1])
            sample = sample.replace(exp, str(exp_ans))
        #            print(sample)
        while sample.count("(") > 0:  # 循环一直有括号的
            par = parre(sample)  # 寻找括号
            #            print(par)
            if par[0] == '(':
                sample = sample.replace(par, str(count(sign_replace(par[1:-1]))))  # 替换括号
            else:
                par_place = par.find('(')
                sign = par[0:par_place]
                par_part = par[par_place:]
                par_ans = count(sign_replace(par_part[1:-1]))
                ans = math_sign(sign, par_ans)
                sample = sample.replace(par, ans)
        else:  # 无括号的情况
            ret = jjf(ccf(sign_replace(sample)))
            if "+" in ret: ret = ret[1:]  # 取正数前面符号
            while len(re.findall("\d+\.?\d*[\+\-\*\/\%]+\d+\.?\d*", ret)) > 0:
                ret = jjf(ccf(sign_replace(ret)))
    #        print("%s = %f" % (sample, float(ret)))
    else:
        print("程序不合法，无法计算!")
    return ret



