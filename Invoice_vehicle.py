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

A = read_xml('Vehicle_12.xml')

D = []
for i in range(0, len(A)):
    B = {}
    C = {}
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        B.update({"Invoice Number": Invoice_No})
        for j in range(0, A[i].shape[0]):
            if A[i]['description'][j] == "Invoice Date":
                Invoice_Date = A[i]['description'][j+2]
                Invoice_Status = A[i]['description'][j+3]
#                if Invoice_Status == 'VOID':
#                    B.update({"Time obtained": None})
#                    B.update({"Date obtained": None})
#                    B.update({"Personel Property Removed": None})
#                    B.update({"Recovery Premise Type": None})
                B.update({"Invoice Date": Invoice_Date})
                B.update({"Invoice Status": Invoice_Status})
            if A[i]['description'][j] == "Invoicing Command":
                Invoicing_Command = A[i]['description'][j+3]
                Property_Type = A[i]['description'][j+4]
                Property_Category = A[i]['description'][j+5]
                B.update({"Invoicing Command": Invoicing_Command})
                B.update({"Property Type": Property_Type})
                B.update({"Property Category": Property_Category})
            if A[i]['description'][j] == "Officers":
                if A[i]['description'][j+5] == "Invoicing":
                    Invoicing_Officer_Tax_No = A[i]['description'][j+3]
                    Invoicing_Officer_Command = A[i]['description'][j+4]
                else:
                    Invoicing_Officer_Tax_No = None
                    Invoicing_Officer_Command = None                    
                if A[i]['description'][j+9] == "Arresting" or A[i]['description'][j+7] == "Arresting":
                    if A[i]['description'][j+9] == "Arresting":
                        Arresting_Officer_Tax_No = A[i]['description'][j+7]
                        Arresting_Officer_Command = A[i]['description'][j+8]                        
                    if A[i]['description'][j+7] == "Arresting":
                        Arresting_Officer_Tax_No = None
                        Arresting_Officer_Command = None                        
                B.update({"Invoicing Officer Tax No.": Invoicing_Officer_Tax_No, "Invoicing Officer Command": Invoicing_Officer_Command, "Arresting Officer Tax No.": Arresting_Officer_Tax_No, "Arresting Officer Command": Arresting_Officer_Command})
            if A[i]['description'][j] == "Owner Notified By":
                a = int((A[i].loc[A[i]['description'] == "CSU/ECT Processing"]).index.values)
                b = int((A[i].loc[A[i]['description'] == "Vehicle Details"]).index.values)
                A_n = A[i][a+1:b].sort_values(by=['x','y']).reset_index(drop=True)
                Owner_Notified_By_Tax_No = A_n[A_n['x']==352]['description'].values
                if list(Owner_Notified_By_Tax_No) == []:
                    Owner_Notified_By_Tax_No = None
                else:
                    Owner_Notified_By_Tax_No = Owner_Notified_By_Tax_No[0]
                Owner_Notified_By_Command = A_n[A_n['x']==437]['description'].values
                if list(Owner_Notified_By_Command) == []:
                    Owner_Notified_By_Command = None
                else:
                    Owner_Notified_By_Command = Owner_Notified_By_Command[0]
                Date = A_n[(A_n['x']>570) & (A_n['x']<700)]['description'].values
                if list(Date) == []:
                    Date = None
                else:
                    Date = Date[0]
                Time = A_n[A_n['x'] > 700]['description'].values
                if list(Time) == []:
                    Time = None
                else:
                    Time = Time[0]
                How_Owner_was_Notified = A_n[(A_n['x']>53) & (A_n['x']<352)]['description'].values
                if list(How_Owner_was_Notified) == []:
                    How_Owner_was_Notified = None
                else:
                    How_Owner_was_Notified = How_Owner_was_Notified[0]
                B.update({"Owner Notified Bt Tax No.": Owner_Notified_By_Tax_No})
                B.update({"Onwer Notified By Command": Owner_Notified_By_Command})
                B.update({"Owner Notified Date": Date})
                B.update({"Owner Notified Time": Time})
                B.update({"How Owner was Notified": How_Owner_was_Notified})
            if A[i]['description'][j] == "Date of Incident":
                a = int((A[i].loc[A[i]['description'] == "Date of Incident"]).index.values)
                b = A[i]['y'][a+5]
                A_n = A[i][A[i]['y']==b].sort_values(by=['x','y']).reset_index(drop=True)
                Date_Of_Incident = A_n['description'][0][0:10]
                Penal_Code = A_n['description'][0][10:-1].lstrip()
                if Penal_Code == "":
                    Penal_Code = None
                Crime_Classification = A_n[A_n['x']==346]['description'].values
                if list(Crime_Classification) == []:
                    Crime_Classification = None
                else:
                    Crime_Classification = Crime_Classification[0]
                Related_To = A_n[(A_n['x']>346) & (A_n['x']<798)]['description'].values
                if list(Related_To) == []:
                    Related_To = None
                else:
                    Related_To = Related_To[0]
                Receipt = A_n[A_n['x'].isin([798,807])]['description'].values
                if list(Receipt) == []:
                    Receipt = None
                else:
                    Receipt = Receipt[0]
                B.update({"Date Of Incident": Date_Of_Incident})
                B.update({"Penal Code/Description": Penal_Code})
                B.update({"Crime Classification": Crime_Classification})
                B.update({"Related To": Related_To})
                B.update({"Receipt": Receipt})
            if A[i]['description'][j] == "Prisoner(s)":
                if A[i][A[i]['x'] == 71].shape[0] != 0:
                    Prisoners = max([int(i) for i in list(A[i][A[i]['x'] == 71]['description'])])
                else:
                    Prisoners = None
                B.update({"Prisoner(s)": Prisoners})
            if A[i]['description'][j] == "Related Invoice(s)":
                Related_Invoices = A[i]['description'][j-1]
                B.update({"Related Invoice(s)": Related_Invoices})
            else:
                B.update({"Related Invoice(s)": None})
        if B != {}:
            D.append(B) 
for i in range(0, len(D)-1):
    if D[i]["Invoice Number"] == D[i+1]["Invoice Number"]:
        D[i].update(D[i+1])
D_n = []
for i in range(0, len(D)):
    if len(D[i]) == 22:
        D_n.append(D[i])
        
General_Frame = pd.DataFrame(D_n)
General_Order = ['Invoice Number', 'Invoice Status', 'Invoice Date', 'Invoicing Command', 'Property Type', 'Property Category', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Arresting Officer Tax No.', 'Arresting Officer Command', 'Owner Notified Bt Tax No.', 'Onwer Notified By Command', 'Owner Notified Date', 'Owner Notified Time', 'How Owner was Notified', 'Date Of Incident', 'Penal Code/Description', 'Crime Classification', 'Related To', 'Receipt', 'Related Invoice(s)', 'Prisoner(s)']
Invoice_Frame = General_Frame[General_Order]

Invoice_Frame.to_csv('Invoice_vehicle_12.csv', sep=',', index = False)