#!/usr/bin/env python
'''
Created on Feb 20, 2013

@author: Tiberiu
'''
#import library to do http requests:
import urllib2


#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
import ConfigParser
#all these imports are standard on most modern python implementations
#def readCcFile():

def createProject(node, projectName):
    print 'copy project metadata for', projectName
    project = Project();
    project.name = projectName;
    project.status = node.getAttribute('status')
    return project

def notifyMonkey():
    print 'allerting monkey'
    
class Project:
    def __init__(self):
        self.name = ''
        self.version = ''
        self.status = ''
    def __str__(self):
        return self.name

#config = ConfigParser()
#config.readfp(open('ccMonkey.cfg'))
#ccXMLUrl = config.get('ccXml', 'url')


config = ConfigParser.RawConfigParser()
config.read('ccMonkey.cfg')

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
ccXmlUrl = config.get('Web resource', 'ccXmlUrl')


#download the ccXmlFile:
ccXmlFile = urllib2.urlopen(ccXmlUrl)
print 'Successfully connected to project status xml file : [', ccXmlUrl,']'
#convert to string:
data = ccXmlFile.read()
print 'project status xml read completed'
#close ccXmlFile because we dont need it anymore:

ccXmlFile.close()
print 'Closed stream'
#parse the xml you downloaded
dom = parseString(data)
print 'Dom data parsed'
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:

nodes = dom.getElementsByTagName('project')
print 'found [', nodes.length, '] projects'
filteredProjects = []
trackProjects = eval(config.get('Projects', 'trackprojects'))

for node in nodes:
    projectName = node.getAttribute('name')
    print 'filter project:', projectName
    for trackProject in trackProjects:
        if trackProject.lower() == projectName.lower():
            print 'ding!!! this guy won :', projectName
            filteredProjects.append(createProject(node, projectName))  
 
failedStatus = config.get("Parser","failedStatus") 
  
for project in filteredProjects:
    print 'Project', project.name, 'is', project.status
    if project.status.lower() == failedStatus.lower():
        notifyMonkey()
        break


