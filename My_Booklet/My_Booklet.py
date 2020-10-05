import sqlite3
import tkinter as tk
from tkinter import *
import tkinter .ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import ImageTk, Image
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyautogui
import time
import os


base=sqlite3.connect('Data_Bib.db')
c=base.cursor()

try:
    c.execute("""CREATE TABLE teachers
    (
        name text,
        mail text,
        remind text,
        phone text,
        consulting text,
        zoom text,
        area text,
        active_team text
    )

    """)
    
    c.execute("""CREATE TABLE students
    (
        name text,
        id text,
        username text,
        phone text,
        active_team text
    )

    """)

    c.execute("""CREATE TABLE tasks
    (
        task text,
        completed text,
        original_id int

    )

    """)    
    
except sqlite3.OperationalError:
    print("Table already exists")


c.execute("SELECT *, oid FROM teachers")
teachers = c.fetchall()

#Actual program starts here
root=tk.Tk()
root.geometry('1275x800')
root.config(bg='#212121', padx=20)
root.title("My_Booklet") #Window Title
root.iconbitmap('icon.ico') 


def zoom_login(meeting_id):
    os.startfile("C:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Zoom/Start Zoom") #Your zoom directory here, with oct 25, 2020 update, my new route is C:/Users/user/Desktop/Zoom
    time.sleep(12)
    joinbtn=pyautogui.locateCenterOnScreen("zoom_join.png")
    pyautogui.moveTo(joinbtn)
    pyautogui.click()
    meet_id=pyautogui.locateCenterOnScreen("enter_id.png")
    pyautogui.moveTo(meet_id)
    pyautogui.write(meeting_id)
    time.sleep(2)
    joinbtn=pyautogui.locateCenterOnScreen("turn_video_off.png")
    pyautogui.moveTo(joinbtn)
    pyautogui.click()
    time.sleep(2)
    join_meetbtn=pyautogui.locateCenterOnScreen("join_meet.png")
    pyautogui.moveTo(join_meetbtn)
    pyautogui.click()





def update_teacher(current, name, mail, remind, phone, day, i_time, f_time, zoom, area, active):
    name_exists=True
    current_consulting=day+" from "+i_time+" to "+f_time
    if i_time=="" and f_time=="":
        current_consulting=""
    if name=="":
        name_exists = False
        no_name=messagebox.showerror("NO NAME GIVEN", "The submission was unable to be completed because there is no NAME given")
    else:
        name_exists=True

    if name_exists:
        c=base.cursor()
        in_active_class=""
        if active==0:
            in_active_class="YES"
        else:
            in_active_class="NO"

        new_name=(str(name), current)
        c.execute("""Update teachers set name=? where ROWID=?""", new_name)
        base.commit()
        new_mail=(str(mail), current)
        c.execute("""Update teachers set mail=? where ROWID=?""", new_mail)
        base.commit()
        if str(remind)!="@":
            new_remind=(str(remind), current)
        else:
            new_remind=("", current)
        c.execute("""Update teachers set remind=? where ROWID=?""", new_remind)
        base.commit()
        new_phone=(str(phone), current)
        c.execute("""Update teachers set phone=? where ROWID=?""", new_phone)
        base.commit()
        new_consulting=(current_consulting, current)
        c.execute("""Update teachers set consulting=? where ROWID=?""", new_consulting)
        base.commit()
        new_zoom=(str(zoom), current)
        c.execute("""Update teachers set zoom=? where ROWID=?""", new_zoom)
        base.commit()
        if str(area)=="" or str(area)==" ":
            new_area=("Other", current)
        else:
            new_area=(str(area), current)
        c.execute("""Update teachers set area=? where ROWID=?""", new_area)
        base.commit()
        new_active_class=(str(in_active_class), current)
        c.execute("""Update teachers set active_team=? where ROWID=?""", new_active_class)
        base.commit()
        edit_teacher(current)


