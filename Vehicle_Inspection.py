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

def Bi(i):
    group_index = list((A[i].loc[A[i]['description'] == "Inspection Desc"]).index.values)
    group_number = len(group_index)
    B = []
    if group_number != 1:
        for j in range(0, group_number-1):
            B.append(A[i][group_index[j]:group_index[j+1]].sort_values(by=['y','x']).reset_index(drop=True))
        B.append(A[i][group_index[-1]:].sort_values(by=['y','x']).reset_index(drop=True))  
    else:
        B = [A[i][group_index[0]:].sort_values(by=['y','x']).reset_index(drop=True)]
    return B

A = read_xml('Vehicle_12.xml')
for i in range(0, len(A)): 
    if "Inspection Desc: INVOICING INSPECTION" in list(A[i]['description']) or "Inspection Desc: INTAKE INSPECTION" in list(A[i]['description']):
        A[i].insert(3, 'kind', None)
        for j in range(0, len(A[i])):
            if A[i]['description'][j] == "Inspection Desc: INVOICING INSPECTION":
                A[i]['description'][j] = "Inspection Desc"
                A[i]['kind'][j] = 'INVOICING INSPECTION'
            if A[i]['description'][j] == "Inspection Desc: INTAKE INSPECTION":
                A[i]['description'][j] = "Inspection Desc"
                A[i]['kind'][j] = 'INTAKE INSPECTION'
        if "Approvals" in list(A[i]['description']):
            end = int((A[i].loc[A[i]['description'] == "Approvals"]).index.values)        
        else:
            end = int((A[i].loc[A[i]['description'] == "PCD Storage No."]).index.values)
        A[i] = A[i][:end]    
    if i % 1000 == 0:
        print(i/len(A))


Error = []
Inspection = []
for i in range(0, len(A)):  
    if "Inspection Desc" in list(A[i]['description']):
        Invoice_No = A[i]['description'][2]
        try:
            B = Bi(i)
            if "Parts:" not in list(B[-1]['description']):
                if "Approvals" in list(A[i+1]['description']) or "PCD Storage No." in list(A[i+1]['description']):
                    if "Approvals" in list(A[i+1]['description']) and "PCD Storage No." not in list(A[i+1]['description']):
                        end = int((A[i+1].loc[A[i+1]['description'] == "Approvals"]).index.values) 
                        C = A[i+1][4:end].reset_index(drop=True)
                    if "Approvals" not in list(A[i+1]['description']) and "PCD Storage No." in list(A[i+1]['description']):
                        end = int((A[i+1].loc[A[i+1]['description'] == "PCD Storage No."]).index.values)
                        C = A[i+1][4:end].reset_index(drop=True)
                    else:
                        end = int((A[i+1].loc[A[i+1]['description'] == "Approvals"]).index.values) 
                        C = A[i+1][4:end].reset_index(drop=True)
                else:
                    C = A[i+1][4:].reset_index(drop=True)
                if "Inspection Desc" in list(C['description']):
                    end_c = list((C.loc[C['description'] == "Inspection Desc"]).index.values)[0]
                    C = C[:end_c]
                C['y'] += 10000
                B[-1] = pd.concat([B[-1],C], axis = 0).sort_values(by=['y','x']).reset_index(drop=True) 
            for j in range(0, len(B)):
## Inspection Desc
                Inspection_Desc = B[j]['kind'][0]             
## Date Time
                Date_Time = B[j][B[j]['x']==395]['description'].values
                if list(Date_Time) == []:
                    Date = [None]
                    Time = [None]
                else:
                    Inspection_Date = Date_Time[0].split()[0]
                    Inspection_Time = Date_Time[0].split()[1]
## Tax ID                
                Tax_ID = B[j][B[j]['x']==516]['description'].values
                if list(Tax_ID) == []:
                    Tax_ID = [None]
                else:
                    Tax_ID = Tax_ID[0].split()[2]
