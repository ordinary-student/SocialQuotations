'''
Created on 2020年3月8日

@author: Administrator
'''

import os
import threading
from tkinter import Tk, ttk, Menu, messagebox, Frame, StringVar, Entry, Button, LabelFrame
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

import quotations.quotations as quo


#
# 初始化窗口
#
def init_window():

    # 初始化窗口
    window = Tk()
    # 设置标题
    window.title('语录')
    # 设置窗口大小
    width = 600
    height = 300
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(alignstr)
    # 设置窗口最小大小
    window.minsize(600, 300)
    # 设置窗口是否可变长、宽，True：可变，False：不可变
    window.resizable(width=True, height=True)
    # 设置图标
    window.iconbitmap(r"mainframe\icon.ico")

    # 创建上边的frame
    top_frame = Frame(window, height=3)
    top_frame.pack(side='top', padx=2, pady=2, expand=True, fill='x')

    # 创建一个下拉列表
    type_str = StringVar()
    type_combobox = ttk.Combobox(top_frame, textvariable=type_str, font=('楷体', 14), state='readonly')
    # 设置下拉列表的值
    type_combobox['values'] = ['社会语录', '情话说']
    # 设置下拉列表默认显示的值
    type_combobox.current(0)
    # 设置列表框字体
    combobox_font = Font(family="楷体", size=14)
    type_combobox.option_add("*TCombobox*Listbox*Font", combobox_font)
    # type_combobox.pack(expand=True, fill='x', side='top')
    type_combobox.pack(side='left', padx=2, expand=True, fill='both')

    # 设置自动删除
    def setautodelete(event):
        quo.autodeleteflag = not quo.autodeleteflag
        if quo.autodeleteflag:
            messagebox.showinfo(title='提示', message='已开启自动删除！')
        else:
            messagebox.showinfo(title='提示', message='已关闭自动删除！')

    # 创建输入框
    entry = Entry(top_frame, show=None, font=('楷体', 14))
    entry.pack(side='left', padx=2, expand=True, fill='both')
    # 键盘监听按键F1
    entry.bind('<Key-F1>', setautodelete)

    # 声音标志
    global sound_flag
    sound_flag = True

    #
    # 获取语录
    #
    def get_says():
        # 获取类型
        type_val = type_combobox.get()
        #判断类型
        if type_val=='社会语录':
            type_='shehui'
        else:
            type_='qinghua'
            
        # 获取语录
        result = quo.get(type_).strip() + '\r\n'
        # 显示语录
        entry.delete(0, 'end')
        entry.insert(0, result)
        global text_area
        text_area.insert(0.0, result)
        # 获取语录语音文件
        quo.get_audio_file(result)
        #判断
        if sound_flag:
            # 朗读语录-开线程
            t = threading.Thread(target=read)
            t.start()

    # 创建获取按键
    button = Button(top_frame, text='获取', font=('楷体', 14), bg='#99FF99', command=get_says)
    button.pack(side='left', padx=2, expand=True, fill='both')

    # 创建下边的frame
    bottom_frame = LabelFrame(window, text='记录')
    bottom_frame.pack(side='top', expand=True, fill='both')

    # 弹出右键菜单
    def popupmenu(event):
        menu.post(event.x_root, event.y_root)

    # 打开目录
    def opendir(event):
        # start_directory = r'E:\temp'
        # os.system("explorer.exe %s" % start_directory)
        # start_directory = r'E:\temp'
        # os.startfile(start_directory)
        os.system("start explorer E:\\temp\\yulu\\")

    # 创建带滚动条的文本域
    global text_area
    text_area = ScrolledText(bottom_frame, width=20, height=20, font=('楷体', 14))
    text_area.pack(expand=True, fill="both")
    #绑定右键鼠标事件
    text_area.bind("<Button-3>", popupmenu)
    # 键盘监听按键F1
    text_area.bind('<Key-F1>', opendir)

    # 朗读
    def read():
        quo.read(quo.last_audio_file)
        
    # 静音
    def mute():
        global sound_flag
        sound_flag = not sound_flag

    # 清空
    def clear():
        # 清空输入框
        entry.delete(0, 'end')
        # 清空文本域
        text_area.delete(0.0, 'end')
        
    # 导出记录
    def export():
        # 写入文件到桌面
        filename=getdesktoppath() + '\\yulu.txt'
        with open(filename, 'w') as f:
            f.write(text_area.get(0.0, 'end'))
        if os.path.exists(filename):
            messagebox.showinfo(title='提示', message='导出成功！')
        else:
            messagebox.showerror(title='错误', message='导出失败！')

    # 创建菜单
    menu = Menu(text_area, tearoff=0)
    menu.add_command(label="朗读", font=('楷体', 12),command=read)
    menu.add_separator()
    menu.add_checkbutton(label="静音", font=('楷体', 12), command=mute)
    menu.add_separator()
    menu.add_command(label="清空记录", font=('楷体', 12), command=clear)
    menu.add_separator()
    menu.add_command(label="导出记录", font=('楷体', 12), command=export)

    # 进入消息循环
    window.mainloop()


#
# 获取当前系统的桌面的路径
#
def getdesktoppath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


#
# 主函数
#
def main():
    # 初始化窗口
    init_window()


#
# 入口
#
if __name__ == '__main__':
    # 主函数
    # main()
    pass
   
