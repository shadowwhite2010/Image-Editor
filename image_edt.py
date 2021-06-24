import cv2
import tkinter as tk
from tkinter import ttk
import json
# from ttkthemes import ThemedTk
from tkinter import scrolledtext
from PIL import ImageTk, Image, ImageEnhance, ImageOps, ImageFilter 
from tkinter import filedialog, colorchooser
from tkinter.messagebox import showinfo
from string import ascii_uppercase, ascii_lowercase, digits
import numpy as np
from numpy.core.numeric import False_

import os
window = tk.Tk() 
# window = ThemedTk(theme="arc")


# window.geometry('700x700+300+150')
window.title("Image Editor")
# window.iconbitmap("icons/atha.ico")
window.resizable(width = True, height = True)
# window.resizable(0, 0)
# window.attributes('-toolwindow', True)
window.state('zoomed')

lenth=1100
wid=660
curr_img = 0
img = None
img_list = []
mask = []

passw_var=tk.StringVar()
key_var=tk.StringVar()
msg_var= tk.StringVar()
ext1_var = tk.StringVar()
ext2_var = tk.StringVar()
ext3_var = tk.StringVar()
ext4_var = tk.StringVar()
ext5_var = tk.StringVar()
ext6_var = tk.StringVar()
ext7_var = tk.StringVar()
ext8_var = tk.StringVar()
ext9_var = tk.StringVar()
ext0_var = tk.StringVar()
##stringvar for crp
crp_l = tk.StringVar()
crp_r = tk.StringVar()
crp_t = tk.StringVar()
crp_b = tk.StringVar()

##stringvar for effect
efct_var = tk.StringVar()
# detector = dtctr_gen()
# best_model = model_load()

panel=tk.LabelFrame(window, padx=2, pady=2, height=wid, width=lenth)
panel.grid(row=0, column=0, padx=0, pady=0,sticky = tk.NW)
# panel.pack(anchor = tk.NW, padx=2, pady=2)

# panel1=tk.Label(window, relief = "ridge", bd = 5, padx=5, pady=5, height=wid, width=int(lenth/3))
panel1=tk.Label(window, relief = "ridge", bd = 2, padx=0, pady=0)
panel1.grid(row=0, rowspan = 2, column=1, padx=0, pady=0, sticky = tk.E)
# panel1.pack(anchor = tk.S,  padx=2, pady=2)

panel_bot = tk.Frame(window, relief = "ridge")
panel_bot.grid(row = 1, column = 0, sticky = tk.SW, padx = 2) 

paned_bot = tk.PanedWindow(panel_bot, height = 105, width = 1107)
paned_bot.pack(fill = tk.BOTH, expand = 1, padx=2)

crop_frame = tk.Frame(paned_bot, relief = tk.SUNKEN, bd = 1, padx = 10, pady = 10)
paned_bot.add(crop_frame)

enhance_frame = tk.Frame(paned_bot, relief = tk.SUNKEN, bd = 1)
paned_bot.add(enhance_frame)
# resize_frame = tk.Frame(paned_bot, relief = tk.RAISED, bd = 1)
# paned_bot.add(resize_frame)

# rotate_frame = tk.Frame(paned_bot, relief = tk.RAISED, bd = 1)
# paned_bot.add(rotate_frame)

show_canv = tk.Canvas(panel, bg='black', height=wid, width=lenth)
# opt_canv=tk.Canvas(panel1, bg='white', height=wid, width = lenth/3)

pane_wind = tk.PanedWindow(panel1, relief = tk.SUNKEN, bd = 3, orient = tk.VERTICAL,  height=window.winfo_screenheight()- 95, width=int(lenth/3)+40)
pane_wind.pack(fill = tk.BOTH, expand = 1)
# opt_canv.create_window((0, 0), anchor = tk.CENTER, window = pane_wind)

# tree_pane = tk.Frame(pane_wind, relief = tk.RAISED)
# pane_wind.add(tree_pane)

tree_frame = tk.Frame(pane_wind, relief = tk.RAISED)
pane_wind.add(tree_frame, minsize = 250)

tree_view_fr = tk.Frame(tree_frame)
tree_view_fr.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
tree_scroll = ttk.Scrollbar(tree_view_fr)
tree_scroll.pack(side = tk.RIGHT, fill =tk.Y)

tree_view  = ttk.Treeview(tree_view_fr, yscrollcommand=tree_scroll.set, selectmode= tk.BROWSE)
tree_view.column("#0")
tree_view.heading('#0', text='Images', anchor='w')
tree_view.pack(fill = tk.BOTH, expand = 1, side = tk.TOP)
tree_scroll.config(command=tree_view.yview)

def del_sel():##kata part remaining
    if (img==None):
        show_error(2, "no image")
    global curr_img, kata
    sel = tree_view.selection()
    if sel==None:
        show_error(2, "Nothing Selected")
        return
    if (tree_view.parent(sel[0])!=""):
        return
    tr = tree_view.index(sel[0])
    
    if (curr_img==0):
        show_error(2, "This is original image")
        return
    elif (curr_img==tr):
        curr_img = tr-1
        show_img(img_list[curr_img], panel, True)
        
    elif (tr<curr_img):
        curr_img = curr_img-1
    img_list.pop(tr)
    tree_view.delete(*sel)        

