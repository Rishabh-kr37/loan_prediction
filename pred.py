import tkinter as tk
from tkinter import messagebox
from sklearn.tree import DecisionTreeClassifier

# Placeholder loan approval model
def predict_loan(income, credit_score, loan_amount):
    # Your actual model prediction code should go here
    # For this example, we use a simple Decision Tree classifier
    model = DecisionTreeClassifier()
    # Assume you have preprocessed features and target data (X_train, y_train)
    # model.fit(X_train, y_train)
    prediction = model.predict([[income, credit_score, loan_amount]])
    return prediction[0]

# Function to handle loan prediction
def handle_prediction():
    try:
        income = float(income_entry.get())
        credit_score = float(credit_score_entry.get())
        loan_amount = float(loan_amount_entry.get())

        prediction = predict_loan(income, credit_score, loan_amount)

        if prediction == 1:
            messagebox.showinfo("Loan Prediction", "Congratulations! Your loan is approved.")
        else:
            messagebox.showinfo("Loan Prediction", "Sorry, your loan application is not approved.")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for income, credit score, and loan amount.")

# Creating the main tkinter window
root = tk.Tk()
root.title("Loan Prediction")

# Creating input fields
income_label = tk.Label(root, text="Income:")
income_label.pack()
income_entry = tk.Entry(root)
income_entry.pack()

credit_score_label = tk.Label(root, text="Credit Score:")
credit_score_label.pack()
credit_score_entry = tk.Entry(root)
credit_score_entry.pack()

loan_amount_label = tk.Label(root, text="Loan Amount:")
loan_amount_label.pack()
loan_amount_entry = tk.Entry(root)
loan_amount_entry.pack()

# Button to trigger loan prediction
predict_button = tk.Button(root, text="Predict", command=handle_prediction)
predict_button.pack()

# Run the tkinter main loop
root.mainloop()
