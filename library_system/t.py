# import datetime
# a = datetime.datetime.now() - datetime.timedelta(minutes=30)
# b = datetime.datetime.now() - datetime.timedelta(hours=13)
# c = datetime.datetime.now() - datetime.timedelta(days=2)
# d = datetime.datetime.now() - datetime.timedelta(weeks=5)
# e = datetime.datetime.now() - datetime.timedelta(days=690)
#
# def till_now_time(time):
#     delta = datetime.datetime.now() - time
#     if delta < datetime.timedelta(hours=1):
#         return "".format("{0} 分钟前", int(delta.seconds / 60))
#     elif delta < datetime.timedelta(days=1):
#         return "".format("{0} 小时前", int(delta.seconds / 60 / 60))
#     elif delta < datetime.timedelta(weeks=4):
#         return "".format("{0} 天前", int(delta.days))
#     elif delta < datetime.timedelta(days=365):
#         return "".format("{0} 月前", int(delta.days / 30))
#     else:
#         return "".format("{0} 年前", int(delta.days / 30 / 12))
#
#
# till_now_time(a)
# till_now_time(b)
# till_now_time(c)
# till_now_time(d)
# till_now_time(e)

from mongoengine import connect
con = connect('library', host="47.98.229.25", username='root', password='zhaohaoran1998_')
print(con)
import pymongo
conn = pymongo.MongoClient(host='47.98.229.25')
print(conn)