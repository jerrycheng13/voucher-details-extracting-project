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

def export_csv(file1,file2):
    A = read_xml(file1)
    D = []
    C1 = []
    C2 = []
    for i in range(0, len(A)):    
        if A[i]['description'][0] == "Property Clerk Invoice":
            Invoice_No = A[i]['description'][2]
            if Invoice_No not in C1:
                B = {'Date Of Incident':None, 'Penal Code/Description':None, 'Crime Classification':None, 'Related To':None, 'Receipt':None}
                C1.append(Invoice_No)
            B["Invoice Number"] = Invoice_No
            for j in range(0, A[i].shape[0]):
                if A[i]['description'][j] == "Invoicing Command":
                    Invocing_Command = A[i]['description'][j+2]
                    Invoice_Status = A[i]['description'][j+3]
                    B["Invoicing Command"] = Invocing_Command
                    B["Invoice Status"] = Invoice_Status
                if A[i]['description'][j] == "Invoice Date":
                    Invoice_Date = A[i]['description'][j+3]
                    Property_Type = A[i]['description'][j+4]
                    Property_Category = A[i]['description'][j+5]
                    B["Invoice Date"] = Invoice_Date
                    B["Property Type"] = Property_Type
                    B["Property Category"] = Property_Category
                if A[i]['description'][j] == "Officers":
                    if A[i]['description'][j+5] == "Invoicing":
                        Invoicing_Officer_Tax_No = A[i]['description'][j+3]
                        Invoicing_Officer_Command = A[i]['description'][j+4]
                    else:
                        Invoicing_Officer_Tax_No = None
                        Invoicing_Officer_Command = None                    
                    if A[i]['description'][j+8] == "Arresting" or A[i]['description'][j+6] == "Arresting":
                        if A[i]['description'][j+8] == "Arresting":
                            Arresting_Officer_Tax_No = A[i]['description'][j+6]
                            Arresting_Officer_Command = A[i]['description'][j+7]                        
                        if A[i]['description'][j+6] == "Arresting":
                            Arresting_Officer_Tax_No = None
                            Arresting_Officer_Command = None                             
                    B["Invoicing Officer Tax No."] = Invoicing_Officer_Tax_No
                    B["Invoicing Officer Command"] = Invoicing_Officer_Command
                    B["Arresting Officer Tax No."] = Arresting_Officer_Tax_No
                    B["Arresting Officer Command"] = Arresting_Officer_Command
                if A[i]['description'][j] == "Date Of Incident":
                    a = int((A[i].loc[A[i]['description'] == "Date Of Incident"]).index.values)
                    b = A[i]['y'][a+5]
                    A_n = A[i][A[i]['y']==b].sort_values(by=['x','y']).reset_index(drop=True)
                    Date_Of_Incident = A_n['description'][0][0:10]
                    Penal_Code = A_n['description'][0][10:].lstrip()
                    if Penal_Code == "":
                        Penal_Code = None
                    Crime_Classification = A_n[A_n['x']==349]['description'].values
                    if list(Crime_Classification) == []:
                        Crime_Classification = None
                    else:
                        Crime_Classification = Crime_Classification[0]
                    Related_To = A_n[A_n['x']==457]['description'].values
                    if list(Related_To) == []:
                        Related_To = None
                    else:
                        Related_To = Related_To[0]
                    Receipt = A_n[A_n['x'].isin([810,800])]['description'].values
                    if list(Receipt) == []:
                        Receipt = None
                    else:
                        Receipt = Receipt[0]
                    if Date_Of_Incident == 'Prisoner(s':
                        Date_Of_Incident = None
                    if Penal_Code == ')':
                        Penal_Code = None
                    B["Date Of Incident"] = Date_Of_Incident
                    B["Penal Code/Description"] = Penal_Code
                    B["Crime Classification"] = Crime_Classification
                    B["Related To"] = Related_To
                    B["Receipt"] = Receipt
                if A[i]['description'][j] == "Prisoner(s)":
                    if A[i][A[i]['x'] == 69].shape[0] != 0:
                        Prisoners = max([int(i) for i in list(A[i][A[i]['x'] == 69]['description'])])
                    else:
                        Prisoners = None
                    B["Prisoner(s)"] = Prisoners
                if A[i]['description'][j] == "Related Invoice(s)":
                    Related_Invoices = A[i]['description'][j-1]
                    B["Related Invoice(s)"] = Related_Invoices
            if len(B) == 17 and B["Invoice Number"] not in C2:
                D.append(B) 
                C2.append(B["Invoice Number"])

    General_Frame = pd.DataFrame(D)
    General_Order = ['Invoice Number', 'Invoice Status', 'Invoice Date', 'Invoicing Command', 'Property Type', 'Property Category', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Arresting Officer Tax No.', 'Arresting Officer Command', 'Date Of Incident', 'Penal Code/Description', 'Crime Classification', 'Related To', 'Receipt', 'Related Invoice(s)', 'Prisoner(s)']
    Invoice_Frame = General_Frame[General_Order]

    Invoice_Frame.to_csv(file2, sep=',', index = False)



export_csv('Cell_Phone_1.xml','Invoice_cell_phone_1.csv')
export_csv('Cell_Phone_2.xml','Invoice_cell_phone_2.csv')
export_csv('Cell_Phone_3.xml','Invoice_cell_phone_3.csv')
export_csv('Cell_Phone_4.xml','Invoice_cell_phone_4.csv')
export_csv('Cell_Phone_5.xml','Invoice_cell_phone_5.csv')
export_csv('Cell_Phone_6.xml','Invoice_cell_phone_6.csv')
export_csv('Cell_Phone_7.xml','Invoice_cell_phone_7.csv')
export_csv('Cell_Phone_8.xml','Invoice_cell_phone_8.csv')
export_csv('Cell_Phone_9.xml','Invoice_cell_phone_9.csv')
export_csv('Cell_Phone_10.xml','Invoice_cell_phone_10.csv')
export_csv('Cell_Phone_11.xml','Invoice_cell_phone_11.csv')
export_csv('Cell_Phone_12.xml','Invoice_cell_phone_12.csv')
export_csv('Cell_Phone_13.xml','Invoice_cell_phone_13.csv')
export_csv('Cell_Phone_14.xml','Invoice_cell_phone_14.csv')
export_csv('Cell_Phone_15.xml','Invoice_cell_phone_15.csv')
export_csv('Cell_Phone_16.xml','Invoice_cell_phone_16.csv')
export_csv('Cell_Phone_17.xml','Invoice_cell_phone_17.csv')
export_csv('Cell_Phone_18.xml','Invoice_cell_phone_18.csv')
export_csv('Cell_Phone_19.xml','Invoice_cell_phone_19.csv')
export_csv('Cell_Phone_20.xml','Invoice_cell_phone_20.csv')
export_csv('Cell_Phone_21.xml','Invoice_cell_phone_21.csv')
export_csv('Cell_Phone_22.xml','Invoice_cell_phone_22.csv')
export_csv('Cell_Phone_23.xml','Invoice_cell_phone_23.csv')
