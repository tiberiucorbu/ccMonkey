#!/usr/bin/env python
'''
Created on Feb 20, 2013

@author: Tiberiu


'''
##################################################################### imports 
#all these imports are standard on most modern python implementations
#import library to do http requests:
import urllib2
#used for xml parser 
from xml.dom.minidom import parseString
# used for configuration file
import ConfigParser
# used for waiting a little bit
from time import sleep
import RPi.GPIO as GPIO

##################################################################### constants 
#files used by this script
CONFIGURATION_FILE = 'ccMonkey.cfg'
# allert 
WARN = 'warn'
CRITICAL = 'critical'

##################################################################### class def 

'''
    Value object that keeps all the metadata for a project: status, previous status, name etc. 
'''
class Project:
    def __init__(self):
        self.name = ''
        self.version = ''
        self.status = ''
        self.previousStatus = ''
    def __str__(self):
        return self.name


##################################################################### methods def 

'''
    connect to the server and get the xml file
'''
def retrieveCCXml(ccXmlUrl):
    #download the ccXmlFile:
    ccXmlFile = urllib2.urlopen(ccXmlUrl)
    print 'Successfully connected to project status xml file :', ccXmlUrl
     #convert to string:
    data = ccXmlFile.read()
    print 'Projects xml read completed' #close ccXmlFile because we dont need it anymore:
    ccXmlFile.close()
    print 'Closed stream'
    #parse the xml you downloaded
    dom = parseString(data)
    print 'Dom data parsed for', ccXmlUrl
    return dom

'''
    interprets fom data
'''
def findProjects(config, dom):
    nameAttribute = config.get('Parser', 'nameAttribute')
    projectTag = config.get('Parser',  'projectTag' )
    trackProjects = eval(config.get('Projects', 'trackprojects'))
    
    nodes = dom.getElementsByTagName(projectTag)
    print 'Found ', nodes.length, ' projects'
    
    filteredProjects = []
    print 'Filtering projects'
    for node in nodes:
        projectName = node.getAttribute(nameAttribute)
        for trackProject in trackProjects:
            if trackProject.lower() == projectName.lower():
                print 'ding!!! this guy is important :', projectName
                filteredProjects.append(createProject(config, node, projectName))
    
    return filteredProjects
'''
    copy dom data
'''
def createProject(config, node, projectName):
    print 'Copy project metadata for', projectName
    currentStatusAttribute = config.get("Parser", "currentStatusAttribute")
    lastStatusAttribute  = config.get("Parser", "lastStatusAttribute")
    
    project = Project();
    
    project.name = projectName;
    project.status = node.getAttribute(currentStatusAttribute)
    project.previousStatus = node.getAttribute(lastStatusAttribute)
    
    return project

'''
    interprets projects status
'''
def computeProjectMetadata(config, filteredProjects):
    failedStatus = config.get("Parser", "failedStatusValue")
    for project in filteredProjects:
        print 'Project', project.name, 'is', project.status
        if project.status.lower() == failedStatus.lower():
            if project.previousStatus.lower() != failedStatus.lower():
                notifyMonkey(config, CRITICAL, project)
            else:
                notifyMonkey(config, WARN, project)
            break

'''
    extract parameters and 
'''
def notifyMonkey(config, level, project):
    cicles = 0
    oscillateDelay = 0
    pin = 0
    print 'Allerting monkey for project', project.name
    if level == CRITICAL:
        cicles = config.getint("Monkey", "criticalAlertCicles")
        oscillateDelay = config.getfloat("Monkey", "criticalOscilateDelay")
        pin = config.getint("Monkey", "criticalGPIO")
        # oscilate  
    elif level== WARN:
        cicles = config.getint("Monkey", "warnAlertCicles")
        oscillateDelay = config.getfloat("Monkey", "warnOscilateDelay")
        pin = config.getint("Monkey", "warnGPIO")
    
    
    oscillatePin(cicles,oscillateDelay,pin)

def oscillatePin(cicles,oscillateDelay,pin):
    print 'Turning on the monkey for ', cicles, ' cicles of a ', oscillateDelay, 'milisec length on pinNum: ', pin
    for i in range(0, cicles):
        #call gpio HIGH
        GPIO.output(pin,GPIO.HIGH)
        sleep(oscillateDelay)
        #call gpio LOW
        GPIO.output(pin,GPIO.LOW)
        sleep(oscillateDelay)
        

##################################################################### script
# run the damn thing 
def setupGPIO():
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)

config = ConfigParser.RawConfigParser()
config.read(CONFIGURATION_FILE)
ccXmlUrl = config.get('Web resource', 'ccXmlUrl')
dom = retrieveCCXml(ccXmlUrl)
filteredProjects = findProjects(config, dom)  
computeProjectMetadata( config, filteredProjects)




