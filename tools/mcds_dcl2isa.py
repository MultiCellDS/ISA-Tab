#
# mcds_dcl2isa.py - using a MultiCellDS digital cell line XML file, generate associated ISA-Tab files
#
# Input:
#   a MultiCellDS digital cell line file  <DCL-root-filename>.xml
# Output:
#   3 ISA files:
#    i_<DCL-root-filename>.txt
#    s_<DCL-root-filename>.txt
#    a_<DCL-root-filename>.txt
#
# Author: Randy Heiland
# Date:
#   v0.1 - May 2018
# 

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path  # Python 3?

if (len(sys.argv) < 2):
  print("Usage: " + sys.argv[0] + " <MultiCellDS Digital Cell Line XML file>")
  sys.exit(0)
else:
  xml_file = sys.argv[1]

# for testing, just set it
#xml_file = "MCDS_L_0000000052.xml"

header = '\
ONTOLOGY SOURCE REFERENCE\n\
Term Source Name	"NCIT"	"UO"	"NCBITAXON"	"EDDA"\n\
Term Source File	"https://ncit.nci.nih.gov/ncitbrowser/"	"https://bioportal.bioontology.org/ontologies/UO"	"http://purl.obolibrary.org/obo/NCBITaxon_1"	"http://bioportal.bioontology.org/ontologies/EDDA"\n\
Term Source Version	"17.02d"	""	""	"2.0"\n\
Term Source Description	"NCI Thesarus"	""	""	"Evidence in Documents, Discovery, and Analytics (EDDA)"\
'

if not Path(xml_file).is_file():
	print(xml_file + 'does not exist!')
	sys.exit(-1)

investigation_filename = "i_" + xml_file[:-4] + ".txt"
study_filename = "s_" + xml_file[:-4] + ".txt"
assay_filename = "a_" + xml_file[:-4] + ".txt"

fp = open(investigation_filename, 'w')

tree = ET.parse(xml_file)  # TODO: relative path using env var?
xml_root = tree.getroot()

sep_char = '\t'

fp.write(header + '\n')
fp.write('INVESTIGATION\n')
#print(xml_root.find(".//MultiCellDB").find(".//ID").text)
i_identifier = '"' + xml_root.find(".//metadata").find(".//ID").text + '"'
i_title = '"' + xml_root.find(".//metadata").find(".//name").text + '"'
i_desc = '"' + xml_root.find(".//metadata").find(".//description").text + '"'
fp.write('Investigation Identifier' + sep_char + i_identifier + '\n')
fp.write('Investigation Title' + sep_char +  i_title + '\n')
fp.write('Investigation Description' + sep_char + i_desc + '\n')
fp.write('Investigation Submission Date' + sep_char + '""\n')
fp.write('Investigation Public Release Date \t "" \n') 
citation_str = '"' + re.sub('[\t\n]','',xml_root.find(".//citation").find(".//text").text) + '"'  # remove all tabs and newlines 
fp.write('Comment [MultiCellDS/cell_line/metadata/citation/text]' + sep_char + citation_str + '\n')

if (xml_root.find(".//citation").find(".//notes")):
  fp.write('Comment [MultiCellDS/cell_line/metadata/citation/notes]' + sep_char + xml_root.find(".//citation").find(".//notes").text  + '\n')
  

fp.write('INVESTIGATION PUBLICATIONS\n')
# Extract over all <PMID> in <data_origin> and <data_analysis>
#print('Investigation PubMed ID	"21988888"	"23084996"	"22342935" ' )
# Extract <PMID> and <DOI> in all <data_origin> and <data_analysis>
# TODO? will we have matching # of each?
pmid = []
doi = []
uep = xml_root.find('.//data_origins')  # uep = unique entry point
for elm in uep.findall('data_origin'):
    doi.append(elm.find('.//DOI').text)
    pmid.append(elm.find('.//PMID').text)

uep = xml_root.find('.//metadata')
for elm in uep.findall('data_analysis'):
#    print(' "' + el.find('.//PMID').text + '"', end='')
  doi.append(elm.find('.//DOI').text)
  pmid.append(elm.find('.//PMID').text)

