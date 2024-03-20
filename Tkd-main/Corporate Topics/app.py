from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from myproject import app, db
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm

#首頁
@app.route('/')
def home():
    return render_template('home.html')

#登入系統
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash("您已經成功的登入系統")
                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('welcome_user')
                return redirect(next)
            else :
                flash(" 帳號或密碼輸入錯誤")
    return render_template('login.html',form=form)


#登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已經登出系統")
    return redirect(url_for('home'))


#使用者註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # 创建注册表单实例
    if form.validate_on_submit():  # 如果表单提交且验证通过
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:  # 如果数据库中已经存在相同邮箱地址的用户
            flash("該郵箱地址已經註冊過了，請使用其他郵箱地址。", "danger")  # 提示用户邮箱地址已被注册
            return redirect(url_for('register'))  # 重定向回注册页面
        else:
            user = User(email=form.email.data, username=form.username.data,
                        password=form.password.data)  # 创建新用户对象
            db.session.add(user)  # 将用户添加到数据库
            db.session.commit()  # 提交事务
            flash("感谢注册本系统成为会员", "success")  # 提示注册成功
            return redirect(url_for('login'))  # 重定向到登录页面
    return render_template('register.html', form=form)  # 渲染注册页面


#登入頁面
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
#     # 指定 IP 地址为本地局域网中的某个有效 IP 地址
#     app.run(host='10.22.2', port=8000, debug=True)
