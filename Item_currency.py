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

Frames = []
for i in range(0, len(A)):
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        try:
            for j in range(0, A[i].shape[0]):
                if A[i]['description'][j] == "Item" and A[i]['description'][j+6] == "Disposition":
                    if "Total Cash Value" in list(A[i]['description']):
                        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                        b = int((A[i].loc[A[i]['description'] == "Total Cash Value"]).index.values)
                        A_n = A[i][a+7:b-1].sort_values(by=['x','y']).reset_index(drop=True)
                        A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                    else:
                        a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                        b = int((A[i].loc[A[i]['description'] == "PCD Storage No."]).index.values)                       
                        A_n = A[i][a+7:b].sort_values(by=['x','y']).reset_index(drop=True)
                        A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                    Item = A_m[A_m['x'] <= 81]["description"].reset_index(drop=True)
                    Total_QTY = A_m[(A_m['x'] > 81) & (A_m['x'] <= 122)]["description"].reset_index(drop=True)
                    Articles = A_n[(A_n['x'] == 162) & (A_n['y'].isin(list(A_n[A_n['x']<=81]["y"])))]["description"].reset_index(drop=True)
                    Description = A_n[A_n['x'] == 162].reset_index(drop=True)
                    if len(Description) == len(Articles):
                        Description = [None] * len(Description)
                    else:
                        for k in range(0, Description.shape[0]):
                            if Description['y'][k] in list(A_n[A_n['x']<=81]["y"]):
                                Description['description'][k] = "?"
                        Description = (" ".join(list(Description['description']))).split("? ")[1:]
                    Cash = A_m[(A_m['x'] > 162) & (A_m['x'] < 549)]["description"].reset_index(drop=True)           
                    Cash = [i.split()[0] for i in list(Cash)]
                    Disposition = [None] * len(Item)
                    
                    
                    if len(A_n[A_n['x'] >= 702]["description"]) != 0:
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
                            item = A_m[A_m['x'] <= 81][['description','y']]
                            item.set_index('y', inplace=True)
                            result = pd.concat([item, D], axis=1)
                            Disposition = list(result['disposition'])   
#                            
                    Frames.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Item': list(Item), "Total QTY": list(Total_QTY), "Articles": list(Articles), "Description": Description, "Cash": Cash, "Disposition": Disposition}))        
        except:
            print(Invoice_No, i)
 
    
Frames.append(pd.DataFrame({'Invoice Number': , 'Item': list(Item), "Total QTY": list(Total_QTY), "Articles": list(Articles), "Description": Description, "Cash": Cash, "Disposition": Disposition}))        
           

Item_Frame = pd.concat(Frames)
Item_Order = ['Invoice Number', 'Item', 'Total QTY', 'Articles', 'Description', "Cash", 'Disposition']
Item_Frame = Item_Frame[Item_Order]

Item_Frame.to_csv('Item_currency_12.csv', sep=',', index = False)
