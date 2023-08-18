from .getPublicData import *
from Dreamapp.models import User

def getPageData():
    jobs = getAllJobs()
    jobType = {}
    for job in jobs:
        if jobType.get(job.type, -1) == -1:
            jobType[job.type] = 1
        else:
            jobType[job.type] += 1

    return list(educational.keys()), workExperience, list(jobType.keys())


def changeSelfInfo(newInfo, fileInfo):
    user = User.objects.get(username=newInfo.get('username'))
    user.educational = newInfo.get('educational')
    user.workExperience = newInfo.get('workExperience')
    user.address = newInfo.get('address')
    user.work = newInfo.get('work')
    if fileInfo.get('avatar') is not None:
        user.avatar = fileInfo.get('avatar')

    user.save()
