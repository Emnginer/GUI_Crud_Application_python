from tkinter import *
import sqlite3

app = Tk()
app.title("Main Interface")
app.geometry('400x400')
app.configure(background="#dcdde1")
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def recordShow():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    global show
    show = Tk()
    show.title("Show record and editing section")
    show.geometry('600x600')
    show.configure(background="#dcdde1")
    cursor.execute("SELECT * FROM studentForm")
    records = cursor.fetchall()
    row_record = ""
    for row in records:
        row_record += f"ID- {str(row[0])}: {str(row[1])}   {str(row[2])}   {str(row[3])} \n"
    print("Record successfully printed!!!")
    lbl_showRecord = Label(show, text=row_record, font=("arial", 16), bg="#0097e6", fg="white")
    lbl_showRecord.grid(row=15, column=2, columnspan=2, ipadx=60, pady=20)

    btn_addRecord = Button(show, text="Add New Student", width=12, command=addRecord, bg="#0097e6", fg="white",
                           font=("arial bold", 10))
    btn_addRecord.grid(row=16, column=1, columnspan=3, ipadx=50, pady=8)

    def cancel_showRecord():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        show.destroy()
        print("Window exit")

    btn_cancel_showRecord = Button(show, text="Exit Window", command=cancel_showRecord, bg="#718093", fg="white",
                                   font=("arial bold", 10))
    btn_cancel_showRecord.grid(row=30, column=2, pady=40, columnspan=2)

    def dlrecord():
        lbl_deleteRecord = Label(show, text="Enter ID for delele the record")
        lbl_deleteRecord.grid(row=18, column=1, columnspan=3)

        box_deleteRecord = Entry(show, width=23, font=("Arial", 12))
        box_deleteRecord.grid(row=19, column=2, pady=5, columnspan=2)

        def confirmDelete():
            cursor.execute("DELETE FROM studentForm WHERE ID =" + box_deleteRecord.get())
            conn.commit()
            print("record delete successfully")
            conn.close()
            show.destroy()

        btn_confirmtoDelete = Button(show, text="Confirm to delete", command=confirmDelete, bg="white", fg="black",
                                     font=("arial bold", 8))
        btn_confirmtoDelete.grid(row=20, column=2, columnspan=2)

        # def lbl_deleteRecord():
        #     conn = sqlite3.connect("database.db")
        #     cursor = conn.cursor()
        #
        #
        # btn_cancel_for_confirm_Delete = Button(show, text="cancel",command=lbl_deleteRecord)
        # btn_cancel_for_confirm_Delete.grid(row=20, column=3)

        # def cancelDelete():
        #     conn = sqlite3.connect("database.db")
        #     cursor = conn.cursor()
        #     btn_confirmtoDelete.destroy()
        #
        # btn_cancelDelete = Button(show, text="cancel", command=cancelDelete)
        # btn_cancelDelete.grid(row=20, column=3)

    def editRecord():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        lbl_editRecord = Label(show, text="Enter ID for Edit the record")
        lbl_editRecord.grid(row=25, column=1, columnspan=3)

        box_editRecord = Entry(show, width=23, font=("Arial", 12))
        box_editRecord.grid(row=26, column=2, pady=5, columnspan=2)

        def confirmToEdit():
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            global confirm_edit
            confirm_edit = Tk()
            confirm_edit.title("confirm edit")
            confirm_edit.geometry('400x400')
            confirm_edit.configure(background="#dcdde1")
            record_id = box_editRecord.get()
            cursor.execute("SELECT * FROM studentForm WHERE ID =" + record_id)
            records = cursor.fetchall()
            global box_Name_Edit
            global box_Email_Edit
            global box_Address_Edit

            lbl_Name_Edit = Label(confirm_edit, text="Name: ", font=("Arial", 14), bg="#dcdde1")
            lbl_Name_Edit.grid(row=5, column=1, columnspan=2)
            box_Name_Edit = Entry(confirm_edit, width=25, font=("Arial", 12))
            box_Name_Edit.grid(row=6, column=2, padx=80, pady=5, columnspan=2)

            lbl_Email_Edit = Label(confirm_edit, text="Email: ", font=("Arial", 14), bg="#dcdde1")
            lbl_Email_Edit.grid(row=7, column=1, columnspan=2)
            box_Email_Edit = Entry(confirm_edit, width=25, font=("Arial", 12))
            box_Email_Edit.grid(row=8, column=1, padx=80, pady=5, columnspan=2)

            lbl_Address_Edit = Label(confirm_edit, text="Address: ", font=("Arial", 14), bg="#dcdde1")
            lbl_Address_Edit.grid(row=9, column=1, columnspan=2)
            box_Address_Edit = Entry(confirm_edit, width=25, font=("Arial", 12))
            box_Address_Edit.grid(row=10, column=1, padx=80, pady=5, columnspan=2)

            btn_confirmToUpdate = Button(confirm_edit, text="Confirm To Update", command=updateRecord, bg="white",
                                         fg="black", font=("arial bold", 8))
            btn_confirmToUpdate.grid(row=12, column=1, padx=100, pady=20, columnspan=2)

            for record in records:
                box_Name_Edit.insert(0, record[1])
                box_Email_Edit.insert(0, record[2])
                box_Address_Edit.insert(0, record[3])

        def updateRecord():
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            global confirm_edit
            record_id = box_editRecord.get()
            cursor.execute("""
                UPDATE studentForm SET
                Name = :stuName, 
                Email= :stuEmail,
                Address= :stuAddress
                WHERE ID = :Id""",
                           {
                               'stuName': box_Name_Edit.get(),
                               'stuEmail': box_Email_Edit.get(),
                               'stuAddress': box_Address_Edit.get(),
                               'Id': record_id
                           }
                           )
            conn.commit()
            print("record updated successfully")
            conn.close()
            confirm_edit.destroy()
            show.destroy()

        btn_confirmtoEdit = Button(show, text="Confirm to Edit", command=confirmToEdit, bg="white", fg="black",
                                   font=("arial bold", 8))
        btn_confirmtoEdit.grid(row=27, column=2, columnspan=2)

    btn_deleteRecord = Button(show, text="Delete Record", width=12, command=dlrecord, bg="#0097e6", fg="white",
                              font=("arial bold", 10))
    btn_deleteRecord.grid(row=17, column=1, columnspan=3, ipadx=50, pady=8)

    btn_updateRecord = Button(show, text="Edit Record", width=12, command=editRecord, bg="#0097e6", fg="white",
                              font=("arial bold", 10))
    btn_updateRecord.grid(row=24, column=1, columnspan=3, ipadx=50, pady=8)