b_undo = ttk.Button(tree_frame, text = "Delete Selected", command = del_sel)
b_undo.pack(side = tk.BOTTOM, fill = tk.BOTH)

def dc_viewer(e):
    global curr_img
    sel = tree_view.selection()
    if sel==None:
        return
    if (tree_view.parent(sel[0])!=""):
        return
    tr = tree_view.index(sel[0])
    curr_img = tr
    print(type(tr), tr)
    show_img(img_list[tr], panel, True)
    # tree_view.delete(sel[0])

tree_view.bind("<Double-1>", dc_viewer)
# opt_fr_can.create_window((0, 0), anchor = tk.NW, window = b_undo)

#for test purpose 
# tree_view.insert('', index='end', text='Administration',  iid=0, open=False)
# tree_view.insert('', index='end', text='Administration',  iid=1, open=False)
# tree_view.insert(0, index='end', text='Administration',  iid=2, open=False)
# tree_view.insert(0, index='end', text='Administration',  iid=3, open=False)
# tree_view.insert(1, index='end', text='Administration',  iid=4, open=False)
# tree_view.insert(1, index='end', text='Administration',  iid=5, open=False)

kata = 0
# for samp in range(20):
#     tree_view.insert('', index='end', text='Administration',  iid=kata, open=False)
#     kata = kata+1

# tree_scroll = ttk.Scrollbar(tree_frame)
# tree_scroll.pack(side = tk.RIGHT, fill =tk.Y)
# tree_scroll.config(command=tree_view.yview)

##for option frame (2nd in paned window)
opt_pane = tk.Frame(pane_wind)
    
pane_wind.add(opt_pane)

opt_fr_can = tk.Canvas(opt_pane)
opt_fr_can.pack(fill = tk.BOTH, expand = 1, side = tk.LEFT)

opt_fr_scroll = tk.Scrollbar(opt_pane, orient = tk.VERTICAL, command = opt_fr_can.yview)
opt_fr_scroll.pack(side = 'right', fill = tk.Y)


##canvas width
can_wid = opt_fr_can.cget('width')
print(can_wid)
opt_fr_can.config(yscrollcommand = opt_fr_scroll.set)
opt_fr_can.bind('<Configure>', lambda e: opt_fr_can.configure(scrollregion = opt_fr_can.bbox("all")))

opt_contfr = tk.Frame(opt_fr_can, width = can_wid)
opt_fr_can.create_window((1, 0), window = opt_contfr, anchor = tk.NW)
print(opt_contfr.cget('width'))
# opt_contfr.grid_propagate(0)

# opt_contfr.pack(fill = tk.BOTH)
# for i in range (50):

#     l1 = tk.Label(opt_contfr, text = "hellp atharva", font = ('calibre',15,'bold'))
#     # f1.create_window((400, 10), window = l1, anchor = tk.NW)
#     l1.pack(fill = tk.X)



pane = tk.Label(panel) 
# pane.pack()

def show_error(*val):
    if val[0] == 0:
        tk.messagebox.showerror(title="shadow", message="open image")
    elif val[0] == 1:
        tk.messagebox.showinfo(title="shadow", message="stego image saved at: " + val[1])
    elif val[0] == 2:
        tk.messagebox.showerror(title="shadow", message=val[1])
    elif val[0] == 3:
        msg = val[1][0]
        for i in range (1, len(val[1])):
            msg = msg + "\n" + val[1][i]
        tk.messagebox.showerror(title= "error", message= msg)

def openfilename(): 
    filename = filedialog.askopenfilename(title ='pen') 
    return filename

def text_open(msg_entry):
    filename = filedialog.askopenfilename(defaultextension=".txt")
    if filename != "":
        with open(filename, 'r') as text:
            msg_entry.delete('1.0', tk.END)
            msg_entry.insert(tk.INSERT, text.read())

def file_save():
    # global img_list
    global img
    if img == None:
        show_error(2, "First Open Image")
        return
    # l=len(img_list)
    # img = img_list[l-1]

    # img = Image.fromarray(img_list[l-1])
    files = [('png', '*.png'),
             ('jpg', '*.jpg')]
    file = filedialog.asksaveasfile(mode= "w", filetypes = files, defaultextension = files)
    print(file)
    if file:
        img.save(file.name)

def save_txt(text_area):
    # file = filedialog.asksaveasfile(mode= "w", filetypes = ('text file', '*.txt'), defaultextension = ('text file', '*.txt'))
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    # print("from save_txt:", mssg)
    if filename != "":
        with open(filename, "w") as file:
            # file.write("\n".join(textentry.get(0, "end")))
            file.write(text_area.get("1.0", tk.END))



#to delete the dir 
def del_dir_file(dir):
    # dir = 'D:/books\google_hash\d_f\cr_face'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

#to fit image in required box
def resz_img(imgt, x, y):
    l=int(imgt.size[0])
    w=int(imgt.size[1])
    
    if(l>w)and(x<l):
        # print("1\n", lenth, " l: ", l)
        w=int(((x-10)/l)*w)
        l= x-20
        
        # print(w, " ")
    elif(l<=w)and(w>y):
        # print("2\n", wid)
        l=int(((y-10)/w)*l)
        w=y-20
    
    return imgt.resize((l, w), Image.ANTIALIAS)

