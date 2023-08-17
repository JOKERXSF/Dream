from Dreamapp.models import *

monthList = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月',
             '11月', '12月']


def getAllUsers():
    return User.objects.all()

def getAllJobs():
    return JobInfo.objects.all()