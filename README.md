#

ETF Web API - Validierung mit Python
====================================

## Inhalt
* [Einleitung](#einleitung)
* [ETF Web API](#etf-web-api)
* [Python Package ETF](#python-package-etf)
* [Summary](#summary)


## Einleitung
Mit der [ETF WebApp](https://inspire.ec.europa.eu/validator/) steht ein sehr gelungener INSPIRE Reference Validator für Daten, Metadaten und Webservices zur Verfügung. In diesem Beitrag wollen wir uns ausschließlich mit der Validierung von Daten beschäftigen, d.h. mit der Validierung von INSPIRE GML-Files. Die ETF WebApp steht zusätzlich in einer [Staging Umgebung](http://staging-inspire-validator.eu-west-1.elasticbeanstalk.com/etf-webapp/) zur Verfügung, die bereits neue Testfälle für die Annex 3 Daten Themen (*am, ef, lu, nz, sd*) implementiert hat.

Wir werden hier mit Python die Validierung von INSPIRE GML-Files über die ETF Web API realisieren. Alternativ kann dies auch mit Hilfe des [FME Custom Transformer](https://hub.safe.com/publishers/enatgvhh/transformers/etf_validator_gml_files) erfolgen, den ich aus den gewonnenen Erkenntnissen heraus demnächst aktualisieren werde.


## ETF Web API
Wir nutzen die [ETF Web API](https://inspire.ec.europa.eu/validator//swagger-ui.html#/) in Version 2 und wollen uns kurz den prinzipiellen Ablauf für eine Validierung von INSPIRE GML-Files ansehen.

* Status der ETF Web App ermitteln: GET [https://inspire.ec.europa.eu/validator/v2/status](https://inspire.ec.europa.eu/validator//swagger-ui.html#!/1._Service_Status/getStatusUsingGET)

* Upload INSPIRE GML-File: POST [https://inspire.ec.europa.eu/validator/v2/TestObjects?action=upload](https://inspire.ec.europa.eu/validator//swagger-ui.html#!/3._Manage_Test_Objects/uploadDataUsingPOST) 

* Starten der ausgewählten Tests: POST [https://inspire.ec.europa.eu/validator/v2/TestRuns](https://inspire.ec.europa.eu/validator//swagger-ui.html#!/4._Manage_Test_Runs/startUsingPOST) 

* Testfortschritt abfragen und auf Testabschluss warten: GET [https://inspire.ec.europa.eu/validator/v2/TestRuns/meineTestRunEID/progress?pos=0](https://inspire.ec.europa.eu/validator//swagger-ui.html#!/4._Manage_Test_Runs/progressLogUsingGET)  

* Testergebnis abfragen: GET [https://inspire.ec.europa.eu/validator/v2/TestRuns/meineTestRunEID.json](https://inspire.ec.europa.eu/validator//swagger-ui.html#!/5._Test_Run_Results/testRunByIdJsonUsingGET_1) 


## Python Package ETF
Das python-package 'etf'  ist zusammen mit einem Client im Ordner [src](src) zu finden. Als Input benötigt der Client einen Ordner mit den zu testenden INSPIRE GML-Files. Die Ergebnisse der Tests (*passed, passed_manual, failed*) werden in ein CSV-File geschrieben, welches neben diesen Testergebnissen auch Online-Referenzen auf die vollständigen Testprotokolle der ETF WebApp enthält.


## Summary
Mit der vorgestellten Lösung lassen sich viele INSPIRE GML-Files automatisch testen. Will man nur einzelne GML-Files testen, dann reicht natürlich die ETF WebApp.

Zum Abschluss noch ein Hinweis zur Performance. Für den File-Upload ist eine Obergrenze der Dateigröße festgelegt. Es kann also kein Upload eines bsp. 1 GB großen GML-Files erfolgen. Ich habe aber schon 3.000 einzelne PlannedLandUse GML-Files mit zusammen >600 MB hochgeladen und erfolgreich validiert. Allerdings war das gesamte System danach auf Tage ausgebremst, da im Hintergrund die Testberichte erst nach Ablauf von 8 Tagen aus dem System gelöscht werden. Man sollte also etwas vorsichtig zu Werke gehen und ggf. die Staging Umgebung nutzen oder die ETF WebApp auf einem eigenen Server hosten.

