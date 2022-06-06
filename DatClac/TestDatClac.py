import DatClacEngine as dce

tQuery = "Select id, birthdate , first_name, last_name, prefix, marital, gender, race, ethinicity, ssn, address from patients;"
# tQuery = "Select id, birthdate, last_name, gender, race, ethinicity, ssn, address from patients;"
# tQuery = "Select first_name, ssn ,address from patients;"     
# tQuery = "SELECT  patient, code, reason_description from procedures;"
# tQuery = "SELECT  patient, code, reason_description from medications;"        

print(dce.Classify_Data(tQuery))