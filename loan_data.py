
 
# Header Section: GUI basic project set up - creates a 1024x768 work area on a full screen background
from tkinter import *
from tkinter.ttk import *  # added just for this app
from tkinter import messagebox
import math
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='SteelBlue4')
scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()  
workwindow = str(1024) + "x" + str(768) + "+" + str(int((scrW-1024)/2)) + "+" + str(int((scrH-768)/2))
top1 = Toplevel(root, bg="light blue")
top1.geometry(workwindow)
top1.title(" Simple Amortization")
top1.attributes("-topmost", 1)  # make sure top1 is on top to start - "wax on"
root.update()                   # but don't leave it locked in place
top1.attributes("-topmost", 0)  # in case you use lower or lift  -  "wax off"
# exit button - note: uses grid
b3 = Button(root, text="Egress", command=root.destroy)
b3.grid(row=0, column=0, ipadx=10, ipady=10, pady=5, padx=5, sticky=W+N)
 
 
# ____________________________
 
# Section I: Constants, variables, etc
setup = False
loan_value = StringVar()
loan_value.set("100.01")
apr_input = StringVar()
apr_input.set("3.5")
apr = StringVar()
apr.set(apr_input.get())
rper = (3.5/100)/12
payment = StringVar()
payment.set('10.01')
new_balance = StringVar()
new_balance.set(1)
start_month = StringVar()
start_month.set("Month")
start_yr = StringVar()
start_yr.set('Year')
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = []
for year in range(1980, 2040):
    years.append(str(year))
date_label_header = "Select MONTH and YEAR to begin your mortgage.\nFor example 'Jan' for a month and '2015' for a year.\n(Available years between 1980 and 2040.)"
focOutWid = StringVar()
focOutWid.set("loan")
focOutWidVal = StringVar()
focOutWidVal.set('100000.01')
 
# ____________________________
 
# Section II: Functions
 
# (1) Utility Functions
 
 
def zap_commas(num):
        if "," in num:                     # some users insist on using commas
            num = "".join(num.split(","))  # so remove them and continue checking
        return num
 
 
def number_check(num, _min, _max):  # need to check several inputs so use this function
    try:
        numchk = float(num)
    except ValueError:
        return False
    else:
        if _min <= numchk <= _max:
            return True
        else:
            return False
 
 
def bad_entry_msg(entry_type, entry_widget, reset_amt_string):
    mymessage = "Oops, Invalid Entry for " + entry_type
    messagebox.showinfo("Incorrect Data Emtry", mymessage, parent=data_frame)
    eval(reset_amt_string)
    eval(entry_widget + '.focus_set()')
    eval(entry_widget + '.selection_range(0, END)')
    return "break"
 
 
def badnews(msg):
    messagebox.showinfo("Data Error", msg, parent=data_frame)
    loan_value.set("100.01")
    payment.set('10.01')
    # apr.set('3.5')
    loan_entry.focus_set()
    loan_entry.selection_range(0, END)
    return "break"
 
 
def clickcheck(self):
    # if user left clicks in an entry and moves focus with the mouse, bad entry info can be uncorrected
    test = loan_amount()
    if test == "break":
        loan_entry.focus_set()
        loan_entry.selection_range(0, END)
        return "break"
    test = pay_amount()
    if test == "break":
        payment_entry.focus_set()
        payment_entry.selection_range(0, END)
        return "break"
    test = apr_amount()
    if test == "break":
        apr_entry.focus_set()
        apr_entry.selection_range(0, END)
        return "break"
 
 
# (2) Widget Functions
 
 
def loan_amount(*args):
    num = zap_commas(loan_value.get())
    loan_value.set(num)
    ckval = number_check(loan_value.get(), 100, 1000000.01)
    if ckval is True:
        temp = round(float(num), 8)
        num = format(temp, " >#12.2f")
        loan_value.set(num)
        loan_entry.update()
        payment_entry.focus_set()
        payment_entry.selection_range(0, END)
    else:
        bad_entry_msg("loan amount", 'loan_entry', 'loan_value.set("100.01")')
        loan_entry.focus_set()
        return "break"
 
 
def pay_amount(*args):
    num = zap_commas(payment.get())
    payment.set(num)
    ckval = number_check(payment.get(), 1.00, float(loan_value.get()))
    if ckval is True:
        temp = round(float(num), 8)
        round(temp, 3)
        num = format(temp, " >#10.2f")
        payment.set(num)
        payment_entry.update()
        apr_entry.focus_set()  # on to the next data to enter
        apr_entry.selection_range(0, END)
    else:
        bad_entry_msg("payment amount", 'payment_entry', 'payment.set("10.01")')
        payment_entry.focus_set()
        return "break"
 
 
