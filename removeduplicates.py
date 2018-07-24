import csv
import glob

files = set(glob.glob('./test_inputs/new-data/*.tsv')) - set(glob.glob('./test_inputs/new-data/*removed_duplicates.tsv'))
for fname in files:
    with open(fname, 'rU') as input_file:
        output_file = open('%s-removed_duplicates.tsv' % fname, "w+")

        def make_writable_line(list):
            return '\t'.join(str(value) for value in list) + '\n'

        def sum_row_values(r, r2):
            new_row = []
            new_row.append(r[0])
            for index in range(1, len(r)-1):
                total = float(r[index]) + float(r2[index])
                new_row.append(total)
            return new_row

        input_reader = csv.reader(input_file, delimiter='\t')
        headers = next(input_reader)
        output_file.write(make_writable_line(headers))
        taxons_entered = {}
        total_rows = 0
        duplicate_count = 0
        new_file_object = {}
        for index, otu_row in enumerate(input_reader):
            total_rows += 1
            otu_name = otu_row[0]
            if otu_name in taxons_entered:
                new_file_object[index] = sum_row_values(taxons_entered[otu_name], otu_row)
                duplicate_count += 1         
            else:
                new_file_object[index] = otu_row
                taxons_entered[otu_name] = otu_row

    with open('%s-removed_duplicates.tsv' % fname, "w+") as output_file:
        output_file.write(make_writable_line(headers))
        for list in new_file_object:
            output_file.write(make_writable_line(new_file_object[list]))

        
    print('remove %d rows' % duplicate_count)
    print('total %d rows' % total_rows)
    