import sqlite3
import random
import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog

# ---------- Setup ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
DB = "students.db"

COURSE_DURATION = {"B.Tech":4,"MCA":3,"MBA":2,"BBA":3,"PhD":5}

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_uid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY student_uid")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_student(name, course, year):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, course, year) VALUES (?, ?, ?)", (name, course, year))
    conn.commit()
    conn.close()

def update_student_db(uid, name, course, year):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, course=?, year=? WHERE student_uid=?", (name, course, year, uid))
    conn.commit()
    conn.close()

def delete_student_db(uid):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_uid=?", (uid,))
    conn.commit()
    conn.close()

def reset_year_column():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT student_uid, course FROM students")
    all_students = cur.fetchall()
    for uid, course in all_students:
        max_year = COURSE_DURATION.get(course,5)
        valid_year = random.randint(1,max_year)
        cur.execute("UPDATE students SET year=? WHERE student_uid=?", (valid_year, uid))
    conn.commit()
    conn.close()

# ---------- App ----------
class StudentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.table_visible = True

        # ---------- Full Screen Fit to Screen ----------
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")  # full screen size
        self.update()  # refresh window size

        # ===== Title =====
        title = ctk.CTkLabel(self, text="STUDENT MANAGEMENT SYSTEM", font=("Arial Black",28))
        title.pack(pady=10)

        # ===== Input Frame =====
        input_frame = ctk.CTkFrame(self, corner_radius=10)
        input_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(input_frame, text="Student U_ID:", font=("Arial",15)).grid(row=0,column=0,padx=10,pady=5)
        self.uid_entry = ctk.CTkEntry(input_frame, width=180)
        self.uid_entry.grid(row=0,column=1,padx=10,pady=5)

        ctk.CTkLabel(input_frame, text="Name:", font=("Arial",15)).grid(row=0,column=2,padx=10,pady=5)
        self.name_entry = ctk.CTkEntry(input_frame, width=180)
        self.name_entry.grid(row=0,column=3,padx=10,pady=5)

        ctk.CTkLabel(input_frame, text="Course:", font=("Arial",15)).grid(row=1,column=0,padx=10,pady=5)
        self.course_dropdown = ctk.CTkComboBox(input_frame, values=list(COURSE_DURATION.keys()), width=180)
        self.course_dropdown.grid(row=1,column=1,padx=10,pady=5)

        ctk.CTkLabel(input_frame, text="Year:", font=("Arial",15)).grid(row=1,column=2,padx=10,pady=5)
        self.year_dropdown = ctk.CTkComboBox(input_frame, values=["1","2","3","4","5"], width=180)
        self.year_dropdown.grid(row=1,column=3,padx=10,pady=5)
        self.year_dropdown.set("1")

        # ===== Sort & Filter Frame =====
        criteria_frame = ctk.CTkFrame(self, corner_radius=10)
        criteria_frame.pack(pady=5, padx=20, fill="x")

        # Sorting
        ctk.CTkLabel(criteria_frame, text="Sort By Column:", font=("Arial",13)).grid(row=0,column=0,padx=10)
        self.sort_column = ctk.CTkComboBox(criteria_frame, values=["student_uid","name","course","year"], width=180)
        self.sort_column.grid(row=0,column=1,padx=10)
        self.sort_column.set("name")

        ctk.CTkLabel(criteria_frame, text="Sort Order:", font=("Arial",13)).grid(row=0,column=2,padx=10)
        self.sort_order = ctk.CTkComboBox(criteria_frame, values=["Ascending","Descending"], width=180)
        self.sort_order.grid(row=0,column=3,padx=10)
        self.sort_order.set("Ascending")

        # Filtering
        ctk.CTkLabel(criteria_frame, text="Filter Column:", font=("Arial",13)).grid(row=0,column=4,padx=10)
        self.filter_column = ctk.CTkComboBox(criteria_frame, values=["student_uid","name","course","year"], width=180)
        self.filter_column.grid(row=0,column=5,padx=10)
        self.filter_column.set("course")

        ctk.CTkLabel(criteria_frame, text="Filter Value:", font=("Arial",13)).grid(row=0,column=6,padx=10)
        self.filter_value = ctk.CTkEntry(criteria_frame, width=180)
        self.filter_value.grid(row=0,column=7,padx=10)

        # ===== Button Frame =====
        btn_frame = ctk.CTkFrame(self, corner_radius=10)
        btn_frame.pack(pady=10, padx=20, fill="x")

        button_style={"width":120,"height":35,"corner_radius":10,"font":("Arial",13)}

        self.add_btn = ctk.CTkButton(btn_frame,text="Add",command=self.add_student,**button_style)
        self.update_btn = ctk.CTkButton(btn_frame,text="Update",command=self.update_student,**button_style)
        self.delete_btn = ctk.CTkButton(btn_frame,text="Delete",command=self.delete_student,fg_color="#F25454",**button_style)
        self.clear_btn = ctk.CTkButton(btn_frame,text="Clear",command=self.clear_fields,fg_color="#9E9E9E",**button_style)
        self.search_btn = ctk.CTkButton(btn_frame,text="Search",command=self.search_student,**button_style)
        self.filter_btn = ctk.CTkButton(btn_frame,text="Filter",command=self.apply_filter,**button_style)
        self.sort_btn = ctk.CTkButton(btn_frame,text="Sort",command=self.apply_sort,**button_style)
        self.refresh_btn = ctk.CTkButton(btn_frame,text="Refresh",command=self.load_data,**button_style)
        self.toggle_btn = ctk.CTkButton(btn_frame,text="Hide Table",command=self.toggle_table,**button_style)
        self.restore_btn = ctk.CTkButton(btn_frame,text="Reset Year",command=self.reset_year_button,**button_style)
        self.random_btn = ctk.CTkButton(btn_frame,text="Random Data",command=self.add_random_student,**button_style)

        buttons=[self.add_btn,self.update_btn,self.delete_btn,self.clear_btn,self.search_btn,self.filter_btn,
                 self.sort_btn,self.refresh_btn,self.toggle_btn,self.restore_btn,self.random_btn]
        for i,btn in enumerate(buttons): btn.grid(row=0,column=i,padx=6,pady=10)

        # ===== Table =====
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_frame, columns=("student_uid","name","course","year"), show="headings")
        for col in ("student_uid","name","course","year"):
            self.tree.heading(col,text=col)
            self.tree.column(col,anchor="center",width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1C1C1C", foreground="white", fieldbackground="#1C1C1C", font=('Arial',12))
        style.configure("Treeview.Heading", background="#004C99", foreground="white", font=('Arial',13,'bold'))

        self.load_data()

    # ---------- CRUD ----------
    def add_student(self):
        name=self.name_entry.get().strip()
        course=self.course_dropdown.get().strip()
        year=self.year_dropdown.get().strip()
        if not name or not course or not year: messagebox.showerror("Error","All fields required"); return
        insert_student(name,course,int(year))
        messagebox.showinfo("Success","Student Added"); self.clear_fields(); self.load_data()

    def update_student(self):
        uid=self.uid_entry.get().strip()
        if not uid: messagebox.showerror("Error","Enter Student UID"); return
        try: uid=int(uid)
        except: messagebox.showerror("Error","UID must be integer"); return
        name=self.name_entry.get().strip()
        course=self.course_dropdown.get().strip()
        year=self.year_dropdown.get().strip()
        if not name or not course or not year: messagebox.showerror("Error","All fields required"); return
        update_student_db(uid,name,course,int(year))
        messagebox.showinfo("Success","Student Updated"); self.clear_fields(); self.load_data()

    def delete_student(self):
        uid=self.uid_entry.get().strip()
        if not uid: messagebox.showerror("Error","Enter Student UID"); return
        try: uid=int(uid)
        except: messagebox.showerror("Error","UID must be integer"); return
        confirm=messagebox.askyesno("Confirm Delete",f"Delete UID {uid}?")
        if confirm: delete_student_db(uid); messagebox.showinfo("Deleted","Student Deleted"); self.clear_fields(); self.load_data()

    def search_student(self):
        query=self.uid_entry.get().strip() or self.name_entry.get().strip()
        if not query: messagebox.showerror("Error","Enter UID or Name"); return
        rows=fetch_all(); result=[]
        for r in rows:
            if str(r[0])==query or query.lower() in r[1].lower(): result.append(r)
        self._populate_tree(result, highlight=True)

    # ---------- Multi-level Sort & Filter ----------
    def apply_sort(self):
        col = self.sort_column.get()
        order = self.sort_order.get()
        rows = [self.tree.item(i)['values'] for i in self.tree.get_children()]
        reverse = True if order=="Descending" else False
        rows.sort(key=lambda r: r[0] if col=="student_uid" else (r[1].lower() if col=="name" else (r[2].lower() if col=="course" else r[3])), reverse=reverse)
        self._populate_tree(rows)

    def apply_filter(self):
        col = self.filter_column.get()
        val = self.filter_value.get().strip()
        rows = fetch_all(); result=[]
        for r in rows:
            if col=="student_uid" and str(r[0])!=val: continue
            if col=="name" and val.lower() not in r[1].lower(): continue
            if col=="course" and val.lower()!=r[2].lower(): continue
            if col=="year" and int(val)!=r[3]: continue
            result.append(r)
        self._populate_tree(result, highlight=True)

    def reset_year_button(self):
        reset_year_column()
        messagebox.showinfo("Success","All Years Reset According to Course")
        self.load_data()

    def add_random_student(self):
        count = simpledialog.askinteger("Random Students", "How many random students to insert?", minvalue=1, maxvalue=100)
        if not count: return
        first_names = ["Alice","Bob","Charlie","Diana","Ethan","Fiona","George","Hannah"]
        last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller"]
        for _ in range(count):
            name = random.choice(first_names) + " " + random.choice(last_names)
            course = random.choice(list(COURSE_DURATION.keys()))
            year = random.randint(1, COURSE_DURATION[course])
            insert_student(name, course, year)
        messagebox.showinfo("Success", f"{count} Random Student(s) Added Successfully!")
        self.load_data()

    def clear_fields(self):
        self.uid_entry.delete(0,'end')
        self.name_entry.delete(0,'end')
        self.course_dropdown.set("")
        self.year_dropdown.set("1")
        self.filter_value.delete(0,'end')

    def toggle_table(self):
        if self.table_frame.winfo_ismapped(): self.table_frame.pack_forget(); self.toggle_btn.configure(text="Show Table")
        else: self.table_frame.pack(pady=10, fill="both", expand=True); self.toggle_btn.configure(text="Hide Table")

    def load_data(self):
        self._populate_tree(fetch_all())

    def _populate_tree(self, rows, highlight=False):
        for row in self.tree.get_children(): self.tree.delete(row)
        for r in rows:
            self.tree.insert('', 'end', values=r, tags=("highlight",) if highlight else ())
        self.tree.tag_configure("highlight", background="#1E90FF")  # Filtered rows highlighted

# ---------- Run ----------
if __name__=="__main__":
    init_db()
    app=StudentApp()
    app.mainloop()
