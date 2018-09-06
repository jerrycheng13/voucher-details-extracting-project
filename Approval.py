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

A = read_xml('Cell_Phone_23.xml')

D = []
for i in range(0, len(A)):
    B = {}
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        for j in range(0, A[i].shape[0]):
            if A[i]['description'][j] == "Approvals":
                if A[i]['description'][j+19] == "Approved By":
                    B.update({"Invoice Number": Invoice_No})
                    B.update({"Entered By Tax No.": A[i]['description'][j+5]})
                    B.update({"Entered By Command": A[i]['description'][j+6]})
                    B.update({"Entered By Date": A[i]['description'][j+7]})
                    B.update({"Entered By Time": A[i]['description'][j+8]})
                    B.update({"Invoicing Officer Tax No.": A[i]['description'][j+10]})
                    B.update({"Invoicing Officer Command": A[i]['description'][j+11]})
                    B.update({"Invoicing Officer Date": A[i]['description'][j+12]})
                    B.update({"Invoicing Officer Time": A[i]['description'][j+13]})
                    B.update({"Approved By Tax No.": A[i]['description'][j+15]})
                    B.update({"Approved By Command": A[i]['description'][j+16]})
                    B.update({"Approved By Date": A[i]['description'][j+17]})
                    B.update({"Approved By Time": A[i]['description'][j+18]})   
                else:
                    B.update({"Invoice Number": Invoice_No})
                    B.update({"Entered By Tax No.": A[i]['description'][j+5]})
                    B.update({"Entered By Command": A[i]['description'][j+6]})
                    B.update({"Entered By Date": A[i]['description'][j+7]})
                    B.update({"Entered By Time": A[i]['description'][j+8]})
                    B.update({"Invoicing Officer Tax No.": A[i]['description'][j+10]})
                    B.update({"Invoicing Officer Command": A[i]['description'][j+11]})
                    B.update({"Invoicing Officer Date": A[i]['description'][j+12]})
                    B.update({"Invoicing Officer Time": A[i]['description'][j+13]})
                    B.update({"Approved By Tax No.": None})
                    B.update({"Approved By Command": None})
                    B.update({"Approved By Date": None})
                    B.update({"Approved By Time": None}) 
        if B != {}:
            D.append(B) 
General_Frame = pd.DataFrame(D)
Approvals_Order = ['Invoice Number', 'Entered By Tax No.', 'Entered By Command', 'Entered By Date', 'Entered By Time', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Invoicing Officer Date', 'Invoicing Officer Time', 'Approved By Tax No.', 'Approved By Command', 'Approved By Date', 'Approved By Time']
Approvals_Frame = General_Frame[Approvals_Order]

Approvals_Frame.to_csv('Approvals_cell_phone_23.csv', sep=',', index = False)
