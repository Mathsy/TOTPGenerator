import tkinter as tk
import threading
import time
import pyotp
from tkinter import messagebox

class TOTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TOTP生成器")
        self.root.geometry("400x250")
        
        # 创建界面元素
        self.create_widgets()
        
        # 初始化变量
        self.totp = None
        self.running = False
        
    def create_widgets(self):
        # 密钥输入区域
        tk.Label(self.root, text="请输入密钥(base32):").pack(pady=5)
        self.secret_entry = tk.Entry(self.root, width=40)
        self.secret_entry.pack(pady=5)
        
        # 生成按钮
        self.generate_btn = tk.Button(self.root, text="生成OTP", command=self.generate_otp)
        self.generate_btn.pack(pady=10)
        
        # OTP显示
        self.otp_label = tk.Label(self.root, text="OTP: ", font=("Arial", 24))
        self.otp_label.pack(pady=10)
        
        # 有效期倒计时
        self.time_label = tk.Label(self.root, text="有效期: --秒")
        self.time_label.pack(pady=5)
        
        # 验证状态
        self.valid_label = tk.Label(self.root, text="状态: 等待生成")
        self.valid_label.pack(pady=5)
    
    def generate_otp(self):
        secret_key = self.secret_entry.get().strip()
        if not secret_key:
            messagebox.showerror("错误", "请输入有效的密钥")
            return
            
        try:
            self.totp = pyotp.TOTP(secret_key)
            current_otp = self.totp.now()
            self.otp_label.config(text=f"OTP: {current_otp}")
            self.update_validity(current_otp)
            
            # 启动倒计时线程
            if not self.running:
                self.running = True
                threading.Thread(target=self.update_countdown, daemon=True).start()
                
        except Exception as e:
            messagebox.showerror("错误", f"无效的密钥: {str(e)}")
    
    def update_validity(self, otp):
        if self.totp.verify(otp):
            self.valid_label.config(text="状态: 有效", fg="green")
        else:
            self.valid_label.config(text="状态: 无效", fg="red")
    
    def update_countdown(self):
        while self.running:
            if self.totp:
                # 计算剩余时间 (30 - (当前时间 % 30))
                remaining = 30 - int(time.time()) % 30
                self.time_label.config(text=f"有效期: {remaining}秒")
                
                # 当剩余时间为0时刷新OTP
                if remaining == 0:
                    current_otp = self.totp.now()
                    self.otp_label.config(text=f"OTP: {current_otp}")
                    self.update_validity(current_otp)
            
            time.sleep(1)
    
    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TOTPApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