def show_img(imgt, panel, flag):
    global lenth, wid, pane, img 
    l=int(imgt.size[0])
    w=int(imgt.size[1])
    # crp_l.set(0)
    # crp_t.set(0)
    # crp_r.set(l)
    # crp_b.set(w) 
    # print("shape: ", l, w)
    if(l>w)and(lenth<l):
        # print("1\n", lenth, " l: ", l)
        w=int(((lenth-10)/l)*w)
        l=lenth-10
        if(w>wid):
            l = int(((wid-10)/w)*l)
            w=wid-10
        # print(w, " ")
    elif(l<=w)and(w>wid):
        # print("2\n", wid)
        l=int(((wid-10)/w)*l)
        w=wid-10
        if (l>lenth):
            w = int(((lenth-10)/l)*w)
            l=lenth-10
    
    if flag:
        img = imgt
        crp_l.set(0)
        crp_t.set(0)
        crp_r.set(img.size[0]) 
        crp_b.set(img.size[1])
        crop_left_text.configure(from_ = 0, to = img.size[0]) 
        crop_right_text.configure(from_ = 0, to = img.size[0])
        crop_top_text.configure(from_ = 0, to = img.size[1])
        crop_bottom_text.configure(from_ = 0, to = img.size[1])
        enh_col_slid.configure(state = tk.NORMAL) 
        enh_brit_slid.configure(state = tk.NORMAL) 
        enh_cntr_slid.configure(state = tk.NORMAL) 
        enh_shrp_slid.configure(state = tk.NORMAL) 
        enh_col_slid.set(1.0)
        enh_brit_slid.set(1.0)
        enh_cntr_slid.set(1.0)
        enh_shrp_slid.set(1.0)
        efct_var.set("No filter")

    imgt = imgt.resize((l, w), Image.ANTIALIAS) 
    print("shape: ", l, w)
    # PhotoImage class is used to add image to widgets, icons etc 
    imgt = ImageTk.PhotoImage(imgt) 
    pane.config(image='')
    pane = tk.Label(panel, image = imgt) 
      
    # set the image as img  
    pane.image = imgt 
    
    # pane.pack()
    # show_canv.create_image(lenth/2, wid/2, image = imgt)
    show_canv.create_window(lenth/2, wid/2,  window=pane)



def open_img(): 
    # Select the Imagename  from a folder  
    global panel, lenth, wid,  show_canv
    global pane, kata, curr_img

    x = openfilename() 
  
    # opens the image 
    # img=cv2.imread(x)
    img = Image.open(x)
    img = img.convert("RGB")
    if img==None:
        show_error(2, "Image Not selected")
        return
    curr_img = 0
    img_list.clear()
    tree_view.delete(*tree_view.get_children())
    f_name = os.path.basename(x)
    if type(f_name) == str:
        tree_view.insert('', index='end', text=f_name+' (Original)',  iid=0, open=False)
        tree_view.insert(
            0, index='end',
            text="Dimensions: " + str(img.size[0])+ "x"+ str(img.size[1]),  
            iid=1, open=False)
        kata = 2
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_list.append(img)
    # imgr=Image.fromarray(img) 
    
    show_img(img, panel, True)



def fl_rec_tree(add_rec_tv):
    with open("key_store.json", "r") as file:
        data = json.load(file)
    i = 0
    add_rec_tv.delete(*add_rec_tv.get_children())
    for d in data:
        add_rec_tv.insert('', index = 'end', text = d, iid = i, open = False)
        i = i+1
    # for i in range(30):
    #     add_rec_tv.insert('', index = 'end', text = "jinga", iid = i, open = False)
        
def cp_pasw(e, add_rec_tv):
    sel = add_rec_tv.selection()
    if sel == None:
        return
    tr = add_rec_tv.index(sel[0])
    with open("key_store.json", "r") as file:
        data = json.load(file)
    sel = add_rec_tv.item(sel)['text']
    d = data[sel]
    window.clipboard_clear()
    window.clipboard_append(d)
    window.update()
    return




def crp_vali(inp):
    if (inp.isdigit()) or (inp==""):
        return True
    else:
        return False

def resz_ok(top, l, w):
    if(l=="") or (w==""):
        show_error(2, "Empty Box")
        return
    l = int(l)
    w = int(w)
    global img
    temp = img
    img = img.resize((l, w), Image.ANTIALIAS)
    file_save()
    img = temp
    top.destroy()



