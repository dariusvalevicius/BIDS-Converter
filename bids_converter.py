from bz2 import compress
import os
import argparse
import shutil
import gzip
from glob import glob

## TODO

# Implement
    # Echo?
    # CE?
# Additional subdirectories and modality support:
    # FMAP?
# Stretch goals:
    # Metadata/json headers


# Argument parser
print('Parsing arguments...')

parser = argparse.ArgumentParser(
    description='Convert an arbitrarily structured brain imaging dataset to BIDS format')
parser.add_argument('-i', '--input', type=str, metavar='',
                    help='Input folder containing data')
parser.add_argument('-s', '--subject', type=str,
                    metavar='', help='Subject number')
parser.add_argument('--sessions', type=str, metavar='',
                    help='Strings identifying sessions')
parser.add_argument('-r', '--runs', type=str, metavar='',
                    help='Strings identifying runs')
parser.add_argument('-t', '--tasks', type=str, metavar='',
                    help='Strings identifying tasks')
parser.add_argument('--task_suffixes', type=str, metavar='',
                    help='Strings identifying tasks')
parser.add_argument('--acq', type=str, metavar='',
                    help='Strings identifying acquisitions')
parser.add_argument('--acq_suffixes', type=str, metavar='',
                    help='Strings identifying acquisition suffixes')


parser.add_argument('-a', '--anat', default=False,
                    action='store_true', help='Presence of anatomical data')
parser.add_argument('--t1w', type=str, metavar='',
                    help='Shell-type expression identifying T1 weighted images')
parser.add_argument('--t2w', type=str, metavar='',
                    help='Shell-type expression identifying T2 weighted images')
parser.add_argument('--flair', type=str, metavar='',
                    help='Shell-type expression identifying FLAIR images')

parser.add_argument('-f', '--func', default=False,
                    action='store_true', help='Presence of functional data')
parser.add_argument('-b', '--bold', type=str, metavar='',
                    help='Shell-type expression describing BOLD data files')
parser.add_argument('--asl', type=str, metavar='',
                    help='Shell-type expression describing ASL data files')
parser.add_argument('-p', '--physio', type=str, metavar='',
                    help='Shell-type expression describing physiological data files')

parser.add_argument('-d', '--dwi', default=False,
                    action='store_true', help='Presence of DWI images')
parser.add_argument('--dwi_strings', type=str, metavar='',
                    help='Shell-type expression identifying WDI images')

parser.add_argument('--nocompress', default=False,
                    action='store_true', help='Turn off gzip compression, saves time while testing')


args = parser.parse_args()

print('Done.')


# Declare global vars

entity_dict = {} # Stores input strings as keys and BIDS entities as values
subject_folder = ''
session_folders = []

# Define helper functions

# Create modality folder
# If there are sessions, nest within sessions
def create_modality_dir(modality_exists, folder_name):

    if not modality_exists:
        return

    if session_folders:
        for folder in session_folders:
            os.mkdir(os.path.join(folder, folder_name))
    else:
        os.mkdir(os.path.join(subject_folder, folder_name))



def compress_nii(file_path):
    # If .nii is uncompressed, compress
    if (not '.gz' in file_path) and (not args.nocompress):
        with open(file_path, 'rb') as f_in:
            with gzip.open(file_path + '.gz', 'wb', compresslevel=3) as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file_path)


def populate_dict(entity_identifier, entity_prefix, entity_suffix=''):

    # If argument is blank, exit function
    if not entity_identifier:
        return
    
    # loop through input sets separated by semicolons
    sets = entity_identifier.split(';')
    for set in sets:

        # Loop through keys within sets
        keys = set.split(',')

        index = 0
        for key in keys:
            # construct appropriate BIDS entity string
            if (entity_suffix):
                entity_suffix_list = entity_suffix.split(',')
                entity_dict[key.casefold()] =  entity_prefix + '-' + entity_suffix_list[index]
            else:
                entity_dict[key.casefold()] =  entity_prefix + '-' + str((index + 1))

            index += 1
  

