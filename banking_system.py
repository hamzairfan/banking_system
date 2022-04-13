from tkinter import *
from tkinter import messagebox
import sys

class User:
    def __init__(self, username, passwd, usertype, info):
        self.username = username
        self.passwd = passwd
        self.usertype = usertype
        self.info = info
    
    def getUserName(self):
        return self.username

    def getPasswd(self):
        return self.passwd
    
    def getUserType(self):
        return self.usertype

    def getInfo(self):
        return self.info

class Account:
    def __init__(self, name, type, balance):
        self.name = name
        self.balance = balance
        self.type = type
    
    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getBalance(self):
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        self.balance -= amount
    
class CurrentAccount(Account):
    def __init__(self, name, od_limit, balance, type='current'):
        super().__init__(name, type, balance)
        self.od_limit = od_limit
    
    def getOdLimit(self):
        return self.od_limit

    def withdraw(self, amount):
        if amount > self.balance + self.od_limit:
            print("You don't have enough balance")
            return
        return super().withdraw(amount)

class SavingsAccount(Account):
    def __init__(self, name, interest_rate, balance,  type='savings'):
        super().__init__(name, type, balance)
        self.interest_rate = interest_rate
    
    def getInterestRate(self):
        return self.interest_rate
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("You don't have enough balance")
            return
        return super().withdraw(amount)
    

# Pre-Set Data
data = [
    User('Arthur', '123', 'admin', None),
    User('Boris', 'ABC', 'user', {'Address': '10 London Road', 
                                'Accounts': [CurrentAccount('Current Account', 100, 1000)]}),
    User('Chloe', '1+x', 'user', {'Address': '99 Queens Road', 
                                'Accounts': [CurrentAccount('Current Account', 100, 1000),
                                            SavingsAccount('Saving Account', 2.99, 4000)]}),
    User('David', 'aBC', 'user', {'Address': '99 Queens Road', 
                                'Accounts': [SavingsAccount('Saving Account 1', 0.99, 200),
                                            SavingsAccount('Saving Account 2', 4.99, 5000)]})
]

def accountAction(point, account_option):
    account_selected = point.getInfo()['Accounts'][int(account_option)-1]
    print('You selected %d - %s: £%d.' % (int(account_option)+1, account_selected.getName(), account_selected.getBalance()))
    print('Please select an option:\n\
        \t1 - Deposit\n\
        \t2 - Withdraw\n\
        \t3 - Go Back')
    action = input('Enter a number to select your option: ')
    if action == '1':
        amount = input('Please enter the amount in £ to be deposited: ')
        account_selected.deposit(float(amount))
        return
    if action == '2':
        amount = input("Please enter the amount in £ to be withdrawn: ")
        account_selected.withdraw(float(amount))
        return
    if action == '3':
        return

def accountSelection(point):
    while(True):
        print('--Account List--\n\
            Please select an option:')
        for ind, val in enumerate(point.getInfo()['Accounts']):
            print('%s - %s: £%s' % (ind+1, val.getName(), val.getBalance()))
        account_option = input("Enter a  number to select your option: ")
        accountAction(point, account_option)

def accountSummary(point):
    totalnum = len(point.getInfo()['Accounts'])
    totalbalnc = sum([x.getBalance() for x in point.getInfo()['Accounts']])
    print("Your account summary is as follows:\n\
            \tTotal number of accounts: %s\n\
            \tTotal balance of all accounts: £%s\n\
            \tAddress: %s" % (totalnum, totalbalnc, point.getInfo()['Address']))

def userAction(point):
    while(True):
        print("Please select an option:\n\
            \t1 - View Account\n\
            \t2 - View Summary\n\
            \t3 - Quit\n")
        option = input("Please enter a number to select your option:")
        # View Account
        if option == '1':
            accountSelection(point)
        if option == '2':
            accountSummary(point)
        if option == '3':
            sys.exit()