## No of Tires
                Number_of_Tires = B[j][B[j]['x']==115]['description'].values
                if list(Number_of_Tires) == []:
                    Number_of_Tires = [None]
                else:
                    Number_of_Tires = Number_of_Tires[0]
## No of Airbags
                Number_of_Airbags = B[j][B[j]['x']==221]['description'].values
                if list(Number_of_Airbags) == []:
                    Number_of_Airbags = [None]
                else:
                    Number_of_Airbags = Number_of_Airbags[0] 
## Battery
                Battery = B[j][B[j]['x']==353]['description'].values
                if list(Battery) == []:
                    Battery = [None]
                else:
                    Battery = Battery[0] 
## Radio
                Radio = B[j][B[j]['x']==475]['description'].values
                if list(Radio) == []:
                    Radio = [None]
                else:
                    Radio = Radio[0] 
## Additional_Audio_Equipment
                Additional_Audio_Equipment = B[j][B[j]['x']==693]['description'].values
                if list(Additional_Audio_Equipment) == []:
                    Additional_Audio_Equipment = [None]
                else:
                    Additional_Audio_Equipment = Additional_Audio_Equipment[0] 
## Special Wheels
                Special_Wheels = B[j][B[j]['x']==125]['description'].values
                if list(Special_Wheels) == []:
                    Special_Wheels = [None]
                else:
                    Special_Wheels = Special_Wheels[0]  
## Wheel Covers
                Wheel_Covers = B[j][B[j]['x']==237]['description'].values
                if list(Wheel_Covers) == []:
                    Wheel_Covers = [None]
                else:
                    Wheel_Covers = Wheel_Covers[0] 
## Keys with Vehicle
                Keys_with_Vehicle = B[j][B[j]['x']==375]['description'].values
                if list(Keys_with_Vehicle) == []:
                    Keys_with_Vehicle = [None]
                else:
                    Keys_with_Vehicle = Keys_with_Vehicle[0] 
## Trunk
                Trunk = B[j][B[j]['x']==542]['description'].values
                if list(Trunk) == []:
                    Trunk = [None]
                else:
                    Trunk = Trunk[0] 
## Glove Compartment
                Glove_Compartment = B[j][B[j]['x']==723]['description'].values
                if list(Glove_Compartment) == []:
                    Glove_Compartment = [None]
                else:
                    Glove_Compartment = Glove_Compartment[0] 
## Exterior Condition
                Exterior_Condition = B[j][B[j]['x']==140]['description'].values
                if list(Exterior_Condition) == []:
                    Exterior_Condition = [None]
                else:
                    Exterior_Condition = Exterior_Condition[0] 
## Interior Condition
                Interior_Condition = B[j][B[j]['x']==417]['description'].values
                if list(Interior_Condition) == []:
                    Interior_Condition = [None]
                else:
                    Interior_Condition = Interior_Condition[0] 
## Odometer Reading
                Odometer_Reading = B[j][B[j]['x']==693]['description'].values
                if list(Odometer_Reading) == []:
                    Odometer_Reading = [None]
                else:
                    Odometer_Reading = Odometer_Reading[-1] 
## Additional Equipment or Accessories
                Additional_Equipment_or_Accessories = B[j][(B[j]['x']==55) & (~B[j]['description'].isin(['Inspection Desc', 'No of Tires:', 'Special Wheels:', 'Exterior Condition:', 'List Missing or Damaged', '(Indicate Which)', 'Parts:']))]['description'].values[0].split(':')[1]
                if Additional_Equipment_or_Accessories == '':
                    Additional_Equipment_or_Accessories = [None]
                else:
                    Additional_Equipment_or_Accessories = Additional_Equipment_or_Accessories[1:]          
## List Missing or Damaged Parts
                List_Missing_or_Damaged_Parts = B[j][B[j]['x']==234]['description'].reset_index(drop=True)
                if list(List_Missing_or_Damaged_Parts) == []:
                    List_Missing_or_Damaged_Parts = [None]
                else:
                    List_Missing_or_Damaged_Parts = (" ".join(list(List_Missing_or_Damaged_Parts))) 
