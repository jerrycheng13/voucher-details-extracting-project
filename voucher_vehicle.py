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

A = read_xml('sample_vehicle.xml')

D = []
Return = []
Vehicle_Details = []
for i in range(0, len(A)):
    B = {}
    C = {}
    if A[i]['description'][0] == "Property Clerk Invoice":
        Invoice_No = A[i]['description'][2]
        #dict
        B.update({"Invoice Number": Invoice_No})
        for j in range(0, A[i].shape[0]):
## Invoice
            if A[i]['description'][j] == "Invoice Date":
                Invoice_Date = A[i]['description'][j+2]
                Invoice_Status = A[i]['description'][j+3]
                if Invoice_Status == 'VOID':
                    B.update({"Time obtained": None})
                    B.update({"Date obtained": None})
                    B.update({"Personel Property Removed": None})
                    B.update({"Recovery Premise Type": None})
                #dict
                B.update({"Invoice Date": Invoice_Date})
                B.update({"Invoice Status": Invoice_Status})
            if A[i]['description'][j] == "Invoicing Command":
                Invoicing_Command = A[i]['description'][j+3]
                Property_Type = A[i]['description'][j+4]
                Property_Category = A[i]['description'][j+5]
                #dict
                B.update({"Invoicing Command": Invoicing_Command})
                B.update({"Property Type": Property_Type})
                B.update({"Property Category": Property_Category})
            if A[i]['description'][j] == "Officers":
                if A[i]['description'][j+5] == "Invoicing":
                    Invoicing_Officer_Tax_No = A[i]['description'][j+3]
                    Invoicing_Officer_Command = A[i]['description'][j+4]
#                    Invoicing = {"Tax No.": A[i]['description'][j+3], "Command": A[i]['description'][j+4]}
                else:
                    Invoicing_Officer_Tax_No = None
                    Invoicing_Officer_Command = None                    
#                    Invoicing = {"Tax No.": None, "Command": None}
                if A[i]['description'][j+9] == "Arresting" or A[i]['description'][j+7] == "Arresting":
                    if A[i]['description'][j+9] == "Arresting":
                        Arresting_Officer_Tax_No = A[i]['description'][j+7]
                        Arresting_Officer_Command = A[i]['description'][j+8]                        
#                        Arresting = {"Tax No.": A[i]['description'][j+6], "Command": A[i]['description'][j+7]}
                    if A[i]['description'][j+7] == "Arresting":
                        Arresting_Officer_Tax_No = None
                        Arresting_Officer_Command = None                        
#                        Arresting = {"Tax No.": None, "Command": None}
                #dict
#                Officers = {"Invoicing": Invoicing, "Arresting": Arresting}
#                B.update({"Officers": Officers})
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
                Crime_Classification = A_n[A_n['x']==346]['description']
                if list(Crime_Classification) == []:
                    Crime_Classification = None
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
                #dict       
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
                #dict
                B.update({"Prisoner(s)": Prisoners})
            if A[i]['description'][j] == "Related Invoice(s)":
                Related_Invoices = A[i]['description'][j-1]
                #dict
                B.update({"Related Invoice(s)": Related_Invoices})
            else:
                B.update({"Related Invoice(s)": None})
## Approval
            if A[i]['description'][j] == "Approvals":
                if A[i]['description'][j+19] == "Approved By":
#                    Entered_By = {"Tax No.": A[i]['description'][j+5], "Command": A[i]['description'][j+6], "Date": A[i]['description'][j+7], "Time": A[i]['description'][j+8]}
#                    Invoicing_Officer = {"Tax No.": A[i]['description'][j+10], "Command": A[i]['description'][j+11], "Date": A[i]['description'][j+12], "Time": A[i]['description'][j+13]}
#                    Approved_By = {"Tax No.": A[i]['description'][j+15], "Command": A[i]['description'][j+16], "Date": A[i]['description'][j+17], "Time": A[i]['description'][j+18]}
                    #dict