def exitRecord():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    app.destroy()


def AddExit():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    ADD.destroy()


def addRecord():
    global ADD
    global show
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    ADD = Tk()
    ADD.title("add record section")
    ADD.geometry('400x300')
    global box_Name
    global box_Email
    global box_Address
    lbl_Name = Label(ADD, text="Name: ", font=("Arial", 14))
    lbl_Name.grid(row=5, column=1, columnspan=2)
    box_Name = Entry(ADD, width=23, font=("Arial", 12))
    box_Name.grid(row=6, column=2, padx=100, pady=5, columnspan=2)

    lbl_Email = Label(ADD, text="Email: ", font=("Arial", 14))
    lbl_Email.grid(row=7, column=1, columnspan=2)
    box_Email = Entry(ADD, width=23, font=("Arial", 12))
    box_Email.grid(row=8, column=1, padx=100, pady=5, columnspan=2)

    lbl_Address = Label(ADD, text="Address: ", font=("Arial", 14))
    lbl_Address.grid(row=9, column=1, columnspan=2)
    box_Address = Entry(ADD, width=23, font=("Arial", 12))
    box_Address.grid(row=10, column=1, padx=100, pady=5, columnspan=2)

    def connec():
        cursor.execute("INSERT INTO studentForm(Name,Email,Address)VALUES(:box_Name,:box_Email,:box_Address)",
                       {
                           'box_Name': box_Name.get(),
                           'box_Email': box_Email.get(),
                           'box_Address': box_Address.get()

                       }
                       )

        conn.commit()
        print("record added successfully")
        conn.close()
        ADD.destroy()
        show.destroy()

    btn_confirmAdd = Button(ADD, text="Confirm to Add", command=connec, bg="white", fg="black", font=("arial bold", 8))
    btn_confirmAdd.grid(row=11, column=1, padx=100, pady=20, columnspan=2)


# lbl_Sdt_mng_pro = Label(app, text="Student Management Project", font=("Arial", 16))
# lbl_Sdt_mng_pro.grid(row=0, column=0, columnspan=2,pady=40,padx=30)
lbl_blank = Label(app, text="                             ", bg="#dcdde1")
lbl_blank.grid(row=0, column=0)

btn_showRecord = Button(app, text="Show Student Information", width=22, command=recordShow, borderwidth=3, bg="#00a8ff",
                        fg="white", activebackground="#00a8ff", activeforeground="white", font=("arial bold", 10),
                        relief=RAISED)

btn_showRecord.grid(row=1, column=1, pady=20, padx=18)

btn_showRecord_Exit = Button(app, text="Exit Window", width=15, command=exitRecord, borderwidth=3, bg="#718093",
                             fg="white", font=("arial bold", 9), relief=RAISED)
btn_showRecord_Exit.grid(row=2, column=1, pady=20, padx=20)

app.mainloop()
