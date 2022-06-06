import psycopg2
import pandas
import rw_PII_tag_table_csv as rwpii
import clips_call as cl
import csv 
import re
import CalcPrivScore as cps
import GenDSFeaturesCSV as fg
import CheckMLModel as chkml

TQ_cols_dict = {}  # dictionary of input query columns
mydict = {}  # dictionary of records for each input query column 
total_records = 0
fdict = {}  # dictionary for saving facts about table columns meta data
qfactdict = {}  # dictioanry for saving facts about each input query PII column
records = []    # list of string data and label before forwarded to feature generation method.
n = []   # List of Tags whose ML is done. 

# method to match input query's attributes ( or column attributes) with PII tag table 
def matchIniPIITag(cname):
    cname = cname.lower()
    df = pandas.read_csv('PIITagTable.csv')
    c = 0
    matchFound = False
    for x in df['PossibleNames']:
        lst = x.rsplit(", ")
        if cname in (one.lower() for one in lst):
            matchFound = True
            return df['PIITag'][c], df['RegularExpr'][c]
        c = c + 1
    
    if matchFound == False:
        return None, None

# method to extract the columns names from input query
def extract_col_table(tQuery):
    q_ingr_list = tQuery.split('from')
    q_cols = q_ingr_list[0].split(',') 
    q_colsList = []
    for item in q_cols:
        q_colsList.append(item.strip())
        
    q_colsList[0] = q_colsList[0][6:].strip()
    return q_colsList  

# method to extract the table names from input query
def extract_table_names(tQuery):
    q_ingr_list = tQuery.split('from')
    q_table = q_ingr_list[1][:-1] 
    
    return q_table.strip()

def ML_Prepross( label,tag, col , colDtdict, n):
    
    
    for tagname in n:
        if tag == tagname and tag == "ContactNo":
            label = "PhoneNumber" 
        if tag == "FName" or tag == "LName" or tag == "MName" or tag == "MMName":
                label = "Name"
        if tag == "SSN":
            label = "ssn"
        if tag == "Address":
            label = "address" 

        
        for c_record in colDtdict[col]:    
            if tag == "FName" or tag == "LName" or tag == "MName" or tag == "MMName":              
                only_alpha = ""
                for char in c_record:
                ## checking whether the char is an alphabet or not using chr.isalpha() method
                    if char.isalpha():
                        only_alpha += char
                ## printing the string which contains only alphabets
                records.append((only_alpha,label))
            else:
                records.append((c_record,label))  
    return records


def pridictColNamebyML(rcdslist):
    acc = 0
    df = pandas.DataFrame(rcdslist, columns=['StringData','Label'])    
    df.to_csv('coldt.csv', index=False, encoding='utf-8',quoting=None,sep=';') 
    print("\n 'coldt.csv' files is generated. \n" )

    df = pandas.read_csv('coldt.csv') 
    
    if df.empty:
        return acc
    fg.geneFeatures('coldt.csv')

    data = pandas.read_csv('TagFeat.csv',skiprows=1)

    data.to_csv('check.csv', index=False, encoding='utf-8',quoting=None) 
    acc = chkml.predictColName('check.csv')
    return acc


# Method to find initial PII tag and its corresponding Regular Expression for columns
def FindIniTagandRE():
    d_tr = {}   
    for col in mydict:
        l = []
         
        tag , rx = matchIniPIITag(col) 
        l.append(tag)
        l.append(rx)
   
        d_tr[col] = l
        
    return d_tr


def FindREMatchScore(tagREDic,total_records):
    dict_REscr = {}
    
    for col in tagREDic:
        lst = []
        t_missmatched = 0
        t_matched = 0
        for c_record in mydict[col]:
            c_record = str(c_record)
            tag = tagREDic[col][0]
            rx = tagREDic[col][1]
            if rx == 'xxx':
                print("No Reg Expr found!")
                break
            if tag != None and rx != None:
                pattern = re.compile(eval(rx))  
                if not re.match(pattern, c_record):
                    t_missmatched += 1
                else: 
                    t_matched += 1 
            else: 
                tag = col
                t_matched = 0
              
        re_match_score = (t_matched*100)/total_records
        lst.append(tag)
        lst.append(re_match_score)
        dict_REscr[col] = lst
        print("Percentage of Records matched against Reg Expr:= ( ", col ," ) ",re_match_score)
    
    return dict_REscr


