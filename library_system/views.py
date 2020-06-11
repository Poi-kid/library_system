from django.shortcuts import render, redirect
from library_system.models import *
import json, datetime
from bson import ObjectId


def index(request):
    login_state = request.session.get("login_state", default=None)
    return render(request, 'index.html', {"login_state": login_state})


def login(request):
    request.session["login_state"] = None
    request.session["userinfo"] = None
    login_state = request.session.get("login_state", default=None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('login_type'):
            user = Manager.objects.filter(username=username).first()
        else:
            user = Reader.objects.filter(username=username).first()
        if user:
            if user.password == password:
                request.session["userinfo"] = user.to_json()
                if request.POST.get('login_type'):
                    request.session["login_state"] = 2
                    return redirect("/manager/")
                else:
                    request.session["login_state"] = 1
                    return redirect("/reader/")
            else:
                return render(request, 'login.html', {"login_state": login_state, "script": "alert", "wrong": "密码错误"})
        else:
            return render(request, 'login.html', {"login_state": login_state, "script": "alert", "wrong": "用户名不存在"})
    return render(request, 'login.html', {"login_state": login_state})


def register(request):
    login_state = request.session.get("login_state", default=None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Reader.objects.filter(username=username).first():
            return render(request, 'register.html', {"login_state": login_state, "script": "alert", "wrong": "用户名已被使用"})
        Reader.objects.create(username=username, password=password, if_lend=True, lend_num=0, )
        return redirect("/login/")
    return render(request, 'register.html', {"login_state": login_state})


def reader_index(request):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    table = {"names": ["#", "书名", "ISBN", "到期时间", "状态", ""],
             "records": []}
    i = 0
    for leadinfo in LeadInfo.objects.filter(rid=userinfo['_id']['$oid']).all():
        if not leadinfo.backed:
            i += 1
            isbn = BookCopy.objects.with_id(leadinfo.bid).isbn
            book = Book.objects.filter(isbn=isbn).first()
            over_time = True
            if datetime.date.today() <= leadinfo.back_date:
                over_time = False
            table["records"].append({"values": [i, book.name, book.isbn, leadinfo.back_date], "backed": leadinfo.backed, "over_time": over_time, "isbn": book.isbn})
    can_lend_num = 3 - int(userinfo["lend_num"])
    return render(request, 'reader.html', {"userinfo": userinfo, "table": table, "can_lend_num": can_lend_num, "login_state": login_state})


def reader_account(request):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    can_lend_num = 1
    if request.method == "POST":
        password = request.POST.get('password')
        Reader.objects.filter(username=userinfo['username']).update(set__password=password)
        return render(request, 'reader_account.html', {"userinfo": userinfo, "login_state": login_state, "script": "alert", "wrong": "修改成功"})
    return render(request, 'reader_account.html', {"userinfo": userinfo, "login_state": login_state})


def reader_lend(request):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    table = {"names": ["#", "书名", "ISBN", "库存", ""],
             "records": []}
    form = {"key": "", "method": {"name": "checked", "isbn": ""}}
    if request.method == "POST":
        key = request.POST.get('key')
        method = request.POST.get('name_or_isbn')
        form["key"] = key
        if method == "name":
            i = 0
            for book in Book.objects(name__contains=key).all():
                i += 1
                table['records'].append({"values": [i, book.name, book.isbn, book.count], "isbn": book.isbn})
        else:
            form['method'] = {"name": "", "isbn": "checked"}
            book = Book.objects(isbn=key).first()
            if book:
                table['records'].append({"values": [0, book.name, book.isbn, book.count], "isbn": book.isbn})
        return render(request, 'reader_lend.html', {"userinfo": userinfo, "table": table, "login_state": login_state, "form": form})
    return render(request, 'reader_lend.html', {"userinfo": userinfo, "table": table, "login_state": login_state, "form": form})


def reader_history(request):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    table = {"names": ["#", "书名", "ISBN", "到期时间", "状态", ""], "records": []}
    i = 0
    for leadinfo in LeadInfo.objects.filter(rid=userinfo['_id']['$oid']).all():
        i += 1
        book_copy = BookCopy.objects.with_id(leadinfo.bid)
        book = Book.objects.filter(isbn=book_copy.isbn).first()
        over_time = True
        if datetime.date.today() <= leadinfo.back_date:
            over_time = False
        table["records"].append({"values": [i, book.name, book.isbn, leadinfo.back_date], "isbn": book.isbn, "backed": leadinfo.backed, "over_time": over_time, "back_date": leadinfo.back_date})
    can_lend_num = 1
    return render(request, 'reader_history.html', {"userinfo": userinfo, "table": table, "can_lend_num": can_lend_num, "login_state": login_state})


def manager_index(request):
    login_state = request.session.get("login_state", default=None)
    table = {"names": ["#", "书名", "编号", "到期时间", ""], "records": [{"values": [3, 4, 5, 8], "isbn": 1}, {"values": [3, 4, 5, 8], "isbn": 1}]}
    can_lend_num = 1
    return render(request, 'manager.html', {"table": table, "can_lend_num": can_lend_num, "login_state": login_state})


def manager_lend(request):
    login_state = request.session.get("login_state", default=None)
    if request.method == "POST":
        type_ = request.POST.get('type')
        username = request.POST.get('username')
        isbn = request.POST.get('isbn')
        reader = Reader.objects.filter(username=username).first()
        if not reader:
            return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "读者ID不存在"})
        rid = reader.id
        if type_ == "lend":
            if not (reader.if_lend and reader.lend_num < 3):
                return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "该读者暂不能借书"})
            book_copy = None
            for copy in BookCopy.objects(isbn=isbn).all():
                if copy.if_book and username == copy.book_username:
                    book_copy = copy
                    break
                elif not copy.if_lend and not copy.if_book:
                    book_copy = copy
                    break
            if not book_copy:
                return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "没有这本书或者库存不足"})
            book_copy.update(set__if_lend=True)

            LeadInfo.objects.create(rid=str(rid), bid=str(book_copy.id), lend_date=datetime.datetime.now(), back_date=(datetime.datetime.now() + datetime.timedelta(days=30)), backed=False, relend_times=0, relend_ability=True)
            reader.update(inc__lend_num=1)
            return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "借书成功"})
        elif type_ == "back":
            book_copy = None
            lead_info = None
            for lead_info_ in LeadInfo.objects(rid=str(rid)).all():
                if not lead_info_.backed:
                    book_copy_ = BookCopy.objects.with_id(lead_info_.bid)
                    if book_copy_.isbn == isbn:
                        lead_info = lead_info_
                        book_copy = book_copy_
                        break
            if not (lead_info and book_copy):
                return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "还书失败"})
            lead_info.update(set__backed=True)
            book_copy.update(set__if_lend=False)
            book_copy.update(set__if_book=False)
            reader.update(dec__lend_num=1)
            return render(request, 'manager_lend.html', {"login_state": login_state, "script": "alert", "wrong": "还书成功"})
    return render(request, 'manager_lend.html', {"login_state": login_state})