def apr_amount(*args):
    num = zap_commas(apr.get())
    apr.set(num)
    val_check = number_check(apr.get(), .1, 24)
    if val_check is True:
        num = round(float(apr.get()), 8)
        apr.set(str(num))
        month_cbox.focus_set()
    else:
        bad_entry_msg("APR amount", "apr_entry", "apr.set('3.5')")
        apr_entry.focus_set()
        return 'break'   # break interrupts the process and keeps focus on the apr entry
 
 
def show_results():
    if start_month.get() == "Month":
        start_month.set('Jan')
    if start_yr.get() == "Year":
        start_yr.set('1980')
# prepare to create header and table
    c1 = "Period"  # header tezt for each column
    c2 = "$ Interest"
    c3 = "$ Principal"
    c4 = "$ New Balance"
    c5 = "Payment Date"
    table_txt.delete(1.0, END)
    lnamt = float(loan_value.get())
    p = float(payment.get())
    apr_num = float(apr.get())/100
    apr2show = format(apr_num, '>5.3%')
    rpermo = apr_num/12
    mopr2show = format(rpermo, '<6.4%')
    # calculate the number of periods - if it is > 370 abort
    num_pay = 0
    try:
        num_pay = (-math.log10(1-(rpermo*lnamt/p)))/(math.log10(1+rpermo))
    except ValueError:
        mymsg = "Payment is insufficient to resolve loan."
        badnews(mymsg)
        exit()
    if num_pay > 361:
        mymsg = "Inconsistent data entered or loan is > 30 years: " + str(num_pay) + " periods."
        badnews(mymsg)
    spacer = "   "
    rtn = "\n"
    table_txt.insert(END, format("Loan Amount: ", '<30s') + format(lnamt, '>15,.2f') + rtn)
    table_txt.insert(END, format("Payment Frequency: ", '<30s') + format('Monthly', '>15s') + rtn)
    table_txt.insert(END, format("Monthly Payment: ", '<30s') + format(float(p), '>15,.2f') + rtn)
    table_txt.insert(END, format("Annual Interest Rate (ARP): ", '<30s') + format(apr2show, '>15s') + rtn)
    table_txt.insert(END, format("Monthly Compound Rate: ", '<30s') + format(mopr2show, '>15s') + rtn)
    table_txt.insert(END, format("Starting Month and Year: ", '<30s') + format((start_month.get() + " " + start_yr.get()), '>15s') + rtn)
    table_txt.insert(END, format("Number of Payments: ", '<30s') + format(num_pay, '>15,.2f') + rtn)
    mopaynum = divmod(num_pay, 1)
    fullpay = mopaynum[0]
    partpay = mopaynum[1]
    table_txt.insert(END, spacer + format(fullpay, '<3.0f') + " full monthly payments" + rtn)
    if partpay > 0:
        table_txt.insert(END, spacer + "plus 1 final payment of about " + format((partpay * float(p)), "<6.2f") + rtn*2)
# display header
    table_txt.insert(END, f"{c1: <8s}{c5: <12s}{spacer}{c2: <10s}{spacer}{c3: <12s}{spacer}{c4: <13s}{rtn}")
# set up table
    period = 1
    mo_payment = float(payment.get())
    month = start_month.get()
    year = start_yr.get()
    per_str = month + " " + year   # string with month and year
    year = int(year)
    principal = float(loan_value.get())
    new_balance = principal
    interest = principal * rpermo
    principal_reduced = mo_payment - interest
    new_balance -= principal_reduced
# create and display table
    while interest > 0:
        table_txt.insert(END, f"{str(period): <8s}{str(per_str): >12s}{spacer}{interest: > 10,.2f}{spacer}{principal_reduced: > 11,.2f}{spacer}{new_balance: > 13,.2f}{rtn}")
        period += 1
        indexno = months.index(month)
        indexno += 1
        if indexno == 12:
            indexno = 0
            year += 1
        month = months[indexno]
        per_str = month + " " + str(year)
        if new_balance <= mo_payment:
            interest = new_balance * rpermo
            principal_reduced = new_balance
            new_balance = 0
        else:
            interest = new_balance * rpermo
            principal_reduced = float(payment.get()) - interest
            new_balance -= principal_reduced
 
 
# ____________________________
 