sep_char_sq = sep_char + '"'   # tab + single quote

pmid_str = ''
for elm in pmid:
  pmid_str += sep_char + '"' + elm + '"'
fp.write('Investigation PubMed ID' + pmid_str + '\n')

doi_str = ''
for elm in doi:
  doi_str += sep_char + '"' + elm + '"'
fp.write('Investigation Publication DOI' + doi_str + '\n')

empty_str = ''.join(sep_char + '""' for x in pmid) 
fp.write('Investigation Publication Author List' + empty_str + '\n')
fp.write('Investigation Publication Title' + empty_str + '\n')

pub_status_str = ''.join('\t"Published"' for x in pmid) 
pub_title_str = ''.join('\t""' for x in pmid) 
fp.write('Investigation Publication Status' + pub_status_str + '\n')
pub_status_TA_str = ''.join('\t"C19026"' for x in pmid) 
fp.write('Investigation Publication Status Term Accession' + pub_status_TA_str + '\n')
pub_status_TSR_str = ''.join('\t"NCIT"' for x in pmid) 
fp.write('Investigation Publication Status Term Source REF' + pub_status_TSR_str + '\n')

fp.write('INVESTIGATION CONTACTS\n') 
fp.write('Investigation Person Last Name' + sep_char_sq + xml_root.find(".//current_contact").find(".//family-name").text + '"\t\n') 
fp.write('Investigation Person First Name' + sep_char_sq + xml_root.find(".//current_contact").find(".//given-names").text + '"\n') 
fp.write('Investigation Person Mid Initials' + sep_char + '""\n')
fp.write('Investigation Person Email' +  sep_char_sq + xml_root.find(".//current_contact").find(".//email").text + '"\n') 
fp.write('Investigation Person Phone' + sep_char +  '""\n')
fp.write('Investigation Person Fax' + sep_char +  '""\n')
fp.write('Investigation Person Address'  + sep_char +  '""\n')
fp.write('Investigation Person Affiliation' + sep_char_sq + xml_root.find(".//current_contact").find(".//organization-name").text + 
            ', ' + xml_root.find(".//current_contact").find(".//department-name").text + '"\n') 
fp.write('Investigation Person Roles' + sep_char +  '""\n')
fp.write('Investigation Person Roles Term Accession Number' + sep_char + '""\n')
fp.write('Investigation Person Roles Term Source REF' + sep_char + '""\n')
fp.write('Comment[Investigation Person REF]' + sep_char + '""\n')


fp.write('STUDY\n')
fp.write('Study Identifier\t' + i_identifier + '\n')
fp.write('Study Title\t' + i_title + '\n')
fp.write('Study Description\t' + i_desc + '\n')
fp.write('Comment[Study Grant Number]\t""\n')
fp.write('Comment[Study Funding Agency]\t""\n')
fp.write('Study Submission Date\t""\n')
fp.write('Study Public Release Date\t""\n')
fp.write('Study File Name\t' + '"' + study_filename + '"\n')


fp.write('STUDY DESIGN DESCRIPTORS\n')
fp.write('Study Design Type\t""\n')
fp.write('Study Design Type Term Accession Number\t""\n')
fp.write('Study Design Type Term Source REF\t""\n')

# TODO? are these different than the previous pubs?
fp.write('STUDY PUBLICATIONS\n')
fp.write('Study PubMed ID' + pmid_str + '\n')
fp.write('Study Publication DOI' + doi_str + sep_char + '\n')
fp.write('Study Publication Author List' + empty_str + '\n')
fp.write('Study Publication Title' + pub_title_str + '\n')
fp.write('Study Publication Status' + pub_status_str + sep_char + '\n')
fp.write('Study Publication Status Term Accession Number' + pub_status_TA_str + sep_char + '\n')
fp.write('Study Publication Status Term Source REF' + pub_status_TSR_str + '\n')