def manager_book(request):
    login_state = request.session.get("login_state", default=None)
    table = {"names": ["#", "书名", "ISBN", "库存", ""],
             "records": []}
    form = {"key": "", "method": {"name": "checked", "isbn": ""}}
    if request.method == "POST":
        key = request.POST.get('key')
        method = request.POST.get('name_or_isbn')
        form["key"] = key
        if method == "name":
            i = 0
            for book in Book.objects(name__contains=key).all():
                i += 1
                table['records'].append({"values": [i, book.name, book.isbn, book.count], "isbn": book.isbn})
        else:
            form['method'] = {"name": "", "isbn": "checked"}
            book = Book.objects(isbn=key).first()
            if book:
                table['records'].append({"values": [0, book.name, book.isbn, book.count], "isbn": book.isbn})
        return render(request, 'manager_book.html', {"table": table, "login_state": login_state, "form": form})
    return render(request, 'manager_book.html', {"table": table, "login_state": login_state, "form": form})


def manager_enter(request):
    login_state = request.session.get("login_state", default=None)
    form = {}
    if request.method == "POST":
        form["isbn"] = request.POST.get('isbn')
        form["name"] = request.POST.get('name')
        form["author"] = request.POST.get('author')
        form["press"] = request.POST.get('press')
        form["category"] = request.POST.get('category')
        form["count"] = request.POST.get('count')
        form["press_date"] = request.POST.get('press_date')
        form["press_date"] = datetime.date(year=int(form["press_date"][3:]), month=int(form["press_date"][:2]), day=1)
        form["buy_data"] = request.POST.get('buy_data')
        form["price"] = request.POST.get('price')
        Book.objects.create(isbn=form['isbn'], name=form['name'], author=form['author'], press=form['press'],
                            category=form['category'], count=form['count'], press_date=form['press_date'],
                            buy_data=form['buy_data'], price=form['price'])
        for i in range(int(form["count"])):
            BookCopy.objects.create(isbn=form['isbn'], if_lend=False, if_book=False)

    return render(request, 'manager_enter.html', {"login_state": login_state})


