import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7000 # Port範圍介於1024~65535，其中0~1023為系統保留不可使用
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 創建socket對象(Ipv4,TCP宣告)
s.bind(ADDR)    # 綁定地址和埠
s.listen()      # 伺服器端監聽socket串接

def handle_client(conn, addr):  # 等待接收client端訊息存放在2個變數conn和addr裡
    # 如果addr不在user字典裡
    if not addr in user:
        print(f"[NEW CONNECTION] {addr} connected.")    # 新的user連線成功

        for scs in ser_cli_soc:    # 從user依序取出address(key:addr)
            ser_cli_soc[scs].send("[".encode(FORMAT) + client_name + "進入聊天室]".encode(FORMAT))  # 依序發送user字典的data(client_name)到client端   # 通知所有原在線的client端 新user(client_name)進入聊天室
        user[addr] = client_name.decode(FORMAT) # client_name是最新進入聊天室的client，解壓後放入user   # 接收的訊息(client_name)解碼成FORMAT(utf-8)並存在字典user裡,鍵名(key)定義為addr
        ser_cli_soc[addr] = conn   # 將伺服器與伺服器埠號為addr的socket對象(conn)放入字典ser_cli_soc裡
    
    # Start to chat
    while True:
        msg = conn.recv(1024)   # receive data(msg) from the client
        # 如果EXIT在發送的data(msg)裡 或 user點選關閉視窗按鈕
        if(('EXIT'.lower() in msg.decode(FORMAT)) | (msg.decode(FORMAT) == 'close')):
            name = user[addr]   # 變數name值為 user字典addr鍵(key)對應的值(client_name)
            user.pop(addr)      # 刪除離開聊天室的user(client)
            ser_cli_soc.pop(addr)   # 刪除離開聊天室的user的addr

            for scs in ser_cli_soc:    # 從user依序取出address(key:addr)
                ser_cli_soc[scs].send((name + "離開聊天室...").encode(FORMAT))  # 依序發送data(client_name)到client端   # 通知所有還在線的client端 有user(client_name)退出聊天室
            print(f"[CLOSED] {addr} closed.")   # 離開聊天室的user(client)的addr(SERVER, PORT)

            global num  # 宣告函數定義外的全域變數(global variable) ，使該全域變數可以在函數中進行處理
            num = num - 1   # 聊天室人數-1
            break
        else:
            print(f"{msg.decode(FORMAT)} from {addr}")  # 哪位user傳了什麼訊息到聊天室
            for scs in ser_cli_soc:    # 從user依序取出address(key:addr)
                if ser_cli_soc[scs] != conn:   # 若 address不等於 目前傳送訊息的user 的address
                    ser_cli_soc[scs].send(msg)   # 就 發送data(msg) 到client端聊天室

num = 0 # 聊天室人數
user = {}   # 存放字典{addr:name}
ser_cli_soc = {}   # 存放{socket:不同線程(thread)的socket對象}

print("[STARTING] Server is starting...")

while True:
    try:
        print(f"[LISTENING] Server is listening on {SERVER}")
        conn, addr = s.accept() # conn存串接對象、addr存連線資訊    # 等待接收client端的連接請求    # 用於伺服器端接收串接，並會回傳(conn,address)串接對象與IP位址資訊
    except ConnectionResetError:    # 掛斷時會報錯
        print("Someone left unexcept.")

    client_name = conn.recv(1024)  # receive data(client name) from the client  # 1024 是緩衝區數據大小限制最大值參數bufsize
    if client_name.decode() == 'close': # user沒有登入，直接關閉視窗
        print(addr, "關閉了登入視窗...")
        continue
    print("client_name = ", client_name.decode())   # 新user的name  # decode client_name to get the string
    num = num + 1   # 聊天室人數+1

    # 為server分配線程
    r = threading.Thread(target=handle_client, args=(conn,addr), daemon=True)   # handle_client(conn, addr) # daemon=True 表示創建的子線程守護主線程，主線程退出子線程直接銷毀
    r.start()

    print("聊天室人數：", num)  # 現在有多少人在聊天室 # 只要有人加入就更新