## Comments
                Comments = B[j][(B[j]['x']>=408) & (B[j]['x']<=414)]['description'].reset_index(drop=True)
                if list(Comments) == []:
                    Comments = [None]
                else:
                    Comments = (" ".join(list(Comments)))                      

                Inspection.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Inspection Desc.': Inspection_Desc, 'Inspection Date': Inspection_Date, 'Inspection Time': Inspection_Time, 'Tax ID': Tax_ID, 'Number of Tires': Number_of_Tires, 'Number of Airbags': Number_of_Airbags, 'Battery': Battery, 'Radio': Radio, 'Additional Audio Equipment': Additional_Audio_Equipment, 'Special Wheels': Special_Wheels, 'Wheel Covers': Wheel_Covers, 'Keys with Vehicle': Keys_with_Vehicle, 'Trunk': Trunk, 'Glove Compartment': Glove_Compartment, 'Exterior Condition': Exterior_Condition, 'Interior Condition': Interior_Condition, 'Odometer Reading': Odometer_Reading, 'Additional Equipment or Accessories': Additional_Equipment_or_Accessories, 'List Missing or Damaged Parts': List_Missing_or_Damaged_Parts, 'Comments': Comments}, index = [0]))
        except:
            print(i+1, Invoice_No)
            Error.append([i+1,j+1, Invoice_No, Inspection_Desc, Inspection_Date, Inspection_Time, Tax_ID, 'Number of Tires', 'Number of Airbags', 'Battery', 'Radio', 'Additional Audio Equipment', 'Special Wheels', 'Wheel Covers', 'Keys with Vehicle', 'Trunk', 'Glove Compartment', 'Exterior Condition', 'Interior Condition', 'Odometer Reading', 'Additional Equipment or Accessories', 'List Missing or Damaged Parts', 'Comments'])

    if i % 1000 == 0:
        print(i/len(A))


Inspection_add = []
for i in range(0, len(Error)):
    Inspection_add.append(pd.DataFrame({'Invoice Number': Error[i][2], 'Inspection Desc.': Error[i][3], 'Inspection Date': Error[i][4], 'Inspection Time': Error[i][5], 'Tax ID': Error[i][6], 'Number of Tires': Error[i][7], 'Number of Airbags': Error[i][8], 'Battery': Error[i][9], 'Radio': Error[i][10], 'Additional Audio Equipment': Error[i][10], 'Special Wheels': Error[i][11], 'Wheel Covers': Error[i][12], 'Keys with Vehicle': Error[i][13], 'Trunk': Error[i][14], 'Glove Compartment': Error[i][15], 'Exterior Condition': Error[i][16], 'Interior Condition': Error[i][17], 'Odometer Reading': Error[i][18], 'Additional Equipment or Accessories': Error[i][19], 'List Missing or Damaged Parts': Error[i][20], 'Comments': Error[i][21]}))


Vehicle_Inspection_Frame = pd.concat(Inspection)
Vehicle_Inspection_Order = ['Invoice Number', 'Inspection Desc.', 'Inspection Date', 'Inspection Time', 'Tax ID', 'Number of Tires', 'Number of Airbags', 'Battery', 'Radio', 'Additional Audio Equipment', 'Special Wheels', 'Wheel Covers', 'Keys with Vehicle', 'Trunk', 'Glove Compartment', 'Exterior Condition', 'Interior Condition', 'Odometer Reading', 'Additional Equipment or Accessories', 'List Missing or Damaged Parts', 'Comments']
Vehicle_Inspection_Frame = Vehicle_Inspection_Frame[Vehicle_Inspection_Order]


Vehicle_Inspection_Frame.to_csv('Vehicle_Inspection_12.csv', sep=',', index = False)