fp.write('STUDY FACTORS' + 3*sep_char + '\n')
fp.write('Study Factor Name\t"phenotype_dataset"\n')
fp.write('Study Factor Type\t""\n')
fp.write('Study Factor Type Term Accession Number\t""\n')
fp.write('Study Factor Type Term Source REF\t""\n')
#fp.write('Comment[phenotype_dataset_keywords] "viable; hypoxic; physioxia(standard);  physioxia(breast); necrotic,chronic hypoxia"\n')
#fp.write('Comment[phenotype_dataset_keywords] "')
comment_str = 'Comment[phenotype_dataset_keywords]\t"'
uep = xml_root.find('.//cell_line')
for elm in uep.findall('phenotype_dataset'):
  comment_str += elm.attrib['keywords'] + '; '
#  print(comment_str)
fp.write(comment_str[:-2] + '"\n')


fp.write('STUDY ASSAYS\t\n')
fp.write('Study Assay Measurement Type\t""\n')
fp.write('Study Assay Measurement Type Term Accession Number\t""\n')
fp.write('Study Assay Measurement Type Term Source REF\t""\n')
fp.write('Study Assay Technology Type\t""\n')
fp.write('Study Assay Technology Type Term Accession Number\t""\n')
fp.write('Study Assay Technology Type Term Source REF\t""\n')
fp.write('Study Assay Technology Platform\t""\n')
fp.write('Study Assay File Name\t' + '"' + assay_filename + '"\n')


fp.write('STUDY PROTOCOLS\t\n')
fp.write('Study Protocol Name\t"microenvironment.measurement"\n')
fp.write('Study Protocol Type\t""\n')
fp.write('Study Protocol Type Term Accession Number\t""\n')
fp.write('Study Protocol Type Term Source REF\t""\n')
fp.write('Study Protocol Description\t""\n')
fp.write('Study Protocol URI\t""\n')
fp.write('Study Protocol Version\t""\n')
#fp.write('Study Protocol Parameters Name  "oxygen.partial_pressure; DCIS_cell_density(2D).surface_density; DCIS_cell_area_fraction.area_fraction; DCIS_cell_volume_fraction.volume_fraction"\n')
comment_str = 'Study Protocol Parameters Name\t"'
# TODO? search for all phenotype_dataset/microenvironment/domain/variables/...
uep = xml_root.find('.//variables')
if (uep):
  for elm in uep.findall('variable'):
    comment_str += elm.attrib['name'] + '.' + elm.attrib['type'] + '; '
#  print(comment_str)
  fp.write(comment_str[:-2] + '"\n')

semicolon_sep_empty_str = ''.join('; ' for x in pmid)
fp.write('Study Protocol Parameters Name Term Accession Number\t" ' + semicolon_sep_empty_str + ' "\n')
fp.write('Study Protocol Parameters Name Term Source REF\t" ' + semicolon_sep_empty_str + ' "\n')
fp.write('Study Protocol Components Name\t"' + semicolon_sep_empty_str + ' "\n')
fp.write('Study Protocol Components Type\t"' + semicolon_sep_empty_str + ' "\n')
fp.write('Study Protocol Components Type Term Accession Number\t"' + semicolon_sep_empty_str + ' "\n')
fp.write('Study Protocol Components Type Term Source REF\t"' + semicolon_sep_empty_str + ' "\n')


fp.write('STUDY CONTACTS\t\n')
fp.write('Study Person Last Name\t"' + xml_root.find(".//current_contact").find(".//family-name").text + '"\n') 
fp.write('Study Person First Name\t"' + xml_root.find(".//current_contact").find(".//given-names").text + '"\n') 
fp.write('Study Person Mid Initials\t""\n')
fp.write('Study Person Email\t"' +  xml_root.find(".//current_contact").find(".//email").text + '"\n') 
fp.write('Study Person Phone\t""\n')
fp.write('Study Person Fax\t""\n')
fp.write('Study Person Address\t""\n')
fp.write('Study Person Affiliation\t"' +  xml_root.find(".//current_contact").find(".//organization-name").text + 
            ', ' + xml_root.find(".//current_contact").find(".//department-name").text + '"\n') 
