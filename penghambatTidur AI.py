import pandas as pd
import numpy as np
import heapq

df = pd.read_csv("TUBESAI01 - Sheet1.csv") #read file from excel
# print(df.head()) #print the first 5 row

#TAHAP FUZIFIKASI
#ipk
def uIPK_buruk(ipk):
  #hasilnya 0-1
  if ipk <= 2.00:
    return 1
  if ipk > 2.00  and ipk < 2.75:
    return (ipk-2.00)/0.75
  
  return 0

def uIPK_cukup(ipk):
  if ipk < 2.00:
    return 0
  if ipk >= 2.00 and ipk < 2.75:
    return (ipk-2.00)/0.75
  if ipk >= 2.75 and ipk < 3.25:
    return -(ipk-3.25)/0.5
  
  return 0

def uIPK_besar(ipk):
  if ipk < 2.75:
    return 0
  if ipk > 2.75 and ipk < 3.25:
    return (ipk-2.75)/0.5
  return 1

def uIPK(ipk):

  return [round(uIPK_buruk(ipk),2),
          round(uIPK_cukup(ipk),2), 
          round(uIPK_besar(ipk),2)]

#insert ipk to array
IPK = df["IPK"]
kecil = []
sedang = []
besar = []
fuzzIPK = []
for ipk in IPK:
  fuzz = uIPK(ipk)
  #print(fuzz)
  fuzzIPK.append(fuzz)
  kecil.append(fuzz[0])
  sedang.append(fuzz[1])
  besar.append(fuzz[2])

df["IPK_kecil"] = kecil
df["IPK_sedang"] = sedang
df["IPK_besar"] = besar
# print(df.head(50)) # print the first 50 row (use it to check data)

#Gaji
def gaji_kecil(gaji):
  if gaji < 8:
    return 1
  if gaji >= 8 and gaji < 18:
    return (gaji-8)/10
  return 0

def gaji_sedang(gaji):
  if gaji < 8:
    return 0
  if gaji >= 8 and gaji < 18:
    return -(gaji-18)/10
  if gaji >= 18 and gaji <28:
    return (gaji-18)/10
  if gaji >= 28:
    return 0
  return 1

def gaji_besar(gaji):
  if gaji < 18:
    return 0
  if gaji >= 18 and gaji < 28:
    return -(gaji-28)/10
  if gaji >= 28 and gaji < 38:
    return (gaji-28)/10
  if gaji >= 38:
    return 0
  
  return 1

def gaji_sangatbesar(gaji):
  if gaji < 28:
    return 0
  if gaji >= 28 and gaji < 38:
    return -(gaji-38)/10
  return 1

def uGaji(gaji):
  return [gaji_kecil(gaji),
          gaji_sedang(gaji), 
          gaji_besar(gaji), 
          gaji_sangatbesar(gaji)]

#Insert gaji into array
Gaji = df["Gaji (Jt)"]
kecil = []
sedang = []
besar = []
sangatBesar = []
fuzzGaji = []
for gaji in Gaji:
  fuzz = uGaji(gaji)
  #print(fuzz)
  fuzzGaji.append(fuzz)
  kecil.append(fuzz[0])
  sedang.append(fuzz[1])
  besar.append(fuzz[2])
  sangatBesar.append(fuzz[3])

df["Gaji_Kecil"] = kecil
df["Gaji_sedang"] = sedang
df["Gaji_besar"] = besar
df["Gaji_sangatBesar"] = sangatBesar
# print(df.head(50)) # print the first 20 row (use it to check data)

#print(fuzzIPK)


#TAHAP INFERENCE
#menentukan kategori dari tiap nilai yang diberikan pada array fuzzXD
total = 0
fuzzAkhirIPK = []
fuzzAkhirGaji = []

for fuzz in fuzzIPK: 
    fuzzXD = list(fuzz)
    if fuzzXD[0] > fuzzXD[1] or fuzzXD[1] > (fuzzXD[0] <fuzzXD[2]):
       # print("ipk ke : "+str(total)+"  kecil "+str(fuzzXD[0])+" sedang "+str(fuzzXD[1]))
       # print(fuzzXD,end='\n\n')
        fuzzAkhirIPK.append(["kecil",fuzzXD[0],"sedang",fuzzXD[1]])
        total+=1
    elif fuzzXD[1] > fuzzXD[2] or fuzzXD[2] >= fuzzXD[1]:
        # print("ipk ke : "+str(total)+"  sedang "+str(fuzzXD[1])+" tinggi "+str(fuzzXD[2]))
        # print(fuzzXD,end='\n\n')
        fuzzAkhirIPK.append(["sedang",fuzzXD[1],"tinggi",fuzzXD[2]])
        total+=1
    else:
        print(fuzzXD)
        
# for i in range(len(fuzzAkhirIPK)):
#     print(str(i)+"  "+str(fuzzAkhirIPK[i]),end="\n\n")