def resize_handle():
    if img == None:
        show_error(2, "Open Image")
        return
    
    top = tk.Toplevel(window)
    top.title("resize")
    x = window.winfo_x()
    y = window.winfo_y()
    top.geometry("+%d+%d" % (x + 300, y + 100))
    top.grab_set()
    resize_frame = tk.Frame(top, relief = tk.SUNKEN)
    # resize_lab = ttk.Label(resize_frame, text = "Resize", relief = tk.RAISED)
    resize_hght_lab = ttk.Label(resize_frame, text = "Length")
    resize_hght_text = ttk.Entry(
        resize_frame, 
        validate='key',
        validatecommand = (crop_frame.register(lambda input: crp_vali(input)), '%P'))
    resize_wid_lab = ttk.Label(resize_frame, text = "Width")
    resize_wid_text = ttk.Entry(
        resize_frame, 
        validate='key',
        validatecommand = (crop_frame.register(lambda input: crp_vali(input)), '%P'))
    resize_ok = ttk.Button(
        resize_frame, text = "Save Copy", 
        command = lambda:resz_ok(top, resize_hght_text.get(), resize_wid_text.get()))

    ##placing resize part in top
    # resize_lab.grid(row = 0, column = 0, columnspan = 2, pady = 5)
    resize_hght_lab.grid(row = 1, column = 0)
    resize_hght_text.grid(row = 1, column = 1, padx = 10)
    resize_wid_lab.grid(row = 2, column = 0)
    resize_wid_text.grid(row = 2, column = 1, padx = 10)
    resize_ok.grid(row = 3, column = 0, columnspan = 2)

    resize_frame.pack(padx = 10, pady = 10)



            



def edit_ok():
    if (img==None):
        show_error(2, "No Image Selected!")
        efct_var.set("No filter")
        return
    elif ((efct_var.get()=="No filter")and(len(mask)==0)) :
        return
    global  kata, curr_img
    ed_img = img
    if (efct_var.get()=="Negative"):
        ed_img = ImageOps.invert(ed_img)
        tree_view.insert('', index='end', text="Effect: Negative",  iid=kata, open=False)
        kata = kata + 1
    elif(efct_var.get()=="Blur"):
        ed_img = ed_img.filter(ImageFilter.BoxBlur(int(ext0_var.get())))
        tree_view.insert('', index='end', text="Effect: Blur",  iid=kata, open=False)
        tree_view.insert(kata, index='end', text="Radius: " + str(ext0_var.get()),  iid=kata+1, open=False)
        kata = kata + 2
    elif(len(mask)>0):
        ed_img = mask[0]
        tree_view.insert('', index='end', text="RGB Manipulation",  iid=kata, open=False)
        kata=kata+1
        mask.clear()
        pane_opt_fr_can.delete("all")
    img_list.append(ed_img)
    curr_img = len(img_list)-1
    efct_var.set("No filter")
    pane_opt_fr_can.delete('all')
    show_img(ed_img, panel, True)

