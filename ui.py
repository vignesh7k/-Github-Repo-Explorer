import tkinter as tk
from tkinter.constants import TOP
import ghex



def ent_email_btn1_click(event):
    if ent_email.get() == 'Email':
        ent_email.config(state=tk.NORMAL)
        ent_email.delete(0, tk.END)
    else:
        ent_email.config(state=tk.NORMAL)


def ent_ghurl_btn1_click(event):
    if url_entry_output.get() == 'Sample URL':
        ent_ghurl.config(state=tk.NORMAL)
        ent_ghurl.delete(0, tk.END)
    else:
        ent_ghurl.config(state=tk.NORMAL)


def ent_email_btn1_unclick(event):
    if ent_email.get() == '':
        ent_email.config(state=tk.NORMAL)
        ent_email.insert(0, 'Email')
        ent_email.config(state=tk.DISABLED)
    elif ent_email.get() == 'Email':
        ent_email.delete(0, tk.END)
        ent_email.config(state=tk.DISABLED)
    else:
        ent_email.config(state=tk.DISABLED)


def ent_ghurl_btn1_unclick(event):
    if ent_ghurl.get() == '':
        ent_ghurl.config(state=tk.NORMAL)
        ent_ghurl.insert(0, 'Sample URL')
        ent_ghurl.config(state=tk.DISABLED)
    elif ent_ghurl.get() == 'Sample URL':
        pass
        # ent_ghurl.delete(0, tk.END)
        # ent_ghurl.insert(0, 'Sample URL')
        ent_ghurl.config(state=tk.DISABLED)
    else:
        ent_ghurl.config(state=tk.DISABLED)


def display_output(output):
    txt_outputarea.configure(state='normal')
    txt_outputarea.delete('1.0', tk.END)
    txt_outputarea.insert(tk.END, output)
    txt_outputarea.configure(state='disabled')


def get_languages_used():
    ghurl = ent_ghurl.get()
    if not ghurl.startswith('https://github.com/'):
        # clear the outut area
        display_output("")
        return
    languages_used_list = ghex.get_languages_used(ghurl)
    languages_used_str = "\n".join(languages_used_list)
    display_output(languages_used_str)
    with open("lang_data.txt",'w')as f:
     f.write(languages_used_str)

def is_valid_ghurl(ghurl):
    if not ghurl.startswith('https://github.com/'):
        return False
    return True

def get_repo_stats():
    ghurl = ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("")
        return
    repo_stats = ghex.get_repo_stats(ghurl)
    display_output(repo_stats)
    with open("repo_data.txt",'w')as f:
     f.write(repo_stats)

def get_open_issues():
    ghurl = ent_ghurl.get()
    if not ghurl.startswith('https://github.com/'):
        display_output("ERROR: Invalid URL")
        return
    open_issues_list = ghex.get_open_issues(ghurl)
    open_issues_str ='\n'.join(open_issues_list)
    display_output(open_issues_str)
    with open("issue_data.txt",'w')as f:
     f.write(open_issues_str)

def get_open_prs():
    ghurl=ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("ERROR:Invalid URL")
        return
    pr_issues_list=ghex.get_open_pulls(ghurl) 
    pr_issues_str='\n'.join(pr_issues_list)
    display_output(pr_issues_str)
    with open("pr_data.txt",'w')as f:
     f.write(pr_issues_str)

def valid_email(email):
    if email == '' or email == 'Email' or '@' not in email:
        return False
    return True

def check(email):
    f=open("emails.txt",'r').readlines()
    seen = set(f)
    for line in f:
        lines_lower = line.lower()
        if lines_lower in seen:
            return True
        return False 


def subscribe_email():
    # Get the email address and store to a file
    email = ent_email.get()
    if not valid_email(email):
        display_output("Invalid Email")
        return
    ghex.save_email(email) 


def mail_data():
    ghex.send_mail(body= """this is a skillaura internship program !!.
                        he following mail consists information of a github repository.
                        Please refer to the below documents for more details""")
    

def subscribers():
    ghurl=ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("ERROR:Invalid URL")
        return
    subscriber_list=ghex.get_subscriber(ghurl)
    subscribers_str='\n'.join(subscriber_list)
    display_output(subscribers_str)
    with open("subscribers_data.txt",'w')as f:
     f.write(subscribers_str)


# Main Window
main_window = tk.Tk()

main_window.title("GitHub Repo Explorer")
main_window.resizable(600, 600)

# Frame for main Label
frm_ghurl = tk.LabelFrame(main_window, bg="Lavender",fg="black")  
frm_ghurl.pack(fill="both", expand="yes")

lbl_title = tk.Label(frm_ghurl, text="GitHub Repo Explorer", bg="Lavender",fg="OrangeRed", font='Helvetica 35 bold', width=50)
lbl_title.pack(side="top", fill="both", expand="yes")


lbl_ghurl = tk.Label(frm_ghurl, text='GitHub Repo URL',bg="Lavender", fg="black", font='Helvetica 20 bold', width=15)
lbl_ghurl.pack(side=tk.LEFT)


