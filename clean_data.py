import csv
import os
from pyproj import Proj, transform

def append_file_name(path, append):
    '''appends in a file name at the between the name and the extension'''
    path_no_extension = path[:len(path)-4]+ append + '.tsv'
    print(path_no_extension)
    return path_no_extension

def uppercase_meta_sites(input_path):
    with open(input_path, 'r') as input_metadata_file:
        output_meta_path = append_file_name(input_path, '_uppercased')
        with open (output_meta_path, 'w') as output_data_file:
            reader = csv.reader(input_metadata_file, delimiter='\t')
            writer = csv.writer(output_data_file, delimiter='\t')
            # skip header
            writer.writerow(next(reader))
            for row in reader:
                uppercase_site_row = row
                uppercase_site_row[0] = uppercase_site_row[0].upper()
                writer.writerow(uppercase_site_row)
            return output_meta_path

def swap_rows(input_path):
    rows_to_swap = input("values to swap format (row1,row2): ")    
    row1, row2 = rows_to_swap.split(',')
    with open(input_path, 'r') as input_file:
        reader = csv.DictReader(input_file , delimiter='\t')
        fieldnames = reader.fieldnames
        output_meta_path = append_file_name(input_path, '_swapped')
        with open(output_meta_path, 'w') as output_file:
            dict_writer = csv.DictWriter(f=output_file, fieldnames=fieldnames, delimiter='\t')
            dict_writer.writeheader()
            for row in reader:
                # assume they're swapping coordinates right now as the qualifier for which rows to swap 
                if (float(row['y']) > 0):
                    original_row1_value, original_row2_value = row[row1], row[row2]
                    print(original_row1_value, original_row2_value)
                    swapped_row = row
                    swapped_row[row1] = original_row2_value
                    swapped_row[row2] = original_row1_value
                    print(swapped_row[row1], swapped_row[row2])
                    dict_writer.writerow(swapped_row)
                else:
                    dict_writer.writerow(row)
            return output_meta_path

def convert_coordinates(input_path):
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
    with open(input_path, 'r') as input_file:
        reader = csv.reader(input_file, delimiter='\t')
        output_meta_path = append_file_name(input_path, '_converted_coordinates')
        with open(output_meta_path, "w") as output_file:
            writer = csv.writer(output_file, delimiter='\t')
            firstLine = True
            for row in reader:
                if firstLine:
                    firstLine = False
                    writer.writerow(row)
                    continue
                # Change to match the column numbers that need to be converted.
                # Doesn't convert x value out of wgs84 range then we know it's nzgd2000 or something else.
                if float(row[1]) > 1000:
                    x, y = _convert_coordinate(row[1], row[2])
                    converted_row = row
                    converted_row[1] = str(x)
                    converted_row[2] = str(y)
                    writer.writerow(converted_row)
                else:
                    writer.writerow(row)
        return output_meta_path

f_out = convert_coordinates('./test_inputs/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv')
print(f_out)
f_out = swap_rows(f_out)
print(f_out)
f_out = uppercase_meta_sites(f_out)
print(f_out)