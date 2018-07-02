import csv

file = open('./Gavin_water_data_2010.tsv', 'rU')
reader = csv.reader(file, delimiter='\t')
next(reader)
richness_count = 0
entry_count = 0
for row in reader:
    for col in row[1:]:
        entry_count += 1
        if float(col) > 0:
            print(col)
            richness_count += 1
# print(richness_count)
print(entry_count)


import_file = open('./bpaotu-35zqg1i4')
reader = csv.reader(import_file)
# skip headers
next(reader)
otu_count = 0
otus_over_zero= 0
row_count = 0
for row in reader:
    row_count += 1
    if row[1] == '14':
        otu_count += 1
        if float(row[2]) > 0:
            otus_over_zero += 1
print(row_count)
print(otu_count)
print(otus_over_zero)