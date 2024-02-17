# Cafe ChillZ Coffee Ordering App

# Standard imports
import smtplib
from sqlite3 import *
from customtkinter import *
from datetime import datetime

c = 'vmpi ddgd lamb sjtk'


class Form:
    def __init__(self, parent):
        self.win = parent

        self.name = None
        self.email = None
        self.choice = None
        self.extras = None
        self.msg = None
        self.dataAllow = None

        self.createUI()

    def checkTime(self):
        now = datetime.now()
        current_date = now.date()
        day = current_date.strftime('%A')
        current_time = now.time()
        hour = str(current_time.hour)
        if ('09' <= hour < '21') and (day == 'Saturday' or day == 'Sunday'):
            return True
        elif ('17' <= hour < '18') and (day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday'):
            return True
        else:
            closed = CTkLabel(self.win, text='Cafe ChillZ is CLOSED', font=('Roboto', 50, 'bold'), text_color='red')
            closed.place(x=380, y=300)
            time_info = CTkLabel(self.win, text="Opening Hours:\nWeekdays: 5:00 to 6:00pm\nWeekends: 9:00am to 6:00pm", font=('Roboto', 20, 'bold'))
            time_info.place(x=500, y=400)
            return False

    def getData(self, name, email, choice, extras, msg, data_allow):
        self.name = name.get()
        self.email = email.get()
        self.choice = choice.get()
        self.extras = extras.get()
        self.msg = msg.get("1.0", 'end')
        self.dataAllow = data_allow.get()

        self.submit_order()

    def saveData(self):
        try:
            con = connect("CoffeeData.sqlite")
            if self.dataAllow:
                query = "INSERT INTO orders (name, email, drink, details, message) VALUES (?,?,?,?,?);"
                valuesTuple = (self.name, self.email, self.choice, self.extras, self.msg)
            else:
                query = "INSERT INTO orders (name, email, drink, details, message) VALUES (?,?,?,?,?);"
                valuesTuple = ("N/A", "N/A", self.choice, self.extras, self.msg)

            cursor = con.cursor()
            cursor.execute(query, valuesTuple)
            con.commit()
            con.close()
        except FileNotFoundError:
            print("Unable to save data! FileNotFoundError!")
        except TypeError:
            print("Unable to save data! TypeError!")
        except Exception as e:
            print(f"Something went wrong... Cannot save data! Error: {e}")

    def submit_order(self):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'abhinavherein@gmail.com'
        smtp_password = c

        from_email = self.email
        to_email = 'abhinavherein@gmail.com'
        subject = 'Cafe ChillZ - New Order Received'
        body = f"""
                    You have received a new order from your Cafe ChillZ Coffee Shop:

                    Name: {self.name}
                    Email Address: {from_email}
                    Drink Choice: {self.choice}
                    Extras: {self.extras}
                    Message: {self.msg}

                    Please send them an email when you have made their order or inform them if you cannot make their order.
                """
        print(body)
        data_allow = "Yes" if self.dataAllow else "No"
        print(data_allow)
        message = f'Subject: {subject}\n\n{body}'

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.sendmail(from_email, to_email, message)

            success = CTkLabel(self.win,
                               text="Your order has been placed successfully! You will receive an email when your order has been made!")
            success.place(x=530, y=600)
            self.saveData()
        except smtplib.SMTPException as e:
            print(f"Failed to send email. Error: {e}")

    def createUI(self):
        self.win.title("Cafe ChillZ Order Form")
        self.win.geometry("1920x1080")

        if self.checkTime():
            frame = CTkFrame(self.win)
            frame.place(x=0, y=0, relwidth=1, relheight=1)

            header = CTkLabel(frame, text="Order your Coffee HERE", font=('Helvetica', 18, 'bold'))
            header.place(x=560, y=50)

            nameVar = StringVar()
            nameLabel = CTkLabel(frame, text="Name: ")
            nameLabel.place(x=565, y=100)
            nmEntry = CTkEntry(frame, width=200, textvariable=nameVar)
            nmEntry.place(x=565, y=125)

            emailVar = StringVar()
            emailLabel = CTkLabel(frame, text="Email Address: ")
            emailLabel.place(x=560, y=175)
            emEntry = CTkEntry(frame, width=200, textvariable=emailVar)
            emEntry.place(x=565, y=200)

            choiceVar = StringVar(value=None)
            opMenuLabel = CTkLabel(frame, text="Drink Choice: ")
            opMenuLabel.place(x=565, y=250)
            opMenu = CTkOptionMenu(frame, values=["Espresso", "Latte", "Chai/Tea", "Cold Coffee Shake", "Babyccino"],
                                   variable=choiceVar, width=200, corner_radius=5)
            opMenu.place(x=565, y=275)

            extrasVar = StringVar()
            extrasLabel = CTkLabel(frame, text="Add Extras: ")
            extrasLabel.place(x=565, y=325)
            extrasOpMenu = CTkOptionMenu(frame, values=["Extra Shot", "Skim Milk", "Sugar (1 tsp)",
                                                        "Whipped Cream (Only for Cold Coffee)"],
                                         variable=extrasVar, width=200, corner_radius=5)
            extrasOpMenu.place(x=565, y=350)

            msgLabel = CTkLabel(frame, text="Any other details: ")
            msgLabel.place(x=565, y=400)
            msgVar = CTkTextbox(frame, width=200, height=100)
            msgVar.insert("1.0", "Type here...")
            msgVar.place(x=565, y=425)

            dataAllowVar = StringVar(value='False')
            checkLabel = CTkLabel(frame, text="Allow my data to be shared for analytics and improvements: ")
            checkLabel.place(x=565, y=525)
            checkbox = CTkCheckBox(frame, variable=dataAllowVar, onvalue=True, offvalue=False, text="Yes/No")
            checkbox.place(x=565, y=550)

            submitBtn = CTkButton(frame, text="Place Order",
                                  command=lambda: self.getData(nameVar, emailVar, choiceVar, extrasVar, msgVar,
                                                               dataAllowVar))
            submitBtn.place(x=565, y=600)


root = CTk()
form = Form(root)
root.mainloop()
