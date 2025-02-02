<h1 align="center">
    KTP-OCR
</h1>

<p align="center">
  <strong>Kartu Tanda Penduduk Extractor</strong><br>
  An attempt to create a production grade KTP extractor.
</p>

<div align="center">
    <img src="https://rossrightangle.files.wordpress.com/2012/05/e-ktp-contoh.jpg">
</div>

**KTP-OCR** is a open source python package that attempts to create a production grade KTP extractor. The aim of the package is to extract as much information as possible yet retain the integrity of the information.

---
<h2 style="font-weight:800;">Requirements</h2>
You will need tesseract with indonesian language support installed in your system. 

```console
$ brew install tesseract-lang
```
<h4 style="font-weight:800;">Tesseract installer for Windows.</h4>

Tesseract program [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

Download indonesian language [ind.traineddata](https://github.com/tesseract-ocr/tessdata) and then move to 'C:\Program Files\Tesseract-OCR\tessdata'

Adding environment path tesseract to system "Path >> C:\Program Files\Tesseract-OCR"

---


<h2 style="font-weight: 800;">🚀 How to launch</h2>

```console
$ git clone https://github.com/YogiDwiAndrian/KTP-OCR.git
$ cd KTP-OCR
$ pip install -r requirements.txt
$ python3 ocr.py <path-image>
```
---

<h2 style="font-weight: 800;">📝 Note from Yuka</h2>

* I am actively working to create a python package out of the main `ocr.py`. For now you can play with the old script.
* I have an idea to verify the address information from the KTP via external service (Google Maps) which can be used to further standardized Indonesian address' information.
