import csv

input_file = open('./test_inputs/new-data/Gavin_water_data_2010_and_Ian_fungi_data.tsv')

output_file = open('./test_outputs/removed_duplicates.tsv', "w+")

def make_writable_line(list):
    return '\t'.join(str(value) for value in list) + '\n'

input_reader = csv.reader(input_file, delimiter='\t')
headers = next(input_reader)
output_file.write(make_writable_line(headers))
taxons_entered = set()
total_rows = 0
remove_count = 0
for row in input_reader:
    total_rows += 1
    if row[0] in taxons_entered:
        remove_count += 1
        continue
    else:
        output_row = make_writable_line(row)
        output_file.write(output_row)
        taxons_entered.add(row[0])
print('remove %d rows' % remove_count)
print('total %d rows' % total_rows)
    