def customerSummary():
    print("-------------------------------------- Customer Summary ---------------------------------------------")
    count = 1
    for point in data:
        if point.getUserType() == 'user':
            print('Customer %s:\n\
                \tName: %s\n\
                \tAddress: %s' % (count, point.getUserName(), point.getInfo()['Address']))
            account_count = 1
            for account in point.getInfo()['Accounts']:
                print('\tAccount %s:\n\
                    \tAccount Type: %s\n\
                    \tBalance: £%s' % (account_count, account.getName(), account.getBalance()))
                if isinstance(account, SavingsAccount):
                    print('\t\t\tInterest Rate: %s' % (account.getInterestRate()))
                if isinstance(account, CurrentAccount):
                    print('\t\t\tInterest Rate: %s' % (account.getOdLimit()))
                account_count += 1
            count += 1
    print("--------------------------------------------------------------------------------------------------------")

def financialForecast():
    count = 1
    for point in data:
        if point.getUserType() == 'user':
            print('Customer %s:\n\
                \tName: %s\n\
                \tNumber of accounts in bank: %s\n\
                \tTotal Money in Bank: £%s' % (count, point.getUserName(), len(point.getInfo()['Accounts']), sum([x.getBalance() for x in point.getInfo()['Accounts']])))
            forecast = sum([x.getBalance() for x in point.getInfo()['Accounts']])
            for account in point.getInfo()['Accounts']:
                if isinstance(account, SavingsAccount):
                    forecast += (account.getInterestRate()/100) * account.getBalance()
            print('\tForecasted money after a year: £%s' % forecast)
            count += 1

def getAccounts(lbuser, lbaccount, status):
    user = str(lbuser.get(ACTIVE))
    for point in data:
        if point.getUserName() == user:
            lbaccount.delete(0,'end')
            for ind, account in enumerate(point.getInfo()['Accounts']):
                lbaccount.insert(ind+1, account.getName())
            status.config(text = "Idle")

def initTransfer(lbuser1, lbaccount1, lbuser2, lbaccount2, transfer_amt, status):
    user1 = str(lbuser1.get(ACTIVE))
    user2 = str(lbuser2.get(ACTIVE))
    for point in data:
        if point.getUserName() == user1:
            for account in point.getInfo()['Accounts']:
                if account.getName() == str(lbaccount1.get(ACTIVE)):
                    account.withdraw(int(transfer_amt.get()))
                    status.config(text = "Success")
        elif point.getUserName() == user2:
            for account in point.getInfo()['Accounts']:
                if account.getName() == str(lbaccount2.get(ACTIVE)):
                    account.deposit(int(transfer_amt.get()))
                    status.config(text = "Success")

def transferMoney():
    master = Tk()
    master.title('Transfer Money')
    Label(master, text='From User').grid(row=0)
    Label(master, text='To User').grid(row=0, column=2)
    Label(master, text='From Account').grid(row=2)
    Label(master, text='To Account').grid(row=2, column=2)
    Label(master, text='Transfer Amount').grid(row=3, column=2)
    status = Label(master, text='')
    LbUser1 = Listbox(master)
    LbAccount1 = Listbox(master)
    generate1 = Button(master, text='Generate Accounts', width=25, command=lambda: getAccounts(LbUser1, LbAccount1, status))
    LbUser2 = Listbox(master)
    LbAccount2 = Listbox(master)
    generate2 = Button(master, text='Generate Accounts', width=25, command=lambda: getAccounts(LbUser2, LbAccount2, status))
    transfer_amt = Entry(master)
    transfer = Button(master, text='Initiate Transfer', width=25, command=lambda: initTransfer(LbUser1, LbAccount1, LbUser2, LbAccount2, transfer_amt, status))
    for num, point in enumerate(data):
        if point.getUserType() == 'user':
            LbUser1.insert(num+1, point.getUserName())
            LbUser2.insert(num+1, point.getUserName())
    LbUser1.grid(row=0, column=1)
    LbUser2.grid(row=0, column=3)
    generate1.grid(row=1, column=1)
    generate2.grid(row=1, column=3)
    LbAccount1.grid(row=2, column=1)
    LbAccount2.grid(row=2, column=3)
    transfer_amt.grid(row=3, column=3)
    transfer.grid(row=4, column=2)
    status.grid(row=5, column=2)
    mainloop()