#                    Approvals = {"Enter By": Entered_By, "Invoicing Officer": Invoicing_Officer, "Approved By": Approved_By}
#                    B.update({"Approvals": Approvals})
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
## Vehicle Details  
            if A[i]['description'][j] == "Vehicle Details":
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
        D.append(B) 
## Inspection
Inspection = []
for i in range(0, len(A)):  
    if "Inspection Desc: INVOICING INSPECTION" in list(A[i]['description']):
        Invoice_No = A[i]['description'][2]
        if "Inspection Desc: INTAKE INSPECTION" in list(A[i]['description']):
            a = int((A[i].loc[A[i]['description'] == "Inspection Desc: INVOICING INSPECTION"]).index.values)
            b = int((A[i].loc[A[i]['description'] == "Inspection Desc: INTAKE INSPECTION"]).index.values)
            c = int((A[i].loc[A[i]['description'] == "Approvals"]).index.values)
            A1 = A[i][a:b].sort_values(by=['y','x']).reset_index(drop=True)
            A2 = A[i][b:c].sort_values(by=['y','x']).reset_index(drop=True)
### Invoicing Inspection
            Date_Time_1 = A1[A1['x']==395]['description'].values
            if list(Date_Time_1) == []:
                Inspection_Date_1 = None
                Inspection_Time_1 = None
            else:
                Inspection_Date_1 = Date_Time_1[0].split()[0]
                Inspection_Time_1 = Date_Time_1[0].split()[1]
            Tax_ID_1 = A1[A1['x']==516]['description'].values
            if list(Tax_ID_1) == []:
                Tax_ID_1 = None
            else:
                Tax_ID_1 = Tax_ID_1[0].split()[2]
            Number_of_Tires_1 = A1[A1['x']==115]['description'].values
            if list(Number_of_Tires_1) == []:
                Number_of_Tires_1 = None
            else:
                Number_of_Tires_1 = Number_of_Tires_1[0]
            Number_of_Airbags_1 = A1[A1['x']==221]['description'].values
            if list(Number_of_Airbags_1) == []:
                Number_of_Airbags_1 = None
            else:
                Number_of_Airbags_1 = Number_of_Airbags_1[0]    
            Battery_1 = A1[A1['x']==353]['description'].values
            if list(Battery_1) == []:
                Battery_1 = None
            else:
                Battery_1 = Battery_1[0]            
            Radio_1 = A1[A1['x']==475]['description'].values
            if list(Radio_1) == []:
                Radio_1 = None
            else:
                Radio_1 = Radio_1[0]  
            Additional_Audio_Equipment_1 = A1[A1['x']==693]['description'].values
            if list(Additional_Audio_Equipment_1) == []:
                Additional_Audio_Equipment_1 = None
            else:
                Additional_Audio_Equipment_1 = Additional_Audio_Equipment_1[0]  
            Special_Wheels_1 = A1[A1['x']==125]['description'].values
            if list(Special_Wheels_1) == []:
                Special_Wheels_1 = None
            else:
                Special_Wheels_1 = Special_Wheels_1[0]  
            Wheel_Covers_1 = A1[A1['x']==237]['description'].values
            if list(Wheel_Covers_1) == []:
                Wheel_Covers_1 = None
            else:
                Wheel_Covers_1 = Wheel_Covers_1[0] 
            Keys_with_Vehicle_1 = A1[A1['x']==375]['description'].values
            if list(Keys_with_Vehicle_1) == []:
                Keys_with_Vehicle_1 = None
            else:
                Keys_with_Vehicle_1 = Keys_with_Vehicle_1[0] 
            Trunk_1 = A1[A1['x']==542]['description'].values
            if list(Trunk_1) == []:
                Trunk_1 = None
            else:
                Trunk_1 = Trunk_1[0] 
            Glove_Compartment_1 = A1[A1['x']==723]['description'].values
            if list(Glove_Compartment_1) == []:
                Glove_Compartment_1 = None
            else:
                Glove_Compartment_1 = Glove_Compartment_1[0] 
            Exterior_Condition_1 = A1[A1['x']==140]['description'].values
            if list(Exterior_Condition_1) == []:
                Exterior_Condition_1 = None
            else:
                Exterior_Condition_1 = Exterior_Condition_1[0] 
            Interior_Condition_1 = A1[A1['x']==417]['description'].values
            if list(Interior_Condition_1) == []:
                Interior_Condition_1 = None
            else:
                Interior_Condition_1 = Interior_Condition_1[0] 
            Odometer_Reading_1 = A1[A1['x']==693]['description'].values
            if list(Odometer_Reading_1) == []:
                Odometer_Reading_1 = None
            else:
                Odometer_Reading_1 = Odometer_Reading_1[-1] 
            Additional_Equipment_or_Accessories_1 = A1[(A1['x']==55) & (~A1['description'].isin(['Inspection Desc: INVOICING INSPECTION', 'No of Tires:', 'Special Wheels:', 'Exterior Condition:', 'List Missing or Damaged', '(Indicate Which)', 'Parts:']))]['description'].values[0].split(':')[1]
            if list(Additional_Equipment_or_Accessories_1) == '':
                Additional_Equipment_or_Accessories_1 = None
            else:
                Additional_Equipment_or_Accessories_1 = Additional_Equipment_or_Accessories_1.lstrip()           
            List_Missing_or_Damaged_Parts_1 = A1[A1['x']==234]['description'].values
            if list(List_Missing_or_Damaged_Parts_1) == []:
                List_Missing_or_Damaged_Parts_1 = None
            else:
                List_Missing_or_Damaged_Parts_1 = List_Missing_or_Damaged_Parts_1[0] 
            Comments_1 = A1[A1['x']==414]['description'].values
            if list(Comments_1) == []:
                Comments_1 = None
            else:
                Comments_1 = Comments_1[0] 
