# R3.5.1 - Orodje za delo z evalvacijskimi nalogami (SuperGLUE)

V tem repozitoriju se nahaja rezultat aktivnosti A3.5 - R3.5.1 Orodje za delo z evalvacijskimi nalogami in za primerjavo različnih postopkov.

#### Povezave, vezane na orodje:
* opisi nalog in dodatne informacije o SuperGLUE: https://super.gluebenchmark.com/tasks
* prevodi SuperGLUE: https://www.clarin.si/repository/xmlui/handle/11356/1380

#### Uporaba:

Skripte poganjamo tako, da v ukazno vrstico vnesemo njihovo ime in dva argumenta. 
Prvi argument predstavlja pot do mape, kjer se nahajajo naloge SuperGLUE v izvornem formatu, drugi pa pot do mape, v katero bodo shranjene datoteke v ciljnem formatu.
Program bo samodejno ustvaril potrebne mape v ciljni datoteki. 
Primer za pretvorbo datotek iz jsonl v csv:

```
python jsonl2csv.py --jsonl path/to/SuperGLUE-json --csv path/to/SuperGLUE-csv 
```

Postopek je podoben tudi pri drugih skriptah, spreminjajo se le imena argumentov.
Na primer, prvi argument skripte, ki prevaja iz txt v csv, bo `--txt`, drugi pa `--csv`.

> Operacijo Razvoj slovenščine v digitalnem okolju sofinancirata Republika Slovenija in Evropska unija iz Evropskega sklada za regionalni razvoj. Operacija se izvaja v okviru Operativnega programa za izvajanje evropske kohezijske politike v obdobju 2014-2020.

![](Logo_EKP_sklad_za_regionalni_razvoj_SLO_slogan.jpg)
