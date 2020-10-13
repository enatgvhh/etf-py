# -*- coding: UTF-8 -*-
#etfTest.py
from __future__ import absolute_import, division, print_function, unicode_literals
import requests
import json
import time

class EtfTest:
    """"Klasse EtfTest ermoeglicht ein GML-File hochzuladen und dazu die
    angegebenen Test Suites auszufuehren.
    """
    
    def __init__(self, urlWebApp: str, proxies: dict):
        """"Konstruktor der Klasse Klasse EtfTest.
        
        Args:
            urlWebApp: str mit URL zur ETF Web App
            proxies: dictionary with hhtp und https proxies
        """
        self.__urlWebApp = urlWebApp
        self.__proxies = proxies
        
    def requestTestObjects(self, gmlFile: str) -> dict:
        """Methode getTestObjects gibt fuer das uebergebene GML-File
        ein temporaeres TestObject zurueck.
        
        Args:
            gmlFile: str mit Path zum GML-File
            
        Returns:
            dictionary with test objects
            
        Raises:
            ConnectionError for File upload failed
        """
        jsonData = {}
        url = '%s%s' % (self.__urlWebApp, '/v2/TestObjects?action=upload')
        headers = {'Accept': 'application/json'}
    
        with open(gmlFile, 'rb') as f:
            files = {'file': f}
            r = requests.post(url, files=files, headers=headers, proxies=self.__proxies)
            
            if r.status_code == 200:
                jsonData = json.loads(r.text)
            elif r.status_code == 413:
                message = '%s: %s' % (r.status_code, 'Uploaded test data are too large')
                raise ConnectionError(message)
            else:
                message = '%s: %s' % (r.status_code, 'File upload failed')
                raise ConnectionError(message)
                
        return jsonData
    
    def requestTestRuns(self, testObjectId: str, testObjectFileName: str, testIdS: list) -> dict:
        """Methode getTestRuns startet die angegebenen Test.
        
        Args:
            testObjectId: str mit TestObjects ID
            testObjectFileName: str mit Name GML-File
            testIdS: List mit Test IDs
        
        Returns:
            dictionary with test runs
                
        Raises:
            ConnectionError for Invalid request
        """
        jsonData = {}
        t = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
        label = '%s %s %s %s' % ('Test run on', t, 'with test suits for', testObjectFileName)
        
        jsonBody = {
            "label": label,
            "executableTestSuiteIds": testIdS,
            "arguments": {
                "files_to_test": ".*",
                "tests_to_execute": ".*"
            },
            "testObject": {
                "id": testObjectId
            }
        }
        data = json.dumps(jsonBody, indent=4, separators=(',', ': '))
        
        url = '%s%s' % (self.__urlWebApp, '/v2/TestRuns')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url, data=data, headers=headers, proxies=self.__proxies)
        
        if r.status_code == 201:
            jsonData = json.loads(r.text)
        elif r.status_code == 400:
            message = '%s: %s' % (r.status_code, 'Invalid request')
            raise ConnectionError(message)
        elif r.status_code == 404:
            message = '%s: %s' % (r.status_code, 'Test Object or Executable Test Suite with ID not found')
            raise ConnectionError(message)
        elif r.status_code == 409:
            message = '%s: %s' % (r.status_code, 'Test Object already in use')
            raise ConnectionError(message)
        else:
            message = '%s: %s' % (r.status_code, 'Internal error')
            raise ConnectionError(message)
        
        return jsonData
    
    def requestTestRunsProgress(self, testRunRef: str) -> bool:
        """Methode requestTestRunsProgress gibt true zurueck wenn der TestRun abgeschlossen ist.
        
        Args:
            testRunRef: str mit der TestRuns Referenz
        
        Returns:
            bool (True) if testRuns finished
            
        Raises:
            ConnectionError for Test Run not found
        """
        url = testRunRef.replace('.json', '/progress?pos=0')
        ist = 0; soll = 100
        
        while ist < soll:
            time.sleep(8)
            r = requests.get(url, proxies=self.__proxies)
            
            if r.status_code == 200:
                json_data = json.loads(r.text)
                ist = int(json_data["val"])
                soll = int(json_data["max"])
            else:
                message = '%s: %s' % (r.status_code, 'Test Run not found')
                raise ConnectionError(message)
            
        return True
    
    def requestTestRunResults(self, testRunRef: str) -> dict:
        """Methode requestTestRunResults gibt das Ergebnis des TestRuns zurueck.
        
        Args:
            testRunRef: str mit der TestRuns Referenz
        
        Returns:
            dictionary with test runs result
            
        Raises:
            ConnectionError for Test Run Results not found
        """
        jsonData = {}
        url = testRunRef
        r = requests.get(url, proxies=self.__proxies)
        
        if r.status_code == 200:
            jsonData = json.loads(r.text)
        else:
            message = '%s: %s' % (r.status_code, 'Test Run Result not found')
            raise ConnectionError(message)
        
        return jsonData
    