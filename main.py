import tkinter as tk


# tkinter gui starts 
window = tk.Tk()



window.title("Loan Prediction system")
window.geometry("500x400+500+150")
window.resizable(width=False, height=False)
greeting = tk.Label(text="Loan Prediction system")
greeting.pack()

B = tk.Button(text ="Loan Calculator", height=2 , width=45, bg="red", fg="white")
B.place(x=90,y=50)

C = tk.Button(text ="Loan Prediction", height=2 , width=45, bg="red", fg="white")
C.place(x=90,y=150)

D = tk.Button(text ="Loan Graph", height=2 , width=45, bg="red", fg="white")
D.place(x=90,y=250)



window.mainloop()
# tkinter gui ends 