def edit_teacher(current):
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)

    c=base.cursor()
    c.execute("SELECT *, oid FROM teachers")
    teachers = c.fetchall()
    current_name=str(teachers[current][0])
    current_mail=str(teachers[current][1])
    current_remind=str(teachers[current][2])
    current_phone=str(teachers[current][3])

    current_consulting=str(teachers[current][4])
    if current_consulting!="":
        split_consulting=current_consulting.split(" from ")
        current_day=split_consulting[0]
        more_split=split_consulting[1].split(" to ")
        current_from=more_split[0]
        current_to=more_split[1]
    else:
        current_to=""
        current_from=""
        current_day=""



    current_zoom=str(teachers[current][5])
    current_area=str(teachers[current][6])
    current_is_class_active=str(teachers[current][7])

    teacher_or_student=IntVar()
    #Type of Person: Student or Teacher
    add_type=Label(main_frame, text="Type of Person:", fg="#ffffff", bg="#272727")
    add_type.place(x=0, y=50)
    add_type_button_teacher=Radiobutton(main_frame, text="Teacher",variable=teacher_or_student, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727", command=add_teacher)
    add_type_button_teacher.place(x=100, y=50)
    add_type_button_student=Radiobutton(main_frame, text="Student",variable=teacher_or_student, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=200, y=50)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=90, y=40)
    add_type_button_teacher.config(state=DISABLED)
    add_type_button_student.config(state=DISABLED)
    #Name
    add_name= Label(main_frame, text="Full Name:", fg="#ffffff", bg="#272727")
    add_name.place(x=0, y=100)
    add_name_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_name_star.place(x=90, y=90)
    add_name_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_name_box.place(x=100, y=100)
    add_name_box.insert(0, current_name)
    #E-Mail
    add_mail= Label(main_frame, text="E-Mail Adress:", fg="#ffffff", bg="#272727")
    add_mail.place(x=0, y=150)
    add_mail_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_mail_box.place(x=100, y=150) 
    add_mail_box.insert(0, current_mail)
    #Remind
    add_remind= Label(main_frame, text="Remind Code:", fg="#ffffff", bg="#272727")
    add_remind.place(x=0, y=200)
    add_remind_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_remind_box.place(x=100, y=200) 
    add_remind_box.insert(0, current_remind)
    #Phone Number
    add_phone= Label(main_frame, text="Phone Number:", fg="#ffffff", bg="#272727")
    add_phone.place(x=0, y=250)
    add_phone_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_phone_box.place(x=100, y=250)
    add_phone_box.insert(0, current_phone)
    #Horas de asesorias
    consulting_day=StringVar()
    consulting_day.set("")
    consulting_initial=StringVar()
    consulting_initial.set("")
    consulting_final=StringVar()
    consulting_final.set("")
    add_consulting= Label(main_frame, text="Office Hours:", fg="#ffffff", bg="#272727")
    add_consulting.place(x=0, y=300)
    add_day_consulting=Label(main_frame, text="Day: ", fg="#ffffff", bg="#272727")
    add_day_consulting.place(x=100, y=300) 
    add_day_select=OptionMenu(main_frame, consulting_day, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
    add_day_select.config(bg="#272727", width=10, fg="#ffffff")
    add_day_select.place(x=140, y=295) 
    add_initial_time_consulting=Label(main_frame, text="From", fg="#ffffff", bg="#272727")
    add_initial_time_consulting.place(x=260, y=300) 
    add_initial_hour_select=OptionMenu(main_frame, consulting_initial, "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00") #Hora
    add_initial_hour_select.config(bg="#272727", width=6, fg="#ffffff")
    add_initial_hour_select.place(x=300, y=295) 
    add_final_time_consulting=Label(main_frame, text="To", fg="#ffffff", bg="#272727")
    add_final_time_consulting.place(x=400, y=300) 
    add_final_hour_select=OptionMenu(main_frame, consulting_final, "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00") #Hora 2
    add_final_hour_select.config(bg="#272727", width=6, fg="#ffffff")
    add_final_hour_select.place(x=440,y=295)
    if current_day=="Monday":
        consulting_day.set("Monday")
    elif current_day=="Tuesday":
        consulting_day.set("Tuesday")
    elif current_day=="Wednesday":
        consulting_day.set("Wednesday")
    elif current_day=="Thursday":
        consulting_day.set("Thursday")
    elif current_day=="Friday":
        consulting_day.set("Friday")
    else:
        consulting_day.set("")
    if current_from=="7:00":
        consulting_initial.set("7:00")
    elif current_from=="8:00":
        consulting_initial.set("8:00")
    elif current_from=="9:00":
        consulting_initial.set("9:00")
    elif current_from=="10:00":
        consulting_initial.set("10:00")
    elif current_from=="11:00":
        consulting_initial.set("11:00")
    elif current_from=="12:00":
        consulting_initial.set("12:00")
    elif current_from=="13:00":
        consulting_initial.set("13:00")
    elif current_from=="14:00":
        consulting_initial.set("14:00")
    elif current_from=="15:00":
        consulting_initial.set("15:00")
    elif current_from=="16:00":
        consulting_initial.set("16:00")
    elif current_from=="17:00":
        consulting_initial.set("17:00")
    elif current_from=="18:00":
        consulting_initial.set("18:00")
    elif current_from=="19:00":
        consulting_initial.set("19:00")
    elif current_from=="20:00":
        consulting_initial.set("20:00")
    else:
        consulting_initial.set("")
################CONSULTING_FINAL######################
    if current_to=="7:00":
        consulting_final.set("7:00")
    elif current_to=="":
        consulting_final.set("")
    elif current_to=="8:00":
        consulting_final.set("8:00")
    elif current_to=="9:00":
        consulting_final.set("9:00")
    elif current_to=="10:00":
        consulting_final.set("10:00")
    elif current_to=="11:00":
        consulting_final.set("11:00")
    elif current_to=="12:00":
        consulting_final.set("12:00")
    elif current_to=="13:00":
        consulting_final.set("13:00")
    elif current_to=="14:00":
        consulting_final.set("14:00")
    elif current_to=="15:00":
        consulting_final.set("15:00")
    elif current_to=="16:00":
        consulting_final.set("16:00")
    elif current_to=="17:00":
        consulting_final.set("17:00")
    elif current_from=="18:00":
        consulting_final.set("18:00")
    elif current_to=="19:00":
        consulting_final.set("19:00")
    else:
        consulting_final.set("20:00")

    #ZOOM ID
    add_zoom= Label(main_frame, text="ZOOM ID:", fg="#ffffff", bg="#272727")
    add_zoom.place(x=0, y=350)
    add_zoom_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_zoom_box.place(x=100, y=350) 
    add_zoom_box.insert(0, current_zoom)
    #Class 
    area=StringVar()
    area.set("")
    add_area= Label(main_frame, text="Class area:", fg="#ffffff", bg="#272727")
    add_area.place(x=0, y=400)
    add_area_select=OptionMenu(main_frame, area, "Human Studies", "Exact Sciences", "Computer Sciences", "Arts", "Other")
    add_area_select.config(bg="#272727", width=16, fg="#ffffff")
    add_area_select.place(x=100, y=395) 
    if current_area=="Human Studies":
        area.set("Human Studies")
    elif current_area=="Exact Sciences":
        area.set("Exact Sciences")
    elif current_area=="Computer Sciences":
        area.set("Computer Sciences")
    elif current_area=="Arts":
        area.set("Arts")
    elif current_area=="Other":
        area.set("Other")
    #Class is Active
    class_is_active=IntVar()
    add_active_team=Label(main_frame, text="Is this class currently active:", fg="#ffffff", bg="#272727")
    add_active_team.place(x=0, y=450)
    add_active_class_button=Radiobutton(main_frame, text="YES",variable=class_is_active, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_active_class_button.place(x=200, y=450)
    add_inactive_class_button=Radiobutton(main_frame, text="NO",variable=class_is_active, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_inactive_class_button.place(x=300, y=450)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=190, y=440)
    if current_is_class_active=="YES":
        add_active_class_button.select()
    else:
        add_inactive_class_button.select()

    #ACTUALLY ADD THE TEACHER TO THE DATABASE
    add_teacher_to_database=Button(main_frame, text="Update Entry", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:update_teacher(
        current,
        add_name_box.get(),
        add_mail_box.get(),
        add_remind_box.get(),
        add_phone_box.get(),
        str(consulting_day.get()),
        str(consulting_initial.get()),
        str(consulting_final.get()),
        add_zoom_box.get(),
        str(area.get()),
        int(class_is_active.get())
         ))
    add_teacher_to_database.place(x=410, y=410)

def delete_teacher(number):
    c=base.cursor()
    c.execute("SELECT *, oid FROM teachers")
    teachers = c.fetchall()
    delete_name=str(teachers[number][0])
    delete_teacher_message="You are about to delete the entry for "+delete_name+", are you sure you want to delete the information for this teacher?"
    delete_teacher=messagebox.askyesno("ARE YOU SURE?", delete_teacher_message)
    if delete_teacher==1:
        for i in range(len(teachers)):
            to_change=(teachers[i][-1])
            c.execute("UPDATE teachers SET ROWID=? WHERE ROWID=?",(i, to_change))
        c.execute("DELETE FROM teachers WHERE ROWID=?", (number,))
        base.commit()
    show_teachers()

def send_mail(mail,subject,message):
    mensaje_auto="" #Write a custom message you want every email to contain at the end
    message=message+mensaje_auto
    msg=MIMEMultipart()
    msg['From']='YOUR_EMAIL@gmail.com' #Insert your email here
    msg['To']=mail
    msg['Subject']=subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('YOUR_EMAIL@gmail.com', 'YOUR_PASSWORD_HERE') #Insert your email follower by your password
        server.ehlo()
        sender = "YOUR_EMAIL@gmail.com" #Insert your email here
        sub = subject
        server.sendmail(sender, mail, msg.as_string())
        server.close()
    except:
        mail_error=messagebox.showerror("ERROR", "Unable to send message, make sure: \n1.\tYou have a stable internet connection\n2.\tThe contact information is correct (either teacher mail or student ID)\n3.\tYou are logged in correctly")
    if mail[:2]=="A0":
        show_students()
    else:
        show_teachers()
def contact_teacher(number):
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    font_titulo=tkFont.Font(family="Lucida Grande", size=20)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    c=base.cursor()
    c.execute("SELECT *, oid FROM teachers")
    teachers = c.fetchall()
    contact_name=str(teachers[number][0])
    contact_mail=str(teachers[number][1])
    contact_remind=str(teachers[number][2])
    title="Contact "+contact_name
    title_text= Label(main_frame, text=title, fg="#ffffff", bg="#272727", font=font_titulo)
    title_text.place(anchor=CENTER, x=575, y=50)
    subject_text= Label(main_frame, text="Subject:", fg="#ffffff", bg="#272727", font=font_chido)
    subject_text.place(x=10, y=100)
    subject_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0, font=font_chido)
    subject_box.place(x=100, y=95, height=40) 
    main_text= Label(main_frame, text="Message:", fg="#ffffff", bg="#272727", font=font_chido)
    main_text.place(x=10, y=150)
    main_box=Text(main_frame, width=161, bg="#2E2E2E", fg="#ffffff", borderwidth=0, font=font_submit)
    main_box.place(x=10, y=350, height=300, anchor=W) 

    add_teacher_to_database=Button(main_frame, text="Send", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:send_mail(
        contact_mail,
        subject_box.get(),
        main_box.get(1.0, END)
         ))
    add_teacher_to_database.place(x=500, y=520)


def show_teachers():
    font_chido=tkFont.Font(family="Lucida Grande", size=10)
    page=1
    #TEACHER INFO
    edit_image=Image.open("edit.png")
    edit_image=edit_image.resize((30,30), Image.ANTIALIAS)
    edit_pencil=ImageTk.PhotoImage(edit_image)
    contact_image=Image.open("contact.png")
    contact_image=contact_image.resize((30,30), Image.ANTIALIAS)
    contact_envelope=ImageTk.PhotoImage(contact_image)
    delete_image=Image.open("delete.png")
    delete_image=delete_image.resize((30,30), Image.ANTIALIAS)
    delete_trash=ImageTk.PhotoImage(delete_image)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)


    

    #Data labels
    title_name=Label(main_frame, text="Name", fg="#ffffff", bg="#272727")
    title_name.place(x=0, y=0)
    title_mail=Label(main_frame, text="Mail", fg="#ffffff", bg="#272727")
    title_mail.place(x=200, y=0)
    title_remind=Label(main_frame, text="Remind", fg="#ffffff", bg="#272727")
    title_remind.place(x=365, y=0)
    title_phone=Label(main_frame, text="Phone", fg="#ffffff", bg="#272727")
    title_phone.place(x=450, y=0)
    title_consulting=Label(main_frame, text="Consulting", fg="#ffffff", bg="#272727")
    title_consulting.place(x=550, y=0)
    title_consulting=Label(main_frame, text="ZOOM CODE", fg="#ffffff", bg="#272727")
    title_consulting.place(x=750, y=0)
    title_area=Label(main_frame, text="Area", fg="#ffffff", bg="#272727")
    title_area.place(x=900, y=0)

    #Display the actual teacher data
    c=base.cursor()
    c.execute("SELECT *, oid FROM teachers")
    teachers = c.fetchall()
    names_text=""
    mail_text=""
    remind_text=""
    phone_text=""
    consulting_text=""
    zoom_text=""
    area_text=""
    y_position=50
    number_of_teachers=0
    zoom_links=[]
    num_teachers=len(teachers)


    main_canvas=Canvas(main_frame, width=1150, height=num_teachers*65, bg="#272727", borderwidth=0, highlightbackground="#272727")
    main_canvas.place(x=0,y=30)

    scroller=ttk.Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    scroller.place(x=1200, y=250)


    second_frame=Frame(main_canvas, width=1150, height=num_teachers*65, bg="#272727", borderwidth=0,highlightbackground="#272727")#####################
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    main_frame.config(borderwidth=0)
    main_frame.update()
    root.update()
    main_canvas.update()
    for record in teachers:
        names_text+=str(record[0])+"\n\n\n\n"
        mail_text+=str(record[1])+"\n\n\n\n"
        remind_text+=str(record[2])+"\n\n\n\n"
        phone_text+=str(record[3])+"\n\n\n\n"
        consulting_text+=str(record[4])+"\n\n\n\n"
        #zoom_text+=str(record[5])+"\n\n\n\n"
        zoom_links.append(str(record[5]))
        area_text+=str(record[6])+"\n\n\n\n"      
        teacher_names=Label(second_frame, text=names_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_names.place(x=0,y=0)
        teacher_mail=Label(second_frame, text=mail_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_mail.place(x=200,y=0)
        teacher_remind=Label(second_frame, text=remind_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_remind.place(x=365,y=0)
        teacher_phone=Label(second_frame, text=phone_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_phone.place(x=450,y=0)
        teacher_consulting=Label(second_frame, text=consulting_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_consulting.place(x=550,y=0)
        #teacher_zoom=Label(main_frame, text=zoom_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        #teacher_zoom.place(x=750,y=50)
        teacher_area=Label(second_frame, text=area_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_area.place(x=900,y=0)
        y_position+=50
        number_of_teachers+=1
    list_of_buttons=[]
    list_of_contact_buttons=[]
    list_of_delete_buttons=[]
    list_of_zoom_buttons=[]
    for i in range (number_of_teachers):
        new_button=Button(second_frame, text="", image=edit_pencil, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: edit_teacher(i), anchor=CENTER)
        new_button.image=edit_pencil
        new_button.place(x=1025, y=(i)*60)
        list_of_buttons.append(new_button)
        new_button_contact=Button(second_frame, text="", image=contact_envelope, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: contact_teacher(i), anchor=CENTER)
        new_button_contact.image=contact_envelope
        new_button_contact.place(x=1065, y=(i)*60)
        list_of_contact_buttons.append(new_button_contact)
        new_button_delete=Button(second_frame, text="", image=delete_trash, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: delete_teacher(i), anchor=CENTER)
        new_button_delete.image=delete_trash
        new_button_delete.place(x=1105, y=(i)*60)
        list_of_delete_buttons.append(new_button_delete)
        if not(zoom_links[i]=="" or zoom_links[i]==" "):
            current_link=str(zoom_links[i])
            zoom_button=Button(second_frame, text=current_link, fg="#ffffff", bg="#272727", justify=LEFT, activebackground="#141414", command=lambda current_link=current_link :zoom_login(current_link), borderwidth=0, anchor=CENTER)
            zoom_button.place(x=750, y=(i)*60)
            list_of_zoom_buttons.append(zoom_button)
    main_canvas.configure(yscrollcommand=scroller.set)
    main_canvas.bind('<Configure>', lambda e:main_canvas.configure(scrollregion=main_canvas.bbox("all")))


    
#Aqui termina show_teachers

def teacher_to_database(name, mail, remind, phone, day, i_time, f_time, zoom, area, active):
    data_name=str(name)
    data_mail=str(mail)
    data_remind=str(remind)
    data_phone=str(phone)
    if not (i_time=="" or f_time==""):
        data_consulting=day+" from "+i_time+" to "+f_time
    else:
        data_consulting=""
    data_zoom=str(zoom)
    data_area=str(area)
    if data_remind=="@":
        data_remind=""
    if data_consulting==" from to ":
        data_consulting=""
    if data_area=="" or data_area==" ":
        data_area="Other"
    data_active=""
    name_exists=True
    if active==0:
        data_active="YES"
    else:
        data_active="NO"

    if data_name=="":
        name_exists = False
        no_name=messagebox.showerror("NO NAME GIVEN", "The submission was unable to be completed because there is no NAME given")
    if name_exists:
        c=base.cursor()
        c.execute("INSERT INTO teachers VALUES (:name, :mail, :remind, :phone, :consulting, :zoom, :area, :active)",
        {
            'name':data_name,
            'mail':data_mail,
            'remind':data_remind,
            'phone':data_phone,
            'consulting':data_consulting,
            'zoom':data_zoom,
            'area':data_area,
            'active':data_active

        })
        base.commit()
        add_teacher()


#Add Teachers Info
def add_teacher():
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)

    teacher_or_student=IntVar()
    #Type of Person: Student or Teacher
    add_type=Label(main_frame, text="Type of Person:", fg="#ffffff", bg="#272727")
    add_type.place(x=0, y=50)
    add_type_button_teacher=Radiobutton(main_frame, text="Teacher",variable=teacher_or_student, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727", command=add_teacher)
    add_type_button_teacher.place(x=100, y=50)
    add_type_button_student=Radiobutton(main_frame, text="Student",variable=teacher_or_student, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=200, y=50)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=90, y=40)
    add_type_button_teacher.config(state=DISABLED)
    add_type_button_student.config(state=DISABLED)
    #Name
    add_name= Label(main_frame, text="Full Name:", fg="#ffffff", bg="#272727")
    add_name.place(x=0, y=100)
    add_name_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_name_star.place(x=90, y=90)
    add_name_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_name_box.place(x=100, y=100)
    #E-Mail
    add_mail= Label(main_frame, text="E-Mail Adress:", fg="#ffffff", bg="#272727")
    add_mail.place(x=0, y=150)
    add_mail_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_mail_box.place(x=100, y=150) 
    #Remind
    add_remind= Label(main_frame, text="Remind Code:", fg="#ffffff", bg="#272727")
    add_remind.place(x=0, y=200)
    add_remind_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_remind_box.place(x=100, y=200) 
    add_remind_box.insert(0, "@")
    #Phone Number
    add_phone= Label(main_frame, text="Phone Number:", fg="#ffffff", bg="#272727")
    add_phone.place(x=0, y=250)
    add_phone_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_phone_box.place(x=100, y=250)
    #Horas de asesorias
    consulting_day=StringVar()
    consulting_day.set("")
    consulting_initial=StringVar()
    consulting_initial.set("")
    consulting_final=StringVar()
    consulting_final.set("")
    add_consulting= Label(main_frame, text="Office Hours:", fg="#ffffff", bg="#272727")
    add_consulting.place(x=0, y=300)
    add_day_consulting=Label(main_frame, text="Day: ", fg="#ffffff", bg="#272727")
    add_day_consulting.place(x=100, y=300) 
    add_day_select=OptionMenu(main_frame, consulting_day, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
    add_day_select.config(bg="#272727", width=10, fg="#ffffff")
    add_day_select.place(x=140, y=295) 
    add_initial_time_consulting=Label(main_frame, text="From", fg="#ffffff", bg="#272727")
    add_initial_time_consulting.place(x=260, y=300) 
    add_initial_hour_select=OptionMenu(main_frame, consulting_initial, "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00") #Hora
    add_initial_hour_select.config(bg="#272727", width=6, fg="#ffffff")
    add_initial_hour_select.place(x=300, y=295) 
    add_final_time_consulting=Label(main_frame, text="To", fg="#ffffff", bg="#272727")
    add_final_time_consulting.place(x=400, y=300) 
    add_final_hour_select=OptionMenu(main_frame, consulting_final, "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00") #Hora 2
    add_final_hour_select.config(bg="#272727", width=6, fg="#ffffff")
    add_final_hour_select.place(x=440,y=295)
    #ZOOM ID
    add_zoom= Label(main_frame, text="ZOOM ID:", fg="#ffffff", bg="#272727")
    add_zoom.place(x=0, y=350)
    add_zoom_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_zoom_box.place(x=100, y=350) 
    #Class 
    area=StringVar()
    area.set("")
    add_area= Label(main_frame, text="Class area:", fg="#ffffff", bg="#272727")
    add_area.place(x=0, y=400)
    add_area_select=OptionMenu(main_frame, area, "Human Studies", "Exact Sciences", "Computer Sciences", "Arts", "Other")
    add_area_select.config(bg="#272727", width=16, fg="#ffffff")
    add_area_select.place(x=100, y=395) 
    #Class is Active
    class_is_active=IntVar()
    add_active_team=Label(main_frame, text="Is this class currently active:", fg="#ffffff", bg="#272727")
    add_active_team.place(x=0, y=450)
    add_type_button_teacher=Radiobutton(main_frame, text="YES",variable=class_is_active, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_teacher.place(x=200, y=450)
    add_type_button_student=Radiobutton(main_frame, text="NO",variable=class_is_active, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=300, y=450)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=190, y=440)
    #ACTUALLY ADD THE TEACHER TO THE DATABASE
    add_teacher_to_database=Button(main_frame, text="Submit Entry", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:teacher_to_database(
        add_name_box.get(),
        add_mail_box.get(),
        add_remind_box.get(),
        add_phone_box.get(),
        str(consulting_day.get()),
        str(consulting_initial.get()),
        str(consulting_final.get()),
        add_zoom_box.get(),
        str(area.get()),
        int(class_is_active.get())
         ))
    add_teacher_to_database.place(x=410, y=410)
    

##########################################################################################students######################################################################
def update_student(current, name, student_id, username, phone, active_team):
    name_exists=True
    id_exists=False
    if name=="":
        name_exists = False
        no_name=messagebox.showerror("NO NAME GIVEN", "The submission was unable to be completed because there is no NAME given")
    else:
        name_exists=True

    if student_id=="":
        id_exists=False
        no_nid=messagebox.showerror("NO STUDENT ID GIVEN", "The submission was unable to be completed because there is no STUDENT ID given")
    else:
        id_exists = True
    if id_exists and name_exists:
        c=base.cursor()
        in_active_team=""
        if active_team==0:
            in_active_team="YES"
        else:
            in_active_team="NO"
        new_name=(str(name), current+1)
        c.execute("""Update students set name=? where ROWID=?""", new_name)
        base.commit()
        new_id=(str(student_id), current+1)
        c.execute("""Update students set id=? where ROWID=?""", new_id)
        base.commit()
        new_username=(str(username), current+1)
        c.execute("""Update students set username=? where ROWID=?""", new_username)
        base.commit()
        new_phone=(str(phone), current+1)
        c.execute("""Update students set phone=? where ROWID=?""", new_phone)
        base.commit()
        new_active_team=(in_active_team, current+1)
        c.execute("""Update students set active_team=? where ROWID=?""", new_active_team)
        base.commit()
        edit_student(current)


def edit_student(number):
    current= number
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)

    c=base.cursor()
    c.execute("SELECT *, oid FROM students")
    students = c.fetchall()
    current_name=str(students[current][0])
    current_id=str(students[current][1])
    current_username=str(students[current][2])
    current_phone=str(students[current][3])
    current_active_team=str(students[current][4])
    teacher_or_student=IntVar()
    #Type of Person: Student or Teacher
    add_type=Label(main_frame, text="Type of Person:", fg="#ffffff", bg="#272727")
    add_type.place(x=0, y=50)
    add_type_button_teacher=Radiobutton(main_frame, text="Teacher",variable=teacher_or_student, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_teacher.place(x=100, y=50)
    add_type_button_student=Radiobutton(main_frame, text="Student",variable=teacher_or_student, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=200, y=50)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=90, y=40)
    add_type_button_teacher.config(state=DISABLED)
    add_type_button_student.config(state=DISABLED)
    #Name
    add_name= Label(main_frame, text="Full Name:", fg="#ffffff", bg="#272727")
    add_name.place(x=0, y=100)
    add_name_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_name_star.place(x=90, y=90)
    add_name_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_name_box.place(x=100, y=100)
    add_name_box.insert(0, current_name)
    #Student ID
    add_id= Label(main_frame, text="Student ID:", fg="#ffffff", bg="#272727")
    add_id.place(x=0, y=150)
    add_id_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_id_star.place(x=90, y=140)
    add_id_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_id_box.place(x=100, y=150)
    add_id_box.insert(0, current_id)
    #Phone Number
    add_phone= Label(main_frame, text="Phone Number:", fg="#ffffff", bg="#272727")
    add_phone.place(x=0, y=200)
    add_phone_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_phone_box.place(x=100, y=200)
    add_phone_box.insert(0, current_phone)
    #GamerTag/Username
    add_username= Label(main_frame, text="Gamertag:", fg="#ffffff", bg="#272727")
    add_username.place(x=0, y=250)
    add_username_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_username_box.place(x=100, y=250) 
    add_username_box.insert(0, current_username)
    #In Active team
    in_active_team=IntVar()
    add_active_team=Label(main_frame, text="Is in an active team:", fg="#ffffff", bg="#272727")
    add_active_team.place(x=0, y=300)
    add_active_team_button=Radiobutton(main_frame, text="YES",variable=in_active_team, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_active_team_button.place(x=150, y=300)
    add_inactive_team_button=Radiobutton(main_frame, text="NO",variable=in_active_team, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_inactive_team_button.place(x=250, y=300)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=140, y=290)
    if current_active_team=="YES":
        add_active_team_button.select()
    else:
       add_inactive_team_button.select()
    add_student_to_database=Button(main_frame, text="Update Entry", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:update_student(
        current,
        add_name_box.get(),
        add_id_box.get(),
        add_username_box.get(),
        add_phone_box.get(),
        int(in_active_team.get())
         ))
    add_student_to_database.place(x=410, y=300)

def delete_student(number):
    c=base.cursor()
    c.execute("SELECT *, oid FROM students")
    students = c.fetchall()
    delete_name=str(students[number][0])
    delete_students_message="You are about to delete the entry for "+delete_name+", are you sure you want to delete the information for this student?"
    delete_students=messagebox.askyesno("ARE YOU SURE?", delete_students_message)
    if delete_students==1:
        for i in range(len(students)):
            to_change=(students[i][5])
            c.execute("UPDATE students SET ROWID=? WHERE ROWID=?",(i, to_change))
        c.execute("DELETE FROM students WHERE ROWID=?", (number,))
        base.commit()
    show_students()

def contact_student(number):
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    font_titulo=tkFont.Font(family="Lucida Grande", size=20)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    c=base.cursor()
    c.execute("SELECT *, oid FROM students")
    teachers = c.fetchall()
    contact_name=str(teachers[number][0])
    contact_mail=str(teachers[number][1])+"@itesm.mx"
    title="Contact "+contact_name
    title_text= Label(main_frame, text=title, fg="#ffffff", bg="#272727", font=font_titulo)
    title_text.place(anchor=CENTER, x=575, y=50)
    subject_text= Label(main_frame, text="Subject:", fg="#ffffff", bg="#272727", font=font_chido)
    subject_text.place(x=10, y=100)
    subject_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0, font=font_chido)
    subject_box.place(x=100, y=95, height=40) 
    main_text= Label(main_frame, text="Message:", fg="#ffffff", bg="#272727", font=font_chido)
    main_text.place(x=10, y=150)
    main_box=Text(main_frame, width=161, bg="#2E2E2E", fg="#ffffff", borderwidth=0, font=font_submit)
    main_box.place(x=10, y=350, height=300, anchor=W) 

    send_mail_button=Button(main_frame, text="Send", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:send_mail(
        contact_mail,
        subject_box.get(),
        main_box.get(1.0, END)
         ))
    send_mail_button.place(x=500, y=520)

def show_students():
    edit_image=Image.open("edit.png")
    edit_image=edit_image.resize((30,30), Image.ANTIALIAS)
    edit_pencil=ImageTk.PhotoImage(edit_image)
    contact_image=Image.open("contact.png")
    contact_image=contact_image.resize((30,30), Image.ANTIALIAS)
    contact_envelope=ImageTk.PhotoImage(contact_image)
    delete_image=Image.open("delete.png")
    delete_image=delete_image.resize((30,30), Image.ANTIALIAS)
    delete_trash=ImageTk.PhotoImage(delete_image)

    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    title_name=Label(main_frame, text="Name", fg="#ffffff", bg="#272727")
    title_name.place(x=0, y=0)
    title_mail=Label(main_frame, text="Student ID", fg="#ffffff", bg="#272727")
    title_mail.place(x=250, y=0)
    title_remind=Label(main_frame, text="GamerTag", fg="#ffffff", bg="#272727")
    title_remind.place(x=450, y=0)
    title_phone=Label(main_frame, text="Phone", fg="#ffffff", bg="#272727")
    title_phone.place(x=650, y=0)

    #Display the actual student data
    c=base.cursor()
    c.execute("SELECT *, oid FROM students")
    students = c.fetchall()
    names_text=""
    id_text=""
    phone_text=""
    username_text=""
    y_position=50
    number_of_students=0

    num_students=len(students)


    main_canvas=Canvas(main_frame, width=1150, height=600, bg="#272727", borderwidth=0, highlightbackground="#272727")
    main_canvas.place(x=0,y=30)

    scroller=ttk.Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    scroller.place(x=1200, y=250)


    second_frame=Frame(main_canvas, width=1150, height=num_students*65, bg="#272727", borderwidth=0,highlightbackground="#272727")#####################
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    main_frame.config(borderwidth=0)
    main_frame.update()
    root.update()



    for record in students:
        names_text+=str(record[0])+"\n\n\n\n"
        id_text+=str(record[1])+"\n\n\n\n"
        username_text+=str(record[2])+"\n\n\n\n"
        phone_text+=str(record[3])+"\n\n\n\n"   
        teacher_names=Label(second_frame, text=names_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_names.place(x=0,y=0)
        teacher_mail=Label(second_frame, text=id_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_mail.place(x=250,y=0)
        teacher_remind=Label(second_frame, text=username_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_remind.place(x=450,y=0)
        teacher_phone=Label(second_frame, text=phone_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        teacher_phone.place(x=650,y=0)
        number_of_students+=1
    list_of_edit_buttons=[]
    list_of_contact_buttons=[]
    list_of_delete_buttons=[]
    for i in range (number_of_students):
        new_button=Button(second_frame, text="", image=edit_pencil, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: edit_student(i), anchor=CENTER)
        new_button.image=edit_pencil
        new_button.place(x=775, y=(i)*58)
        list_of_edit_buttons.append(new_button)
        new_button_contact=Button(second_frame, text="", image=contact_envelope, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: contact_student(i), anchor=CENTER)
        new_button_contact.image=contact_envelope
        new_button_contact.place(x=825, y=(i)*58)
        list_of_contact_buttons.append(new_button_contact)
        new_button_delete=Button(second_frame, text="", image=delete_trash, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: delete_student(i), anchor=CENTER)
        new_button_delete.image=delete_trash
        new_button_delete.place(x=875, y=(i)*58)
        list_of_delete_buttons.append(new_button_delete)
    main_canvas.configure(yscrollcommand=scroller.set)
    main_canvas.bind('<Configure>', lambda e:main_canvas.configure(scrollregion=main_canvas.bbox("all")))

#Aqui termina show_students

def students_to_database(name, student_id, username, phone, active_team):
    data_name=str(name)
    data_id=str(student_id)
    data_username=str(username)
    data_phone=str(phone)
    data_active=""
    name_exists=True
    id_exists = True
    if active_team==0:
        data_active="YES"
    else:
        data_active="NO"

    if data_name=="":
        name_exists = False
        no_name=messagebox.showerror("NO NAME GIVEN", "The submission was unable to be completed because there is no NAME given")
    if data_id=="":
        id_exists=False
        no_nid=messagebox.showerror("NO STUDENT ID GIVEN", "The submission was unable to be completed because there is no STUDENT ID given")
    if name_exists and id_exists:
        c=base.cursor()
        c.execute("INSERT INTO students VALUES (:name, :id, :username, :phone, :active_team)",
        {
            'name':data_name,
            'id':data_id,
            'username':data_username,
            'phone':data_phone,
            'active_team':data_active

        })
        base.commit()
        add_student()

def add_student():
    font_submit=tkFont.Font(family="Lucida Grande", size=10)
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)

    teacher_or_student=IntVar()
    #Type of Person: Student or Teacher
    add_type=Label(main_frame, text="Type of Person:", fg="#ffffff", bg="#272727")
    add_type.place(x=0, y=50)
    add_type_button_teacher=Radiobutton(main_frame, text="Teacher",variable=teacher_or_student, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_teacher.place(x=100, y=50)
    add_type_button_student=Radiobutton(main_frame, text="Student",variable=teacher_or_student, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=200, y=50)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=90, y=40)
    add_type_button_teacher.config(state=DISABLED)
    add_type_button_student.config(state=DISABLED)
    #Name
    add_name= Label(main_frame, text="Full Name:", fg="#ffffff", bg="#272727")
    add_name.place(x=0, y=100)
    add_name_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_name_star.place(x=90, y=90)
    add_name_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_name_box.place(x=100, y=100)
    #Student ID
    add_id= Label(main_frame, text="Student ID:", fg="#ffffff", bg="#272727")
    add_id.place(x=0, y=150)
    add_id_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_id_star.place(x=90, y=140)
    add_id_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_id_box.place(x=100, y=150)
    #Phone Number
    add_phone= Label(main_frame, text="Phone Number:", fg="#ffffff", bg="#272727")
    add_phone.place(x=0, y=200)
    add_phone_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_phone_box.place(x=100, y=200)
    #GamerTag/Username
    add_username= Label(main_frame, text="Gamertag:", fg="#ffffff", bg="#272727")
    add_username.place(x=0, y=250)
    add_username_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_username_box.place(x=100, y=250) 
    #In Active team
    in_active_team=IntVar()
    add_active_team=Label(main_frame, text="Is in an active team:", fg="#ffffff", bg="#272727")
    add_active_team.place(x=0, y=300)
    add_type_button_teacher=Radiobutton(main_frame, text="YES",variable=in_active_team, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_teacher.place(x=150, y=300)
    add_type_button_student=Radiobutton(main_frame, text="NO",variable=in_active_team, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727")
    add_type_button_student.place(x=250, y=300)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=140, y=290)
    add_student_to_database=Button(main_frame, text="Submit Entry", fg="#000000", bg="#00B8D9", font=font_submit, activebackground=("#199db5"), width=20, height=3, command=lambda:students_to_database(
        add_name_box.get(),
        add_id_box.get(),
        add_username_box.get(),
        add_phone_box.get(),
        int(in_active_team.get())
         ))
    add_student_to_database.place(x=410, y=300)

#Funcion add_person
def add_person():
    cover_up=Label(root, text="", bg="#212121", width=250, height=3)
    cover_up.place(x=0, y=85)
    font_chido=tkFont.Font(family="Lucida Grande", size=10)
    font_add_task=tkFont.Font(family="Lucida Grande", size=10)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)

    teacher_or_student=IntVar()
    #Type of Person: Student or Teacher
    add_type=Label(main_frame, text="Type of Person:", fg="#ffffff", bg="#272727")
    add_type.place(x=0, y=50)
    add_type_button_teacher=Radiobutton(main_frame, text="Teacher",variable=teacher_or_student, value=0, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727", command=add_teacher)
    add_type_button_teacher.place(x=100, y=50)
    add_type_button_student=Radiobutton(main_frame, text="Student",variable=teacher_or_student, value=1, fg="#ffffff", bg="#272727", selectcolor="#292929", activebackground="#272727", command=add_student)
    add_type_button_student.place(x=200, y=50)
    add_type_star=Label(main_frame, text="*", fg="#FF5630", bg="#272727", font=font_chido)
    add_type_star.place(x=90, y=40)

def add_task(task):
    max_id=0
    task_exists=True
    if task=="":
        task_exists = False
        no_name=messagebox.showerror("NO NAME GIVEN", "The submission was unable to be completed because there is no NAME given")
    c=base.cursor()
    c.execute("SELECT *, oid FROM tasks")
    all_tasks = c.fetchall()
    task_number=0
    max_variable=""
    for i in range(len(all_tasks)):
        to_change=(all_tasks[i][3])
        c.execute("UPDATE tasks SET ROWID=? WHERE ROWID=?",(i, to_change))
        base.commit()
    if task_exists:
        if len(all_tasks)==0:
            max_variable=1
        else:
            max_variabel=int(all_tasks[len(all_tasks)-1][3])+1
        c=base.cursor()
        c.execute("INSERT INTO tasks VALUES (:task, :completed, :original_id)",
        {
            'task':task,
            'completed':"NO",
            'original_id':max_variable
        })
        base.commit()
    show_to_do()

def change_task(number_of_task):
    c=base.cursor()
    c.execute("SELECT *, oid FROM tasks")
    all_tasks = c.fetchall()
    for i in range(len(all_tasks)):
        to_change=(all_tasks[i][3])
        c.execute("UPDATE tasks SET ROWID=? WHERE ROWID=?",(i, to_change))
        base.commit()
    current_value=str(all_tasks[number_of_task][1])
    if current_value=="NO":
        c.execute("UPDATE tasks SET completed=? WHERE ROWID=?",("YES", number_of_task))
        base.commit()
    else:
        c.execute("UPDATE tasks SET completed=? WHERE ROWID=?",("NO", number_of_task))
        base.commit()
    show_to_do()

def delete_task(number_of_task):
    c=base.cursor()
    c.execute("SELECT *, oid FROM tasks")
    all_tasks = c.fetchall()
    delete_name=str(all_tasks[number_of_task][0])
    delete_task_message="You are about to delete the following task:\n"+delete_name+"\nAre you sure you want to delete this task?"
    delete_task=messagebox.askyesno("ARE YOU SURE?", delete_task_message)
    if delete_task==1:
        for i in range(len(all_tasks)):
            to_change=(all_tasks[i][3])
            c.execute("UPDATE tasks SET ROWID=? WHERE ROWID=?",(i, to_change))
        c.execute("DELETE FROM tasks WHERE ROWID=?", (number_of_task,))
        base.commit()
    show_to_do()

def show_to_do():
    cover_up=Label(root, text="", bg="#212121", width=250, height=3)
    cover_up.place(x=0, y=85)
    completed_image=Image.open("completed.png")
    completed_image=completed_image.resize((30,30), Image.ANTIALIAS)
    completed_check=ImageTk.PhotoImage(completed_image)
    incomplete_image=Image.open("incomplete.png")
    incomplete_image=incomplete_image.resize((30,30), Image.ANTIALIAS)
    incomplete_x=ImageTk.PhotoImage(incomplete_image)
    delete_image=Image.open("delete.png")
    delete_image=delete_image.resize((30,30), Image.ANTIALIAS)
    delete_trash=ImageTk.PhotoImage(delete_image)

    #Create add_task
    font_chido=tkFont.Font(family="Lucida Grande", size=10)
    font_add_task=tkFont.Font(family="Lucida Grande", size=10)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    add_task_text=Label(main_frame, text="New task: ", fg="#00B8D9", bg="#272727", font=font_chido)
    add_task_text.place(x=0, y=550)
    add_task_box=Entry(main_frame, width=80, bg="#2E2E2E", fg="#ffffff", borderwidth=0)
    add_task_box.place(x=70, y=555)
    add_task_button=Button(main_frame, text="Add Task", fg="#000000", bg="#00B8D9", font=font_add_task, activebackground=("#199db5"), width=10, command=lambda: add_task(str(add_task_box.get())))
    add_task_button.place(x=575, y=550)


    c=base.cursor()
    c.execute("SELECT *, oid FROM tasks")
    all_tasks = c.fetchall()
    num_tasks=len(all_tasks)

    main_canvas=Canvas(main_frame, width=1150, height=530, bg="#272727", borderwidth=0, highlightbackground="#272727")
    main_canvas.place(x=0,y=0)

    scroller=ttk.Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    scroller.place(x=1200, y=250)


    second_frame=Frame(main_canvas, width=1150, height=num_tasks*65, bg="#272727", borderwidth=0,highlightbackground="#272727")#####################
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    main_frame.config(borderwidth=0)
    main_frame.update()

    #Display tasks

    task_text=""
    for record in all_tasks:
        task_text+=str(record[0])+"\n\n\n\n"
        task_label=Label(second_frame, text=task_text, fg="#ffffff", bg="#272727", anchor="e", justify=LEFT)
        task_label.place(x=100,y=10)

    list_of_complete_buttons=[]
    list_of_delete_buttons=[]
    for i in range (len(all_tasks)):
        task_image=incomplete_x
        is_task_completed=all_tasks[i][1]
        if str(is_task_completed)=="NO":
            task_image=incomplete_x
        else:
            task_image=completed_check
        new_button=Button(second_frame, text="", image=task_image, bg="#272727", activebackground="#141414", borderwidth=0, command=lambda i=i: change_task(i), anchor=CENTER)
        new_button.image=task_image
        new_button.place(x=5, y=(i)*60)
        list_of_complete_buttons.append(new_button)
        new_delete_button=Button(second_frame, text="", image=delete_trash, bg="#666666", activebackground="#141414", borderwidth=0, command=lambda i=i: delete_task(i), anchor=CENTER)
        new_delete_button.image=delete_trash
        new_delete_button.place(x=55, y=(i)*60)
        list_of_delete_buttons.append(new_delete_button)

def show_home():
    font_chido=tkFont.Font(family="Lucida Grande", size=10)
    cover_up=Label(root, text="", bg="#212121", width=250, height=3)
    cover_up.place(x=0, y=85)
    #landing_image=Image.open("Landing_Page.png")
    landing_page=ImageTk.PhotoImage(Image.open("Landing_Page.png"))
    font_chido=tkFont.Font(family="Lucida Grande", size=15)
    show_text= Label(root, text="Developed by: Santiago Reyes", fg="#ffffff", bg="#212121", font=font_chido)
    show_text.grid(column=0, row=2, columnspan=4)
    show_text2= Label(root, text="", fg="#272727", bg="#212121")
    show_text2.grid(column=0, row=3)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    home_msg=Label(main_frame,image=landing_page, borderwidth=0)
    home_msg.image=landing_page
    home_msg.pack()


def what_to_show(type_of):
    if type_of=="Teachers":
        show_teachers()
    elif type_of=="Students":
        show_students()
    else:
        no_show=messagebox.showerror("NO TYPE OF CONTACT SELECTED", "Please select the type of contact you want to visualize from the dropdown menu")

def show_contacts():
    font_chido=tkFont.Font(family="Lucida Grande", size=10)
    font_add_task=tkFont.Font(family="Lucida Grande", size=10)
    main_frame=Frame(root, width=1225, height=600)
    main_frame.config(bg="#272727", borderwidth=0)
    main_frame.grid(column=0,columnspan=4, row=4, pady=15)
    type_of_contact=StringVar()
    type_of_contact.set("Teachers")
    type_of_filter=StringVar()
    type_of_filter.set("None")
    cover_up=Label(root, text="", bg="#212121", width=250, height=3)
    cover_up.place(x=0, y=85)
    show_type= Label(root, text="Show:", fg="#ffffff", bg="#272727", anchor='e', font=font_chido)
    show_type.place(x=50, y=100)
    select_type=OptionMenu(root, type_of_contact, "Teachers", "Students")
    select_type.config(bg="#272727", width=10, fg="#ffffff", anchor='w')
    select_type.place(x=120, y=95)
    """
    show_text= Label(root, text="Filter:", fg="#ffffff", bg="#272727", anchor='e', font=font_chido)
    show_text.place(x=300, y=100)
    select_filter=OptionMenu(root, type_of_filter, "None", "Active Classes", "By name", "By area")
    select_filter.config(bg="#272727", width=10, fg="#ffffff")
    select_filter.place(x=350, y=95
    """
    search_contacts_button=Button(root, font=font_chido, width=10, text="SEARCH",fg="#000000", bg="#00B8D9", command=lambda:what_to_show(str(type_of_contact.get())))
    search_contacts_button.place(x=250, y=97)


#############  MAIN  #################
font_chido=tkFont.Font(family="Lucida Grande", size=15)
#current_teachers=Button(root, text="Teachers", fg="#0A030D", bg="#C495FD", font=font_chido, activebackground=("#a582cf"), width=20, command=show_teachers)
#current_teachers.grid(column=0, row=0, pady=20,padx=5)
home=Button(root, text="Home", fg="#0A030D", bg="#C495FD", font=font_chido, activebackground=("#a582cf"), width=20, command=show_home)
home.grid(column=0, row=0, pady=20,padx=5)
current_students=Button(root, text="Contacts", fg="#0A030D", bg="#F4A1BD", font=font_chido, activebackground=("#a582cf"), width=20, command=show_contacts)
current_students.grid(column=1, row=0, pady=20,padx=5)
plus_person=Button(root, text="Add Contact", fg="#0A030D", bg="#04D9C4", font=font_chido, activebackground=("#16c9b8"), width=20, command=add_person)
plus_person.grid(column=2, row=0, pady=20, padx=5)
contact=Button(root, text="To-Do List", fg="#0A030D", bg="#B2EE9F", font=font_chido, activebackground=("#91c282"), width=20, command=show_to_do)
contact.grid(column=3, row=0, pady=20,padx=5)
show_text= Label(root, text="", fg="#ffffff", bg="#212121")
show_text.grid(column=0, row=2, columnspan=4)
show_text2= Label(root, text="", fg="#ffffff", bg="#212121")
show_text2.grid(column=0, row=3)
main_frame=Frame(root, width=1225, height=600)
main_frame.config(bg="#272727", borderwidth=0)
main_frame.grid(column=0,columnspan=4, row=4, pady=15)
show_home()
root.mainloop()

