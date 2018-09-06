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
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        try:
            for j in range(0, A[i].shape[0]):
                if A[i]['description'][j] == "Invoice Date":
                    Invoice_Status = A[i]['description'][j+3]
                    if Invoice_Status == 'VOID':
                        B.update({"Time obtained": None})
                        B.update({"Date obtained": None})
                        B.update({"Personel Property Removed": None})
                        B.update({"Recovery Premise Type": None})
                if A[i]['description'][j] == "Vehicle Details":
                    B.update({"Invoice Number": Invoice_No})
                    A_n = A[i][A[i]['y'] == A[i]['y'][j+1]].sort_values(by=['x','y']).reset_index(drop=True)
                    if set(list(A_n['x'])).issubset([133, 254, 431, 564, 743]):
                        Vehicle_year = list(A_n[A_n['x'] == 133]['description'])
                        if Vehicle_year == []:
                            Vehicle_year = None
                        else:
                            Vehicle_year = Vehicle_year[0]
                        Make = list(A_n[A_n['x'] == 254]['description'])
                        if Make == []:
                            Make = None
                        else:
                            Make = Make[0]
                        Model = list(A_n[A_n['x'] == 431]['description'])
                        if Model == []:
                            Model = None
                        else:
                            Model = Model[0]
                        Type = list(A_n[A_n['x'] == 564]['description'])
                        if Type == []:
                            Type = None
                        else:
                            Type = Type[0]
                        Color = list(A_n[A_n['x'] == 743]['description'])
                        if Color == []:
                            Color = None
                        else:
                            Color = Color[0]
                        b = int((A[i].loc[A[i]['description'] == "No. of Lic. Plates:"]).index.values)
                        A_m = A[i][j+1:b+5].sort_values(by=['y','x']).reset_index(drop=True)
                        No_of_Lic_Plates = list(A_m[A_m['x'] == 541]['description'])
                        if No_of_Lic_Plates == []:
                            No_of_Lic_Plates = None
                        else:
                            No_of_Lic_Plates = No_of_Lic_Plates[0]
                        State = list(A_m[A_m['x'] == 454]['description'])[0].split(":")[1]
                        if State == "":
                            State = None
                        else:
                            State = State.lstrip()
                        Yr = list(A_m[A_m['x'] == 603]['description'])[0].split(".")[1]
                        if Yr == "":
                            Yr = None
                        else:
                            Yr = Yr.lstrip()
                        Vehicle_Running = list(A_m[A_m['x'] == 698]['description'])[0].split(":")[1]
                        if Vehicle_Running == "":
                            Vehicle_Running = None
                        else:
                            Vehicle_Running = Vehicle_Running.lstrip()
                    else:
                        Vehicle_year = None
                        Make = None
                        Model = None
                        Type = None
                        Color = None
                        No_of_Lic_Plates = None
                        State = None
                        Yr = None
                        Vehicle_Running = None 
                    B.update({"Vehicle year": Vehicle_year})
                    B.update({"Make": Make})
                    B.update({"Model": Model})
                    B.update({"Type": Type})
                    B.update({"Color": Color})
                    B.update({"No. of Lic. Plates": No_of_Lic_Plates})
                    B.update({"State": State})
                    B.update({"Yr.": Yr})
                    B.update({"Vehicle Running": Vehicle_Running})
                if A[i]['description'][j][:4] == "Time" and A[i]['x'][j] == 53:
                    A_n = A[i][A[i]['y']==A[i]['y'][j]].sort_values(by=['x','y']).reset_index(drop=True)
                    Time = A_n[(A_n['x']>53) & (A_n['x']<180)]['description'].values
                    if list(Time) == []:
                        Time = None
                    else:
                        Time = Time[0]
                    Date = (A_n[A_n['x']==180]['description'].values[0]).split(':')[1]
                    if Date == '':
                        Date = None
                    else:
                        Date = Date.split()[0]
                    Personel_Property_Removed = (A_n[A_n['x'] == 350]['description'].values[0]).split(':')[1]
                    if Personel_Property_Removed == '':
                        Personel_Property_Removed = None
                    else:
                        Personel_Property_Removed = Personel_Property_Removed.split()[0]
                    Recovery_Premise_Type = (A_n[A_n['x'] == 563]['description'].values[0]).split(':')[1]
                    if Recovery_Premise_Type == '':
                        Recovery_Premise_Type = None
                    else:
                        Recovery_Premise_Type = Recovery_Premise_Type.split()[0]
                    B.update({"Time obtained": Time})
                    B.update({"Date obtained": Date})
                    B.update({"Personel Property Removed": Personel_Property_Removed})
                    B.update({"Recovery Premise Type": Recovery_Premise_Type})
            if B != {}:
                D.append(B) 
            
        except:
            print(Invoice_No)

#D.append({'Invoice Number': 4000445666, 'Vehicle year': 2004, 'Make': 'BUICK', 'Model': 'OTHER', 'Type': '4 DOOR SEDAN', 'Color': 'WHITE', "No. of Lic. Plates": 2, "State": 'VE - MX', "Yr.": None, "Vehicle Running": 'NO', "Date obtained": '11/21/2016', "Time obtained": '05:05', "Personel Property Removed": 'No', "Recovery Premise Type": '20 AVENUE AND 49'})
#D.append({'Invoice Number': 3000801909, 'Vehicle year': 2013, 'Make': 'TOYOTA', 'Model': 'Other', 'Type': '2 DOOR SEDAN', 'Color': 'BLACK', "No. of Lic. Plates": 2, "State": 'NY - US', "Yr.": 2018, "Vehicle Running": 'YES', "Date obtained": None, "Time obtained": None, "Personel Property Removed": 'No', "Recovery Premise Type": None})



for i in range(0, len(D)-1):
    if D[i]["Invoice Number"] == D[i+1]["Invoice Number"]:
        D[i].update(D[i+1])
D_n = []
for i in range(0, len(D)):
    if len(D[i]) == 14:
        D_n.append(D[i])

General_Frame = pd.DataFrame(D_n)
Vehicle_Details_Order = ['Invoice Number', 'Vehicle year', 'Make', 'Model', 'Type', 'Color', "No. of Lic. Plates", "State", "Yr.", "Vehicle Running", "Date obtained", "Time obtained", "Personel Property Removed", "Recovery Premise Type"]
Vehicle_Details_Frame = General_Frame[Vehicle_Details_Order]

Vehicle_Details_Frame.to_csv('Vehicle_Details_12.csv', sep=',', index = False)