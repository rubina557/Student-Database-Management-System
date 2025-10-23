"""
🎓 Student Database Management System
Developed by Rubina Nazeer
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

DB_FILENAME = 'students.db'

# Colors
BG = "#FFF7FA" 
CARD = '#FFFFFF'
BUTTON = '#00796B'
BUTTON_ACTIVE = '#004D40'
TEXT = '#263238'
ROW_ALT = '#E0F2F1'
HEADER = '#00796B'

# ---------------- Database ----------------
class StudentDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILENAME)
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                father_name TEXT,
                age INTEGER,
                gender TEXT,
                course TEXT,
                email TEXT,
                phone TEXT,
                result TEXT,
                attendance REAL
            )
        ''')
        self.conn.commit()

    def add_student(self, data):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO students (name, father_name, age, gender, course, email, phone, result, attendance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['father_name'], data['age'], data['gender'], data['course'],
              data['email'], data['phone'], data['result'], data['attendance']))
        self.conn.commit()

    def update_student(self, student_id, data):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE students SET name=?, father_name=?, age=?, gender=?, course=?, email=?, phone=?, result=?, attendance=?
            WHERE id=?
        ''', (data['name'], data['father_name'], data['age'], data['gender'], data['course'],
              data['email'], data['phone'], data['result'], data['attendance'], student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM students WHERE id=?', (student_id,))
        self.conn.commit()

    def fetch_all(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM students')
        return cur.fetchall()

    def search(self, keyword='', course=''):
        cur = self.conn.cursor()
        keyword = f'%{keyword}%'
        course = f'%{course}%'
        cur.execute('SELECT * FROM students WHERE name LIKE ? AND course LIKE ?', (keyword, course))
        return cur.fetchall()

    def close(self):
        self.conn.close()

# ---------------- App ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎓 Student Database Management System")
        self.configure(bg=BG)
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.db = StudentDB()
        self.selected_id = None

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure_styles()

       
        self.grid_rowconfigure(2, weight=1)   
        self.grid_columnconfigure(0, weight=1)

        self.build_ui()
        self.load_table()

    def configure_styles(self):
        self.style.configure('TLabel', background=BG, foreground=TEXT, font=('Segoe UI', 10))
        self.style.configure('Header.TFrame', background=HEADER)
        self.style.configure('Header.TLabel', background=HEADER, foreground='white', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Card.TFrame', background=CARD)
        self.style.configure('Card.TLabelframe', background=CARD, borderwidth=0)
        self.style.configure('Card.TLabelframe.Label', background=CARD, foreground=HEADER, font=('Segoe UI', 11, 'bold'))

        self.style.configure('Rounded.TButton',
                             font=('Segoe UI', 10, 'bold'),
                             foreground='white',
                             padding=8,
                             borderwidth=0)
        self.style.map('Rounded.TButton',
                       background=[('active', BUTTON_ACTIVE), ('!active', BUTTON)],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        self.style.configure('Custom.Treeview',
                             background='white',
                             fieldbackground='white',
                             rowheight=26)
        self.style.configure('Custom.Treeview.Heading',
                             background=HEADER,
                             foreground='white',
                             font=('Segoe UI', 10, 'bold'))

    def build_ui(self):
        # Header 
        header = ttk.Frame(self, style='Header.TFrame')
        header.grid(row=0, column=0, sticky='ew', padx=0, pady=(0,6))
        header.grid_columnconfigure(0, weight=1)
        ttk.Label(header, text="🎓 Student Database Management System", style='Header.TLabel').grid(row=0, column=0, padx=12, pady=12)

        # Card container for content 
        card = ttk.Frame(self, style='Card.TFrame')
        card.grid(row=1, column=0, sticky='nsew', padx=16, pady=(0,8))
        card.grid_columnconfigure(0, weight=1)

        # ---- Top: Form (full width) ----
        form_frame = ttk.LabelFrame(card, text='Student Information', style='Card.TLabelframe', padding=12)
        form_frame.grid(row=0, column=0, sticky='ew', padx=8, pady=6)
        
        for c in range(4):
            form_frame.columnconfigure(c, weight=1)

        fields = [
            ('name', 'Name'),
            ('father_name', "Father's Name"),
            ('age', 'Age'),
            ('gender', 'Gender'),
            ('course', 'Course'),
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('result', 'Result (Grade)'),
            ('attendance', 'Attendance (%)'),
        ]
        self.vars = {k: tk.StringVar() for k, _ in fields}

        
        ttk.Label(form_frame, text='Name:').grid(row=0, column=0, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['name']).grid(row=0, column=1, sticky='ew', padx=6, pady=6)

        ttk.Label(form_frame, text="Father's Name:").grid(row=0, column=2, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['father_name']).grid(row=0, column=3, sticky='ew', padx=6, pady=6)

       
        ttk.Label(form_frame, text='Age:').grid(row=1, column=0, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['age']).grid(row=1, column=1, sticky='w', padx=6, pady=6)

        ttk.Label(form_frame, text='Gender:').grid(row=1, column=2, sticky='w', padx=6, pady=6)
        gender_cb = ttk.Combobox(form_frame, textvariable=self.vars['gender'], values=['Male', 'Female', 'Other'], state='readonly')
        gender_cb.grid(row=1, column=3, sticky='w', padx=6, pady=6)
        gender_cb.set('Male')

        
        ttk.Label(form_frame, text='Course:').grid(row=2, column=0, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['course']).grid(row=2, column=1, sticky='ew', padx=6, pady=6)

        ttk.Label(form_frame, text='Email:').grid(row=2, column=2, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['email']).grid(row=2, column=3, sticky='ew', padx=6, pady=6)

        
        ttk.Label(form_frame, text='Phone:').grid(row=3, column=0, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['phone']).grid(row=3, column=1, sticky='ew', padx=6, pady=6)

        ttk.Label(form_frame, text='Result (Grade):').grid(row=3, column=2, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['result']).grid(row=3, column=3, sticky='w', padx=6, pady=6)

        ttk.Label(form_frame, text='Attendance (%):').grid(row=4, column=0, sticky='w', padx=6, pady=6)
        ttk.Entry(form_frame, textvariable=self.vars['attendance']).grid(row=4, column=1, sticky='w', padx=6, pady=6)

        # Buttons row 
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=(8,0))
        btn_frame.columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text='Add Student', style='Rounded.TButton', command=self.add_student).pack(side='left', padx=6)
        ttk.Button(btn_frame, text='Update Student', style='Rounded.TButton', command=self.update_student).pack(side='left', padx=6)
        ttk.Button(btn_frame, text='Delete Student', style='Rounded.TButton', command=self.delete_student).pack(side='left', padx=6)
        ttk.Button(btn_frame, text='Clear', style='Rounded.TButton', command=self.clear_form).pack(side='left', padx=6)

        # ---- Middle: Search / Filter ----
        search_frame = ttk.LabelFrame(card, text='Search & Filter', style='Card.TLabelframe', padding=10)
        search_frame.grid(row=1, column=0, sticky='ew', padx=8, pady=6)
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)

        ttk.Label(search_frame, text='Name:').grid(row=0, column=0, sticky='w', padx=6)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, sticky='ew', padx=6)

        ttk.Label(search_frame, text='Course:').grid(row=0, column=2, sticky='w', padx=6)
        self.filter_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.filter_var).grid(row=0, column=3, sticky='ew', padx=6)

        ttk.Button(search_frame, text='Search', style='Rounded.TButton', command=self.search_table).grid(row=0, column=4, padx=6)
        ttk.Button(search_frame, text='Show All', style='Rounded.TButton', command=self.load_table).grid(row=0, column=5, padx=6)

        # ---- Bottom: Table ----
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky='nsew', padx=16, pady=(0,12))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ('ID', 'Name', 'Father', 'Age', 'Gender', 'Course', 'Email', 'Phone', 'Result', 'Attendance')
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', style='Custom.Treeview')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor='center', stretch=True, width=100)

        self.tree.tag_configure('odd', background='white')
        self.tree.tag_configure('even', background=ROW_ALT)

        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Footer
        footer = ttk.Frame(self)
        footer.grid(row=3, column=0, sticky='ew', padx=16, pady=(2,10))
        footer.grid_columnconfigure(0, weight=1)
        ttk.Label(footer, text='Developed by Rubina Nazeer — Python Tkinter Project', background=BG, foreground=TEXT).grid(row=0, column=0)

        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # ---------------- Helpers & Validation ----------------
    def get_form_data(self):
        d = {k: v.get().strip() for k, v in self.vars.items()}
        
        d['age'] = int(d['age']) if d['age'].isdigit() else None
        
        if d['attendance']:
            try:
                d['attendance'] = float(d['attendance'])
            except ValueError:
                d['attendance'] = None
        else:
            d['attendance'] = None
        return d

    def clear_form(self):
        for v in self.vars.values():
            v.set('')
        self.vars['gender'].set('Male')
        self.selected_id = None
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def validate(self, data):
        if not data['name']:
            messagebox.showwarning('Validation', 'Name is required.')
            return False
        if data['age'] is None or not (5 <= int(data['age']) <= 100):
            messagebox.showwarning('Validation', 'Enter a valid age (5–100).')
            return False
        if data['email']:

            if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
                messagebox.showwarning('Validation', 'Enter a valid email address.')
                return False
        # phone is required and must be 11 digits
        if not (data['phone'].isdigit() and len(data['phone']) == 11):
            messagebox.showwarning('Validation', 'Phone must be 11 digits.')
            return False
        if data['result']:
            if data['result'].upper() not in ['A', 'B', 'C', 'D', 'F']:
                messagebox.showwarning('Validation', 'Result must be one of A,B,C,D,F.')
                return False
        if data['attendance'] is not None:
            try:
                att = float(data['attendance'])
                if not (0 <= att <= 100):
                    raise ValueError
            except ValueError:
                messagebox.showwarning('Validation', 'Attendance must be a number between 0 and 100.')
                return False
        return True

    # ---------------- CRUD ----------------
    def add_student(self):
        data = self.get_form_data()
        if not self.validate(data):
            return
        self.db.add_student(data)
        self.load_table()
        self.clear_form()
        messagebox.showinfo('Success', 'Student added.')

    def update_student(self):
        if not self.selected_id:
            messagebox.showwarning('Select', 'Select a student to update.')
            return
        data = self.get_form_data()
        if not self.validate(data):
            return
        self.db.update_student(self.selected_id, data)
        self.load_table()
        self.clear_form()
        messagebox.showinfo('Updated', 'Student updated.')

    def delete_student(self):
        if not self.selected_id:
            messagebox.showwarning('Select', 'Select a student to delete.')
            return
        if messagebox.askyesno('Confirm', 'Delete selected student?'):
            self.db.delete_student(self.selected_id)
            self.load_table()
            self.clear_form()
            messagebox.showinfo('Deleted', 'Student deleted.')

    def load_table(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.fetch_all()
        for i, row in enumerate(rows):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert('', 'end', values=row, tags=(tag,))

    def search_table(self):
        kw = self.search_var.get().strip()
        crs = self.filter_var.get().strip()
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.search(kw, crs)
        for i, row in enumerate(rows):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert('', 'end', values=row, tags=(tag,))
        # clear filters after search
        self.search_var.set('')
        self.filter_var.set('')

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], 'values')
        self.selected_id = vals[0]
        keys = list(self.vars.keys())
        for i, k in enumerate(keys):
            # tree values start at index 1 for the form vars (0 is ID)
            self.vars[k].set(vals[i+1] if vals[i+1] is not None else '')

    def on_close(self):
        try:
            self.db.close()
        except:
            pass
        self.destroy()

if __name__ == '__main__':
    app = App()
    app.protocol('WM_DELETE_WINDOW', app.on_close)
    app.mainloop()

