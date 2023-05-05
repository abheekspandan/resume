import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry 
import sqlite3
import customtkinter


# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)
# Connecting to the Database where all information will be stored
connector = sqlite3.connect('studentManagement.db')
cursor = connector.cursor()
connector.execute(
    "CREATE TABLE IF NOT EXISTS STUDENT_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,ID TEXT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)
# Creating the functions


def reset_fields():
    global id_strvar,name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    for i in ['id_strvar','name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


def reset_form():
    global tree
    tree.delete(*tree.get_children())
    reset_fields()


def display_records():
    global bt1
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM STUDENT_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)
    bt1.configure(state="disabled")


def add_record():
    global id_strvar,name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    id=id_strvar.get()
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute(
                'INSERT INTO STUDENT_MANAGEMENT (ID,NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?,?)', (id,
                    name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Record added',
                        f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror(
                'Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        connector.execute(
            'DELETE FROM STUDENT_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo(
            'Done', 'The record you wanted deleted was successfully deleted.')
        display_records()


def view_record():
    global id_strvar,name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    if not tree.selection():
        mb.showerror('Error!', 'Please select a record to view')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        id_strvar.set(selection[1])
        name_strvar.set(selection[2])
        email_strvar.set(selection[3])
        contact_strvar.set(selection[4])
        gender_strvar.set(selection[5])
        date = datetime.date(int(selection[6][:4]), int(
            selection[6][5:7]), int(selection[6][8:]))
        dob.set_date(date)
        stream_strvar.set(selection[7])

def update_record():
    global id_strvar,name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    id=id_strvar.get()
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    elif (len((connector.execute('SELECT * FROM STUDENT_MANAGEMENT WHERE ID=(?)',(id,))).fetchall())==0):
        add_record()
    else:
        try:
            connector.execute(
                'UPDATE STUDENT_MANAGEMENT SET NAME=(?),EMAIL=(?),PHONE_NO=(?),GENDER=(?),DOB=(?),STREAM=(?) WHERE ID=(?)', (
                    name, email, contact, gender, DOB, stream,id)
            )
            connector.commit()
            mb.showinfo('Record added',
                        f"Record of {name} was successfully updated")
            reset_fields()
            display_records()
        except:
            mb.showerror(
                'Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

def search_record():
    global search_strvar,bt1
    search=search_strvar.get()
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM STUDENT_MANAGEMENT WHERE ID=(?)',(search,))
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)
    if(bt1.cget('state')=="disabled"):
        bt1.configure(state="enabled")
    


# Initializing the GUI window
main = customtkinter.CTk()
main.title('STUDENT Management System',)
main.geometry('1200x700')
main.resizable(0, 0)
# Creating the background and foreground color variables
lf_bg = 'gray14'  # bg color for the left_frame
cf_bg = 'gray14'  # bg color for the center_frame
# Creating the StringVar or IntVar variables
search_strvar=StringVar()
id_strvar=StringVar()
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()
# Placing the components in the main window
style=ttk.Style()
style.theme_use("default")
style.configure('Treeview.Heading', background="grey18",foreground="white",rowheight=60)
style.configure("Treeview",background="grey30",rowheight=30,foreground="white",fieldbackground="gray30")
style.map("Treeview",backgroud=[('selected','yellow')])
Label(main, text="STUDENT MANAGEMENT SYSTEM", font=headlabelfont,
      bg='gray20',fg="white").pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)
# Placing components in the left frame
customtkinter.CTkLabel(left_frame, text="ID Number", font=labelfont,
      bg_color=lf_bg).place(relx=0.275, rely=0.0001)
customtkinter.CTkLabel(left_frame, text="Name", font=labelfont,
      bg_color=lf_bg).place(relx=0.375, rely=0.1)
customtkinter.CTkLabel(left_frame, text="Contact Number", font=labelfont,
      bg_color=lf_bg).place(relx=0.175, rely=0.19)
customtkinter.CTkLabel(left_frame, text="Email Address", font=labelfont,
      bg_color=lf_bg).place(relx=0.2, rely=0.31)
customtkinter.CTkLabel(left_frame, text="Gender", font=labelfont,
      bg_color=lf_bg).place(relx=0.3, rely=0.44)
customtkinter.CTkLabel(left_frame, text="Date of Birth (DOB)",
      font=labelfont, bg_color=lf_bg).place(relx=0.1, rely=0.57)
customtkinter.CTkLabel(left_frame, text="Stream", font=labelfont,
      bg_color=lf_bg).place(relx=0.3, rely=0.7)
customtkinter.CTkEntry(left_frame, width=180, textvariable=id_strvar,
      font=entryfont,fg_color="grey30").place(x=20, rely=0.05)
customtkinter.CTkEntry(left_frame, width=180, textvariable=name_strvar,
      font=entryfont,fg_color="grey30").place(x=20, rely=0.15)
customtkinter.CTkEntry(left_frame, width=180, textvariable=contact_strvar,
      font=entryfont,fg_color="grey30").place(x=20, rely=0.23)
customtkinter.CTkEntry(left_frame, width=180, textvariable=email_strvar,
      font=entryfont,fg_color="grey30").place(x=20, rely=0.36)
customtkinter.CTkEntry(left_frame, width=180, textvariable=stream_strvar,
      font=entryfont,fg_color="grey30").place(x=20, rely=0.75)
customtkinter.CTkOptionMenu(left_frame,fg_color="grey30", values=['Male', "Female"],variable=gender_strvar).place(
    x=45, rely=0.49, relwidth=0.5)
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)
customtkinter.CTkButton(left_frame, text='Submit and Update Record', font=labelfont,
       command=update_record, width=200,height=40,hover_color="grey25",fg_color='#005EFF').place(relx=0.1, rely=0.85)
# Placing components in the center frame
customtkinter.CTkButton(center_frame, text='Delete Record', font=labelfont,
       command=remove_record, width=180,height=40,hover_color="grey40",fg_color='#005EFF').place(relx=0.1, rely=0.55)
customtkinter.CTkButton(center_frame, text='View Record', font=labelfont,
       command=view_record, width=180,height=40,hover_color="grey40",fg_color='#005EFF').place(relx=0.1, rely=0.65)
customtkinter.CTkButton(center_frame, text='Reset Fields', font=labelfont,
       command=reset_fields, width=180,height=40,hover_color="grey40",fg_color='#005EFF').place(relx=0.1, rely=0.75)
customtkinter.CTkButton(center_frame, text='Delete database', font=labelfont,
       command=reset_form, width=180,height=40,hover_color="grey40",fg_color='#005EFF').place(relx=0.1, rely=0.85)
# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont,
      bg='gray10', fg='white').pack(side=TOP, fill=X)
customtkinter.CTkEntry(right_frame, width=180, textvariable=search_strvar,
      font=entryfont,fg_color="grey10").place(x=100, rely=0.05)
customtkinter.CTkButton(right_frame, text='Search Record', font=labelfont,
       command=search_record, width=180,height=30,hover_color="grey30",fg_color='#005EFF').place(x=380, rely=0.05)
bt1=customtkinter.CTkButton(right_frame, text='Display ALL', font=labelfont,
        command=display_records, width=2,height=30,hover_color="grey30",fg_color='#005EFF' , state=DISABLED)
bt1.place(x=580, rely=0.05)
# Placing components in the right frame
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('S.no','ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))
X_scroller = customtkinter.CTkScrollbar(tree, orientation=HORIZONTAL, command=tree.xview)
Y_scroller = customtkinter.CTkScrollbar(tree, orientation=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('S.no', text='S.no', anchor=CENTER)
tree.heading('ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.column('#8', width=150, stretch=NO)
tree.place(y=70, relwidth=1, relheight=0.9, relx=0)
display_records()
# Finalizing the GUI window
main.update()
main.mainloop()
