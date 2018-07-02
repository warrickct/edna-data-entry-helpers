import csv
import unittest

class TestTempFileMethods(unittest.TestCase):

    def testDuplicateAbundanceForeignKeys(self):
        '''Checks for duplicate sample_otu primary keys'''
        self.file = open('./testfiles/bpaotu-9giql3lf')
        self.reader = csv.reader(self.file)
        pks_entered = []
        for line in self.reader:
            pk = "sample"+line[0] + "otu" + line[1]
            assert pk not in pks_entered, pk
            pks_entered.append(pk)
            

class TestTsvFiles(unittest.TestCase):

    def setUp(self):
        '''open abundance and meta files and set up readers'''
        self.abundance_file = open('./testfiles/new-data/Gavin_water_data_2010_and_Ian_fungi_data.tsv')
        self.meta_file = open('./testfiles/new-data/Gavin_water_metadata_2010_and_Ian_fungi_metadata.tsv')
        self.meta_reader = csv.DictReader(self.meta_file, delimiter='\t')
        self.abundance_reader = csv.reader(self.abundance_file, delimiter='\t')

    def testSitesInAbundanceFileExist(self):
        ''' testing all abundance column sites exist in the meta file '''
        # generate list of all sites in metadata file.
        sites_list = []
        for row in self.meta_reader:
            site_code = row['site'].upper()
            sites_list.append(site_code)
        # iterates through all abundance data headers excluding otu name column. Checks if it exists in the site list.
        abundance_site_headers = next(self.abundance_reader)[1:]
        for site_header in abundance_site_headers:
            assert site_header in sites_list, site_header

    def testRowAbundanceFileRowLength(self):
        ''' testing if the abundance file is a valid matrix '''
        expected_row_length = len(next(self.abundance_reader))
        for row in self.abundance_reader:
            assert len(row) == expected_row_length

    def testSameAmountOfSitesInBothFiles(self):
        abundance_site_headers = next(self.abundance_reader)[1:]
        meta_sites = []
        for line in self.meta_reader:
            meta_sites.append(line['site'])
        print('first and last in meta files', meta_sites[0], meta_sites[len(meta_sites)-1])
        print('first and last in abundance files', abundance_site_headers[0], abundance_site_headers[len(abundance_site_headers)-1])
        assert len(abundance_site_headers) == len(meta_sites), meta_sites

if __name__== '__main__':
    unittest.main()