### Intake Inspection
            Date_Time_2 = A2[A2['x']==395]['description'].values
            if list(Date_Time_2) == []:
                Inspection_Date_2 = None
                Inspection_Time_2 = None
            else:
                Inspection_Date_2 = Date_Time_2[0].split()[0]
                Inspection_Time_2 = Date_Time_2[0].split()[1]
            Tax_ID_2 = A2[A2['x']==516]['description'].values
            if list(Tax_ID_2) == []:
                Tax_ID_2 = None
            else:
                Tax_ID_2 = Tax_ID_2[0].split()[2]
            Number_of_Tires_2 = A2[A2['x']==115]['description'].values
            if list(Number_of_Tires_2) == []:
                Number_of_Tires_2 = None
            else:
                Number_of_Tires_2 = Number_of_Tires_2[0]
            Number_of_Airbags_2 = A2[A2['x']==221]['description'].values
            if list(Number_of_Airbags_2) == []:
                Number_of_Airbags_2 = None
            else:
                Number_of_Airbags_2 = Number_of_Airbags_2[0]  
            Battery_2 = A2[A2['x']==353]['description'].values
            if list(Battery_2) == []:
                Battery_2 = None
            else:
                Battery_2 = Battery_2[0]            
            Radio_2 = A2[A2['x']==475]['description'].values
            if list(Radio_2) == []:
                Radio_2 = None
            else:
                Radio_2 = Radio_2[0]              
            Additional_Audio_Equipment_2 = A2[A2['x']==693]['description'].values
            if list(Additional_Audio_Equipment_2) == []:
                Additional_Audio_Equipment_2 = None
            else:
                Additional_Audio_Equipment_2 = Additional_Audio_Equipment_2[0]             
            Special_Wheels_2 = A2[A2['x']==125]['description'].values
            if list(Special_Wheels_2) == []:
                Special_Wheels_2 = None
            else:
                Special_Wheels_2 = Special_Wheels_2[0]    
            Wheel_Covers_2 = A2[A2['x']==237]['description'].values
            if list(Wheel_Covers_2) == []:
                Wheel_Covers_2 = None
            else:
                Wheel_Covers_2 = Wheel_Covers_2[0]                 
            Keys_with_Vehicle_2 = A2[A2['x']==375]['description'].values
            if list(Keys_with_Vehicle_2) == []:
                Keys_with_Vehicle_2 = None
            else:
                Keys_with_Vehicle_2 = Keys_with_Vehicle_2[0] 
            Trunk_2 = A2[A2['x']==542]['description'].values
            if list(Trunk_2) == []:
                Trunk_2 = None
            else:
                Trunk_2 = Trunk_2[0] 
            Glove_Compartment_2 = A2[A2['x']==723]['description'].values
            if list(Glove_Compartment_2) == []:
                Glove_Compartment_2 = None
            else:
                Glove_Compartment_2 = Glove_Compartment_2[0] 
            Exterior_Condition_2 = A2[A2['x']==140]['description'].values
            if list(Exterior_Condition_2) == []:
                Exterior_Condition_2 = None
            else:
                Exterior_Condition_2 = Exterior_Condition_2[0] 
            Interior_Condition_2 = A2[A2['x']==417]['description'].values
            if list(Interior_Condition_2) == []:
                Interior_Condition_2 = None
            else:
                Interior_Condition_2 = Interior_Condition_2[0] 
            Odometer_Reading_2 = A2[A2['x']==693]['description'].values
            if list(Odometer_Reading_2) == []:
                Odometer_Reading_2 = None
            else:
                Odometer_Reading_2 = Odometer_Reading_2[-1]                             
            Additional_Equipment_or_Accessories_2 = A2[(A2['x']==55) & (~A2['description'].isin(['Inspection Desc: INVOICING INSPECTION', 'No of Tires:', 'Special Wheels:', 'Exterior Condition:', 'List Missing or Damaged', '(Indicate Which)', 'Parts:']))]['description'].values[0].split(':')[1]
            if list(Additional_Equipment_or_Accessories_2) == '':
                Additional_Equipment_or_Accessories_2 = None
            else:
                Additional_Equipment_or_Accessories_2 = Additional_Equipment_or_Accessories_2.lstrip()                           
            List_Missing_or_Damaged_Parts_2 = A2[A2['x']==234]['description'].values
            if list(List_Missing_or_Damaged_Parts_2) == []:
                List_Missing_or_Damaged_Parts_2 = None
            else:
                List_Missing_or_Damaged_Parts_2 = List_Missing_or_Damaged_Parts_2[0]                 
            Comments_2 = A2[A2['x']==414]['description'].values
            if list(Comments_2) == []:
                Comments_2 = None
            else:
                Comments_2 = Comments_2[0]                 
            Inspection.append(pd.DataFrame({'Invoice Number': [Invoice_No], 'Inspection Desc.': 'INVOICING INSPECTION', 'Inspection Date': [Inspection_Date_1], 'Inspection Time': [Inspection_Time_1], 'Tax ID': [Tax_ID_1], 'Number of Tires': [Number_of_Tires_1], 'Number of Airbags': [Number_of_Airbags_1], 'Battery': [Battery_1], 'Radio': [Radio_1], 'Additional Audio Equipment': [Additional_Audio_Equipment_1], 'Special Wheels': [Special_Wheels_1], 'Wheel Covers': [Wheel_Covers_1], 'Keys with Vehicle': [Keys_with_Vehicle_1], 'Trunk': [Trunk_1], 'Glove Compartment': [Glove_Compartment_1], 'Exterior Condition': [Exterior_Condition_1], 'Interior Condition': [Interior_Condition_1], 'Odometer Reading': [Odometer_Reading_1], 'Additional Equipment or Accessories': [Additional_Equipment_or_Accessories_1], 'List Missing or Damaged Parts': [List_Missing_or_Damaged_Parts_1], 'Comments': [Comments_1]}))            
            Inspection.append(pd.DataFrame({'Invoice Number': [Invoice_No], 'Inspection Desc.': 'INTAKE INSPECTION', 'Inspection Date': [Inspection_Date_2], 'Inspection Time': [Inspection_Time_2], 'Tax ID': [Tax_ID_2], 'Number of Tires': [Number_of_Tires_2], 'Number of Airbags': [Number_of_Airbags_2], 'Battery': [Battery_2], 'Radio': [Radio_2], 'Additional Audio Equipment': [Additional_Audio_Equipment_2], 'Special Wheels': [Special_Wheels_2], 'Wheel Covers': [Wheel_Covers_2], 'Keys with Vehicle': [Keys_with_Vehicle_2], 'Trunk': [Trunk_2], 'Glove Compartment': [Glove_Compartment_2], 'Exterior Condition': [Exterior_Condition_2], 'Interior Condition': [Interior_Condition_2], 'Odometer Reading': [Odometer_Reading_2], 'Additional Equipment or Accessories': [Additional_Equipment_or_Accessories_2], 'List Missing or Damaged Parts': [List_Missing_or_Damaged_Parts_2], 'Comments': [Comments_2]}))  
        else:
            a = int((A[i].loc[A[i]['description'] == "Inspection Desc: INVOICING INSPECTION"]).index.values)
            c = int((A[i].loc[A[i]['description'] == "Approvals"]).index.values)
            A1 = A[i][a:c].sort_values(by=['y','x']).reset_index(drop=True)
            Date_Time_1 = A1[A1['x']==395]['description'].values
            if list(Date_Time_1) == []:
                Inspection_Date_1 = None
                Inspection_Time_1 = None
            else:
                Inspection_Date_1 = Date_Time_1[0].split()[0]
                Inspection_Time_1 = Date_Time_1[0].split()[1]
            Tax_ID_1 = A1[A1['x']==516]['description'].values
            if list(Tax_ID_1) == []:
                Tax_ID_1 = None
            else:
                Tax_ID_1 = Tax_ID_1[0].split()[2]
            Number_of_Tires_1 = A1[A1['x']==115]['description'].values
            if list(Number_of_Tires_1) == []:
                Number_of_Tires_1 = None
            else:
                Number_of_Tires_1 = Number_of_Tires_1[0]  
            Number_of_Airbags_1 = A1[A1['x']==221]['description'].values
            if list(Number_of_Airbags_1) == []:
                Number_of_Airbags_1 = None
            else:
                Number_of_Airbags_1 = Number_of_Airbags_1[0]  
            Battery_1 = A1[A1['x']==353]['description'].values
            if list(Battery_1) == []:
                Battery_1 = None
            else:
                Battery_1 = Battery_1[0]            
            Radio_1 = A1[A1['x']==475]['description'].values
            if list(Radio_1) == []:
                Radio_1 = None
            else:
                Radio_1 = Radio_1[0]                 
            Additional_Audio_Equipment_1 = A1[A1['x']==693]['description'].values
            if list(Additional_Audio_Equipment_1) == []:
                Additional_Audio_Equipment_1 = None
            else:
                Additional_Audio_Equipment_1 = Additional_Audio_Equipment_1[0] 
            Special_Wheels_1 = A1[A1['x']==125]['description'].values
            if list(Special_Wheels_1) == []:
                Special_Wheels_1 = None
            else:
                Special_Wheels_1 = Special_Wheels_1[0] 
            Wheel_Covers_1 = A1[A1['x']==237]['description'].values
            if list(Wheel_Covers_1) == []:
                Wheel_Covers_1 = None
            else:
                Wheel_Covers_1 = Wheel_Covers_1[0] 
            Keys_with_Vehicle_1 = A1[A1['x']==375]['description'].values
            if list(Keys_with_Vehicle_1) == []:
                Keys_with_Vehicle_1 = None
            else:
                Keys_with_Vehicle_1 = Keys_with_Vehicle_1[0] 
            Trunk_1 = A1[A1['x']==542]['description'].values
            if list(Trunk_1) == []:
                Trunk_1 = None
            else:
                Trunk_1 = Trunk_1[0] 
            Glove_Compartment_1 = A1[A1['x']==723]['description'].values
            if list(Glove_Compartment_1) == []:
                Glove_Compartment_1 = None
            else:
                Glove_Compartment_1 = Glove_Compartment_1[0] 
            Exterior_Condition_1 = A1[A1['x']==140]['description'].values
            if list(Exterior_Condition_1) == []:
                Exterior_Condition_1 = None
            else:
                Exterior_Condition_1 = Exterior_Condition_1[0] 
            Interior_Condition_1 = A1[A1['x']==417]['description'].values
            if list(Interior_Condition_1) == []:
                Interior_Condition_1 = None
            else:
                Interior_Condition_1 = Interior_Condition_1[0] 
            Odometer_Reading_1 = A1[A1['x']==693]['description'].values
            if list(Odometer_Reading_1) == []:
                Odometer_Reading_1 = None
            else:
                Odometer_Reading_1 = Odometer_Reading_1[-1]             
            Additional_Equipment_or_Accessories_1 = A1[(A1['x']==55) & (~A1['description'].isin(['Inspection Desc: INVOICING INSPECTION', 'No of Tires:', 'Special Wheels:', 'Exterior Condition:', 'List Missing or Damaged', '(Indicate Which)', 'Parts:']))]['description'].values[0].split(':')[1]
            if list(Additional_Equipment_or_Accessories_1) == '':
                Additional_Equipment_or_Accessories_1 = None
            else:
                Additional_Equipment_or_Accessories_1 = Additional_Equipment_or_Accessories_1.lstrip()           
            List_Missing_or_Damaged_Parts_1 = A1[A1['x']==234]['description'].values
            if list(List_Missing_or_Damaged_Parts_1) == []:
                List_Missing_or_Damaged_Parts_1 = None
            else:
                List_Missing_or_Damaged_Parts_1 = List_Missing_or_Damaged_Parts_1[0]                 
            Comments_1 = A1[A1['x']==414]['description'].values
            if list(Comments_1) == []:
                Comments_1 = None
            else:
                Comments_1 = Comments_1[0]                      
            Inspection.append(pd.DataFrame({'Invoice Number': [Invoice_No], 'Inspection Desc.': 'INVOICING INSPECTION', 'Inspection Date': [Inspection_Date_1], 'Inspection Time': [Inspection_Time_1], 'Tax ID': [Tax_ID_1], 'Number of Tires': [Number_of_Tires_1], 'Number of Airbags': [Number_of_Airbags_1], 'Battery': [Battery_1], 'Radio': [Radio_1], 'Additional Audio Equipment': [Additional_Audio_Equipment_1], 'Special Wheels': [Special_Wheels_1], 'Wheel Covers': [Wheel_Covers_1], 'Keys with Vehicle': [Keys_with_Vehicle_1], 'Trunk': [Trunk_1], 'Glove Compartment': [Glove_Compartment_1], 'Exterior Condition': [Exterior_Condition_1], 'Interior Condition': [Interior_Condition_1], 'Odometer Reading': [Odometer_Reading_1], 'Additional Equipment or Accessories': [Additional_Equipment_or_Accessories_1], 'List Missing or Damaged Parts': [List_Missing_or_Damaged_Parts_1], 'Comments': [Comments_1]}))
    
