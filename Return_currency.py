import pandas as pd

def read_xml(file):
    with open(file, encoding = "ISO-8859-1") as myfile:
        location = []
        description = []
        x = []
        y = []
        for line in myfile:
            if line[:5] == "<text":
                description.append(line.split(">")[1][:-6])
                x.append(int(line.split(">")[0].split()[2][6:-1]))
                y.append(int(line.split(">")[0].split()[1][5:-1]))                
            if line[:7] == "</page>":
                location.append([description, x, y])
                description = []
                x = []
                y = []
    A = []
    for i in range(0, len(location)):
        data = pd.DataFrame({'description':location[i][0], 'x':location[i][1], 'y':location[i][2]}).sort_values(by=['y', 'x']).reset_index(drop=True)
        A.append(data)
    return A

A = read_xml('Currency_12.xml')

Payment = []
for i in range(0, len(A)):
    if A[i]['description'][0] == "RTO Cash - Payment Voucher":
        Invoice_No = A[i]['description'][1]
        Transaction_Date = A[i]['description'][6]
        try:
            for j in range(0, A[i].shape[0]):
                if A[i]['description'][j] == "Item":
                    a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                    b = int((A[i].loc[A[i]['description'] == "Total Amount in Invoice"]).index.values)
                    A_n = A[i][a+4:b-1].sort_values(by=['x','y']).reset_index(drop=True)
                    A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                    Item = A_m[A_m['x'] <= 55]["description"].reset_index(drop=True)
                    Quantity = A_m[(A_m['x'] > 590) & (A_m['x'] <= 621)]["description"].reset_index(drop=True)
                    Article_Description = list(A_n[A_n['x'] == 183]['description'])
                    Actual_amt_value = list(A_m[A_m['x'] > 621]["description"].reset_index(drop=True))
                if A[i]['description'][j] == "Returning Officer":
                    Tax_No = A[i]['description'][j+5]
                    Command = A[i]['description'][j+6]
                    Date = A[i]['description'][j+7]
                    Time = A[i]['description'][j+8]
            Payment.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Transaction Date': Transaction_Date, 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity), "Actual amt value": Actual_amt_value}))
        except:
            print(Invoice_No)

Payment_Forms = pd.concat(Payment)
Payment_Order = ['Invoice Number', 'Transaction Date', 'Returning Officer Tax No.', 'Returning Officer Command', 'Return Date', 'Return Time', 'Item (Number)', "Returning Article Description", "Return Quantity", "Actual amt value"]
Payment_Frame = Payment_Forms[Payment_Order]

Payment_Frame.to_csv('Return_currency_12.csv', sep=',', index = False)




