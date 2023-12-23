import PySimpleGUI as sg
import pandas as pd
import mysql.connector
import os

mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="aplikasi")
mycursor=mysqldb.cursor()


sg.theme('DarkGreen4')

EXCEL_FILE = 'Data Mahasiswa.xlsx'

df = pd.read_excel(EXCEL_FILE)

layout=[
[sg.Text('Masukan Data Diri: ')],
[sg.Text('Nama Lengkap',size=(15,1)), sg.InputText(key='Nama Lengkap')],
[sg.Text('NIM',size=(15,1)), sg.InputText(key='NIM')],
[sg.Text('Alamat',size=(15,1)), sg.Multiline(key='Alamat')],
[sg.Text('Tgl Lahir',size=(15,1)), sg.InputText(key='Tgl Lahir'),
                                    sg.CalendarButton('Kalender', target='Tgl Lahir', format=('%Y-%m-%d'))],
[sg.Text('Jenis Kelamin',size=(15,1)), sg.Combo(['pria','wanita'],key='Jekel')],
[sg.Text('Peminatan',size=(15,1)), sg.Checkbox('Distributed Computing',key='DC'),
                             sg.Checkbox('Kecerdasan Artifisial',key='AI')],
[sg.Submit(), sg.Button('clear'), sg.Button('view data'), sg.Button('open excel'), sg.Exit()]

]

window=sg.Window('From Data Mahasiswa',layout)

def select():
    results = []
    mycursor.execute("select nama_lengkap,nim,alamat,tgl_lahir,jekel,peminatan from pendaftaran order by id desc")
    for res in mycursor:
        results.append(list(res))

    headings=['Nama Lengkap','NIM','Alamat','Tgl Lahir', 'Jekel', 'Peminatan'] 

    layout2=[
        [sg.Table(values=results,
        headings=headings,
        max_col_width=35,
        auto_size_columns=True,
        display_row_numbers=True,
        justification='right',
        num_rows=20,
        key='-Table-',
        row_height=35)]
    ]   

    window=sg.Window("List Data", layout2)
    event, values = window.read()

def clear_input():
    for key in values:
        window[key]('')
        return None

while True :
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'EXIT':
        break
    if event == 'Clear':
        clear_input()
    if event == 'view data':
        select()  
    if event == 'open excel':
        os.startfile(EXCEL_FILE)     
    if event == 'Submit':
        nama_lengkap=values["Nama Lengkap"]
        nim=values["NIM"]
        alamat=values["Alamat"]
        tgl_lahir=values["Tgl Lahir"]
        jekel=values["Jekel"]
        dc=values["Distibuted Computing"]
        ai=values["Kecerdasan Artifisial"]

        if distibutedcomputing == True:
            hobi="Distributed Computing"
        if kecerdasanartifisial == True:
            hobi="Kecerdasan Artifisial"

        sql="insert into pendaftaran(nama_lengkap,nim,alamat,tgl_lahir,jekel,peminatan) values(%s,%s,%s,%s,%s,%s)"
        val=(nama_lengkap,nim,alamat,tgl_lahir,jekel,peminatan)
        mycursor.execute(sql,val)
        mysqldb.commit()
        
        df =df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Berhasil Di Simpan')
        clear_input()
window.close()       