total = 0
for fuzz in fuzzGaji:
    fuzzXD = list(fuzz)
    if fuzzXD[0] > fuzzXD[1] or fuzzXD[1] > (fuzzXD[0] <fuzzXD[3]) and fuzzXD[0] != 0.0 and fuzzXD[0] != 0:
        # print("gaji ke : "+str(total)+"  kecil "+str(fuzzXD[0])+" sedang "+str(fuzzXD[1]))
        # print(fuzzXD,end='\n\n')
        fuzzAkhirGaji.append(["kecil",fuzzXD[0],"sedang",fuzzXD[1]])
        total+=1
    elif fuzzXD[1] > fuzzXD[2] or fuzzXD[2] >= fuzzXD[1] and fuzzXD[0] == 0 and fuzzXD[0] == 0.0 and fuzzXD[3] == 0 and fuzzXD[3] == 0.0:
        # print("gaji ke : "+str(total)+"  sedang "+str(fuzzXD[1])+" besar "+str(fuzzXD[2]))
        # print(fuzzXD,end='\n\n')
        fuzzAkhirGaji.append(["sedang",fuzzXD[1],"besar",fuzzXD[2]])
        total+=1
    elif fuzzXD[2] > fuzzXD[3] or fuzzXD[3] >= fuzzXD[2]:
        # print("gaji ke : "+str(total)+"  besar "+str(fuzzXD[2])+" sangat besar "+str(fuzzXD[3]))
        # print(fuzzXD,end='\n\n')
        fuzzAkhirGaji.append(["besar",fuzzXD[2],"sangat besar",fuzzXD[3]])
        total+=1
    else:
        print(fuzzXD)

# for i in range(len(fuzzAkhirGaji)):
#     print(str(i)+"  "+str(fuzzAkhirGaji[i]),end="\n\n")


#INFERENCE XD
def inferenceRule(ipk,gaji):
    if ipk == "kecil" and gaji == "kecil":
        return "rendah"
    if ipk == "kecil" and gaji == "sedang":
        return "rendah"
    if ipk == "kecil" and gaji == "besar":
        return "rendah"
    if ipk == "kecil" and gaji == "sangat besar":
        return "rendah"
    if ipk == "sedang" and gaji == "kecil":
        return "tinggi"
    if ipk == "sedang" and gaji == "sedang":
        return "rendah"
    if ipk == "sedang" and gaji == "besar":
        return "rendah"
    if ipk == "sedang" and gaji == "sangat besar":
        return "rendah"
    if ipk == "tinggi" and gaji == "kecil":
        return "tinggi"
    if ipk == "tinggi" and gaji == "sedang":
        return "tinggi"
    if ipk == "tinggi" and gaji == "besar":
        return "tinggi"
    if ipk == "tinggi" and gaji == "sangat besar":
        return "rendah"

nk = []

for i in range(len(fuzzAkhirIPK)):
    isi = []
        #quarter 
    isi.append(inferenceRule(fuzzAkhirIPK[i][0],fuzzAkhirGaji[i][0]))
    isi.append(min(fuzzAkhirIPK[i][1],fuzzAkhirGaji[i][1]))
    isi.append(inferenceRule(fuzzAkhirIPK[i][0],fuzzAkhirGaji[i][2]))
    isi.append(min(fuzzAkhirIPK[i][1],fuzzAkhirGaji[i][3]))

    isi.append(inferenceRule(fuzzAkhirIPK[i][2],fuzzAkhirGaji[i][0]))
    isi.append(min(fuzzAkhirIPK[i][3],fuzzAkhirGaji[i][1]))
    isi.append(inferenceRule(fuzzAkhirIPK[i][2],fuzzAkhirGaji[i][2]))
    isi.append(min(fuzzAkhirIPK[i][3],fuzzAkhirGaji[i][3]))
    nk.append(isi)


rendah = []
tinggi = []
for i in range(len(nk)):
  xd = []
  dx = []
  for j in range(len(nk[i])-1):
    if(nk[i][j] == "rendah"):
      xd.append(nk[i][j+1])
    elif(nk[i][j] == "tinggi"):
      dx.append(nk[i][j+1])
    elif(len(dx)==0):
      dx.append(0)
  rendah.append(xd)
  tinggi.append(dx)


# for i in range(len(nk)):
#   print("data ke"+str(i)+str(nk[i]),end ="\n")
#   print("dengan rendah : "+str(rendah[i]),end="\n")
#   print("dengan tinggi : "+str(tinggi[i]),end="\n\n")


finalNK = []
for i in range(len(nk)):
  finalNK.append(["rendah",max(rendah[i]),"tinggi",max(tinggi[i])])

for i in range(len(finalNK)):
  print("data ke : "+str(i+1)+"  "+str(finalNK[i]),end ="\n")


#TAHAP DEFUZIFIKASI
       
        


