# -*- coding: UTF-8 -*-
#etfWebApp.py
from __future__ import absolute_import, division, print_function, unicode_literals
import requests
import json
import re

class EtfWebApp:
    """"Klasse EtfWebApp dient zum speichern der URL der ETF Web App und
    ermoeglicht Requests auf den Status sowie die definierten Testfälle (TestSuites) der App.
    """
    
    def __init__(self, urlWebApp: str, proxies: dict):
        """"Konstruktor Klasse EtfWebApp.
        
        Args:
            urlWebApp: str mit URL zur ETF Web App
            proxies: dictionary with hhtp und https proxies
        """
        self.__urlWebApp = urlWebApp
        self.__proxies = proxies
        
    def getUrlWebApp(self) -> str:
        """Methode getUrlWebApp gibt die URL der ETF Web App zurueck.
        """
        return self.__urlWebApp
    
    def requestStatus(self) -> dict:
        """Methode getStatus gibt den Status der ETF Web App zurueck.
        
        Returns:
            dictionary with etf web app status
            
        Raises:
            ConnectionError for Service is down
        """
        jsonData = None
        url = '%s%s' % (self.__urlWebApp, '/v2/status')
        r = requests.get(url, proxies=self.__proxies)
        
        if r.status_code == 200:
            jsonData = json.loads(r.text)
        else:
            message = '%s: %s' % (r.status_code, 'Service is down')
            raise ConnectionError(message)
        
        return jsonData
    
    def requestTestSuites(self) -> dict:
        """Methode getTestSuitesProd gibt alle Test Suites der ETF Web App zurueck.
        
        Returns:
            dictionary with test suites {'id': 'label'}
            
        Raises:
            ConnectionError for Service is down
        """
        testSuitesDict = {}
        testSuitesList = []
        url = '%s%s' % (self.__urlWebApp, '/v2/ExecutableTestSuites.json')
        r = requests.get(url, proxies=self.__proxies)
        
        if r.status_code == 200:
            jsonData = json.loads(r.text)
            testSuites = jsonData['EtfItemCollection']['executableTestSuites']['ExecutableTestSuite']
            
            #sortedTestSuites = sorted(testSuites, key=lambda item: item['label'])
            #
            #for element in sortedTestSuites:
            #    #print('%s: %s, %s' % (element['id'], element['label'], element['remoteResource']))
            #    testSuitesDict.update({element['id']: element['label']}) 
            
            for element in testSuites:
                resourceList = element['remoteResource'].split('/')
                
                if re.search("data", resourceList[-2]): 
                    labelStr = '%s/%s - %s' % (resourceList[-2], resourceList[-1], element['label'])
                else:
                    labelStr = element['label']
                    
                testSuitesList.append({'id': element['id'], 'label': labelStr})
                
            sortedTestSuitesList = sorted(testSuitesList, key=lambda item: item['label'])
            
            for element in sortedTestSuitesList:
                testSuitesDict.update({element['id']: element['label']})
                
        else:
            message = '%s: %s' % (r.status_code, 'Service is down')
            raise ConnectionError(message)
        
        return testSuitesDict
    
    def getTestIds(self, theme: str) -> list:
        """Methode getTestIds gibt eine Liste mit den TestIDs fuer das uebergebene Thema zurueck.
        
        Es sind beispielhaft nur die Test IDs fuer gml und plu codiert!
        
        Args:
            theme: str mit Thema
            
                gml = Interoperable data sets in GML
                ad = Data Theme Addresses
                au = Data Theme Administrative Units
                cp = Data Theme Cadastral Parcels
                gn = Data Theme Geographical Names
                hy = Data Theme Hydrography - PysicalWaters
                hy-n = Data Theme Hydrography - Network
                ps = Data Theme Protected Sites
                tn-a = Data Theme Transport Networks - Air
                tn-ra = Data Theme Transport Networks - Rail
                tn-ro = Data Theme Transport Networks - Road
                tn = Data Theme Transport Networks - Water
                tn-w = Data Theme Transport Networks
                
                only staging:
                am = Data Theme Area Management, Restriction/Regulation Zones and Reporting Units
                plu = Data Theme Land Use - PlannedLandUse
                elu = Data Theme Land Use - ExistingLandUse
                sd = Data Theme Species Distribution
                ef = Data Theme Environmental Monitoring Facilities
            
        Returns:
            list mit Test IDs
        """
        testIdDict = {'gml': ["EID61070ae8-13cb-4303-a340-72c8b877b00a","EID09820daf-62b2-4fa3-a95f-56a0d2b7c4d8","EID499937ea-0590-42d2-bd7a-1cafff35ecdb","EID63f586f0-080c-493b-8ca2-9919427440cc"],
                      'plu': ["EIDeefb2267-a0ca-40b4-87ee-a286ff6dd97f","EID9251e31c-1318-4f52-afe5-900eb16f5647","EIDa4bf4091-b26d-4e13-ab94-4d26ea10a625","EIDda4c0f98-f97a-44ad-9366-cef577cf809a"]}
        
        return testIdDict[theme]
    