fp.write('Study Person Roles\t""\n')
fp.write('Study Person Roles Term Accession Number\t""\n')
fp.write('Study Person Roles Term Source REF\t""\n')
fp.write('Comment[creator_orcid-id_family-name]\t"' + xml_root.find(".//creator").find(".//family-name").text + '"\n') 
fp.write('Comment[creator_orcid-id_given-names]\t"' + xml_root.find(".//creator").find(".//given-names").text + '"\n') 
fp.write('Comment[creator_orcid-id_email]\t"' + xml_root.find(".//creator").find(".//email").text + '"\n')
fp.write('Comment[creator_orcid-id_organization-name]\t"' +  xml_root.find(".//creator").find(".//organization-name").text + 
            ', ' + xml_root.find(".//creator").find(".//department-name").text + '"\n') 
fp.write('Comment[curator_orcid-id_family-name]\t"' + xml_root.find(".//curator").find(".//family-name").text + '"\n') 
fp.write('Comment[curator_orcid-id_given-names]\t"' + xml_root.find(".//curator").find(".//given-names").text + '"\n')
fp.write('Comment[curator_orcid-id_email]\t"' + xml_root.find(".//curator").find(".//email").text + '"\n')
fp.write('Comment[curator_orcid-id_organization-name]\t"' +  xml_root.find(".//curator").find(".//organization-name").text + 
            ', ' + xml_root.find(".//creator").find(".//department-name").text + '"\n') 
fp.write('Comment[last_modified_by_orcid-id_family-name]\t"' + xml_root.find(".//last_modified_by").find(".//family-name").text + '"\n')
fp.write('Comment[last_modified_by_orcid-id_given-names]\t"' + xml_root.find(".//last_modified_by").find(".//given-names").text + '"\n')
fp.write('Comment[last_modified_by_orcid-id_email]\t"' + xml_root.find(".//last_modified_by").find(".//email").text + '"\n')
fp.write('Comment[last_modified_by_orcid-id_organization-name]\t"' +  xml_root.find(".//last_modified_by").find(".//organization-name").text + 
            ', ' + xml_root.find(".//last_modified_by").find(".//department-name").text + '"\n') 
fp.write('Comment[Study Person REF]' + sep_char + '""' + '\n')

fp.close()
print(' --> ' + investigation_filename)


#=======================================================================
fp = open(study_filename, 'w')

fp.write('Source Name' + sep_char)
source_name = i_identifier[1:-1] + '.0'

uep = xml_root.find('.//data_origins')  # uep = unique entry point
for elm in uep.findall('data_origin'):
  for elm2 in elm.findall('citation'):
    fp.write('Comment[citation]' + sep_char)
    pmid_origin = elm.find('.//PMID').text

uep = xml_root.find('.//metadata')
for elm in uep.findall('data_analysis'):
  for elm2 in elm.findall('citation'):
    fp.write('Comment[citation]' + sep_char)

uep = xml_root.find('.//cell_origin')
cell_origin_characteristics = []
for elm in uep.getchildren():
  fp.write('Characteristics[' + elm.tag + ']' + sep_char)
  cell_origin_characteristics.append(elm.text)

fp.write('Factor Value[phenotype_dataset]' + sep_char + 'Sample Name\n')

uep = xml_root.find('.//cell_line')
suffix = 0
for elm in uep.findall('phenotype_dataset'):
  row_str = source_name + sep_char 
  for p in pmid:
    row_str += 'PMID: ' + p + sep_char
  for c in cell_origin_characteristics:
    row_str += c + sep_char 
  row_str += elm.attrib['keywords'] + sep_char + source_name + '.' + str(suffix)
              
  suffix += 1
#  print(row_str)
  fp.write(row_str + '\n')

fp.close()
print(' --> ' + study_filename)


#=======================================================================
fp = open(assay_filename, 'w')

fp.write('Sample Name' + sep_char + 'Protocol REF' + sep_char + 'Parameter Value[')


fp.close()
print(' --> ' + assay_filename)