# Section 3: Widget Objects
# Remember - creating everything inside top1, our work window
 
 
# starting out with a pair of labelframes, 1 for inputs, 1 for table display
data_frame = LabelFrame(top1, width=300, height=748, borderwidth=10)
table_frame = LabelFrame(top1, width=904, height=748, borderwidth=10)
data_frame.pack(side=LEFT, padx=5, pady=5, expand=FALSE, fill="y")
table_frame.pack(side=LEFT, padx=5, pady=5, expand=FALSE, fill="y")
# alternatively, we could use:
# data_frame.grid(row=1, column=0)
# table_frame.grid(row=1, column=1)
data_frame.pack_propagate(FALSE)
table_frame.pack_propagate(FALSE)
 
 
# ~~~
# Now fill the Data Frame with data related widgets
# ------ frame header stuff --------
# a title
title = Label(data_frame, text="Simple Amortization Table", justify=CENTER)
title.grid(row=1, column=1, sticky=NW)
title.configure(font="14")
 
 
# spacer
spacer1 = LabelFrame(data_frame)
spacer1.grid(row=2, column=1, pady=5)
 
 
# a notes/assumptions text box
notes = Text(data_frame,  height=4, width=40)
notes.grid(row=3, column=1, padx=15)
assumptions = "Assumptions:\nMonthly compounding with payments \ndue monthly at the end of the month.\n30 year + 1 mo max term"
notes.insert(END, assumptions)
 
 
# spacer
spacer2 = LabelFrame(data_frame)
spacer2.grid(row=4, column=1, pady=10)
 
 
# ------ this is where the data is collected--------
 
# loan amount label and entry box
 
lltxt = "Enter Loan Amount: $(100 -> 1000000)"
loan_frame = Frame(data_frame, height=3)
loan_label = Label(loan_frame, text=lltxt)
loan_entry = Entry(loan_frame,  textvariable=loan_value)
loan_frame.grid(row=5, column=1, sticky=W)
loan_label.grid(row=0, column=0, sticky=W)
loan_entry.grid(row=1, column=0, pady=10, sticky=W)
loan_entry.bind('<Return>', loan_amount)
loan_entry.bind('<Tab>', loan_amount)
loan_entry.bind('<1>', clickcheck)
 
# spacer
spacer3 = LabelFrame(data_frame)
spacer3.grid(row=6, column=1, pady=10)
 
# loan payment amount label and entry box
loan_pay_txt = "Enter Loan Payment Amount: $(1 -> loan amount)"
payment_frame = Frame(data_frame, height=3)
payment_label = Label(payment_frame, text=loan_pay_txt)
payment_entry = Entry(payment_frame,  textvariable=payment)
payment_frame.grid(row=7, column=1, sticky=W)
payment_label.grid(row=0, column=0, sticky=W)
payment_entry.grid(row=1, column=0, pady=10, sticky=W)
payment_entry.bind('<Return>', pay_amount)
payment_entry.bind('<Tab>', pay_amount)
payment_entry.bind('<1>', clickcheck)
 
# spacer
spacer4 = LabelFrame(data_frame)
spacer4.grid(row=8, column=1, pady=10)
 
# APR amount label and entry box
apr_label_txt = "Enter APR (annual percentage rate):\nFor example 7.5 for 7.5% annual rate.\n" \
                "( .1 -> 24 ) Note: 24 is the max legal in U.S. (TN)"
apr_frame = Frame(data_frame, height=2)
apr_label = Label(apr_frame, text=apr_label_txt)
apr_entry = Entry(apr_frame, textvariable=apr)
apr_frame.grid(row=9, column=1, sticky=W)
apr_label.grid(row=0, column=0, sticky=W)
apr_entry.grid(row=1, column=0, pady=10, sticky=W)
apr_entry.bind('<Return>', apr_amount)
apr_entry.bind('<Tab>', apr_amount)
apr_entry.bind('<1>', clickcheck)
 
# spacer
spacer5 = LabelFrame(data_frame)
spacer5.grid(row=10, column=1, pady=10)
 
# date input grid
date_frame = Frame(data_frame)
date_label = Label(date_frame, text=date_label_header)
date_frame.grid(row=11, column=1, sticky=W)
date_label.grid(row=0, column=0, sticky=W, columnspan=3)
month_cbox = Combobox(date_frame, values=months, width=12, textvariable=start_month, state="readonly")
month_cbox.grid(row=2, column=0, sticky=E+W)
year_cbox = Combobox(date_frame, values=years, width=12, textvariable=start_yr, state="readonly")
year_cbox.grid(row=2, column=1, sticky=E+W, padx=10)
month_cbox.bind('<1>', clickcheck)
year_cbox.bind('<1>', clickcheck)
 
# spacer
spacer6 = LabelFrame(data_frame)
spacer6.grid(row=13, column=1, pady=20)
 
# calculate button
b1 = Button(data_frame, text="LEFT CLICK TO CALCULATE AMORTIZATION TABLE", command=show_results, width=24)
b1.grid(row=15, column=1, columnspan=3, sticky="nsew")
 
# In the table frame next to the data frame create text display to hold the loan table
 
table_txt = Text(table_frame, width=600)
table_txt.pack(fill="both", expand=TRUE)
sbar1 = Scrollbar(table_txt, orient="vertical", command=table_txt.yview)
sbar1.pack(side="right", anchor="ne", fill="y")
table_txt.configure(yscrollcommand=sbar1.set(0, .1))
 
# ____________________________
# Section4: Startup Code
 
setup = TRUE
loan_entry.focus_set()
loan_entry.selection_range(0, END)
top1.update()
 
# starts execution
root.mainloop()
