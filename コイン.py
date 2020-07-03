import cv2 

def header(input_file): # NCプログラムのヘッダー部分
    file.write('%\n')
    file.write('O0031\n')
    file.write('G90G54G1F1000\n')
    file.write('G0G43Z200.0H32\n')
    file.write('G0X0Y0\n')
    file.write('S3000M3\n')

def footer(input_file): # NCプログラムのフッター部分
    file.write('G0Z200.0M5\n')
    file.write('M30\n')
    file.close()

Zmax=0 # 最大Z高さ
Zmin=-0.1 #　最小Z高さ
pik=0.1 # 1ピクセルを何ミリにするかを設定
Ap_Z=5.0 #　アプローチ高さ

img = cv2.imread('Oita.bmp') # 画像の読込
gry=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # グレイスケールに変換
height1,width1= gry.shape # 画像の高さと幅を変数にセット
file = open('output.NC', 'w') # 書き込みファイルを設定
header(file) # NCプログラムのヘッダー部分をファイルに書き込み

for i in range(0,width1) : # X方向のループ
    Command1=['X',str(round(i*pik,3)),'\n']
    file.writelines(Command1)
    Command2=['G0Z',str(Ap_Z),'\n']
    file.writelines(Command2)
    file.write('G1')
    for j in reversed(range(0,height1)): # Y方向のループ
         color1=(gry[j,i]) #各ピクセルの濃淡情報を変数にセット
         Z1=(Zmax-Zmin)*(color1-255)/255+Zmin #濃淡情報を高さ情報に変換(黒い方をふかく削る)
         j1=height1-1-j
         Command3=['Y',str(round(j1*pik,3)),'Z',str(round(Z1,3)),'\n']
         file.writelines(Command3)
    file.writelines(Command2)

footer(file) # NCプログラムのフッター部分をファイルに書き込み

