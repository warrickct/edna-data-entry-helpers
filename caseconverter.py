import csv

# Makes new headers all uppercase, outputs to a new file in the output directory.
with open('./test_inputs/new-data/Gavin_water_data_2010_and_Ian_fungi_data.tsv', 'r') as input_data_file:
    with open ('./test_outputs/data_uppercase_headers.tsv', 'w') as output_data_file:
        input_reader = csv.reader(input_data_file, delimiter='\t')
        input_headers = next(input_reader)
        uppercase_headers = []
        for header in input_headers:
            uppercase_headers.append(header.upper())
        writer = csv.writer(output_data_file, delimiter='\t')
        writer.writerow(uppercase_headers)
        for input_row in input_reader:
            writer.writerow(input_row)


# metadata_file = open('./testfiles/new-data/*_metadata.tsv')
with open('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv', 'r') as input_metadata_file:
    with open ('./test_outputs/metadata_uppercase_sites.tsv', 'w') as output_data_file:
        reader = csv.reader(input_metadata_file, delimiter='\t')
        writer = csv.writer(output_data_file, delimiter='\t')
        # skip header
        writer.writerow(next(reader))
        for row in reader:
            uppercase_site_row = row
            uppercase_site_row[0] = uppercase_site_row[0].upper()
            writer.writerow(uppercase_site_row)