def getMLPreprossesData(dictTagRE):
    rec = []
    labelnm = {1:"FName" , 2:"Email" , 3:"PhoneNumber", 4:"SSN" , 5: "Address" }
    for i in labelnm.values():
        n.append(i)
    
    for col in dictTagRE:
        tag = dictTagRE[col][0]
        if tag in n:
            
            label = tag
            rec = ML_Prepross(label,tag,col,mydict,n)
               
    return dictTagRE, rec


def Classify_Data(tQuery):

    try:

        connection = psycopg2.connect(user = "karan",
                                    password = "tongey",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "Synthea")

        cursor = connection.cursor()

        cursor.execute(tQuery)
        print("Toal Rows", cursor.rowcount)
        total_records = cursor.rowcount
        _records = cursor.fetchall() 

        if _records:
            table_query_columns = extract_col_table(tQuery)
            table_query_tableName = extract_table_names(tQuery)

        TQ_cols_dict = { i : table_query_columns[i] for i in range(0, len(table_query_columns) ) }
        
        print("\nYour SQL input query contains columns  = ",TQ_cols_dict, "from table named as \'",table_query_tableName,"\' \n")  
        
        for i in range(len(table_query_columns)):
            templist = []
            for row in _records:
                templist.append(row[i])
                
            mydict[table_query_columns[i]] = templist  # dict of lists containing query column records
        
    #   Generate a dynamic Select query for meta data depending on Table's Select query..
    #   Like extract data types, names and other meta information of columns selected in Table query.  
        
        postgreSQL_select_Query = "SELECT table_name, column_name ,data_type, is_nullable, is_identity FROM information_schema.COLUMNS WHERE TABLE_NAME = " + "\'"+ table_query_tableName.strip('\"') +"\'" 
        cursor.execute(postgreSQL_select_Query)
        print("--------- Extracting metadata for query columns -------\n")
        q_meta_records = cursor.fetchall() 
        for mrow in q_meta_records:
            colname = mrow[1]        
            fdict = {"table":mrow[0] , "column-name":mrow[1] , "data-type":mrow[2] ,"is-null":mrow[3], "is-unique":mrow[4] }
                       
            if colname in table_query_columns:
                print("META-DATA = ",fdict)
                cl.putfact("columns-meta",fdict)

        print("\n-------Saving meta-data facts into CLIPS Knowledge-base ------") 
        cl.save_the_facts()

        for fact in cl.env.facts(): 
            print(fact)   

    
    except (Exception, psycopg2.Error) as error :
        print ("\nError while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("\nPostgreSQL connection is closed")


    # Read the CSV file of PII TAgs Table
    with open('PIITagTable.csv', newline='') as csvfile:
        PIITagreader = csv.DictReader(csvfile)

    #### -------------------------------------------------------------------- ####
    #### To match records with corresponding regular expressions of PII tags. ####
    #### 1. Take each columns name from dictionary of data column records (mydict)'
    #### 2. Match the columns name with possible names list from PII tag table and
    #### if matched take it as initial tag otherwise make column name as initial tag. 
    #### 3. Take every single record (or element) from list of the chosen column and
    ####    match against corresponsing regular expression if it is a PII column. 
    #### ---------------------------------------------------------------------####

    print("\n--------Finding Initial PII tags and regular expressions for columns using PII Tag Table!---\n") 
    print(FindIniTagandRE())
    print("\n--------Match Records of columns against corresponding PII Regular Expressions. ----- \n")
    d = FindIniTagandRE()
    x = FindREMatchScore(d,total_records)
    print("\n\nTags with RE Match Score\n",x)

    a , b = getMLPreprossesData(x)  
    r = 100*pridictColNamebyML(b)
    print("\n------ Confirm Tags by Regular Expr, ML and Rules -----")
    for i in a:
        tag = a[i][0]
        re_match_score = a[i][1]
        cps.confirm_tag(tag, table_query_tableName ,r, re_match_score)  # 63 is temp ML accuracy

    CTaglist = cps.DBTableColumtags
    print("\n\nConfirmed Tags List",CTaglist)
    PIScoreSum = cps.Calc_PIScoreSum(CTaglist)
    print("\nPII Tags Score Sum = ", PIScoreSum)

    # save selected column names from SQL Query as facts in clips
    for tag in CTaglist:
        qfactdict = {"QCol-name": tag , "table": table_query_tableName , "is_PII": ("TRUE" if tag in cps.PI_PredefinedScores.keys() else "FALSE" ) }
        cl.putfact("PII-validate",qfactdict)

    for fact in cl.env.facts(): 
        print(fact)

    clacScore = cl.Rules_Classif_score_Calc(CTaglist, PIScoreSum,table_query_tableName)
    print("Classification Score for given data = ", clacScore)

    return clacScore


