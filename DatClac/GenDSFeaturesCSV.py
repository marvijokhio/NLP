import re 
import numpy as np
import pandas as pd 
import os

def geneFeatures(csvfile):
    # Getting the Input names
    data_list = pd.read_csv(csvfile,sep=';') #csvfile is file with just data and Label but no features

    BigDataSource = data_list[['StringData','Label']].drop_duplicates().copy()
    BigDataSource.StringData = BigDataSource.StringData.str.lower()

    vowels = ('a','e','i','o','u')
    spec = ('[','@','_','+','-','!','#','$','%','^','&','*','(',')','<','>','?','/','\\',';',',','}','{','~',':',']')

    BigDataSource.loc[:,'last_char_vow'] = np.where(BigDataSource.StringData.str.endswith(vowels),1,0)
    BigDataSource.loc[:,'first_char_vow'] = np.where(BigDataSource.StringData.str.startswith(vowels),1,0)
    BigDataSource.loc[:,'only_digits'] = np.where(BigDataSource.StringData.str.isdigit(),1,0)
    BigDataSource.loc[:,'only_alphas'] = np.where(BigDataSource.StringData.str.isalpha(),1,0)
    BigDataSource.loc[:,'startwith_spec'] = np.where(BigDataSource.StringData.str.startswith(spec),1,0)
    BigDataSource.loc[:,'endwith_spec'] = np.where(BigDataSource.StringData.str.endswith(spec),1,0)
    BigDataSource.loc[:,'str_len'] = BigDataSource.StringData.str.len()

    # feature unique char length
    unq = []
    for elem in BigDataSource['StringData']:
        unq.append(len(list(set(elem))))
    BigDataSource['unq_char'] = unq

    # feature special char length
    spec_chrLength = []
    for elem in BigDataSource['StringData']:
        spec_chrLength.append(len(re.sub('[\\w]+' ,'', elem)))
    BigDataSource['spec_char_length'] = spec_chrLength

    # feature spaces length
    spacesLength = []
    for elem in BigDataSource['StringData']:
        spacesLength.append(sum(c.isspace() for c in elem))
    BigDataSource['spaces_length'] = spacesLength

    # feature number length
    numLength = []
    for elem in BigDataSource['StringData']:
        numLength.append(sum(c.isdigit() for c in elem))
    BigDataSource['num_length'] = numLength

    # feature alphabet length
    alphaLength = []
    for elem in BigDataSource['StringData']:
        alphaLength.append(sum(c.isalpha() for c in elem))
    BigDataSource['alphaLength'] = alphaLength

    # feature Vowel length
    vowelLength = []
    for elem in BigDataSource['StringData']:
        vowelLength.append(len(re.findall(r'[aeiou]', elem)))
    BigDataSource['vowelLength'] = vowelLength

    # feature Consonant length
    ConsonantLength = []
    for elem in BigDataSource['StringData']:
        ConsonantLength.append(len(re.findall(r'[bcdfghjklmnpqrstvwxyz]', elem)))
    BigDataSource['ConsonantLength'] = ConsonantLength

    # feature plus sign length
    plusLength = []
    for elem in BigDataSource['StringData']:
        plusLength.append(len(re.findall(r'[+]', elem)))
    BigDataSource['plusLength'] = plusLength

    # feature minus sign length
    minusLength = []
    for elem in BigDataSource['StringData']:
        minusLength.append(len(re.findall(r'[-]', elem)))
    BigDataSource['minusLength'] = minusLength

    # feature _ sign length
    _Length = []
    for elem in BigDataSource['StringData']:
        _Length.append(len(re.findall(r'[_]', elem)))
    BigDataSource['_Length'] = _Length

    # feature @ sign length
    atLength = []
    for elem in BigDataSource['StringData']:
        atLength.append(len(re.findall(r'[@]', elem)))
    BigDataSource['atLength'] = atLength

    # feature dot sign length
    dotLength = []
    for elem in BigDataSource['StringData']:
        dotLength.append(len(re.findall(r'[.]', elem)))
    BigDataSource['dotLength'] = dotLength

    # feature / sign length
    FsllashLength = []
    for elem in BigDataSource['StringData']:
        FsllashLength.append(len(re.findall(r'[.]', elem)))
    BigDataSource['FsllashLength'] = FsllashLength

    # feature : sign length
    ColonLength = []
    for elem in BigDataSource['StringData']:
        ColonLength.append(len(re.findall(r'[:]', elem)))
    BigDataSource['ColonLength'] = ColonLength

    # feature # sign length
    hashLength = []
    for elem in BigDataSource['StringData']:
        hashLength.append(len(re.findall(r'[#]', elem)))
    BigDataSource['hashLength'] = hashLength

    # feature () braces length
    SbracLength = []
    for elem in BigDataSource['StringData']:
        SbracLength.append(len(re.findall(r'[()]', elem)))
    BigDataSource['SbracLength'] = SbracLength

    # feature comma length
    commaLength = []
    for elem in BigDataSource['StringData']:
        commaLength.append(len(re.findall(r'[,]', elem)))
    BigDataSource['commaLength'] = commaLength

    # feature Xx length
    xLength = []
    for elem in BigDataSource['StringData']:
        xLength.append(len(re.findall(r'[Xx]', elem)))
    BigDataSource['xLength'] = xLength
    BigDataSource = BigDataSource.iloc[1:,] 
    df = pd.DataFrame(BigDataSource)  
    df.to_csv('TagFeat.csv', index=False, encoding='utf-8',quoting=None,sep=';') #RBigDT is file along with features with header row
    print("'TagFeat.csv' generated!")
