import clips

env = clips.Environment()

table_meta_template_string = """
                        (deftemplate qtable-meta
                                (slot name (type STRING))
                                (slot users-granted (type STRING))
                                (slot total-Recs (type STRING))
                                (slot total-cols (type STRING))                        
                        )
                        """

columns_meta_template_string = """
                        (deftemplate columns-meta
                                (slot table (type STRING))
                                (slot column-name (type STRING))
                                (slot data-type (type STRING))
                                (slot is-unique (type STRING))
                                (slot is-null (type STRING))                        
                        )
                        """

PII_validate_template_string = """
                        (deftemplate PII-validate
                                (slot QCol-name (type STRING))
                                (slot table (type STRING))
                                (slot is_PII (type STRING))                        
                        )
                        """

temp_template_string = """
                        (deftemplate response
                                (slot action (type STRING))
                        )
                        """

env.build(table_meta_template_string)
env.build(columns_meta_template_string)
env.build(PII_validate_template_string)
env.build(temp_template_string)

def clips_ord_fact_assert(fname,fstr):    
    
    # Assert the first ordeded-fact as string so its template can be retrieved
    fact_string = "("+fname+fstr+")"
    fact = env.assert_string(fact_string)
    template = fact.template
    assert template.implied == True
    new_fact = template.new_fact()
    new_fact.extend((fstr))
    new_fact.assertit()
    new_fact.retract()


def facts_print():
    for fact in env.facts():
        print(fact)

def save_the_facts():
    env.save_facts("p_fct.clp", mode=0)


#Method returns score for table based on Business comodity rules
def Rules_Classif_score_Calc(DBtable_confirmed_PIITagList, PIScoreSum,tablename):
        
        clf_score = 0 #classification score
        # define clips rules here for PII attributes and their score
        
        rules = {1:"""
        (defrule checkprocedures
        (and (PII-validate (QCol-name "ID") (table "procedures") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "procedurescode"|"proceduresdesc") (table "procedures") (is_PII "FALSE"))
        (PII-validate (QCol-name "procedures_reason_code"|"procedures_reason_desc") (table "procedures") (is_PII "FALSE"))))

        =>
        (assert (score 15))
        )
        """ , 2: """    
        (defrule checkmedications
        (and (PII-validate (QCol-name "ID") (table "medications") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "medicationscode"|"medicationsdesc") (table "medications") (is_PII "FALSE"))
        (PII-validate (QCol-name "medications_reason_code"|"medications_reason_desc") (table "medications") (is_PII "FALSE"))))

        =>
        (assert (score 13))
        )
        """ , 3: """    
        (defrule checkobservations
        (and (PII-validate (QCol-name "ID") (table "observations") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "observationscode"|"observationsdesc") (table "observations") (is_PII "FALSE"))
        (PII-validate (QCol-name "observations_reason_code"|"observations_reason_desc") (table "observations") (is_PII "FALSE"))))

        =>
        (assert (score 11))
        )
        """ , 4: """    
        (defrule checkimmunizations
        (and (PII-validate (QCol-name "ID") (table "immunizations") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "immunizationscode"|"immunizationsdesc") (table "immunizations") (is_PII "FALSE"))
        (PII-validate (QCol-name "immunizations_reason_code"|"immunizations_reason_desc") (table "immunizations") (is_PII "FALSE"))))

        =>
        (assert (score 11))
        )
        """ , 5: """    
        (defrule checkencounters
        (and (PII-validate (QCol-name "ID") (table "encounters") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "encounterscode"|"encountersdesc") (table "encounters") (is_PII "FALSE"))
        (PII-validate (QCol-name "encounters_reason_code"|"encounters_reason_desc") (table "encounters") (is_PII "FALSE"))))

        =>
        (assert (score 9))
        )
        """ , 6: """    
        (defrule checkconditions
        (and (PII-validate (QCol-name "ID") (table "conditions") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "conditionscode"|"conditionsdesc") (table "conditions") (is_PII "FALSE"))
        (PII-validate (QCol-name "conditions_reason_code"|"conditions_reason_desc") (table "conditions") (is_PII "FALSE"))))

        =>
        (assert (score 13))
        )
        """ , 7: """    
        (defrule checkcareplans
        (and (PII-validate (QCol-name "ID") (table "careplans") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "careplanscode"|"careplansdesc") (table "careplans") (is_PII "FALSE"))
        (PII-validate (QCol-name "careplans_reason_code"|"careplans_reason_desc") (table "careplans") (is_PII "FALSE"))))

        =>
        (assert (score 10))
        )
        """ , 8: """    
        (defrule checkallergies
        (and (PII-validate (QCol-name "ID") (table "allergies") (is_PII "TRUE"))
        (or (PII-validate (QCol-name "allergiescode"|"allergiesdesc") (table "allergies") (is_PII "FALSE"))
        (PII-validate (QCol-name "allergies_reason_code"|"allergies_reason_desc") (table "allergies") (is_PII "FALSE"))))

        =>
        (assert (score 10))
        )
        """
        }

        rules_score_lst = [15, 13, 11, 11, 9, 13, 10, 10]
        
        for k in rules:
                env.build(rules[k])

        env._agenda.run()
        
        f = 0
        if tablename !="patients":                
                for fact in env.facts():
                        l=fact
                print(str(l))
                s = str(l).split(" ")
                f = int(s[1].strip()[0:-1])
         
        clf_score = f + PIScoreSum
        return clf_score
 
