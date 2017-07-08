import os
import pandas
import numpy as np


tfms = '/Users/jakevogel/Dropbox/Work/SCC_paper/Revisions/SCD Score/values_for_transformations.csv'


# Data must be set so that all "depressed" answers are equal to 1.
# If this is not already the case, the script will do it for you.
# However, you must specify below which columns to invert.

# Please note that there are different GDS versions. The default 
# for our version may not be applicable to your version.

# These are the question numbers to invert.
icols = [1,5,7,10,15,19,21,27,29,30]



def main(sheet, col_start, out_dir = './', output_orig = True, tfms = tfms,
        encode=True, cols_2_invert = icols, gds_axis = 0, header = True
        ):
    '''
    sheet -> a string path to the spreadsheet containing the GDS data.

    col_start -> the column number where GDS question 1 is. Please note that,
    if the GDS data is in the first column, col_start should be 0. If in the
    second column, col_start should 1, and so forth.

    out_dir -> the directory where the GDS files should be outputted to.

    output_orig -> If True, the GDS factor scores will be appended to the end
    of the input spreadsheet. Otherwise, only the factor scores will be
    included in the output document.

    tfms -> A path to the spreadsheet containing the normative data and factor
    weights (included with script package).

    encode -> If True, script will invert values of columns listed in
    cols_2_invert. This is to make it so, for all questions, 1="depressed
    answer".

    cols_2_invert -> A list of integers corresponding to the Question # s that
    need to be inverted.

    gds_axis -> If GDS questions are the rows, set this to 1. Otherwise, if GDS
    questions are the columns, leave this as 0.

    header -> If columns/rows have labels, leave this as True. If no column
    labels are present, set to False

    to display similar information in your command line:
    GDS_SCD_conversion_wrapper --help
    '''

    # prepare data
    main_df = open_spreadsheet(sheet, header)
    resps = prep_spreadsheet(main_df, col_start, gds_axis)

    # encode
    # note, Python's 1 is 0, so we need to change the columns to fit this
    # rubric by subtracting 1 from the GDS question number. In addition,
    # since we removed question 22, we need to subtract 2 from questions 
    # after 22, in order to fit the data we have prepared
    print('transforming data')
    if encode:
        # convert cols_2_invert so relevant to this dataframe
        cols_2_invert = list(map(lambda x: x-2 if x > 22 else x-1,
                                                        cols_2_invert))
        # encode
        jnk = resps.columns[cols_2_invert]
        resps[jnk] = np.logical_not(resps[jnk]).astype(int)

    # zscore

    tfms = pandas.read_csv(tfms)
    tfms.index = tfms[:][tfms.columns[0]]
    tfms.drop(tfms.columns[0],axis=1,inplace=True)
    zscored = (resps - tfms.loc['means'].values) / tfms.loc['sds'].values

    print('calculating scores')
    # Calculate factor scores
    scores = pandas.DataFrame(index=resps.index,columns=tfms.index[2:6])
    for i,row in tfms.loc[tfms.index[2:6]].iterrows():
        scores.ix[:,i] = (zscored * row.values).sum(axis=1)
    # invert dypshoria and apathy
    scores.dysphoria = scores.dysphoria * -1
    scores.apathy = scores.apathy * -1
    # calculate affective score
    aff = (scores.dysphoria + scores.apathy + scores.anxiety) / 3
    scores.ix[:,'affective_score'] = aff

    new_fl = os.path.join(out_dir,'SCD_scores.csv')
    if output_orig:
        for sub in scores.index:
            for col in scores.columns:
                main_df.ix[sub,col] = scores.ix[sub,col]
        print('creating new file %s'%(new_fl))
        main_df.to_csv(new_fl)
    else:
        print('creating new file %s'%(new_fl))
        scores.to_csv(new_fl)

def open_spreadsheet(sheet, header):

    print('reading spreadsheet')
    opened = False
    if header:
        header = 'infer'
    else:
        header = None
    if sheet[-3:] == 'csv':
        try:
            df = pandas.read_csv(sheet, sep=None, header=header)
            opened = True
        except:
            opened = False
    elif sheet[-3:] == 'txt':
        try:
            df = pandas.read_table(sheet, sep=None, header=header)
            opened = True
        except:
            opened = False
    elif sheet[-3:] == 'xls' or sheet[-3:] == 'lsx':
        try:
            jnk = pandas.ExcelFile(sheet)
            df = pandas.ExcelFile(sheet).parse(jnk.sheet_names[0])
            opened = True
        except:
            opened = False
    else:
        print('I don\'t recognize the extension of your spreadsheet. \n',
                'I\'m going to try one more thing...')
        try:
            df = pandas.read_table(sheet, sep=None, header=header)
            opened = True
            print('okay that worked!')
        except:
            opened = False
    if not opened:
        print('I cannot recognize the file extension of your spreadsheet.\n',
                'please save the file as a .csv, .txt, or excel file...')
        raise IOError('Spreadsheet file extension not recognized')

    return df


def prep_spreadsheet(df, col_start, gds_axis):

    print('preparing data')
    # reset index to prevent confusion later
    df.reset_index(drop=True,inplace=True)

    # Transpose if necessary
    if gds_axis == 1:
        df = df.transpose()

    # Isolate GDS columns
    resps = df[df.columns[col_start: col_start+30]]

    # Remove NaNs
    print('warning: construction of factor scores requires',
            'all data to be present. Therefore, subjects with',
            'missing data are going to be removed. soz.')
    drop_no = len(resps) - len(resps.dropna())
    if drop_no > 0:
        print('removing %s subjects with missing values'%(drop_no))
        print('if this seems wrong, the script is probably failing somewhere')
        resps.dropna(inplace=True)
    else:
        print('no missing data detected')

    # Remove #22
    resps.drop(resps.columns[21],axis=1,inplace=True)

    # Make sure values are integers
    resps.astype(int)

    return resps

if __name__ == '__main__':
    '''This script will take a spreadsheet with binarized GDS data and use them
    to calculate factor scores, based on the methods, weights and normative
    data described in Vogel et al, 2017 Neurology. The output will contain
    scores for the following GDS factors: "SCD", "Dysphoria", "Apathy",
    "Anxiety", "Total Affective Score", the latter being the combination of all
    scores except SCD, which is non-affective.

    The script will recognize most types of spreadsheets (excel, csv, text,
    etc). Script expects data to be binarized as 1s and 0s. If 1 = "depressed"
    answer, nothing further needs to be done. If 1=Yes and 2=No, the script can
    transform the data so that 1="depressed" answer. The user need only change
    the variable icols in the script so that the GDS questions that need to be
    "inverted" are supplied.

    Please note that the script assumes that the GDS questions are represented
    by 30 consecutive columns (or rows) of 1s and 0s. If this structure is not
    represented in the spreadsheet, results will be unreliable. Other columns
    may be present, as long as the 30 binary GDS columns are present and
    consecutive.

    Also note that missing data should be represented with blank cells or NaNs,
    and will be removed.

    Finally, the simpler a spreadsheet is, the more reliable the performance
    will be. For absolute best results, have rows as subjects and columns as
    variables, and do not use any multi-indexing. 
    '''