## Return         
    if A[i]['description'][0] == "PROPERTY RETURN RECEIPT":
        Invoice_No = A[i]['description'][3]
        Delivery_No = A[i]['description'][4]
        for j in range(0, A[i].shape[0]):
            if A[i]['description'][j] == "Item":
                a = int((A[i].loc[A[i]['description'] == "Item"]).index.values)
                b = int((A[i].loc[A[i]['description'] == "Returning Officer"]).index.values)
                A_n = A[i][a+3:b-1].sort_values(by=['x','y']).reset_index(drop=True)
                A_m = A_n.sort_values(by=['y','x']).reset_index(drop=True)
                Item = A_m[A_m['x'] <= 60]["description"].reset_index(drop=True)
                Quantity = A_m[A_m['x'] >= 739]["description"].reset_index(drop=True)
                Article_Description = A_m[(A_n['x'] >= 165) & (A_m['x'] < 739)].sort_values(by=['y','x']).reset_index(drop=True)
                Article_Description = Article_Description['description'].reset_index(drop=True)
                for k in range(1, len(Article_Description)):
                    if Article_Description[k] == "VEHICLE / BOAT |VEHICLE":
                        Article_Description[k-1] += ","
                Article_Description = (" ".join(list(Article_Description))).split(", ")
            if A[i]['description'][j] == "Returning Officer":
                Tax_No = A[i]['description'][j+5]
                Command = A[i]['description'][j+6]
                Date = A[i]['description'][j+7]
                Time = A[i]['description'][j+8]
        Return.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Delivery Number': Delivery_No, 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity)}))
        
