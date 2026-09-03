import pandas as pd
import PySimpleGUI as sg
from pathlib import Path
import chardet
import matplotlib.pyplot as plt
import seaborn as sns

sg.theme("DarkBrown3")

layout = [[sg.B("CSVファイルを選択してください",k="btn1"),sg.T(k="txt1")],[sg.ML(k="txt2",font=(None,14),size=(80,15))]]
win = sg.Window("ファイルを選択してください",layout)

def loadtext():
    global loadname, enc
    loadname = sg.popup_get_file("CSVファイルを選択してください")
    if not loadname.lower().endswith('.csv'):
        return
    with open(loadname,"rb") as data:
        sns.set(font=["Meiryo","Yu Gothic","Hiragino Maru Gothic Pro"])
        data = pd.read_csv(loadname, usecols=["都市","気温", "緯度"])
        if len(data["都市"]) == len(set(data["都市"])):
            df = pd.DataFrame(data)
            df = df.dropna(axis=0)
            txt1 = "データを読み込みました。"
            win["txt1"].update(txt1)
            df.plot.scatter(x="緯度",y="気温",c="b",figsize=(30,8))
            plt.title("緯度と気温の相関について")
            plt.show()
            print(df.shape)
        else:
           txt1 = "データが重複しています。ファイルを読み込みなおしてください。"
           win["txt1"].update(txt1)
            

while True:
    e,v = win.read()
    if e == "btn1":
        loadtext()
    if e == None:
        break
win.close()



layout = [[sg.T("緯度を入力してください。")],[sg.T(k = "txt2")],[sg.I("",k="in1")],[sg.B( "実行" ,k = "btn"),sg.T(k = "txt1")]]
win = sg.Window("平均気温推定アプリ",layout,font=(None,14),size=(500,150))

def execute():
 data = pd.read_csv(loadname,usecols=["都市","気温", "緯度"])
 if len(data["都市"]) == len(set(data["都市"])):
        data = pd.read_csv(loadname,index_col=0)
        df = pd.DataFrame(data)
        df = df.dropna(axis=0)
        df = df.drop(df[((df["緯度"]<=30) & (df["気温"]<=20)) | (((df["緯度"]<=40) & (df["緯度"]>30)) & ((df["気温"]<=10) | (df["気温"]>=25))) | (((df["緯度"]<=50) & (df["緯度"]>40)) & ((df["気温"]<=5) | (df["気温"]>=20))) | ((df["緯度"]>50) & (df["気温"]>=10))].index,axis=0)
        print(df.shape)
    
        x = df.drop("気温",axis=1)
        t = df["気温"]
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(x,t)
        from sklearn.model_selection import train_test_split
        x_train,x_test,t_train,t_test = train_test_split(x,t,test_size=0.4,random_state=1)
        model.fit(x_train,t_train)
    
        #print(model.score(x_train,t_train))
        #print(model.score(x_test,t_test))
        try:
            if float(v["in1"]) < 0 or float(v["in1"]) > 90:
                txt2 = f"精度は、{round(model.score(x_test,t_test),2) * 100}％ "
                txt1 = f"緯度は0°から90°まで入力してください。"
                win["txt2"].update(txt2)
                win["txt1"].update(txt1) 
            else:  
                y_pred = model.predict([[float(v["in1"])]])
                txt2 = f"精度は、{round(model.score(x_test,t_test),2) * 100}％ "
                txt1 = f"推定平均気温は、{round(y_pred[0],2)}℃です。"
                win["txt2"].update(txt2)
                win["txt1"].update(txt1)     
        except ValueError:
            txt2 = f"精度は、{round(model.score(x_test,t_test),2) * 100}％ "
            txt1 = "数字を入力してください。"
            win["txt2"].update(txt2)
            win["txt1"].update(txt1) 
 else:
    txt2 = "データが重複していたため、正常に学習できませんでした。"
    win["txt2"].update(txt2)      

while True:
    e,v = win.read()
    if e == "btn":
        execute()
    if e == None:
        break
win.close()