##here left
def ex_view(e, act):
    ed_img = img
    if(act==1):
        ed_img = ed_img.filter(ImageFilter.BoxBlur(int(ext0_var.get())))
    
    elif (act == "rgb_col"):
        if (len(mask)==0):
            return
        ed_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        b, g, r = cv2.split(ed_img)
        _, tr = cv2.threshold(
            r, int(ext2_var.get())-1, int(ext1_var.get()), cv2.THRESH_BINARY)
        tr = (tr//int(ext1_var.get()))*int(ext7_var.get())
        r = cv2.add(r, tr)
        print("rl: ", int(ext2_var.get())-1, " ru: ",int(ext1_var.get()), " val: ",int(ext7_var.get()))
        _, tg = cv2.threshold(
            g, int(ext4_var.get())-1, int(ext3_var.get()), cv2.THRESH_BINARY)
        tg = (tg//int(ext3_var.get()))*int(ext8_var.get())
        g = cv2.add(g, tg)
        print("gl: ", int(ext4_var.get())-1, " gu: ",int(ext3_var.get()), " val: ",int(ext8_var.get()))
        _, tb = cv2.threshold(
            b, int(ext6_var.get())-1, int(ext5_var.get()), cv2.THRESH_BINARY)
        tb = (tb//int(ext5_var.get()))*int(ext9_var.get())
        b = cv2.add(b, tb)
        print("bl: ", int(ext6_var.get())-1, " bu: ",int(ext5_var.get()), " val: ",int(ext9_var.get()))
        ed_img = cv2.merge((b, g, r))
        ed_img = Image.fromarray(cv2.cvtColor(ed_img, cv2.COLOR_BGR2RGB))
        mask[0]=ed_img
    elif (act == "rlb"):
        ed_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        tr = ed_img[:, :, 2]%2
        tr = tr*255
        ed_img = Image.fromarray(cv2.cvtColor(tr, cv2.COLOR_GRAY2RGB))
    elif (act == "glb"):
        ed_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        tr = ed_img[:, :, 1]%2
        tr = tr*255
        ed_img = Image.fromarray(cv2.cvtColor(tr, cv2.COLOR_GRAY2RGB))
    elif (act == "blb"):
        ed_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        tr = ed_img[:, :, 0]%2
        tr = tr*255
        ed_img = Image.fromarray(cv2.cvtColor(tr, cv2.COLOR_GRAY2RGB))
    show_img(ed_img, panel, False)
    

def rgb_from_to_set(act, widg):
    if len(mask) == 0:
        show_error(2, "No Image Selected!")
        return
    ru = int(ext1_var.get())
    rl = int(ext2_var.get())
    gu = int(ext3_var.get())
    gl = int(ext4_var.get())
    bu = int(ext5_var.get())
    bl = int(ext6_var.get())
    print("ru: ", ru, ", rl: ", rl, ", gu: ", gu,", gl: ", gl,", bu: ", bu,", bl: ", bl)
    if (act=="ru"):
        widg.configure(from_ = 0, to = ru-5, increment = step_var.get())
    elif(act == "rl"):
        widg.configure(from_ = rl+5, to = 255, increment = step_var.get())
    elif(act == "gu"):
        widg.configure(from_ = 0, to = gu-5, increment = step_var.get())
    elif(act == "gl"):
        widg.configure(from_ = gl+5, to = 255, increment = step_var.get())
    elif(act == "bu"):
        widg.configure(from_ = 0, to = bu-5, increment = step_var.get())
    elif(act == "bl"):
        widg.configure(from_ = bl+5, to = 255, increment = step_var.get())

    

#function for edito=ing currently no use
def edit_img(val):
    if (img==None):
        efct_var.set("No filter")
        show_error(2, "No Image Selected!")
        return
    elif (val=="No filter") :
        pane_opt_fr_can.delete('all')
        show_img(img, panel, True)
        return
    mask.clear()
    ed_img = img
    pane_opt_fr_can.delete('all')
    simple_fr = tk.Frame(pane_opt_fr_can, width = pane_opt_fr_can.winfo_width())
    if (val=="Negative"):
        try:
            ed_img = ImageOps.invert(ed_img)
        except:
            print(ed_img.mode)
    elif(val == 'Blur'):
        ext0_var.set(0)
        bx_blur_slid = tk.Scale(
            simple_fr,
            from_ = 0,
            to = 5,
            variable = ext0_var,
            orient=tk.HORIZONTAL,
            command = lambda e:ex_view(e, 1))
        bx_blur_slid.pack(fill = tk.BOTH, expand = 1)
        # pane_opt_fr_can.create_window((pane_opt_fr_can.cget('width')/2, 30), window = bx_blur_slid)
        # ed_img = ed_img.filter(ImageFilter.BoxBlur(2))
    
    elif (val == "rgb_col"):
        ext1_var.set(255)
        print(ext1_var.get())
        ext2_var.set(0)
        ext3_var.set(255)
        ext4_var.set(0)
        ext5_var.set(255)
        ext6_var.set(0)
        ext7_var.set(0)
        ext8_var.set(0)
        ext9_var.set(0)
        mask.append(img)
        r_lab = tk.Label(simple_fr, text = "Red")
        r_u_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext1_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        r_lab_to = tk.Label(simple_fr, text = "to")
        r_l_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext2_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        g_lab = tk.Label(simple_fr, text = "Green")
        g_u_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext3_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        g_lab_to = tk.Label(simple_fr, text = "to")
        g_l_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext4_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        b_lab = tk.Label(simple_fr, text = "Blue")
        b_u_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext5_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        b_lab_to = tk.Label(simple_fr, text = "to")
        b_l_text = ttk.Spinbox(
            simple_fr, 
            from_ = 0, to = 255,
            textvariable = ext6_var,
            increment = step_var.get(),    
            state = 'readonly'
        )
        # rgb_ok = tk.Button(simple_fr, text = "Ok", command = None)
        r_u_text.configure(command=lambda : rgb_from_to_set("ru", r_l_text))
        r_l_text.configure(command=lambda : rgb_from_to_set("rl", r_u_text))
        g_u_text.configure(command=lambda : rgb_from_to_set("gu", g_l_text))
        g_l_text.configure(command=lambda : rgb_from_to_set("gl", g_u_text))
        b_u_text.configure(command=lambda : rgb_from_to_set("bu", b_l_text))
        b_l_text.configure(command=lambda : rgb_from_to_set("bl", b_u_text))
        
        red_enh = tk.Scale(
            simple_fr,
            from_ = 0,
            to = 255,
            variable = ext7_var,
            orient=tk.HORIZONTAL,
            command = lambda e:ex_view(e, "rgb_col"))

        green_enh = tk.Scale(
            simple_fr,
            from_ = 0,
            to = 255,
            variable = ext8_var,
            orient=tk.HORIZONTAL,
            command = lambda e:ex_view(e, "rgb_col"))

        blue_enh = tk.Scale(
            simple_fr,
            from_ = 0,
            to = 255,
            variable = ext9_var,
            orient=tk.HORIZONTAL,
            command = lambda e:ex_view(e, "rgb_col"))
        
        r_lab.grid(row = 0, column = 0)
        r_u_text.grid(row = 0, column = 3)
        r_lab_to.grid(row = 0, column=2)
        r_l_text.grid(row = 0, column=1)
        red_enh.grid(row = 1, column=0, columnspan=4)
        ttk.Separator(simple_fr, orient=tk.HORIZONTAL).grid(row = 2, column=0, columnspan=4, pady = 5)
        g_lab.grid(row = 3, column=0)
        g_u_text.grid(row = 3, column=3)
        g_lab_to.grid(row = 3, column=2)
        g_l_text.grid(row = 3, column=1)
        green_enh.grid(row = 4, column=0, columnspan=4)
        ttk.Separator(simple_fr, orient=tk.HORIZONTAL).grid(row = 5, column=0, columnspan=4, pady = 5)
        b_lab.grid(row = 6, column=0)
        b_u_text.grid(row = 6, column=3)
        b_lab_to.grid(row = 6, column=2)
        b_l_text.grid(row = 6, column=1)
        blue_enh.grid(row = 7, column=0, columnspan=4)
        
        
    elif (val == "bit_plane"):
        red_last = tk.Button(simple_fr, text = "Red Last Bit", command = lambda:ex_view(1, "rlb"))
        green_last = tk.Button(simple_fr, text = "Green Last Bit", command = lambda:ex_view(1, "glb"))
        blue_last = tk.Button(simple_fr, text = "Blue Last Bit", command = lambda:ex_view(1, "blb"))
        red_last.grid(row = 0, column = 0)
        green_last.grid(row = 0, column = 1)
        blue_last.grid(row = 0, column = 2)
        
    pane_opt_fr_can.create_window(
        (0, 0), anchor=tk.NW, 
        width=  pane_opt_fr_can.winfo_width(),
        window = simple_fr
        )
    show_img(ed_img, panel, False)
    
    
def crp_ok():
    global kata, curr_img
    if img == None:
        show_error(2, "No Image Selected!")
        return
    l = int(crp_l.get())
    t = int(crp_t.get())
    r = int(crp_r.get())
    b = int(crp_b.get())
    imgc = img.crop((l, t, r, b))
    img_list.append(imgc)
    curr_img = len(img_list)-1
    tree_view.insert('', index='end', text="croped Image",  iid=kata, open=False)
    tree_view.insert(
        kata, index='end', 
        text="Dimensions: " + str(imgc.size[0])+ "x"+ str(imgc.size[1]),  
        iid=kata+1, open=False)
    kata = kata + 2
    show_img(imgc, panel, True)
    


def crp_from_to_set(flag):
    if img == None:
        show_error(2, "No Image Selected!")
        return
    l = int(crp_l.get())
    t = int(crp_t.get())
    r = int(crp_r.get())
    b = int(crp_b.get())
    # if (flag):
    #     widget.configure(from_ = e+1)
    # else:
    #     widget.configure(to = e-1)
    if (flag==1):
        crop_left_text.configure(from_ = 0, to = r-50)
        # widget.configure(from_ = e+1)
    elif flag == 2:
        crop_right_text.configure(from_ = l+50, to = img.size[0])
    elif flag == 3:
        crop_top_text.configure(from_ = 0, to = b - 50)
    else:
        crop_bottom_text.configure(from_ = t+50, to = img.size[1])
    # if x_y:
    #     show_img(img.crop())
    
    print("crp_rect: ", l, t, r, b)
    show_img(img.crop((l, t, r, b)), panel, False)
    # show_img()

opt = [1, 10, 45, 90]
step_var = tk.IntVar()
##for test purpose
# crp_l.set('0')
# crp_r.set('500')
# crp_t.set(0)
# crp_b.set(500)
step_var.set(1)

# vali_reg = crop_frame.register(lambda input: crp_vali(input, crp))

##buttons for panel_bot
crop_lab = ttk.Label(crop_frame, text = "Crop", relief = tk.RAISED)
crop_by_lab = ttk.Label(crop_frame, text = " crop step")
# crop_by = ttk.Entry(crop_frame, font = ('calibre',9,'bold'), width = 10)



crop_left_lab = ttk.Label(crop_frame, text = "left margin")
# crop_left_inc = ttk.Button(crop_frame, text = "+", command = None)
crop_left_text = ttk.Spinbox(
    crop_frame, font = ('calibre',9,'bold'), 
    command = lambda : crp_from_to_set(1),
    textvariable = crp_l,
    # from_ = crp_l.get(),
    # to = crp_r.get(),
    increment = step_var.get(),
    # validatecommand = (crop_frame.register(lambda input: crp_vali(input, crp_l.get(), crp_r.get())), '%P'),
    state = 'readonly'
)
# crop_left_dec = ttk.Button(crop_frame, text = "-", command = None)

crop_right_lab = ttk.Label(crop_frame, text = "right margin")
# crop_right_inc = ttk.Button(crop_frame, text = "+", command = None)
crop_right_text = ttk.Spinbox(
    crop_frame, font = ('calibre',9,'bold'),
    # from_ = crp_l.get(),
    # to = crp_r.get(),
    command = lambda : crp_from_to_set(2),
    textvariable = crp_r,
    increment = step_var.get(),    
    # validatecommand = (crop_frame.register(lambda input: crp_vali(input, crp_l.get(), crp_r.get())), '%P'),
    state = 'readonly'
)
# crop_right_dec = ttk.Button(crop_frame, text = "-", command = None)

crop_top_lab = ttk.Label(crop_frame, text = "top margin")
# crop_top_inc = ttk.Button(crop_frame, text = "+", command = None)
crop_top_text = ttk.Spinbox(
    crop_frame, font = ('calibre',9,'bold'),
    # from_ = crp_t.get(),
    # to = crp_b.get(),
    command = lambda : crp_from_to_set(3),
    textvariable = crp_t,
    increment = step_var.get(),
    # validatecommand = (crop_frame.register(lambda input: crp_vali(input, crp_t.get(), crp_b.get())), '%P'),
    state = 'readonly'
)
# crop_top_dec = ttk.Button(crop_frame, text = "-", command = None)

crop_bottom_lab = ttk.Label(crop_frame, text = "bottom margin")
# crop_bottom_inc = ttk.Button(crop_frame, text = "+", command = None)
crop_bottom_text = ttk.Spinbox(
    crop_frame, font = ('calibre',9,'bold'),
    # from_ = crp_t.get(),
    # to = crp_b.get(),
    command = lambda : crp_from_to_set(4),
    textvariable = crp_b,
    increment = step_var.get(),
    # validatecommand = (crop_frame.register(lambda input: crp_vali(input, crp_t.get(), crp_b.get())), '%P'), 
    state = 'readonly'
)
# crop_bottom_dec = ttk.Button(crop_frame, text = "-", command = None)

# crop_left_text.configure(command = lambda : crp_from_to_set(1))
# crop_right_text.configure(command = lambda : crp_from_to_set(2))
# crop_top_text.configure(command = lambda : crp_from_to_set(3))
# crop_bottom_text.configure(command = lambda : crp_from_to_set(4))


def crp_inc_set(e):
    crop_left_text.configure(increment = e)
    crop_right_text.configure(increment = e)
    crop_top_text.configure(increment = e)
    crop_bottom_text.configure(increment = e)
    


crop_by = ttk.OptionMenu(
    crop_frame,
    step_var,
    *opt,
    command = crp_inc_set 
) 


crop_ok = ttk.Button(crop_frame, text = "OK", command = crp_ok)

##placing crop part in panel_bot
crop_lab.grid(row = 0, column = 0, padx = 3)
crop_by_lab.grid(row = 1, column = 0, sticky = tk.S)
crop_by.grid(row = 2, column = 0, rowspan = 2, padx = 10)

crop_left_lab.grid(row = 0, column = 1, padx = 4)
# crop_left_inc.grid(row = 0, column = 2)
crop_left_text.grid(row = 0, column = 3, padx = 4)
# crop_left_dec.grid(row = 0, column = 4)

crop_right_lab.grid(row = 1, column = 1, padx = 4)
# crop_right_inc.grid(row = 1, column = 2)
crop_right_text.grid(row = 1, column = 3, padx = 4)
# crop_right_dec.grid(row = 1, column = 4)

crop_top_lab.grid(row = 2, column = 1, padx = 4)
# crop_top_inc.grid(row = 2, column = 2)
crop_top_text.grid(row = 2, column = 3, padx = 4)
# crop_top_dec.grid(row = 2, column = 4)

crop_bottom_lab.grid(row = 3, column = 1, padx = 4)
# crop_bottom_inc.grid(row = 3, column = 2)
crop_bottom_text.grid(row = 3, column = 3, padx = 4)
# crop_bottom_dec.grid(row = 3, column = 4)

crop_ok.grid(row = 0, column = 5, rowspan = 4, padx = 5)

# crop_lab.grid(row= 0, column = 0)
# crop_by.grid(row = 1, column = 0)

def enh_com(e, flag):
    if img == None:
        enh_col_slid.set(0.0)
        enh_brit_slid.set(0.0)
        enh_cntr_slid.set(0.0)
        enh_shrp_slid.set(0.0)
        show_error(2, "No Image Selected!")
        return
    global kata, curr_img
    en_img = img
    c = enh_col_slid.get()
    b = enh_brit_slid.get()
    ct = enh_cntr_slid.get()
    s = enh_shrp_slid.get()
    
    if (c!=1.0):
        en_img = ImageEnhance.Color(en_img).enhance(c)
    if (b!=1.0):
        en_img = ImageEnhance.Brightness(en_img).enhance(b)
    if (ct!=1.0):
        en_img = ImageEnhance.Contrast(en_img).enhance(ct)
    if (s!=1.0):
        en_img = ImageEnhance.Sharpness(en_img).enhance(s)
    
    if (flag):
        img_list.append(en_img)
        curr_img = len(img_list) - 1
        tree_view.insert('', index='end', text="Enhanced Image",  iid=kata, open=False)
        tree_view.insert(kata, index = 'end',text = "color: "+str(c),iid = kata+1, open = False)
        tree_view.insert(kata, index = 'end',text = "Brightness: "+str(b),iid = kata+2, open = False)
        tree_view.insert(kata, index = 'end',text = "Contrast: "+str(ct),iid = kata+3, open = False)
        tree_view.insert(kata, index = 'end',text = "Sharpness: "+str(s),iid = kata+4, open = False)
            
        kata = kata+5
        enh_col_slid.set(1.0)
        enh_brit_slid.set(1.0)
        enh_cntr_slid.set(1.0)
        enh_shrp_slid.set(1.0)
        show_img(en_img, panel, True)
    else :
        show_img(en_img, panel, False)


##enhance_frame stuff
enh_col_lab = tk.Label(enhance_frame, text = "Color: ")
enh_brit_lab = tk.Label(enhance_frame, text = "Brightness: ")
enh_cntr_lab = tk.Label(enhance_frame, text = "Contrast: ")
enh_shrp_lab = tk.Label(enhance_frame, text = "Sharpness: ")
enh_col_slid  = tk.Scale(
    enhance_frame, orient = tk.HORIZONTAL,
    from_ = 0.0,
    to = 2.0,
    resolution= 0.2,
    # width=10,
    state = tk.DISABLED,
    length=200,
    command=lambda e:enh_com(e, False) 
)

enh_brit_slid  = tk.Scale(
    enhance_frame, orient = tk.HORIZONTAL,
    from_ = 0.0,
    to = 2.0,
    resolution= 0.2,
    # width=10,
    state = tk.DISABLED,
    length=200,
    command=lambda e:enh_com(e, False)
)

enh_cntr_slid  = tk.Scale(
    enhance_frame, orient = tk.HORIZONTAL,
    from_ = 0.0,
    to = 2.0,
    resolution= 0.2,
    # width=10,
    state = tk.DISABLED,
    length=200,
    command=lambda e:enh_com(e, False)
)

enh_shrp_slid  = tk.Scale(
    enhance_frame, orient = tk.HORIZONTAL,
    from_ = 0.0,
    to = 2.0,
    resolution= 0.2,
    # width=10,
    state = tk.DISABLED,
    length=200,
    command=lambda e:enh_com(e, False)
)

enh_ok = ttk.Button(enhance_frame, text = "Ok", command = lambda :enh_com(1, True) )

##grid the enhance_frame
enh_col_lab.grid(row = 0, column = 0, padx = 3, pady = 4)
enh_brit_lab.grid(row = 1, column = 0, padx = 3, pady = 4)
enh_cntr_lab.grid(row = 0, column = 2, padx = 3, pady = 4)
enh_shrp_lab.grid(row = 1, column = 2, padx = 3, pady = 4)
enh_col_slid.grid(row = 0, column = 1, padx = 3, pady = 4)
enh_brit_slid.grid(row = 1, column = 1, padx = 3, pady = 4)
enh_cntr_slid.grid(row = 0, column = 3, padx = 3, pady = 4)
enh_shrp_slid.grid(row = 1, column = 3, padx = 3, pady = 4)
enh_ok.grid(row = 0, column = 4, rowspan=2, padx = 5, pady = 4)

def com_rotate():
    if img == None:
        show_error(2, "No Image Selected!")
        return
    # imgr = img_list[curr_img]
    img_list[curr_img] = img_list[curr_img].transpose(Image.ROTATE_90)
    show_img(img_list[curr_img], panel, True)

def com_flip():
    if img == None:
        show_error(2, "No Image Selected!")
        return
    img_list[curr_img] = img_list[curr_img].transpose(Image.FLIP_LEFT_RIGHT)
    show_img(img_list[curr_img], panel, True)

b_rotate = tk.Button(opt_contfr, text = "Rotate", command= com_rotate, height = 4, width = 25)
b_flip = tk.Button(opt_contfr, text = "Filp", command = com_flip, width = 25, height = 4)

b_rotate.grid(row = 0, column = 0, columnspan=2, sticky = tk.E+tk.W, padx=2)
b_flip.grid(row = 0, column = 2, columnspan=2, sticky = tk.E+tk.W, padx = 2)
# b_rotate.pack(padx=2, fill = tk.X, side = tk.LEFT)
# b_flip.pack(padx = 2, fil = tk.X, side = tk.RIGHT)





opt_efct = ["No filter", "Negative", "Blur"]
effect_lab = tk.Label(opt_contfr, text = "Effect: ")
effect_opt = ttk.OptionMenu(
    opt_contfr,
    efct_var,
    *opt_efct,
    command = edit_img
) 
b_effect_ok = ttk.Button(opt_contfr, text = "Ok", command = edit_ok)

effect_lab.grid(row = 1, column = 0, padx = 5, pady = 5)
effect_opt.grid(row = 1, column = 1, columnspan= 2, pady = 5, sticky = tk.E+tk.W)
b_effect_ok.grid(row = 1, column = 3, sticky = tk.E+tk.W)
# effect_lab.pack(padx = 5, pady = 5, side = tk.LEFT)
# effect_opt.pack(padx = 5, pady = 5, side = tk.RIGHT, fill = tk.X)
ttk.Separator(opt_contfr, orient=tk.HORIZONTAL).grid(row = 2, column = 0, columnspan = 4, sticky = tk.E+tk.W)

paned_opt_fr = tk.Frame(opt_contfr)
paned_opt_fr.grid(row = 3, column = 0, columnspan = 4, sticky = tk.E+tk.W)
pane_opt_fr_can = tk.Canvas(paned_opt_fr)
pane_opt_fr_can.pack(fill = tk.BOTH, expand = 1)

#menubar start/***
menubar = tk.Menu(window)

filemenu= tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_img)  
filemenu.add_command(label="save", command=file_save)
filemenu.add_separator()
filemenu.add_command(label="Resize Image", command=resize_handle)

# filemenu.add_command(label="Quit!", command=window.quit)  

menubar.add_cascade(label="File", menu=filemenu)

editmenu= tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Color Manipulator", command=lambda: edit_img("rgb_col"))  
editmenu.add_command(label="Bitplane Viewer", command=lambda: edit_img("bit_plane"))
editmenu.add_separator()
editmenu.add_command(label="test!", command=None)  

menubar.add_cascade(label="Tools", menu=editmenu)



window.config(menu=menubar)  
#***/menubar end/***




#button  for gray image
# b1=tk.Button(panel1, text="color gray", command=edit_img)
# opt_canv.create_window(40, 20, window=b1)



show_canv.pack()
# opt_canv.pack()




window.mainloop()