def manager_delete(request):
    login_state = request.session.get("login_state", default=None)
    if request.method == "POST":
        isbn = request.POST.get('isbn')
        if not Book.objects.with_id(isbn):
            return render(request, 'manager_delete.html', {"login_state": login_state, "script": "alert", "wrong": "没有这本书"})
        Book.objects(isbn=isbn).delete()
        BookCopy.objects(isbn=isbn).delete()
        return render(request, 'manager_delete.html', {"login_state": login_state, "script": "alert", "wrong": "删除成功"})
    return render(request, 'manager_delete.html', {"login_state": login_state})


def manager_lend_info(request):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    table = {"names": ["#", "读者ID", "书名", "ISBN", "到期时间", "状态"], "records": []}
    i = 0
    for leadinfo in LeadInfo.objects.all():
        i += 1
        book_copy = BookCopy.objects.with_id(leadinfo.bid)
        book = Book.objects.filter(isbn=book_copy.isbn).first()
        reader = Reader.objects.with_id(leadinfo.rid)
        over_time = True
        if datetime.date.today() <= leadinfo.back_date:
            over_time = False
        table["records"].append({"values": [i, reader.username, book.name, book.isbn, leadinfo.back_date], "isbn": book.isbn, "backed": leadinfo.backed, "over_time": over_time, "back_date": leadinfo.back_date})
    return render(request, 'manager_lend_info.html', {"userinfo": userinfo, "table": table, "login_state": login_state})


def till_now_time(time):
    delta = datetime.datetime.now() - time
    if delta < datetime.timedelta(hours=1):
        return str(int(delta.seconds / 60)) + "分钟前"
    elif delta < datetime.timedelta(days=1):
        return str(int(delta.seconds / 60 / 60)) + "小时前"
    elif delta < datetime.timedelta(weeks=4):
        return str(int(delta.days)) + "天前"
    elif delta < datetime.timedelta(days=365):
        return str(int(delta.days / 30)) + "月前"
    else:
        return str(int(delta.days / 30 / 12)) + "年前"


def book(request, isbn):
    login_state = request.session.get("login_state", default=None)
    userinfo = json.loads(request.session["userinfo"])
    book = json.loads(Book.objects.with_id(isbn).to_json())
    comments = []
    for comment in Comment.objects(isbn=isbn).all():
        comments.append({"isbn": comment.isbn, "username": comment.username, "content": comment.content,
                         "time": till_now_time(comment.date)})
        print(till_now_time(comment.date))
    if request.method != "POST":
        return render(request, 'book.html',
              {"login_state": login_state, "book": book, "comments": comments, "isbn": isbn})

    if request.session["login_state"] != 1:
        return render(request, 'book.html', {"login_state": login_state, "book": book, "comments": comments, "isbn": isbn, "script": "alert", "wrong": "请先登录"})

    if request.POST.get('book_or_comment') == "book":
        for copy in BookCopy.objects(isbn=isbn).all():
            if not copy.if_lend and not copy.if_book:
                copy.update(set__if_book=True, set__book_username=userinfo['username'])
                return render(request, 'book.html', {"login_state": login_state, "book": book, "comments": comments, "isbn": isbn, "script": "alert", "wrong": "预定成功"})
        return render(request, 'book.html', {"login_state": login_state, "book": book, "comments": comments, "isbn": isbn, "script": "alert", "wrong": "该书已没有库存"})
    elif request.POST.get('book_or_comment') == "comment":
        content = request.POST.get('content')
        username = userinfo['username']
        Comment.objects.create(isbn=isbn, username=username, content=content, date=datetime.datetime.now())
        for comment in Comment.objects(isbn=isbn).all():
            comments.append({"isbn": comment.isbn, "username": comment.username, "content": comment.content, "time": till_now_time(comment.date)})
        return render(request, 'book.html', {"login_state": login_state, "book": book, "comments": comments, "isbn": isbn})