def createAccountAction(ins, user, title, type, limit, balance):
    for point in data:
        if point.getUserName() == user:
            selected_user = point
            break
    if str(type.get(ACTIVE)) == 'current':
        for account in selected_user.getInfo()['Accounts']:
            if account.getType() == 'current':
                messagebox.showerror("Error!", "Cannot create another current account!")
                return
        selected_user.getInfo()['Accounts'].append(CurrentAccount(str(title.get()), float(limit.get()), float(balance.get())))
        ins.destroy()
        accountMngmnt()
    else:
        selected_user.getInfo()['Accounts'].append(SavingsAccount(str(title.get()), float(limit.get()), float(balance.get())))
        ins.destroy()
        accountMngmnt()




def createAccountWin(ins, lbuser):
    user = str(lbuser.get(ACTIVE))
    ins.destroy()
    account_win = Tk()
    account_win.title('Create Account')
    Label(account_win, text='Title').grid(row=0)
    title = Entry(account_win)
    title.grid(row=0, column=1)
    Label(account_win, text='Type').grid(row=0, column=2)
    types = ['current', 'savings']
    type_menu = Listbox(account_win)
    for num, point in enumerate(types):
        type_menu.insert(num+1, point)
    type_menu.grid(row=0, column=3)
    Label(account_win, text='Overdraft Limit/Interest Rate').grid(row=1, column=0)
    od_limit_ir = Entry(account_win)
    od_limit_ir.grid(row=1,column=1)
    Label(account_win, text='Balance').grid(row=1, column=2)
    balance = Entry(account_win)
    balance.grid(row=1, column=3)
    create = Button(account_win, text='Create Account', width=25, command=lambda: createAccountAction(account_win, user, title, type_menu, od_limit_ir, balance))
    create.grid(row=2, column=2)
    mainloop()

def deleteAccountAction(ins, user, account):
    for acc in user.getInfo()['Accounts']:
        if acc.getName() == account.get(ACTIVE):
            user.getInfo()['Accounts'].remove(acc)
            del acc
            ins.destroy()
            accountMngmnt()
            break

def deleteAccountWin(ins, lbuser):
    user = str(lbuser.get(ACTIVE))
    for point in data:
        if point.getUserName() == user:
            selected_user = point
            if len(selected_user.getInfo()['Accounts'])<=1:
                messagebox.showerror('Error!', 'Cannot delete the last account!')
                return
            break
    ins.destroy()
    account_win = Tk()
    account_win.title('Delete Account')
    Label(account_win, text='Select Account').grid(row=0)
    accounts_menu = Listbox(account_win)
    for num, point in enumerate(selected_user.getInfo()['Accounts']):
        accounts_menu.insert(num+1, point.getName())
    accounts_menu.grid(row=0, column=1)
    delete = Button(account_win, text='Delete Account', width=25, command=lambda: deleteAccountAction(account_win, selected_user, accounts_menu))
    delete.grid(row=1, column=1)
    mainloop()



def accountMngmnt():
    master = Tk()
    master.title('Account Management')
    Label(master, text='Choose User').grid(row=0)
    LbUser = Listbox(master)
    for num, point in enumerate(data):
        if point.getUserType() == 'user':
            LbUser.insert(num+1, point.getUserName())
    LbUser.grid(row=0, column=1)
    create = Button(master, text='Create an account', width=25, command=lambda: createAccountWin(master, LbUser))
    delete = Button(master, text='Delete an account', width=25, command=lambda: deleteAccountWin(master, LbUser))
    create.grid(row=1, column=0)
    delete.grid(row=1, column=1)
    mainloop()

def adminAction():
    while(True):
        print("Please select an option:\n\
            \t1 - Customer Summary\n\
            \t2 - Financial Forecast\n\
            \t3 - Transfer Money - GUI\n\
            \t4 - Account Management - GUI")
        option = input("Please enter a number to select your option:")
        if option == '1':
            customerSummary()
        if option == '2':
            financialForecast()
        if option == '3':
            transferMoney()
        if option == '4':
            accountMngmnt()

if __name__ == '__main__':
    print("****************Welcome to the Banking System***************")
    username = input("Please enter your username: ")
    for point in data:
        if point.getUserName() == username:
            passwd = input("Please enter your password: ")
            if point.getPasswd() == passwd:
                if point.getUserType() == 'user':
                    userAction(point)
                    sys.exit()
                if point.getUserType() == 'admin':
                    adminAction()
                    sys.exit()
    print("There is no user registered against this username.")
