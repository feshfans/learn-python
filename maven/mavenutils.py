# -*- coding: utf-8 -*-

import os
import sys
import xml.dom.minidom as xml
from xml.dom.minidom import Document
from xml.etree import ElementTree as et
import time
import zipfile
sys.setrecursionlimit(1000000)

#maven仓库目录
maven_repo = 'F:\maven-repo'
#pom.xml输出路径
xmlOutPath="pom.xml"
#压缩包保存路径
archive_out_path=maven_repo
#模板文件路径
xmlTemplate='template.xml'

jarFiles=[]
errLogs=[]

dom=xml.parse(xmlTemplate)
dependenciesNode=dom.getElementsByTagName('dependencies')[0]

class Pom:
    def __init__(self, groupId, artifactId, version, type):
        self.groupId=groupId
        self.artifactId=artifactId
        self.version=version
        self.type=type
    def __repr__(self):
        return self.groupId+" : "+self.artifactId+" : "+self.version+" : "+self.type

def parseDir(dir):
    """"
    解析maven_repo目录，获取最底层的文件目录
    """
    files = os.listdir(dir)
    isFileDir=True
    for file in files:
        if os.path.isdir(os.path.join(dir,file)):
            # 排除隐藏文件
            if file[0] == '.':
                pass
            else:
                isFileDir=False
                parseDir(os.path.join(dir,file))
    if isFileDir:
        jarFiles.append(dir)


def parsePom(filePath):
    """
    根据pom.xml生成实例对象
    :param filePath: pom.xml文件路径
    :return: Pom类对象
    """
    dom=et.parse(filePath).getroot()
    for child in dom:
        if child.tag.endswith('groupId'):
            groupId= child.text
        if child.tag.endswith('artifactId'):
            artifactId=child.text
        if child.tag.endswith('version'):
            version=child.text
        if child.tag.endswith('packaging'):
            packaging=child.text
    pom=Pom(groupId if locals().has_key('groupId') else '',artifactId if locals().has_key('artifactId') else '',
            version if locals().has_key('version') else '', packaging if locals().has_key('packaging') else '')
    return pom

def createDenpenceny(pom):
    """"
    根据pom实例生成依赖的xml节点
    """
    dependencyNode=dom.createElement("dependency")
    if len(pom.groupId)!=0:
        groupIdNode=dom.createElement("groupId")
        groupId_text=dom.createTextNode(pom.groupId)
        groupIdNode.appendChild(groupId_text)
        dependencyNode.appendChild(groupIdNode)

    if len(pom.artifactId) != 0:
        artifactIdNode = dom.createElement("artifactId")
        artifactId_text = dom.createTextNode(pom.artifactId)
        artifactIdNode.appendChild(artifactId_text)
        dependencyNode.appendChild(artifactIdNode)

    if len(pom.version) != 0:
        versionNode = dom.createElement("version")
        version_text = dom.createTextNode(pom.version)
        versionNode.appendChild(version_text)
        dependencyNode.appendChild(versionNode)

    if len(pom.type) != 0:
        packagingNode = dom.createElement("packaging")
        packaging_text = dom.createTextNode(pom.type)
        packagingNode.appendChild(packaging_text)
        dependencyNode.appendChild(packagingNode)

    return dependencyNode

parseDir(maven_repo)

#生成依赖节点
for jarfile in jarFiles:
    files=os.listdir(jarfile)
    for file in files:
        try:
            if file.endswith('.pom'):
                pom=parsePom(os.path.join(jarfile,file))
                node= createDenpenceny(pom)
                dependenciesNode.appendChild(node)
        except:
            errLogs.append(jarfile+file+"\n\r")

#将生成的xml写入文件中
f=open(xmlOutPath,'w')
f.write(dom.toprettyxml(indent=''))
f.close()

#将错误的pom.xml路径写入到错误文件中
f=open("error.log",'w')
for log in errLogs:
    f.write(log)
f.close()


# statinfo=os.stat(r'F:\maven-repo\antlr\antlr\2.7.2')
# print statinfo.st_ctime
# print time.time()

#获取上一次打包的时间点
f=open(r'archive.log')
preVersion=f.readline()
f.close()

newJarFiles=[]
#如果上一次打包的时间点不存在，则默认打全包
if preVersion=="":
    newJarFiles=jarFiles
else: #否则比较时间，将需要打包的文件加入集合中
    for jarfile in jarFiles:
        statinfo=os.stat(jarfile)
        ctime_file=statinfo.st_ctime
        if float(ctime_file)>float(preVersion):
            newJarFiles.append(jarfile)

#将文件压缩到指定压缩文件
f=zipfile.ZipFile(os.path.join(archive_out_path,'archive.zip'),'w',zipfile.ZIP_DEFLATED)
for jarfile in newJarFiles:
    index=len(maven_repo)
    newDir=jarfile[index:]
    for file in os.listdir(jarfile):
        f.write(os.path.join(jarfile,file),os.path.join(newDir,file))

f.close();

#记录本次打包的时间点
curTime=time.time()
f=open('archive.log','w')
f.write(str(curTime))
f.close()


