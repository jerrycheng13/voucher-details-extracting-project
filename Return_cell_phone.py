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

def An(i):
    if "Returning Officer" in list(A[i]['description']):
        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
        b = int((A[i].loc[A[i]['description'] == "Returning Officer"]).index.values)
    else:
        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
        b = len(A[i])-1                      
    A_n = A[i][a+3:b].sort_values(by=['y','x']).reset_index(drop=True)
    return A_n

def Am(i):
    j = i
    while "Returning Officer" not in list(A[j]['description']):
        j += 1
    c = int((A[j].loc[A[j]['description'] == "Returning Officer"]).index.values)
    A_m = A[j][c+5:].sort_values(by=['y','x']).reset_index(drop=True)
    return A_m

A = read_xml('Cell_Phone_23.xml')

Error = []
Return = []
for i in range(0, len(A)):
    if A[i]['description'][0] == "PROPERTY RETURN RECEIPT":
        Invoice_No = A[i]['description'][3]
        Delivery_No = A[i]['description'][4]
        j = i
        while Invoice_No.isdigit() == False:           
            j -= 1
            Invoice_No = A[j]['description'][3]
            Delivery_No = A[j]['description'][4]                        
        try:
            if "Item" in list(A[i]['description']):
                A_n = An(i)
                Item = A_n[A_n['x'] <= 60]['description'].reset_index(drop=True)           
                Quantity = list(A_n[A_n['x'] == 739]["description"].reset_index(drop=True))
                if list(A_n[A_n['x'] <= 60]['y']) != []:
                    y_min = min(list(A_n[A_n['x'] <= 60]['y']))
                else:
                    y_min = float('Inf')
                Article_Description = A_n[(A_n['x'] > 60) & (A_n['x'] < 739) & (A_n['y'] >= y_min)]['description'].reset_index(drop=True)
                if len(Article_Description) != 0:
                    for k in range(1, len(Article_Description)):
                        if Article_Description[k][:16] == "GENERAL PROPERTY":
                            Article_Description[k-1] += "?"
                    Article_Description = (" ".join(list(Article_Description))).split("? ")
                    if len(Quantity) != len(Article_Description):
                        for k in range(0, len(Article_Description)):
                            if (Article_Description[k].split(' ')[-1].lstrip()).isdigit() and Article_Description[k].split(' ')[-2].lstrip() not in ['SIZE','LOCAL', 'PHONE', 'IPHONE', 'I-PHONE', 'GALAXY', 'ITEM'] and len(Article_Description[k].split(' ')[-1].lstrip()) <= 3:
                                Quantity_add = Article_Description[k].split(' ')[-1].lstrip()
                                Article_Description[k] = Article_Description[k][:-len(Quantity_add)]
                                Quantity.insert(k, Quantity_add)
                            if (Article_Description[k].split('|')[-1].lstrip()).isdigit() and Article_Description[k].split('|')[-2].lstrip() not in ['SIZE','LOCAL', 'PHONE', 'IPHONE', 'I-PHONE', 'GALAXY', 'ITEM'] and len(Article_Description[k].split('|')[-1].lstrip()) <= 3:
                                Quantity_add = Article_Description[k].split('|')[-1].lstrip()
                                Article_Description[k] = Article_Description[k][:-len(Quantity_add)]
                                Quantity.insert(k, Quantity_add)

                if len(Item) != 0:                
                    A_m = Am(i)                                          
                    Tax_No = A_m[A_m['x'] == 353]["description"].reset_index(drop=True)[0]
                    Command = A_m[A_m['x'] == 438]["description"].reset_index(drop=True)[0]
                    Date = A_m[A_m['x'] == 608]["description"].reset_index(drop=True)[0]
                    Time = A_m[A_m['x'] == 736]["description"].reset_index(drop=True)[0]


                    Return.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Delivery Number': Delivery_No, 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity)}))
        except:
            print(Delivery_No, i)
            Error.append([i, Invoice_No, Delivery_No, Tax_No, Command, Date, Time, list(Item), Article_Description, Quantity])

#    print(i)        
#    if i % 1000 == 0:
#        print(i/len(A))
#Return.append(pd.DataFrame({'Invoice Number': , 'Delivery Number': , 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity)}))   

Error[0][9].insert(6,1)
Error[1][9].insert(22,1)
Error[2][9].insert(5,1)
Error[3][9].insert(3,1)
Error[4][9].insert(3,1)
Error[5][8].pop(12)
Error[6][8].pop(25)
Error[7][8].pop(13)
Error[8][9].pop(4)
Error[9][9].insert(2,1)
Error[10][9].insert(3,1)
Error[11][9].insert(6,1)
Error[12][9].pop(6)
Error[13][9].insert(2,1)
Error[14][9].insert(20,1)
Error[15][9].insert(5,2)



Return_add = []
for i in range(0, len(Error)):
    Return_add.append(pd.DataFrame({'Invoice Number': Error[i][1], 'Delivery Number': Error[i][2], 'Returning Officer Tax No.': Error[i][3], 'Returning Officer Command': Error[i][4], 'Return Date': Error[i][5], 'Return Time': Error[i][6], 'Item (Number)': Error[i][7], "Returning Article Description": Error[i][8], "Return Quantity": Error[i][9]}))

        
Return_Forms = pd.concat(Return + Return_add)
Return_Order = ['Invoice Number', 'Delivery Number', 'Returning Officer Tax No.', 'Returning Officer Command', 'Return Date', 'Return Time', 'Item (Number)', "Returning Article Description", "Return Quantity"]
Return_Frame = Return_Forms[Return_Order]

Return_Frame.to_csv('Return_cell_phone_23.csv', sep=',', index = False)
