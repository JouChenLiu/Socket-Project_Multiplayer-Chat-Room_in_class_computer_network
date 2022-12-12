import socket
import sys
import tkinter as tk
import tkinter.messagebox
import tkinter.scrolledtext
import threading

SERVER = "140.115.140.103"
PORT = 7000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 創建socket對象(Ipv4,TCP宣告)
c.connect(ADDR) # 建立連接  # 客戶端指定要串接的IP位址跟Port號

# 傳送訊息給socket對象
def send(soc):
    if string != "":
        message = name + ": " + string  # 誰(name)傳送了什麼訊息(string)
        data = message.encode(FORMAT)
        soc.send(data)  # 傳送資料過去給串接對象(server/其它User聊天室)
        if string.lower() == "EXIT".lower():    # 關閉聊天室視窗
            exit() 

# 將訊息插入ScrolledText聊天室框框內
def chatblock(s):
        output_area.config(state='normal')    # normal:可編輯的模式
        output_area.insert('end', s)    # 插入內容到原內容的尾端
        output_area.yview('end')        # focus of text to the end of the text input. 直接顯示最下方的文字
        output_area.config(state='disabled')    # disabled:無法編輯的模式

# 接受訊息(threading)
def recv(soc):
    soc.send(name.encode(FORMAT))
    while True:
        data = soc.recv(1024)   # 接收資料
        s = data.decode(FORMAT)+'\n'
        chatblock(s)    # 將訊息插入ScrolledText聊天室框框內

# 將自己傳送的訊息插入到聊天室框框內 且傳送給socket對象
def myMsg():
    global string   # 宣告函數定義外的全域變數(global variable) ，使該全域變數可以在函數中進行處理
    string = input_area.get()   # 字串變數 取得文字內容
    send(c)         # 傳送資料過去給串接對象(server/其它User聊天室)
    if string != "":
        s = '我: ' + string + '\n'
        chatblock(s)    # 將訊息插入ScrolledText聊天室框框內
        input_area.set('')     # 輸入傳送訊息的文字框 的文字，才能再輸入新的訊息文字

# 建立聊天室視窗
def create():
    global name
    name = user_name.get()

    # 接收進程
    tr = threading.Thread(target=recv, args=(c,), daemon=True)  # recv(sock) # daemon=True 表示創建的子線程守護主線程，主線程退出子線程直接銷毀
    tr.start()

    # 關閉登入的視窗
    enter_label.destroy()
    enter_name.destroy()
    login_button.destroy()
    # 建立聊天室視窗
    window.title("多人聊天室")
    window.configure(bg='#FFD1A4')
    window.geometry("450x430+500+150")
    
    # 聊天室名稱之Label
    roomname = tk.Label(window, text="%s的聊天室" %name, width=35, bg='#A3D1D1', relief="ridge") # relief:指定邊框樣式(預設groove，其它還有flat.sunken.raised.ridge.solid)
    roomname.config(font=("微軟正黑體", 13))
    roomname.pack(pady=5)
    
    # 上方聊天室框框ScrolledText
    output_area.pack(padx=10, pady=5)
    output_area.config(state='disabled')    # disabled:無法編輯的模式

    # 下方User輸入想傳送的文字 的框架
    frame = tk.Frame(window, bg='#FFD1A4')
    # 請輸入訊息之Label
    input_label = tk.Label(frame, text="請輸入訊息:", anchor='w', width=10, bg='#FFD1A4')   # anchor='w':靠左側
    input_label.config(font=("微軟正黑體", 11))
    input_label.pack(side=tk.LEFT)  # pack:採用塊的方式組織配件 # side=tk.LEFT:靠左邊
    # User輸入想傳送的文字之Entry
    input_entry = tk.Entry(frame, bg='#B8B8DC', textvariable=input_area)    # textvariable可以看作是動態版的text，文字內容隨著變數值設置而改變
    input_entry.pack(side=tk.LEFT) # pack:採用塊的方式組織配件 # side=tk.LEFT:靠左邊
    # 傳送訊息之Button
    input_button = tk.Button(frame, text="傳送", command=myMsg, bg='#A3D1D1')    # 執行myMsg()
    input_button.config(font=("微軟正黑體", 11))
    input_button.pack(side=tk.LEFT, padx=15) # pack:採用塊的方式組織配件 # side=tk.LEFT:靠左邊

    frame.pack(anchor='center', pady=10)    # anchor='center':在整個視窗(window)向下pack的中間

# 再次確認是否關閉聊天室視窗
def quit():
    msgBox = tkinter.messagebox.askokcancel("剛才點擊了關閉按鈕", "確定要離開嗎?")
    if msgBox == True:  # 確定關閉視窗
        c.send('close'.encode(FORMAT))  # 傳送關閉視窗的通知給socket對象
        exit(0) # 關閉視窗

# 創建父容器GUI
window = tk.Tk()    #宣告
window.title("多人聊天室")  # 父容器標題
window.geometry("250x120+500+250")  # 設置父容器視窗初始大小，如果沒有這個設置，視窗會隨著物件大小的變化而變化  # 第1個加號是距離屏幕左邊的寬，第2個加號是距離屏幕頂部的高

# User登入視窗
# 請輸入名稱之Label
enter_label = tk.Label(window, text="請輸入您的名稱", width=40, height=2)
enter_label.config(font=("微軟正黑體", 11))
enter_label.pack(pady=2)    # pack:採用塊的方式組織配件 # 加入版面時預設會由上而下, 由左而右排版    # padx(pady):物件外部在x(y)方向保留空白的大小，單位預設為像素
# 輸入名字之Entry
user_name = tk.StringVar()  # 字串參數
enter_name = tk.Entry(window, width=20, textvariable=user_name) # textvariable可以看作是動態版的text，文字內容隨著變數值設置而改變
name = user_name.get()      # 字串變數 取得文字內容
enter_name.pack(pady=6)
# 登入之Button
login_button = tk.Button(window, text="登入", command=create)   # 執行create()->建立聊天室視窗  # relief:指定邊框樣式(預設groove，其它還有flat.sunken.raised.ridge.solid)
login_button.config(font=("微軟正黑體", 11))
login_button.pack(padx=20, pady=5)

print("Client connect to server")

# 聊天室視窗
# input_area:輸入傳送訊息的文字框 的文字
input_area = tk.StringVar()
# 聊天室框框scrolledtext卷軸文字圖形物件
output_area = tkinter.scrolledtext.ScrolledText(window, bg='#B8B8DC', wrap=tk.WORD)    # wrap=tk.WORD 表示該行的尾端如果有單字跨行列印，則把此單字放到下一行顯示

window.protocol("WM_DELETE_WINDOW", quit)   # 定義當用戶使用窗口管理器顯式關閉窗口時發生的情況  # 執行quit()
window.mainloop()   # 自動刷新畫面

c.close()   # 關閉Socket連接，並釋放所有相關資源