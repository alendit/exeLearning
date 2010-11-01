# temporary saves a list of open packages

packagelList = getPackageList()

def getPackageList():
    if packageList:
        return packageList
    else:
        return []
