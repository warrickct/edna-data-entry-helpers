import csv
import glob
from collections import OrderedDict

def sum_row_values(r, r2):
    '''
    Goes through the values, adds them together and returns summed row.
    '''
    new_row = []
    new_row.append(r[0])
    for index in range(1, len(r)):
        total = float(r[index]) + float(r2[index])
        if (float(r[index]) > 0 and float(r2[index]) > 0):
            print("non-zero values at site index: ", index)
        if (total.is_integer()):
            new_row.append(int(total))
        else:
            new_row.append(total)
    return new_row

dev_test = False
add_abundances = True
if dev_test:
    files = glob.glob('.' + '/test_outputs/syrie_no_unassigned.tsv')
else:
    file_name = input("Enter file path from script name (with extension) to remove duplicates from: ")
    files = glob.glob('.' + file_name)
    print(files)

    add_abundances_input = input("Do you want to \n[1] add abundances \nor \n[2] overwrite chronologically?: ")
    add_abundances = True
    if add_abundances_input == '2':
        add_abundances = False

for fname in files:
    with open(fname, 'rU') as input_file:
        input_reader = csv.reader(input_file, delimiter='\t')
        headers = next(input_reader)
        rows_checked = 0
        duplicates_handled_count = 0
        otu_row_dict = OrderedDict()
        for otu_key, otu_row in enumerate(input_reader):
            rows_checked += 1
            otu_name = otu_row[0]
            if otu_name in otu_row_dict:
                if add_abundances:
                    print("duplicate of otu name: ", otu_name)
                    otu_row_dict[otu_name] = sum_row_values(otu_row_dict[otu_name], otu_row)
                else:
                    otu_row_dict[otu_name] = otu_row
                duplicates_handled_count += 1         
            else:
                otu_row_dict[otu_name] = otu_row

    with open('%s-removed_duplicates.tsv' % fname, "w+") as output_file:
        writer = csv.writer(output_file, delimiter="\t")
        writer.writerow(headers)
        for row in otu_row_dict:
            # TODO: small casting of values to reduce file size ?
            writer.writerow(otu_row_dict[row])

    print('Rows combined: %d' % duplicates_handled_count)
    print('Rows checked: %d' % rows_checked)
