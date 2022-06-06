import clips_call as cl

DBTableColumtags = []   # list of all the selected tags matched to column names from input query select statement. 
PI_PredefinedScores = {'ID':6,'FName':3, 'LName':3, 'MName':3 , 'MMName':4,'FullName':6, 'DOB':4 ,'Passport':6 ,'DriversLNo':6 ,'Gender':3 , 'Prefix':2, 'Marital':2, 'Race':2 , 'Ethinicity':3 , 'Email':6, 'Address':6, 'ContactNo':5,'SSN':6, 'Birthplace':4 } 

# Method to finalize a PII tag to column.
def confirm_tag(initaltag, table ,ml_acc, re_match_score):
    if (ml_acc > 60 and re_match_score > 80):
        # confirm the tag of database column
        print("Tag confirmed")
        DBTableColumtags.append(initaltag)
        return DBTableColumtags
    else: 
        # set other clips rules to confirm tag
        print("not confirmed by ML and RE")
        DBTableColumtags.append(cl.confirmtag_byconditions(initaltag,table))
        return DBTableColumtags

# Method returns sum of PI predefiend scores for colums found in a given table
def Calc_PIScoreSum(ConfiremedTaglist):
    PIScore_sum = 0 
    
    for tag in ConfiremedTaglist:
        if tag in PI_PredefinedScores:
            print (tag, PI_PredefinedScores[tag])
            PIScore_sum += PI_PredefinedScores[tag]

    return PIScore_sum

CTagLst = ['Id','FName','SSN']
print(Calc_PIScoreSum(CTagLst))