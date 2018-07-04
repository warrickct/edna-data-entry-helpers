from csv import DictReader, DictWriter

rows_to_swap = input("values to swap format (row1,row2): ")    
row1, row2 = rows_to_swap.split(',')
with open('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv', 'r') as input_file:
    reader = DictReader(input_file , delimiter='\t')
    fieldnames = reader.fieldnames
    with open('./test_outputs/Gavin_water_metadata_2010_and_Ian_fungi_metadata-swapped.tsv', 'w') as output_file:
        dict_writer = DictWriter(f=output_file, fieldnames=fieldnames, delimiter='\t')
        dict_writer.writeheader()
        for row in reader:
            original_row1_value, original_row2_value = row[row1], row[row2]
            print(original_row1_value, original_row2_value)
            swapped_row = row
            swapped_row[row1] = original_row2_value
            swapped_row[row2] = original_row1_value
            print(swapped_row[row1], swapped_row[row2])
            dict_writer.writerow(swapped_row)