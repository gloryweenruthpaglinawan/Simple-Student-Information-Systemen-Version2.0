from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox


def main():
    root = Tk()
    root.title("STUDENT INFORMATION SYSTEM")
    w = 1350
    h = 400
    root.geometry(f'{w}x{h}+{1}+{150}')
    root.config(bg='black')
    root.resizable(False, False)

    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS studentlist (
              ID_NUMBER,
              NAME,
              GENDER,
              YEAR_LEVEL,
              COURSE_CODE
              )""")

    c.execute("""CREATE TABLE IF NOT EXISTS courselist (
              COURSE_CODE,
              COURSE
                )""")

    def filled_table():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        c.execute("""SELECT ID_NUMBER, NAME, GENDER, YEAR_LEVEL, courselist.COURSE_CODE, courselist.COURSE FROM studentlist
                      INNER JOIN courselist ON courselist.COURSE_CODE = studentlist.COURSE_CODE;""")

        records = c.fetchall()

        for i in records:
            tree.insert('', 'end', value=i)

    def cclist():
        conn = sqlite3.connect("StudentsList.db")
        c = conn.cursor()
        c.execute('''SELECT COURSE_CODE FROM courselist''')
        result = c.fetchall()
        result = [i[0] for i in result]
        return result

    def cnlist():
        conn = sqlite3.connect("StudentsList.db")
        c = conn.cursor()
        c.execute('''SELECT COURSE FROM courselist''')
        result = c.fetchall()
        result = [i[0] for i in result]
        return result

    def register():
        if E1.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E2.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif gender.get() == 'Select Gender':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif yearlvl.get() == 'Select Year Level':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif course_code.get() == 'Select Course Code':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif course_code.get() not in cclist():
            messagebox.showinfo("OH NO!", "PLEASE ENTER COURSE NAME")
            reg_coursecode.insert(0, course_code.get())
            print(cclist())

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        c.execute("INSERT INTO studentlist VALUES(:ID_NUMBER, :NAME, :GENDER,:YEAR_LEVEL,:COURSE_CODE)",
                  {
                      'ID_NUMBER': E1.get(),
                      'NAME': E2.get(),
                      'GENDER': gender.get(),
                      'YEAR_LEVEL': yearlvl.get(),
                      'COURSE_CODE': course_code.get()
                  })

        conn.commit()
        if course_code.get() in cclist():
            messagebox.showinfo("REGISTRATION INFORMATION", "YEHEY! YOU JUST GOT REGISTERED!")
        conn.close()

        filled_table()

        E1.delete(0, END)
        E2.delete(0, END)
        gender.set("Select Gender")
        yearlvl.set("Select Year Level")
        course_code.set("Select Course Code")

    def course_reg():
        if reg_coursecode.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif reg_course.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        c.execute("INSERT INTO courselist VALUES(:COURSE_CODE, :COURSE)",
                  {
                      'COURSE_CODE': reg_coursecode.get(),
                      'COURSE': reg_course.get()
                  })

        conn.commit()
        messagebox.showinfo("COURSE REGISTRATION INFO", "YEHEY! COURSE REGISTERED!")
        conn.close()

        filled_table()

        course_code['values'] = cclist()
        root_coursecode['values'] = cclist()
        edlt_coursecode['values'] = cclist()
        edlt_course['values'] = cnlist()

        reg_coursecode.delete(0, END)
        reg_course.delete(0, END)

    def course_edit():
        if edlt_coursecode.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif edlt_course.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        data6 = edlt_coursecode.get()
        data7 = edlt_course.get()

        c.execute("UPDATE courselist set COURSE_CODE=?, COURSE=?  WHERE COURSE_CODE=? ",
                  (data6, data7, data6))

        conn.commit()
        messagebox.showinfo("COURSE EDIT INFO", "YEHEY! COURSE EDITED!")
        conn.close()

        filled_table()

        course_code['values'] = cclist()
        root_coursecode['values'] = cclist()

        edlt_coursecode['values'] = cclist()
        edlt_course['values'] = cnlist()

        edlt_coursecode.delete(0, END)
        edlt_course.delete(0, END)

    def course_list():
        top = Tk()
        top.title("COURSE LIST")
        w = 370
        h = 250
        top.geometry(f'{w}x{h}+{970}+{380}')
        top.config(bg='black')
        top.resizable(False, False)

        def delete():
            selected_item = tree1.focus()

            if selected_item == "":
                messagebox.showwarning("ERROR!", "PLEASE SELECT INFORMATION TO DELETE")
                top.lift()
            else:
                if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
                    return
                else:
                    messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
                    top.lift()
                    conn = sqlite3.connect("StudentsList.db")
                    c = conn.cursor()
                    for selected_item in tree1.selection():
                        c.execute("DELETE FROM courselist WHERE COURSE_CODE=?", (tree1.set(selected_item, '#1'),))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.close()
                    top.lift()

        conn = sqlite3.connect("StudentsList.db")
        c = conn.cursor()
        c.execute("SELECT * FROM courselist")
        courses = c.fetchall()

        Course_Dlt = Button(top, text="DELETE", font=("Lucida Console", 12, "bold"), command=delete)
        Course_Dlt.place(x=145, y=215)

        frm = Frame(top)
        frm.pack(side=LEFT, padx=0, pady=(0, 40))

        tree1 = ttk.Treeview(frm, columns=(1, 2), show="headings", height=9)
        tree1.pack()

        tree1.heading(1, text="COURSE CODE", anchor=CENTER)
        tree1.column("1", minwidth=0, width=120)
        tree1.heading(2, text="COURSE", anchor=CENTER)
        tree1.column("2", minwidth=0, width=245)

        for i in courses:
            tree1.insert('', 'end', value=i)

        top.mainloop()

    def select():
        conn = sqlite3.connect('StudentsList.db')

        E3.delete(0, END)
        E4.delete(0, END)
        root_gender.delete(0, END)
        root_yearlvl.delete(0, END)
        root_coursecode.delete(0, END)

        selected = tree.focus()
        values = tree.item(selected, 'values')

        E3.insert(0, values[0])
        E4.insert(0, values[1])
        root_gender.insert(0, values[2])
        root_yearlvl.insert(0, values[3])
        root_coursecode.insert(0, values[4])

        conn.commit()
        conn.close()

    def update():
        if E3.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E4.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_gender.get() == 'Select Gender':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_yearlvl.get() == 'Select Year Level':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_coursecode.get() == 'Select Course Code':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        messagebox.showinfo("UPDATE INFORMATION", "YEHEY! DATA UPDATED")
        data1 = E3.get()
        data2 = E4.get()
        data3 = root_gender.get()
        data4 = root_yearlvl.get()
        data5 = root_coursecode.get()

        selected = tree.selection()
        tree.item(selected, values=(data1, data2, data3, data4, data5))
        c.execute(
            "UPDATE studentlist set  ID_NUMBER=?, NAME=?, GENDER=?, YEAR_LEVEL=?, COURSE_CODE=?  WHERE ID_NUMBER=? ",
            (data1, data2, data3, data4, data5, data1))

        conn.commit()
        conn.close()
        filled_table()

        E3.delete(0, END)
        E4.delete(0, END)
        root_gender.set("Select Gender")
        root_yearlvl.set("Select Year Level")
        root_coursecode.set("Select Course Code")

    def delete():
        selected_item = tree.focus()

        if selected_item == "":
            messagebox.showwarning("ERROR!", "PLEASE SELECT INFORMATION TO DELETE")

        else:
            if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
                return
            else:
                messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
                conn = sqlite3.connect("StudentsList.db")
                c = conn.cursor()
                for selected_item in tree.selection():
                    c.execute("DELETE FROM studentlist WHERE ID_NUMBER=?", (tree.set(selected_item, '#1'),))
                    conn.commit()
                    tree.delete(selected_item)
                conn.close()

    def search():
        root1 = Tk()
        root1.title("STUDENT FOUND!")
        root1.geometry("1000x100")
        root1.config(bg='white')
        root1.resizable(False, False)

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        c.execute("""SELECT ID_NUMBER, NAME, GENDER, YEAR_LEVEL, courselist.COURSE_CODE, courselist.COURSE FROM studentlist
                       INNER JOIN courselist ON courselist.COURSE_CODE = studentlist.COURSE_CODE WHERE ID_NUMBER=?""",
                  (E3.get(),))
        records = c.fetchall()

        frm = Frame(root1)
        frm.pack(side=LEFT, padx=5, pady=(0, 0))

        tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
        tree.pack()

        tree.heading(1, text="ID NUMBER", anchor=CENTER)
        tree.column("1", minwidth=0, width=150)
        tree.heading(2, text="NAME", anchor=CENTER)
        tree.heading(3, text="GENDER", anchor=CENTER)
        tree.column("3", minwidth=0, width=150)
        tree.heading(4, text="YEAR LEVEL", anchor=CENTER)
        tree.column("4", minwidth=0, width=150)
        tree.heading(5, text="COURSE CODE", anchor=CENTER)
        tree.column("5", minwidth=0, width=150)
        tree.heading(6, text="COURSE", anchor=CENTER)

        for i in records:
            tree.insert('', 'end', value=i)

        if not records:
            root1.destroy()
            messagebox.showinfo("SEARCH INFORMATION", "STUDENT DOESN'T EXIST or ENTER ID NUMBER")

        root1.mainloop()

    # LABEL FRAMES
    Reg = LabelFrame(root, text="Registration Form", width=465, height=200, bg="black", fg="white",
                     font=("Lucida Console", 15, "bold"))
    Reg.place(x=500, y=0)
    Upd_Del = LabelFrame(root, text="Update and Delete Form", width=500, height=200, bg="black", fg="white",
                         font=("Lucida Console", 15, "bold"))
    Upd_Del.place(x=0, y=0)
    Course = LabelFrame(root, text="Course Registration Form", width=385, height=100, bg="black", fg="white",
                        font=("Lucida Console", 15, "bold"))
    Course.place(x=965, y=0)
    Course_Edlt = LabelFrame(root, text="Course Edit/Delete Form", width=385, height=100, bg="black", fg="white",
                             font=("Lucida Console", 15, "bold"))
    Course_Edlt.place(x=965, y=100)

    # REGISTRATION LABELS
    L1 = Label(root, text="ID NUMBER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L1.place(x=510, y=35)
    L2 = Label(root, text="NAME:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L2.place(x=510, y=60)
    L3 = Label(root, text="GENDER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L3.place(x=510, y=85)
    L4 = Label(root, text="YEAR LEVEL:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L4.place(x=510, y=110)
    L5 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L5.place(x=510, y=135)

    # REGISTRATION ENTRIES
    E1 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E1.place(x=650, y=35)
    E2 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E2.place(x=650, y=60)

    gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    gender.set("Select Gender")
    gender['values'] = ("Male", "Female", "Other")
    gender.place(x=650, y=85)

    yearlvl = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    yearlvl.set("Select Year Level")
    yearlvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    yearlvl.place(x=650, y=110)

    course_code = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    course_code.set("Select Course Code")
    course_code['values'] = cclist()
    course_code.place(x=650, y=135)

    # BUTTONS
    Sel = Button(root, text="SELECT", font=("Lucida Console", 9, "bold"), command=select)
    Sel.place(x=300, y=15)
    Upd = Button(root, text="UPDATE", font=("Lucida Console", 9, "bold"), command=update)
    Upd.place(x=365, y=15)
    Del = Button(root, text="DELETE", font=("Lucida Console", 9, "bold"), command=delete)
    Del.place(x=430, y=15)
    Sea = Button(root, text="SEARCH", font=("Lucida Console", 9, "bold"), command=search)
    Sea.place(x=430, y=40)
    Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=register)
    Reg.place(x=865, y=170)
    Course_Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=course_reg)
    Course_Reg.place(x=1270, y=75)
    Course_Edt = Button(root, text="EDIT", font=("Lucida Console", 9, "bold"), command=course_edit)
    Course_Edt.place(x=1300, y=175)
    Course_Lst = Button(root, text="COURSE LIST", font=("Lucida Console", 9, "bold"), command=course_list)
    Course_Lst.place(x=970, y=175)

    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()

    c.execute("""SELECT ID_NUMBER, NAME, GENDER, YEAR_LEVEL, courselist.COURSE_CODE, courselist.COURSE FROM studentlist
              INNER JOIN courselist ON courselist.COURSE_CODE = studentlist.COURSE_CODE;""")

    records = c.fetchall()

    frm = Frame(root)
    frm.pack(side=LEFT, padx=5, pady=(200, 0))

    tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
    tree.pack()

    tree.heading(1, text="ID NUMBER", anchor=CENTER)
    tree.column("1", minwidth=0, width=200)
    tree.heading(2, text="NAME", anchor=CENTER)
    tree.column("2", minwidth=0, width=270)
    tree.heading(3, text="GENDER", anchor=CENTER)
    tree.column("3", minwidth=0, width=200)
    tree.heading(4, text="YEAR LEVEL", anchor=CENTER)
    tree.column("4", minwidth=0, width=200)
    tree.heading(5, text="COURSE CODE", anchor=CENTER)
    tree.column("5", minwidth=0, width=200)
    tree.heading(6, text="COURSE", anchor=CENTER)
    tree.column("6", minwidth=0, width=270)

    for i in records:
        tree.insert('', 'end', value=i)

    # UPDATE AND DELETE ENTRIES
    E3 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E3.place(x=200, y=40)
    E4 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E4.place(x=130, y=75)

    root_gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_gender.set("Select Gender")
    root_gender['values'] = ("Male", "Female", "Other")
    root_gender.place(x=130, y=100)

    root_yearlvl = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_yearlvl.set("Select Year Level")
    root_yearlvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    root_yearlvl.place(x=130, y=125)

    root_coursecode = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_coursecode.set("Select Course Code")
    root_coursecode['values'] = cclist()
    root_coursecode.place(x=130, y=150)

    # UPDATE AND DELETE LABELS
    L7 = Label(root, text="ID NUMBER TO FIND:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L7.place(x=5, y=38)
    L8 = Label(root, text="NAME:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L8.place(x=5, y=75)
    L9 = Label(root, text="GENDER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L9.place(x=5, y=100)
    L10 = Label(root, text="YEAR LEVEL:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L10.place(x=5, y=125)
    L11 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L11.place(x=5, y=150)

    # COURSE REGISTRATION LABELS
    L12 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L12.place(x=970, y=25)
    L13 = Label(root, text="COURSE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L13.place(x=970, y=50)

    # COURSE REGISTRATION ENRTRIES
    reg_coursecode = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    reg_coursecode.place(x=1100, y=25)
    reg_course = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    reg_course.place(x=1100, y=50)

    # COURSE EDIT/DELETE LABELS
    L14 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L14.place(x=970, y=125)
    L15 = Label(root, text="COURSE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L15.place(x=970, y=150)

    ##COURSE EDIT/DELETE ENRTRIES
    edlt_coursecode = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    edlt_coursecode.set("Select Course Code")
    edlt_coursecode['values'] = cclist()
    edlt_coursecode.place(x=1100, y=125)

    edlt_course = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    edlt_course.set("Select Course Name")
    edlt_course['values'] = cnlist()
    edlt_course.place(x=1100, y=150)

    conn.commit()
    conn.close()

    root.mainloop()

main()
