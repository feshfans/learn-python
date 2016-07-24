# -*- coding: utf-8 -*-

import os

maven_repo = 'F:\maven-repo'

class Pom:
    def __init__(self,groupId,artifactId,version):
        self.groupId=groupId;
        self.artifactId=artifactId;
        self.version=version;
    def __repr__(self):
        return self.groupId+" : "+self.artifactId+" : "+self.version

files=os.listdir(maven_repo)
for file in files:
    if os.path.isdir(maven_repo+os.sep+file):
        # 排除隐藏文件
        if file[0]=='.':
            pass
        else:
            pass


pom=Pom('com.kang','test','0.01')
print str(pom)
