import csv
from pyproj import Proj, transform

'''
* Uppercases the site codes in data and metadata
* Has option to swap the coordinate values for the columns
* Has the option to convert the coordinates from NZGD2000 to WGS84
'''

def swap_columns():
    rows_to_swap = input("values to swap format (row1,row2): ")    
    row1, row2 = rows_to_swap.split(',')
    with open('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv', 'r') as input_file:    # NOTE: COMMON
        reader = csv.DictReader(input_file , delimiter='\t')
        fieldnames = reader.fieldnames
        with open('./test_outputs/Gavin_water_metadata_2010_and_Ian_fungi_metadata-swapped.tsv', 'w') as output_file:   # NOTE: COMMON
            dict_writer = csv.DictWriter(f=output_file, fieldnames=fieldnames, delimiter='\t')
            dict_writer.writeheader()
            for row in reader:
                original_row1_value, original_row2_value = row[row1], row[row2]
                print(original_row1_value, original_row2_value)
                swapped_row = row
                swapped_row[row1] = original_row2_value
                swapped_row[row2] = original_row1_value
                print(swapped_row[row1], swapped_row[row2])
                dict_writer.writerow(swapped_row)

def uppercase_metadata_sites():
    # metadata_file = open('./testfiles/new-data/*_metadata.tsv')
    with open('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv', 'r') as input_metadata_file:
        with open ('./test_outputs/metadata_uppercase_sites.tsv', 'w') as output_data_file:
            reader = csv.reader(input_metadata_file, delimiter='\t') # NOTE: COMMON
            writer = csv.writer(output_data_file, delimiter='\t')   # NOTE: COMMON
            # skip header
            writer.writerow(next(reader))
            for row in reader:
                uppercase_site_row = row
                uppercase_site_row[0] = uppercase_site_row[0].upper()
                writer.writerow(uppercase_site_row)

def uppercase_sites():
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

def convert_coordinates():
    def _convert_coordinate(x, y):
        '''
        Casts coordinates into numeric floats, converts them from NZGD2000 to epsg:4326
        '''
        x = float(x)
        y = float(y)
        inProj = Proj(init='epsg:2193')
        outProj = Proj(init='epsg:4326')
        out_x, out_y = transform(inProj, outProj, x, y)
        return out_x, out_y

    # Change to file you want to convert.
    file = open('./Gavin_water_data_2010_metadata.tsv') # NOTE: COMMON
    reader = csv.reader(file, delimiter='\t')   # NOTE: COMMON
    # Change change to desired output name
    with open("./output/new_meta.tsv", "w") as output_file: # NOTE: COMMON
        firstLine = True
        for row in reader:
            if firstLine:
                firstLine = False
                output_file.write('\t'.join(row) + '\n')
                continue
            # Change to match the column numbers that need to be converted.
            x, y = _convert_coordinate(row[1], row[2])
            converted_row = row
            converted_row[1] = str(x)
            converted_row[2] = str(y)
            output_file.write("\t".join(converted_row) + '\n')

def remove_duplicates():
    def _make_writable_line(list):  # NOTE: COMMON
        return '\t'.join(str(value) for value in list) + '\n'

    input_file = open('./test_inputs/new-data/Gavin_water_data_2010_and_Ian_fungi_data.tsv')    # NOTE: COMMON
    output_file = open('./test_outputs/removed_duplicates.tsv', "w+")   # NOTE: COMMON
    input_reader = csv.reader(input_file, delimiter='\t')   # NOTE: COMMON
    # NOTE: COMMON ADD WRITER
    headers = next(input_reader)
    output_file.write(_make_writable_line(headers))
    taxons_entered = set()
    total_rows = 0
    remove_count = 0
    for row in input_reader:
        total_rows += 1
        if row[0] in taxons_entered:
            remove_count += 1
            continue
        else:
            output_row = _make_writable_line(row)
            output_file.write(output_row)
            taxons_entered.add(row[0])
    print('remove %d rows' % remove_count)
    print('total %d rows' % total_rows)

def main():
    uppercase_option_input = input("Uppercase the data and metadata? [y/n]: ")
    run_uppercase = uppercase_option_input == 'y'
    swap_columns_input = input("Swap columns? [y/n]: ")
    run_swap_columns = swap_columns_input == 'y'
    convert_coordinates_input = input("Convert coordinates from NZGD2000 to WGS84? [y/n]: ")
    run_convert_coordinates = convert_coordinates_input == 'y'
    remove_duplicates_input = input("Remove duplicate rows in abundance data? [y/n]: ")
    run_remove_duplicate = remove_duplicates_input == 'y'

    with open('./test_inputs/new-data/Gavin_water_data_2010_and_Ian_fungi_data.tsv', 'r') as input_data_file:
        with open ('./test_outputs/cleaned_abundance_data.tsv', 'w') as output_data_file:
            if run_uppercase:
                uppercase_sites()
            if run_remove_duplicate:
                remove_duplicates()

    with open('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv', 'r') as input_metadata_file:
        with open ('./test_outputs/cleaned_metadata.tsv', 'w') as output_metadata_file:
            if run_swap_columns:
                swap_columns()
            if run_convert_coordinates:
                convert_coordinates()
            if run_uppercase:
                uppercase_metadata_sites()


if __name__ == "__main__": 
    main()