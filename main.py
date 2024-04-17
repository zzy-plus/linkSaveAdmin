import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from service import *

_version = '0.1.1'

# 上传存档
def upload():
    try:
        # 获取下拉框选择的值
        if cbx.get() == '':
            messagebox.showwarning('提示', '需要先选择存档！')
            return
        profileName = profilesMap[cbx.get()]
        # 压缩文件
        profilesPath = getUserDoc() + r'\Euro Truck Simulator 2\profiles'
        profilePath = f'{profilesPath}\\{profileName}'
        zipPath = f'{profilesPath}\\zip1'
        zipFile(profilePath, zipPath)
        # 上传文件
        ftpUpload(zipPath + '.zip', '/shared/zip1.zip')

        messagebox.showinfo('提示', '存档上传成功.')
    except Exception as ex:
        print(f'上传失败{ex}')
        messagebox.showerror('错误', f'文件上传失败！\n{ex}')


# 更新坐标
def update():
    if cbx.get() == '':
        messagebox.showwarning('提示', '需要先选择存档！')
        return
    result = updateData(profilesMap[cbx.get()])
    if result:
        messagebox.showinfo('提示', '中途点更新成功.')
    else:
        messagebox.showerror('错误', '中途点更新失败！\n可能是服务器暂时不可用...')


def clean():
    result = messagebox.askokcancel("确认", "您确定要执行这个操作吗？")
    if result:
        cleanData()


def add():
    if cbx.get() == '':
        messagebox.showwarning('提示', '需要先选择存档！')
        return
    value = simpledialog.askstring("坐标名称", "为这个坐标点起一个名字：", parent=window)
    if value == '':
        return
    if value is not None:
        location = getCurLocation(profilesMap[cbx.get()])
        newData = {
            'name': value,
            **location
        }
        addData(newData)


if __name__ == '__main__':

    pwd = simpledialog.askstring("验证", "输入密码：")
    status = getAccess(pwd)
    if not status:
        exit(0)

    profiles, profilesMap = getProfiles()
    try:
        window = tk.Tk()
        window.title('接档器管理面板' + ' V' + _version)
        screenWidth = window.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = window.winfo_screenheight()  # 获取显示区域的高度
        width = 290  # 设定窗口宽度 300
        height = 215  # 设定窗口高度 180
        left = (screenWidth - width) // 2
        top = (screenHeight - height) // 2
        window.geometry(f'{width}x{height}+{left}+{top}')
        window.resizable(width=False, height=False)
        #window.iconphoto(True, tk.PhotoImage(file=resource_path("res/icon1.png")))

        tk.Label(window,text='选择要操作的活动存档:', font=('宋体', 11)).place(x=60,y=15)

        cbx = ttk.Combobox(window, state='readonly', width=20)
        cbx.config(values=profiles)
        cbx.place(x=60, y=42)

        tk.Button(window, text='清空坐标', font=('宋体', 12), foreground='red', width=10,
                  command=clean).place(x=60, y=80)
        tk.Button(window, text='获取坐标', font=('宋体', 12), foreground='blue', width=10,
                  command=add).place(x=60, y=112)
        tk.Button(window, text='上传坐标', font=('宋体', 12), foreground='orange', width=10,
                  command=update).place(x=60, y=144)
        tk.Button(window, text='上\n传\n存\n档', font=('宋体', 12), foreground='green', width=7, height=5,
                  command=upload).place(x=155, y=80)


        tk.Label(window, text='上传坐标前最好确认下data.json文件！', font=('宋体', 9),
                 foreground='red').place(x=150, y=188, anchor='center')

        window.mainloop()
    except Exception as e:
        print(e)