for i in range(0, len(D)-1):
    if D[i]["Invoice Number"] == D[i+1]["Invoice Number"]:
        D[i].update(D[i+1])
D_n = []
for i in range(0, len(D)):
    if len(D[i]) == 45:
        D_n.append(D[i])
        
General_Frame = pd.DataFrame(D_n)
General_Order = ['Invoice Number', 'Invoice Status', 'Invoice Date', 'Invoicing Command', 'Property Type', 'Property Category', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Arresting Officer Tax No.', 'Arresting Officer Command', 'Owner Notified Bt Tax No.', 'Onwer Notified By Command', 'Owner Notified Date', 'Owner Notified Time', 'How Owner was Notified', 'Date Of Incident', 'Penal Code/Description', 'Crime Classification', 'Related To', 'Receipt', 'Related Invoice(s)', 'Prisoner(s)']
Invoice_Frame = General_Frame[General_Order]
Approvals_Order = ['Invoice Number', 'Entered By Tax No.', 'Entered By Command', 'Entered By Date', 'Entered By Time', 'Invoicing Officer Tax No.', 'Invoicing Officer Command', 'Invoicing Officer Date', 'Invoicing Officer Time', 'Approved By Tax No.', 'Approved By Command', 'Approved By Date', 'Approved By Time']
Approvals_Frame = General_Frame[Approvals_Order]
Vehicle_Details_Order = ['Invoice Number', 'Vehicle year', 'Make', 'Model', 'Type', 'Color', "No. of Lic. Plates", "State", "Yr.", "Vehicle Running", "Date obtained", "Time obtained", "Personel Property Removed", "Recovery Premise Type"]
Vehicle_Details_Frame = General_Frame[Vehicle_Details_Order]

Vehicle_Inspection_Frame = pd.concat(Inspection)
Vehicle_Inspection_Order = ['Invoice Number', 'Inspection Desc.', 'Inspection Date', 'Inspection Time', 'Tax ID', 'Number of Tires', 'Number of Airbags', 'Battery', 'Radio', 'Additional Audio Equipment', 'Special Wheels', 'Wheel Covers', 'Keys with Vehicle', 'Trunk', 'Glove Compartment', 'Exterior Condition', 'Interior Condition', 'Odometer Reading', 'Additional Equipment or Accessories', 'List Missing or Damaged Parts', 'Comments']
Vehicle_Inspection_Frame = Vehicle_Inspection_Frame[Vehicle_Inspection_Order]

Return_Forms = pd.concat(Return)
Return_Order = ['Invoice Number', 'Delivery Number', 'Returning Officer Tax No.', 'Returning Officer Command', 'Return Date', 'Return Time', 'Item (Number)', "Returning Article Description", "Return Quantity"]
Return_Frame = Return_Forms[Return_Order]


        
Invoice_Frame.to_csv('Invoice_vehicle.csv', sep=',', index = False)
Approvals_Frame.to_csv('Approvals_vehicle.csv', sep=',', index = False)
Vehicle_Details_Frame.to_csv('Vehicle_Details.csv', sep=',', index = False)
Vehicle_Inspection_Frame.to_csv('Vehicle_Inspection.csv', sep=',', index = False)
Return_Frame.to_csv('Return_vehicle.csv', sep=',', index = False)
            
        
