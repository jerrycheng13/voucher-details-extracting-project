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
    if "Prisoner(s)" in list(A[i]['description']):
        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
        b = int((A[i].loc[A[i]['description'] == "Prisoner(s)"]).index.values)
    else:
        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
        b = int((A[i].loc[A[i]['description'] == "PCD Storage No."]).index.values)                       
    if 'Total Cash Value' in list(A[i]['description']):
        A_n = A[i][a+7:b].sort_values(by=['y','x']).reset_index(drop=True)
    else:
        A_n = A[i][a+6:b].sort_values(by=['y','x']).reset_index(drop=True)
    return A_n



A = read_xml('Cell_Phone_14.xml')

Error = []
Frames = []
for i in range(0, len(A)):
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        try:
#            for j in range(0, A[i].shape[0]):
            if "Item" in list(A[i]['description']):
                A_n = An(i)
                Item = A_n[(A_n['x'] >= 60) & (A_n['x'] <= 81)]["description"].reset_index(drop=True)
                Total_QTY = A_n[(A_n['x'] > 81) & (A_n['x'] <= 122)]["description"].reset_index(drop=True)
                Articles = A_n[(A_n['x'] >= 162) & (A_n['x'] <= 164) & (A_n['y'].isin(list(A_n[(A_n['x'] > 81) & (A_n['x'] <= 122)]["y"])))]["description"].reset_index(drop=True)
                Description = A_n[(A_n['x'] >= 162) & (A_n['x'] <= 164)].reset_index(drop=True)
                if len(Description) == len(Articles):
                    Description = [None] * len(Description)
                else:
                    for k in range(0, Description.shape[0]):
                        if Description['y'][k] in list(A_n[(A_n['x'] > 81) & (A_n['x'] <= 122)]["y"]):
                            Description['description'][k] = "?"
                    Description = (" ".join(list(Description['description']))).split("? ")[1:]
                if len(Item) != len(Description):
                    Description[-1] = Description[-1][0:-2]
                    A_m = An(i+1)
                    if list(A_m[(A_m['x'] > 81) & (A_m['x'] <= 122)]["y"]) != []:
                        y_max = min(list(A_m[(A_m['x'] > 81) & (A_m['x'] <= 122)]["y"]))
                        Description_add = A_m[(A_m['x'] >= 162) & (A_m['x'] <= 164) & (A_m['y'] < y_max)].reset_index(drop=True)
                    else:
                        Description_add = A_m[(A_m['x'] >= 162) & (A_m['x'] <= 164)].reset_index(drop=True)
                    Description_add = (" ".join(list(Description_add['description'])))
                    Description.append(Description_add)
                    
                Disposition = [None] * len(Item) 
                    
                if len(A_n[(A_n['x'] >= 687) & (A_n['x'] <= 693)]["description"]) != 0:
                    disposition = A_n[(A_n['x'] >= 687) & (A_n['x'] <= 693)].sort_values(by=['y','x']).reset_index(drop=True)
                    for k in range(1, disposition.shape[0]):
                        if disposition['x'][k] == 687:
                            replace = " ".join([disposition['description'][k-1], disposition['description'][k]])
                            disposition['description'][k-1] = replace
                    disposition = list(disposition[disposition['x'] == 693]['description'])
                    disposition_y = list(A_n[A_n['x'] == 693]["y"])
                    disposition_y = [i-4 for i in list(disposition_y)]
                    item_q = A_n[(A_n['x'] > 81) & (A_n['x'] <= 122)][['description','y']]
                    while [i for i in disposition_y if i in list(item_q['y'])] == []:
                        disposition_y = [i-1 for i in list(disposition_y)]                    
                    item_q.set_index('y', inplace=True)
                    if len(Item) == 1:
                        Disposition[0] = disposition[0]
                    else:
                        D = pd.DataFrame({'disposition':disposition, 'y':disposition_y})
                        D.set_index('y', inplace=True)
                        result = pd.concat([item_q, D], axis=1)
                        Disposition = list(result['disposition'])                     

                if len(A_n[(A_n['x'] >= 702) & (A_n['x'] <= 708)]["description"]) != 0:
                    disposition = A_n[(A_n['x'] >= 702) & (A_n['x'] <= 708)].sort_values(by=['y','x']).reset_index(drop=True)
                    for k in range(1, disposition.shape[0]):
                        if disposition['x'][k] == 702:
                            replace = " ".join([disposition['description'][k-1], disposition['description'][k]])
                            disposition['description'][k-1] = replace
                    disposition = list(disposition[disposition['x'] == 708]['description'])
                    disposition_y = list(A_n[A_n['x'] == 708]["y"])
                    if len(Item) == 1:
                        Disposition[0] = disposition[0]
                    else:
                        D = pd.DataFrame({'disposition':disposition, 'y':disposition_y})
                        D.set_index('y', inplace=True)
                        item_q = A_n[(A_n['x'] > 81) & (A_n['x'] <= 122)][['description','y']]
                        item_q.set_index('y', inplace=True)
                        result = pd.concat([item_q, D], axis=1)
                        Disposition = list(result['disposition'])                                  
                                
                Frames.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Item': list(Item), "Total QTY": list(Total_QTY), "Articles": list(Articles), "Description": Description, "Disposition": Disposition}))     
        except:
            print(Invoice_No, i)
            Error.append([Invoice_No, i])
    if i % 1000 == 0:
        print(i/len(A))
 
    
Frames.append(pd.DataFrame({'Invoice Number': , 'Item': list(Item), "Total QTY": list(Total_QTY), "Articles": list(Articles), "Description": Description, "Disposition": Disposition}))        
           


Item_Frame = pd.concat(Frames)
Item_Order = ['Invoice Number', 'Item', 'Total QTY', 'Articles', 'Description', 'Disposition']
Item_Frame = Item_Frame[Item_Order]

Item_Frame.to_csv('Item_cell_phone_14.csv', sep=',', index = False)

