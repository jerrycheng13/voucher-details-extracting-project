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

Return = []
for i in range(0, len(A)):  
    if A[i]['description'][0] == "PROPERTY RETURN RECEIPT":
        Invoice_No = A[i]['description'][3]
        Delivery_No = A[i]['description'][4]
        try:
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
                            Article_Description[k-1] += "?"
                    Article_Description = (" ".join(list(Article_Description))).split("? ")
                if A[i]['description'][j] == "Returning Officer":
                    Tax_No = A[i]['description'][j+5]
                    Command = A[i]['description'][j+6]
                    Date = A[i]['description'][j+7]
                    Time = A[i]['description'][j+8]
            Return.append(pd.DataFrame({'Invoice Number': Invoice_No, 'Delivery Number': Delivery_No, 'Returning Officer Tax No.': Tax_No, 'Returning Officer Command': Command, 'Return Date': Date, 'Return Time': Time, 'Item (Number)': list(Item), "Returning Article Description": Article_Description, "Return Quantity": list(Quantity)}))
        except:
            print(Invoice_No)
            
Return.append(pd.DataFrame({'Invoice Number': 3000720783, 'Delivery Number': 201455789, 'Returning Officer Tax No.': 935714, 'Returning Officer Command': '62ND PRECINCT', 'Return Date': '10/26/2016', 'Return Time': '06:37', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |PART |SEAT |NYSPIN ALARM:NO | TAN REAR PASSENGER VAN SEAT', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 3000790759, 'Delivery Number': 201768987, 'Returning Officer Tax No.': 906417, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '11/09/2017', 'Return Time': '09:28', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |PART |OTHER PARTS |NYSPIN ALARM:NO | TRAILER HITCH', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000568267, 'Delivery Number': 201510192, 'Returning Officer Tax No.': 955313, 'Returning Officer Command': '41ST PRECINCT', 'Return Date': '01/05/2017', 'Return Time': '17:32', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |MOTORCYCLE |YEAR:2004 |MAKE:KAWASAKI |COLOR:GREEN, DARK |TYPE:2 WHEELER |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:0 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNING:YES |DOUBLE TOW', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 1000935779, 'Delivery Number': 201624903, 'Returning Officer Tax No.': 954854, 'Returning Officer Command': '32ND PRECINCT', 'Return Date': '05/19/2017', 'Return Time': '22:16', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2003 |MAKE:CHEVROLET |MODEL:TRAILBLAZER |COLOR:GREEN, DARK |TYPE:SUBURBAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNING', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000641138, 'Delivery Number': 201612265, 'Returning Officer Tax No.': 938956, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '05/05/2017', 'Return Time': '15:58', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2005 |MAKE:FORD |MODEL:EXPLORER |COLOR:BLUE, DARK |TYPE:4 DOOR SEDAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:2 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NY - US |VEHICLE RUNNING:Y', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000642571, 'Delivery Number': 201586098, 'Returning Officer Tax No.': 953198, 'Returning Officer Command': '41ST PRECINCT', 'Return Date': '04/06/2017', 'Return Time': '11:08', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2002 |MAKE:MITSUBISHI |MODEL:GALANT |COLOR:GREEN, DARK |TYPE:4 DOOR SEDAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:2 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |CERTIFICATE OF INSPECTION NO.:87', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000646991, 'Delivery Number': 201738857, 'Returning Officer Tax No.': 906417, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '10/05/2017', 'Return Time': '09:20', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |SCOOTER/MOPED |YEAR:UNKNOWN |MAKE:UNKNOWN |MODEL:OTHER |COLOR:BLUE, DARK |TYPE:SCOOTER |VIN AVAILABLE:NO |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:0 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNING:Y', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000647440, 'Delivery Number': 201678642, 'Returning Officer Tax No.': 367017, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '07/25/2017', 'Return Time': '10:50', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2010 |MAKE:FORD |MODEL:ESCAPE |COLOR:BLUE, LIGHT |TYPE:SPORT UTILITY |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |CERTIFICATE OF INSPECTION NO.:NONE |I', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000648711, 'Delivery Number': 201611178, 'Returning Officer Tax No.': 343573, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '05/04/2017', 'Return Time': '13:20', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2015 |MAKE:CHEVROLET |MODEL:C15 SILVERADO 2WD |COLOR:BLUE, DARK |TYPE:PICKUP TRUCK |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:2 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NY - US |YEA', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 2000650322, 'Delivery Number': 201716026, 'Returning Officer Tax No.': 366414, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '09/08/2017', 'Return Time': '12:20', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:1999 |MAKE:NISSAN |MODEL:ALTIMA |COLOR:BLUE, LIGHT |TYPE:4 DOOR SEDAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NY - US |VEHICLE RUNNING:', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 3000799582, 'Delivery Number': 201586601, 'Returning Officer Tax No.': 954723, 'Returning Officer Command': '70TH PRECINCT', 'Return Date': '04/06/2017', 'Return Time': '19:40', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2003 |MAKE:FORD |MODEL:CROWN VICTORIA |COLOR:BLUE, LIGHT |TYPE:4 DOOR SEDAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNI', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 3000803521, 'Delivery Number': 201593538, 'Returning Officer Tax No.': 319363, 'Returning Officer Command': '77TH PRECINCT', 'Return Date': '04/14/2017', 'Return Time': '11:03', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |VEHICLE |YEAR:2001 |MAKE:FORD |MODEL:ESCAPE |COLOR:GREEN, DARK |TYPE:4 DOOR SEDAN |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NY - US |VEHICLE RUNNING:NO', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 3000810959, 'Delivery Number': 201607535, 'Returning Officer Tax No.': 955756, 'Returning Officer Command': '71ST PRECINCT', 'Return Date': '05/01/2017', 'Return Time': '01:46', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |MOTORCYCLE |YEAR:2017 |MAKE:KYMCO |MODEL:4 GLILITY |COLOR:BLUE, DARK |TYPE:2 WHEELER |VIN AVAILABLE:YES |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:1 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |CERTIFICATE OF INSPECTION NO.:05283', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 4000478617, 'Delivery Number': 201640968, 'Returning Officer Tax No.': 942270, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '06/08/2017', 'Return Time': '16:11', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |SCOOTER/MOPED |YEAR:UNKNOWN |MAKE:UNKNOWN |MODEL:OTHER |COLOR:GREEN, LIGHT |TYPE:SCOOTER |VIN AVAILABLE:NO |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:0 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNING', "Return Quantity": [1]}))
#Return.append(pd.DataFrame({'Invoice Number': 4000478621, 'Delivery Number': 201709840, 'Returning Officer Tax No.': 931452, 'Returning Officer Command': 'PROP CLERK DIV', 'Return Date': '08/31/2017', 'Return Time': '13:00', 'Item (Number)': [1], "Returning Article Description": 'VEHICLE / BOAT |VEHICLE |SCOOTER/MOPED |YEAR:UNKNOWN |MAKE:UNKNOWN |MODEL:OTHER |COLOR:BLUE, LIGHT |TYPE:SCOOTER |VIN AVAILABLE:NO |DISCREPANCY IN VIN:NO |NO. OF LIC. PLATES:0 |ALT. NO. OF PLATES:0 |ALT. LIC. STATE:NONE |INSP STATE:NONE |VEHICLE RUNNING:', "Return Quantity": [1]}))

Return_Forms = pd.concat(Return)
Return_Order = ['Invoice Number', 'Delivery Number', 'Returning Officer Tax No.', 'Returning Officer Command', 'Return Date', 'Return Time', 'Item (Number)', "Returning Article Description", "Return Quantity"]
Return_Frame = Return_Forms[Return_Order]

Return_Frame.to_csv('Return_vehicle_12.csv', sep=',', index = False)



      