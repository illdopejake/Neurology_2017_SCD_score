import os
import sys
import argparse
import gds_scd_conversion as scd 

# Data must be set so that all "depressed" answers are equal to 1.
# If this is not already the case, the script will do it for you.
# However, you must specify below which columns to invert.

# Please note that there are different GDS versions. The default 
# for our version may not be applicable to your version.

# These are the question numbers to invert.
icols = [1,5,7,10,15,19,21,27,29,30]


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
    transform the data so that 1="depressed" answer. The user need only
    open the wrapper script (this one) and change the variable icols so that the 
    GDS questions that need to be "inverted" are supplied. Then, make sure the 
    encode option is set to "True"

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


    parser = argparse.ArgumentParser(
        description='converts GDS data into factor scores (SCD, etc.)')

    ###INPUTS###

    parser.add_argument('sheet', type=str, nargs=1,
        help='Path to input spreadsheet with GDS data')

    parser.add_argument('col_start', type=int, nargs=1,
        help = 'column # of first GDS question. Note: 0 = col1, 1 = col2, etc')

    
 	###OPTIONS###

 	parser.add_argument('-out', type=str, default='./',
        help = 'path to desired output directory. Default = current directory')

    parser.add_argument('-output_orig', type=bool, 
    	default=True, choices=[True, False],
        help='True=append scores to original spreadsheet, False=make new csv')

    parser.add_argument('-tfms', type=str, 
    	default=os.path.join(os.get_cwd(),'values_for_transformations.csv'),
        help='path to spreadsheet with means, sds and factor weights')

     parser.add_argument('-encode', type=bool, 
     	default=False, choices = [True, False],
        help = 'If True, invert columns supplied in the icols variable')

    parser.add_argument('-axis', type=int, 
    	default=0, choices = [0, 1]
        help='1 if GDS questions are rows. 0 if GDS questions are columns')

    parser.add_argument('-header', type=bool, 
    	default=True, choices = [True, False]
        help='If rows/columns have labels, set to True. If not, set to False.')

    if len(sys.argv) < 2:
        parser.print_help()
        print(help(scd.main))
    else:
        args=parser.parse_args()

        scd.main(sheet = args.sheet[0], col_start = args.col_start[0],
        		out_dir = args.out, output_orig = args.output_orig, 
        		tfms = args.tfms, encode = args.encode, cols_2_invert = icols, 
        		gds_axis = args.axis, header = args.header
        		)


