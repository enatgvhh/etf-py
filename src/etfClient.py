# -*- coding: UTF-8 -*-
#etfClient.py
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
import pathlib
from etf import etfWebApp
from etf import etfTest

def main():
    proxies = {
        'http': 'http://111.11.111.111:80',
        'https': 'http://111.11.111.111:80',
        }
    
    #urlWebApp = 'https://inspire.ec.europa.eu/validator' #produktiv
    urlWebApp = 'http://staging-inspire-validator.eu-west-1.elasticbeanstalk.com/etf-webapp' #staging   
    webApp = etfWebApp.EtfWebApp(urlWebApp, proxies)
    fileDir = r'D:\Test-ETF\files'
    resultFile = r'D:\Test-ETF\results.csv'
    
    #1. Status ETF WebApp
    try:
        print('Status der ETF Web App %s ist: %s' % (urlWebApp, webApp.requestStatus()['status']))
    except ConnectionError:
        print('%s; %s' % (sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit()
        
    '''
    #2. Welche TestSuits sind vorhanden - Write to csv-file
    fileTestSuites = r'D:\Test-ETF\testSuites.csv'
    try:
        testSuites = webApp.requestTestSuites()
        
        with open(fileTestSuites, 'w') as f:
            for dictKey, dictValue in testSuites.items():
                f.write('%s;%s\n' % (dictKey, dictValue))
    except ConnectionError:
        print('%s; %s' % (sys.exc_info()[0], sys.exc_info()[1]))
        '''
        
    if os.path.exists(fileDir) == True:
        if os.path.isdir(fileDir) == True:
            objects = list(pathlib.Path(fileDir).glob('*.gml'))         
            if objects:
                with open(resultFile, 'w') as f:
                    header = '%s;%s;%s;%s;%s\n' % ('fileName', 'testRunTime', 'testRunId', 'testRunRef', 'testRunResultStatus')
                    f.write(header)
                    
                    for element in objects:
                        test = etfTest.EtfTest(urlWebApp, proxies)
                        gmlFile = str(element)
                        
                        try:
                            #3. TestObjects - File upload
                            testObject = test.requestTestObjects(gmlFile)
                            testObjectId = testObject['testObject']['id']
                            testObjectFileName = testObject['files'][0]['name']                        
                            
                            #4. TestRun for a file-based Test, using a temporary Test Object
                            testIds = webApp.getTestIds('gml')
                            testRun = test.requestTestRuns(testObjectId, testObjectFileName, testIds)
                            testRunId = testRun['EtfItemCollection']['testRuns']['TestRun']["id"]
                            testRunRef = testRun['EtfItemCollection']['ref']
                            
                            #5. TestRuns progress
                            if test.requestTestRunsProgress(testRunRef) == True:
                                #6. TestRuns Result
                                testRunResult = test.requestTestRunResults(testRunRef)
                                testRunResultStatus = testRunResult["EtfItemCollection"]["testRuns"]["TestRun"]["status"]
                                testRunTime = testRunResult["EtfItemCollection"]["testRuns"]["TestRun"]["startTimestamp"]
                                
                                result = '%s;%s;%s;%s;%s\n' % (testObjectFileName, testRunTime, testRunId, testRunRef, testRunResultStatus)
                                f.write(result)
                                
                        except ConnectionError:
                            print('%s; %s; raised by %s' % (sys.exc_info()[0], sys.exc_info()[1], gmlFile))
                                          
if __name__ == '__main__':
    main()