
import pickle
import pandas
from sklearn.utils import shuffle
from sklearn import model_selection

def predictColName(featureCSVfile):
    # Load dataset
    names = ['Label','last_char_vow', 'first_char_vow', 'only_digits', 'only_alphas','startwith_spec','endwith_spec','str_len', 'unq_char', 'spec_char_length', 'spaces_length','num_length','alphaLength','vowelLength','ConsonantLength','plusLength','minusLength', '_Length','atLength','dotLength','FsllashLength','ColonLength','hashLength','SbracLength','commaLength','xLength']
    dataset = pandas.read_csv(featureCSVfile,sep=';', names=names, skiprows=1,index_col=None)   #DSToTrain is file without header row with features
    dataset = shuffle(dataset)
    dataset.groupby('Label').size()
    # # Split-out validation dataset
    array = dataset.values
    X = array[:,1:]
    Y = array[:,0]
    validation_size = .95
    seed = 10
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    filename = 'finalized_model.sav'
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(X_validation, Y_validation)
    print("\n Result",result)
    return result
