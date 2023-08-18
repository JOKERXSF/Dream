from Dreamapp.models import *

monthList = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月',
             '11月', '12月']

educational = {'博士': 1, '硕士': 2, '研究生': 3, '本科': 4, '大专': 5, '高中': 6, '中专': 7, '初中及以下': 8, '学历不限': 9, }
workExperience = ['在校/应届生', '经验不限', '1-3年', '3-5年', '5-10年', '10年以上']


def getAllUsers():
    return User.objects.all()


def getAllJobs():
    return JobInfo.objects.all()
