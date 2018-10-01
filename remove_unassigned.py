import csv

with open ('./test_inputs/Syrie-plant-16S-COI-Fish-data-warrick-edited.csv', 'r') as input_file:
    with open('./test_outputs/syrie_no_unassigned.tsv', 'w') as out_file:
        reader = csv.reader(input_file)
        writer = csv.writer(out_file, delimiter='\t')
        # skipping line regarding what type of data syria data is.
        next(reader)
        for line in reader:
            if line[0].startswith("Unassigned"):
                continue
            else:
                writer.writerow(line)