def copy_modality_files(modality, identifier, category):

    # if argument is empty, return
    if not identifier:
        return

    # Find all files with identifier
    source_files = glob(args.input + '/**/*' + identifier + '*', recursive=True)

    # For each file of modality
    for source_file in source_files:

        # Find which entities are present
        # This_entities stores values of present entities
        this_entities = {}
        entity_strings = ['ses', 'task', 'acq', 'run']

        for key in entity_dict:
            if key in source_file.casefold():
                value =  entity_dict.get(key).split('-')[0]
                #print('value:')
                #print(value)
                for entity_string in entity_strings:
                    if value == entity_string:
                        this_entities[entity_string] = entity_dict[key] + '_'

        entity_string = this_entities.get('ses', "") + this_entities.get('task', "") + this_entities.get('acq', "") + this_entities.get('run', "")
        ext = os.path.splitext(source_file)[1]
        #print('ext: ')
        #print(ext)
        dest_filename = subject_folder + '_' + entity_string + modality + ext
        dest_filepath = os.path.join(subject_folder, this_entities.get('ses', "").strip('_'), category, dest_filename)

        # copy file
        shutil.copy(source_file, dest_filepath)

        if '.nii' in dest_filepath:
            compress_nii(dest_filepath)


# Main
if __name__ == '__main__':

    #for arg in vars(args):
    #    print(arg, getattr(args, arg))

    print('Creating subject folder...')

    # Get subject number
    subject_num = ''

    if args.subject:
        # If explicitly declared, get from argument
        subject_num = args.subject.zfill(2)
    else:
        # Else, try to extract from input foldername
        print('Subject number not explicitly declared. Attempting to extract from input foldername...')
        extracted_num = ''
        for m in args.input:
            if m.isdigit():
                extracted_num += m
        if not extracted_num:
            print('Error! Did not find subject number in folder name.')
            # throw error
        subject_num = extracted_num.zfill(2)
        #print('subject num:')
        #print(subject_num)

    # Create top-level subject folder
    subject_folder = 'sub-' + subject_num

    # If folder exists, remove
    if os.path.isdir(subject_folder):
        shutil.rmtree(subject_folder)

    os.mkdir(subject_folder)

    print('Done.')

    # If sessions were input, create a list of sessions and
    # a folder for each one.
    # Also create a dictionary mapping session strings to session directory names.
    session_folders = []

    if args.sessions:
        print('Creating session folders...')
        session_string_sets = args.sessions.split(';')
        # print(session_string_sets)

        index = 0
        for session in session_string_sets[0].split(','):
            subdir_name = 'ses-' + str(index + 1)

            session_folders.append(os.path.join(subject_folder, subdir_name))
            os.mkdir(session_folders[index])

            index += 1
        print('Done.')


    print('Creating modality subfolders...')
    # create modality folders

    modality_subdirs = [
        [args.anat, 'anat'],
        [args.func, 'func'],
        [args.dwi, 'dwi']
        ]

    for subdir in modality_subdirs:
        create_modality_dir(subdir[0], subdir[1])

    print('Done.')

    print('Creating BIDS entity dictionary...')
    # collect up all entities
    arg_list = [
        [args.sessions, 'ses', ''],
        [args.tasks, 'task', args.task_suffixes],
        [args.runs, 'run', ''],
        [args.acq, 'acq', args.acq_suffixes],
        ]

    # Populate entity dictionary using input strings
    for arg_set in arg_list:
        populate_dict(arg_set[0], arg_set[1], arg_set[2])

    print('Done.')
    print('Entity dictionary:')
    for key in entity_dict:
        print('Key: ' + key + '\t Value: ' + entity_dict.get(key, 'None').strip('_'))


    modalities = [
        ['T1w', args.t1w, 'anat'],
        ['T2w', args.t2w, 'anat'],
        ['FLAIR', args.flair, 'anat'],
        ['BOLD', args.bold, 'func'],
        ['ASL', args.asl, 'func'],
        ['physio', args.physio, 'func'],
        ['DWI', args.dwi, 'dwi']
    ]

    print('Modality identifiers:')
    for md in modalities:
        if md[1]:
            print('Modality: ' + md[0] + '\tIdentifier: ' + md[1])


    print('NIFTI compression is set to ' + str(not args.nocompress) + '.')

    print('Copying files...')

    for modality in modalities:
        copy_modality_files(modality[0], modality[1], modality[2])

    print('Done.')

