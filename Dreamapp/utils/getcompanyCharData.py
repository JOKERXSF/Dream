from .getPublicData import *

def getPageData():
    jobs = getAllJobs()
    typeData = []
    for i in jobs: typeData.append(i.type)
    return list(set(typeData))