# URL Entry
url_entry_output = tk.StringVar()
ent_ghurl = tk.Entry(frm_ghurl, bg="AliceBlue", textvariable=url_entry_output,fg="black", font='Helvetica 20 ', width=72)
ent_ghurl.insert(0, 'Sample URL')
# ent_ghurl.config(state=tk.DISABLED)
ent_ghurl.bind("<Button-1>", ent_ghurl_btn1_click)
ent_ghurl.bind('<Leave>', ent_ghurl_btn1_unclick)
ent_ghurl.pack(side=tk.LEFT, padx=45, pady=5)

# Frame for buttons
frm_buttons = tk.LabelFrame(main_window,bg="Lavender", padx=15, pady=15)
frm_buttons.pack(side=tk.TOP, anchor=tk.W, fill="both", expand="yes")

# Buttons
btn_langused = tk.Button(frm_buttons, text='Languages Used',font='Helvetica 20 ', width=15, fg='blue', command=get_languages_used)
btn_langused.grid(row=0, column=0)

btn_repostats = tk.Button(frm_buttons, text='Repo Stats',font='Helvetica 20 ', width=15, fg='blue', command=get_repo_stats)
btn_repostats.grid(row=1, column=0)

btn_openissues = tk.Button(frm_buttons, text='Open Issues', font='Helvetica 20 ', width=15, fg='blue', command=get_open_issues)
btn_openissues.grid(row=2, column=0)

btn_openprs = tk.Button(frm_buttons, text='Open PRs',font='Helvetica 20 ', width=15, fg='blue', command=get_open_prs)
btn_openprs.grid(row=3, column=0)

btn_subscriber = tk.Button(frm_buttons, text='Subscribed Users', font='Helvetica 20 ', width=15, fg='blue', command=subscribers)
btn_subscriber.grid(row=4, column=0)

btn_langused.bind('<Motion>', lambda _: btn_langused.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_langused.bind('<Leave>', lambda _: btn_langused.config(bg='white', highlightbackground='white', fg='blue'))


btn_repostats.bind('<Motion>', lambda _: btn_repostats.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_repostats.bind('<Leave>', lambda _: btn_repostats.config(bg='white', highlightbackground='white', fg='blue'))

btn_openissues.bind('<Motion>', lambda _: btn_openissues.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_openissues.bind('<Leave>', lambda _: btn_openissues.config(bg='white', highlightbackground='white', fg='blue'))

btn_openprs.bind('<Motion>', lambda _: btn_openprs.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_openprs.bind('<Leave>', lambda _: btn_openprs.config(bg='white', highlightbackground='white', fg='blue'))

btn_subscriber.bind('<Motion>', lambda _: btn_subscriber.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_subscriber.bind('<Leave>', lambda _: btn_subscriber.config(bg='white', highlightbackground='white', fg='blue'))


# Nested Frame for text area i.e Output Layout

frm_outputarea = tk.LabelFrame(frm_buttons, bg="AliceBlue", padx=1, pady=2, width=150)
frm_outputarea.grid(row=0, column=1, rowspan=5, padx=8, pady=9)

# text area i.e Output Layout

txt_outputarea = tk.Text(frm_outputarea, bg='beige')
txt_outputarea.pack(side=tk.RIGHT, anchor=tk.E, expand=tk.YES)
txt_outputarea.configure(state='disabled')

# Frame for email Entry

frm_subscription = tk.LabelFrame(main_window, bg="Lavender", padx=9, pady=9)
frm_subscription.pack(fill="both", expand="yes")

# entry for email 

ent_email = tk.StringVar()
ent_email = tk.Entry(frm_subscription, bg="AliceBlue",textvariable=ent_email, fg="black", font='Helvetica 20', width=75)
ent_email.insert(0, 'Email')
ent_email.config(state=tk.DISABLED)
ent_email.bind("<Button-1>", ent_email_btn1_click)
ent_email.bind('<Leave>', ent_email_btn1_unclick)
ent_email.pack(side=tk.LEFT, padx=10)

# button for subscription

btn_subscribe = tk.Button(frm_subscription, text='Subscibe', font='Helvetica 20', width=12, fg='blue', command=subscribe_email)
btn_subscribe.pack(side=tk.LEFT, padx=15)
btn_subscribe.bind('<Motion>', lambda _: btn_subscribe.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_subscribe.bind('<Leave>', lambda _: btn_subscribe.config(bg='white', highlightbackground='white', fg='blue'))

# button for send 
btn_send = tk.Button(frm_subscription, text='Send', font='Helvetica 20', width=12, fg='blue', command=mail_data)
btn_send.pack(side=tk.LEFT, padx=15)
btn_send.bind('<Motion>', lambda _: btn_send.config(bg='LightSalmon', highlightbackground='blue', fg='white'))
btn_send.bind('<Leave>', lambda _: btn_send.config(bg='white', highlightbackground='white', fg='blue'))

check_box=tk.Checkbutton(main_window,text="Accpect",width=35,font=("Helvetica",20))
check_box.pack(side=TOP)


main_window.mainloop()
