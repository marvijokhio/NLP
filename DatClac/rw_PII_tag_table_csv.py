import csv

with open('PIITagTable.csv', 'w') as csvfile:
    fieldnames = ['PIITag', 'PossibleNames','RegularExpr','TagDesc']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')

    writer.writeheader()
    writer.writerow({'PIITag': 'ID', 'PossibleNames': 'id, idNo, id_num, id_no, id_no:, idno: ','RegularExpr':'r"^[a-f0-9-]{36}$"','TagDesc':'id'})
    writer.writerow({'PIITag': 'FName', 'PossibleNames': 'fname, f_name, first_name, given_name, firstname','RegularExpr':'r"^[a-zA-Z]+(([\',. -][a-zA-Z ])?[a-zA-Z0-9]*)*$"','TagDesc':'First Name'})
    writer.writerow({'PIITag': 'LName', 'PossibleNames': 'Lname, l_name, last_name, caste, FamilyName, Family_Name, surname, sur_name, lastname','RegularExpr':'r"^([\w-]+) *(?!(Jr|Sr|III))(\w+)?$|^([\w-]+)( \w+)? (Jr|Sr|III)$"','TagDesc':'Last Name'})
    writer.writerow({'PIITag': 'MName', 'PossibleNames': 'Mname, maiden, m_name, maiden_name, maidenName','RegularExpr':'xxx','TagDesc':'Maiden Name'})   # no Regular expression
    writer.writerow({'PIITag': 'MMName', 'PossibleNames': 'MMname, mothers_maiden, mothers maiden, mm_name, mothers_maiden_name, mothersmaidenName','RegularExpr':'xxx','TagDesc':'Mothers Maiden Name'})  # no Regular expression
    writer.writerow({'PIITag': 'DOB', 'PossibleNames': 'DOB, birthdate, birth_date, date_of_birth, date_birth','RegularExpr':'r"^((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$"','TagDesc':'Date of Birth'})
    writer.writerow({'PIITag': 'Passport', 'PossibleNames': 'Passport, passportNo, passport_number, passport number, passport_no, passport_id','RegularExpr':'xxx','TagDesc':'Passport Number'}) # no Regular expression
    writer.writerow({'PIITag': 'SSN', 'PossibleNames': 'SSN, SSNo, SS_no, SSN_no, SSNum, SS_num, social security number, social_security_number, social security no, ss_number','RegularExpr':'r"^\d{3}-\d{2}-\d{4}$"','TagDesc':'social security number'})
    writer.writerow({'PIITag': 'DriversLNo', 'PossibleNames': 'Drivers, DriversLNo, drivers_ln, drivers_LNo, drivers_no, drivers_lNum, drivers_lsc_num, drivers lnumber, drivers license number, drivers_license_number, drivers_license_no, drivers license no, dl_number','RegularExpr':'xxx','TagDesc':'drivers license number'}) # no Regular expression
    writer.writerow({'PIITag': 'Gender', 'PossibleNames': 'Gender, gender_type, sex, sex_type','RegularExpr':'r"^(?:m|M|male|Male|f|F|female|Female)$"','TagDesc':'Gender'})
    writer.writerow({'PIITag': 'Salary', 'PossibleNames': 'Salary, wage, pay, remuneration','RegularExpr':'xxx','TagDesc':'Salary'}) # no Regular expression
    writer.writerow({'PIITag': 'Email', 'PossibleNames': 'E-mail, email-id, EmailID','RegularExpr':'r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"','TagDesc':'Email Address'}) 
    writer.writerow({'PIITag': 'Address', 'PossibleNames': 'address, addr, residential address, res Address, address_info, addr_info','RegularExpr':'r"[A-Za-z0-9\'\.\-\s\,]"','TagDesc':'Address'})
    writer.writerow({'PIITag': 'Prefix', 'PossibleNames': 'Prefix, NamePrefix, name_prefix ','RegularExpr':'r"^(?:Mrs.|Mr.|Ms)$"','TagDesc':'Prefix'})
    writer.writerow({'PIITag': 'Suffix', 'PossibleNames': 'Suffix, NameSuffix, name_Suffix ','RegularExpr':'xxx','TagDesc':'Suffix'})
    writer.writerow({'PIITag': 'Marital', 'PossibleNames': 'marital, maritalstatus, marital_status ','RegularExpr':'r"^(?:m|M|s|S|married|Married|single|Single|D|d|divorced|Divorced|w|W|widowed|Widowed)$"','TagDesc':'Marital'})
    writer.writerow({'PIITag': 'Race', 'PossibleNames': 'Race, humanRace, human_Race ','RegularExpr':'r"^(?:American Indian|american indian|Alaska Native|alaska native|Asian|asian|Black|black|White|white|African American|african american|Hispanic|hispanic)$"','TagDesc':'Huaman Race'})
    writer.writerow({'PIITag': 'Ethinicity', 'PossibleNames': 'Ethinicity, humanEthinicity, human_Ethinicity ','RegularExpr':'r"^(?:irish|chinese|portuguese|dominican|mexican|french|english|polish|asian_indian|italian|west_indian|american|german|puerto_rican|swedish|central_american|scottish|african|french_canadian|russian)$"','TagDesc':'Huaman ethinicity'})
    writer.writerow({'PIITag': 'Birthplace', 'PossibleNames': 'birthplace, place of birth, birth_place, place_of_birth','RegularExpr':'xxx','TagDesc':'Birth Place'})  # no Regular expression
    writer.writerow({'PIITag': 'ContactNo', 'PossibleNames': 'ContactNo, Contact_No, Contact No, Contact, ContactNumber, Contact Number, Contact_Number, telephone, telephone no, ','RegularExpr':'r"(([+][(]?[0-9]{1,3}[)]?)|([(]?[0-9]{4}[)]?))\s*[)]?[-\s\.]?[(]?[0-9]{1,3}[)]?([-\s\.]?[0-9]{3})([-\s\.]?[0-9]{3,4})"','TagDesc':'Contact Number'})


# No regular expression defined for Maiden Name , Mothers Maiden Name,  Passport Number, drivers license number, Salary, Birth Place