# Method to define clips rules for PII attributes tag confirmation    
def confirmtag_byconditions(initaltag,table):
        tagName = initaltag
        swt = {'careplans':1,'allergies':2,'claims':3,'conditions':4,'encounters':5,'immunizations':6,'medications':7,'observations':8, 'procedures':9}
        num = swt.get(table, 'table Not Found')
        if table != "patients":
                switcher = {
                        1: "careplanid" if initaltag == "id" else "ID" if initaltag == "patient" else "careplancode" if initaltag == "code" else "careplandesc" if initaltag == "description" else "careplan_reason_code" if initaltag == "reason_code" else "careplan_reason_desc" if initaltag == "reason_description" else initaltag ,
                        2: "allergiesid" if initaltag == "id" else "ID" if initaltag == "patient" else "allergiescode" if initaltag == "code" else "allergiesdesc" if initaltag == "description" else initaltag ,
                        3: "claimsid" if initaltag == "id" else  "ID" if initaltag == "patient" else initaltag ,
                        4: "conditionsid" if initaltag == "id" else "ID" if initaltag == "patient" else "conditionscode" if initaltag == "code" else "conditionsdesc" if initaltag == "description" else initaltag ,
                        5: "encountersid" if initaltag == "id" else "ID" if initaltag == "patient" else "encounterscode" if initaltag == "code" else "encountersdesc" if initaltag == "description" else "encounters_reason_code" if initaltag == "reason_code" else "encounters_reason_desc" if initaltag == "reason_description" else initaltag ,
                        6: "immunizationsid" if initaltag == "id" else "ID" if initaltag == "patient" else "immunizationscode" if initaltag == "code" else "immunizationsdesc" if initaltag == "description" else initaltag ,
                        7: "medicationsid" if initaltag == "id" else "ID" if initaltag == "patient" else "medicationscode" if initaltag == "code" else "medicationsdesc" if initaltag == "description" else "medications_reason_code" if initaltag == "reason_code" else "medications_reason_desc" if initaltag == "reason_description" else initaltag ,
                        8: "observationsid" if initaltag == "id" else "ID" if initaltag == "patient" else "observationscode" if initaltag == "code" else "observationsdesc" if initaltag == "description" else initaltag ,
                        9: "proceduresid" if initaltag == "id" else "ID" if initaltag == "patient" else "procedurescode" if initaltag == "code" else "proceduresdesc" if initaltag == "description" else "procedures_reason_code" if initaltag == "reason_code" else "procedures_reason_desc" if initaltag == "reason_description" else initaltag , 
                        }
                tagName = switcher.get(num)
        return tagName        


def putfact(temp,factsdict):
        template = env.find_template(temp)
        new_fact = template.new_fact()
        for k in factsdict:
                new_fact[k] = factsdict[k]

        new_fact.assertit()

