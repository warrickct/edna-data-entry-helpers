import csv
import glob

def make_writable_line(list):
            return '\t'.join(str(value) for value in list) + '\n'

def sum_row_values(r, r2):
    print('r: ', len(r))
    print('r2: ', len(r2))
    new_row = []
    new_row.append(r[0])
    for index in range(1, len(r)):
        total = float(r[index]) + float(r2[index])
        new_row.append(total)
    return new_row

files = set(glob.glob('./test_inputs/new-data/*.tsv')) - set(glob.glob('./test_inputs/new-data/*removed_duplicates.tsv'))
for fname in files:
    with open(fname, 'rU') as input_file:
        input_reader = csv.reader(input_file, delimiter='\t')
        headers = next(input_reader)
        rows_checked = 0
        duplicate_count = 0
        new_rows = {}
        row_lookup = []
        for index, otu_row in enumerate(input_reader):
            rows_checked += 1
            otu_name = otu_row[0]
            if otu_name in new_rows:
                new_rows[otu_name] = sum_row_values(new_rows[otu_name], otu_row)
                duplicate_count += 1         
            else:
                new_rows[otu_name] = otu_row
            row_lookup.append(otu_name)

    with open('%s-removed_duplicates.tsv' % fname, "w+") as output_file:
        writer = csv.writer(output_file, delimiter="\t")
        writer.writerow(headers)
        # writer.writerows(new_rows)
        for index in row_lookup:
            writer.writerow(new_rows[index])

    print('remove %d rows' % duplicate_count)
    print('total %d rows' % rows_checked)
