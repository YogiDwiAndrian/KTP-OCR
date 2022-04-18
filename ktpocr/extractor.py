import cv2
import json
import re
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from ktpocr.form import KTPInformation
from ktpocr.kota import ListKota
from PIL import Image

class KTPOCR(object):
    def __init__(self, image):
        self.image = cv2.imread(image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.th, self.threshed = cv2.threshold(self.gray, 127, 255, cv2.THRESH_TRUNC)
        self.kota = ListKota()
        self.result = KTPInformation()
        self.master_process()

    def process(self, image):
        raw_extracted_text = pytesseract.image_to_string((self.threshed), lang="ind")
        return raw_extracted_text

    def word_to_number_converter(self, word):
        word_dict = {
            '|' : "1"
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res


    def nik_extract(self, word):
        word_dict = {
            'b' : "6",
            'e' : "2",
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res
    
    def extract(self, extracted_result):
        #print(extracted_result.replace('\n', ' -- '))
        for word in extracted_result.split("\n"):
            if "NIK" in word:
                try:
                    word = word.split(':')
                    self.result.nik = self.nik_extract(word[-1].replace(" ", ""))
                except:
                    self.result.nik =''
                continue

            if "Nama" in word:
                try:
                    word = word.split(':')
                    self.result.nama = word[-1].replace('Nama ','')
                except:
                    self.result.nama = ''
                continue

            if "Tempat" in word:
                word = word.split(':')
                try:
                    num = ''
                    for s in word:
                        num = re.findall(r'\d+', s)

                    txt = ''
                    for i in num:
                        txt+=i
                   
                    if len(txt) == 8:
                        self.result.tanggal_lahir = f'{txt[:2]}-{txt[2:4]}-{txt[4:]}'
                    else:
                        self.result.tanggal_lahir = ''
                    
                    for split in word:
                        for i in self.kota.kota_lahir:
                            kota = re.findall(i, split.title())
                            if (kota):
                                self.result.tempat_lahir = kota[0].upper()
                                break
                            else:
                                self.result.tempat_lahir = ''
                except:
                    self.result.tanggal_lahir = ''
                    self.result.tempat_lahir = ''
                continue
            
            if 'LAKI-LAKI' or 'LAKILAKI' or 'LAKI' or 'LELAKI' in word:
                self.result.jenis_kelamin = 'LAKI-LAKI'
            elif 'PEREMPUAN' or 'PEREM' or 'MPUAN' or 'PEREMP' in word:
                self.result.jenis_kelamin = 'PEREMPUAN'

            if 'Darah' in word:
                word = word.split(':')
                try:
                    self.result.golongan_darah = re.search("(O|A|B|AB)", word[-1])[0]
                except:
                    self.result.golongan_darah = '-'
            if 'Alamat' in word:
                try:
                    self.result.alamat = self.word_to_number_converter(word).replace("Alamat ","")
                except:
                    self.result.alamat = ''
                
            if 'NO.' in word:
                try:
                    self.result.alamat = self.result.alamat + ' '+word
                except:
                    self.result.alamat = ''
                
            if "Kecamatan" in word:
                try:
                    self.result.kecamatan = word.split(':')[1].strip()
                except:
                    self.result.kecamatan = ''
            if "Desa" in word:
                try:
                    wrd = word.split()
                    desa = []
                    for wr in wrd:
                        if not 'desa' in wr.lower():
                            desa.append(wr)
                    self.result.kelurahan_atau_desa = ''.join(wr)
                except:
                    self.result.kelurahan_atau_desa = ''

            if 'Kewarganegaraan' in word:
                try:
                    self.result.kewarganegaraan = word.split(':')[1].strip()
                except:
                    self.result.kewarganegaraan =''
                
            if 'Pekerjaan' in word:
                try:
                    wrod = word.split()
                    pekerjaan = []
                    for wr in wrod:
                        if not '-' in wr:
                            pekerjaan.append(wr)
                    self.result.pekerjaan = ' '.join(pekerjaan).replace('Pekerjaan', '').strip()
                except:
                    self.result.pekerjaan = ' '
                
            if 'Agama' in word:
                try:
                    self.result.agama = word.replace('Agama',"").strip()
                except:
                    self.result.agama = ''
                
            if 'Status Perkawinan' in word:
                try:
                    self.result.status_perkawinan = word.split(':')[1]
                except:
                    self.result.status_perkawinan = ''
                
            if "RT/RW" in word:
                try:
                    word = word.replace("RT/RW",'')
                    self.result.rt = word.split('/')[0].strip()
                    self.result.rw = word.split('/')[1].strip()
                except:
                    self.result.rt = ''
                    self.result.rw = ''
                

    def master_process(self):
        raw_text = self.process(self.image)
        print(raw_text)
        self.extract(raw_text)

    def to_json(self):
        return json.dumps(self.result.__dict__, indent=4)



