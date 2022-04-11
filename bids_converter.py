from bz2 import compress
from ctypes import sizeof
import os
import argparse
import shutil
import gzip
import csv
from datetime import date, datetime
from glob import glob
# from bids_validator import BIDSValidator

# TODO

# JSON sidecars
# Plug in BIDS validator


# Argument parser
print('Parsing arguments...')

parser = argparse.ArgumentParser(
    description='Convert an arbitrarily structured brain imaging dataset to BIDS format')
parser.add_argument('--input', type=str, metavar='',
                    help='Input folder containing data')
parser.add_argument('--output_prefix', type=str, metavar='',
                    help='Top-level output folder prefix, to be combined with input foldername')
parser.add_argument('--subject', type=str,
                    metavar='', help='Subject number')


# Entities
# Session
parser.add_argument('--session', type=str, metavar='',
                    help='Strings identifying sessions')
parser.add_argument('--session_labels', type=str, metavar='',
                    help='Corresponding session labels')
parser.add_argument('--session_use_index', default=False, action='store_true',
                    help='Use index numbers for directory and file names? e.g. ses-1, ses-2')
# Tasks
parser.add_argument('--task', type=str, metavar='',
                    help='Strings identifying tasks')
parser.add_argument('--task_labels', type=str, metavar='',
                    help='Corresponding task labels')
# Runs
parser.add_argument('--run', type=str, metavar='',
                    help='Strings identifying runs')
# Acquisitions
parser.add_argument('--acq', type=str, metavar='',
                    help='Strings identifying acquisitions')
parser.add_argument('--acq_labels', type=str, metavar='',
                    help='Corresponding acquisition labels')
# Constrast enhancing agents
parser.add_argument('--ce', type=str, metavar='',
                    help='Strings identifying constrast enhancing agents')
parser.add_argument('--ce_labels', type=str, metavar='',
                    help='Corresponding contrast enhancing agent labels')
# Tracers
parser.add_argument('--trc', type=str, metavar='',
                    help='Strings identifying tracers')
parser.add_argument('--trc_labels', type=str, metavar='',
                    help='Corresponding tracer labels')
# Reconstructions
parser.add_argument('--rec', type=str, metavar='',
                    help='Strings identifying reconstruction algorithms')
parser.add_argument('--rec_labels', type=str, metavar='',
                    help='Corresponding reconstruction labels')
# Phase-encoding directions
parser.add_argument('--dir', type=str, metavar='',
                    help='Strings identifying phase-encoding directions')
parser.add_argument('--dir_labels', type=str, metavar='',
                    help='Corresponding direction labels')
# Corresponding modality
parser.add_argument('--mod', type=str, metavar='',
                    help='For defacing masks, strings identifying corresponding modality')
parser.add_argument('--mod_labels', type=str, metavar='',
                    help='Corresponding modality labels')
# Echo times
parser.add_argument('--echo', type=str, metavar='',
                    help='Strings identifying different echo times')
parser.add_argument('--echo_values', type=str, metavar='',
                    help='Corresponding echo times')
# Flip angles
parser.add_argument('--flip', type=str, metavar='',
                    help='Strings identifying different flip angles')
parser.add_argument('--flip_values', type=str, metavar='',
                    help='Corresponding flip angles')
# Inversion times
parser.add_argument('--inv', type=str, metavar='',
                    help='Strings identifying different inversion times')
parser.add_argument('--inv_values', type=str, metavar='',
                    help='Corresponding inversion times')
# Magnetization transfer states
parser.add_argument('--mt', type=str, metavar='',
                    help='Strings identifying different magnetization transfer states')
parser.add_argument('--mt_labels', type=str, metavar='',
                    help='Corresponding magnetization transfer labels')
# MRI components
parser.add_argument('--part', type=str, metavar='',
                    help='Strings identifying components of complex MRI signal')
parser.add_argument('--part_labels', type=str, metavar='',
                    help='Corresponding component labels')
# Recordings
parser.add_argument('--recording', type=str, metavar='',
                    help='Strings identifying recordings')
parser.add_argument('--recording_labels', type=str, metavar='',
                    help='Corresponding recording labels')

# Other entity
# parser.add_argument('--other_entity_name', type=str, metavar='',
#                     help='If needed, enter an entity not listed among previous arguments. Use a lower case term or abbreviation.')
# parser.add_argument('--other_entity_strings', type=str, metavar='',
#                     help='Strings identifying other entity keys')
# parser.add_argument('--other_entity_labels', type=str, metavar='',
#                     help='Corresponding entity labels (strings only)')
# parser.add_argument('--other_entity_values', type=str, metavar='',
#                     help='Correspinding entity values (floating point numbers only)')


# ANATOMICAL
# parser.add_argument('-a', '--anat', default=False,
#                     action='store_true', help='Presence of anatomical data')
parser.add_argument('--t1w', type=str, metavar='',
                    help='String identifying T1 weighted images')
parser.add_argument('--t2w', type=str, metavar='',
                    help='String identifying T2 weighted images')
parser.add_argument('--t1rho', type=str, metavar='',
                    help='String identifying T1rho images')
parser.add_argument('--t1map', type=str, metavar='',
                    help='String identifying T1map images')
parser.add_argument('--t2map', type=str, metavar='',
                    help='String identifying T2map images')
parser.add_argument('--t2star', type=str, metavar='',
                    help='String identifying T2* images')
parser.add_argument('--flair', type=str, metavar='',
                    help='String identifying FLAIR images')
parser.add_argument('--flash', type=str, metavar='',
                    help='String identifying FLASH images')
parser.add_argument('--pd', type=str, metavar='',
                    help='String identifying PD images')
parser.add_argument('--pdmap', type=str, metavar='',
                    help='String identifying PDmap images')
parser.add_argument('--pdt2', type=str, metavar='',
                    help='String identifying PDT2 images')
parser.add_argument('--inplanet1', type=str, metavar='',
                    help='String identifying inplaneT1 images')
parser.add_argument('--inplanet2', type=str, metavar='',
                    help='String identifying inplaneT2 images')
parser.add_argument('--angio', type=str, metavar='',
                    help='String identifying angio images')


# FUNCTIONAL
# parser.add_argument('-f', '--func', default=False,
#                     action='store_true', help='Presence of functional data')
parser.add_argument('--bold', type=str, metavar='',
                    help='String identifying BOLD images')
parser.add_argument('--bold_events', type=str, metavar='',
                    help='String identifying BOLD events files')

# PHYSIOLOGICAL
parser.add_argument('--physio', type=str, metavar='',
                    help='String identifying physiological recordings')
parser.add_argument('--stim', type=str, metavar='',
                    help='String identifying stimulus files')

# PERFUSION
parser.add_argument('--asl', type=str, metavar='',
                    help='String identifying ASL images')
parser.add_argument('--asl_m0scan', type=str, metavar='',
                    help='String identifying m0scan images')
parser.add_argument('--asl_context', type=str, metavar='',
                    help='String identifying ASL context files')
parser.add_argument('--asl_labeling', type=str, metavar='',
                    help='String identifying ASL labeling images')

# DIFFUSION WEIGHTED IMAGING
# parser.add_argument('-d', '--dwi', default=False,
#                     action='store_true', help='Presence of DWI images')
parser.add_argument('--dwi', type=str, metavar='',
                    help='String identifying DWI images')

# FMAP
parser.add_argument('--phasediff', type=str, metavar='',
                    help='String identifying FMAP phasediff images')
parser.add_argument('--magnitude1', type=str, metavar='',
                    help='String identifying FMAP magnitude1 images')
parser.add_argument('--magnitude2', type=str, metavar='',
                    help='String identifying FMAP magnitude2 images')
parser.add_argument('--phase1', type=str, metavar='',
                    help='String identifying FMAP phase1 images')
parser.add_argument('--phase2', type=str, metavar='',
                    help='String identifying FMAP phase2 images')
parser.add_argument('--fieldmap', type=str, metavar='',
                    help='String identifying FMAP fieldmap images')
parser.add_argument('--epi', type=str, metavar='',
                    help='String identifying FMAP epi images')

# MEG
parser.add_argument('--meg', type=str, metavar='',
                    help='String identifying MEG images')
parser.add_argument('--meg_channels', type=str, metavar='',
                    help='String identifying MEG channels file')
parser.add_argument('--meg_events', type=str, metavar='',
                    help='String identifying MEG events files')
parser.add_argument('--meg_photo', type=str, metavar='',
                    help='String identifying MEG photo files')
parser.add_argument('--meg_fid', type=str, metavar='',
                    help='String identifying MEG fid files')
parser.add_argument('--meg_fidinfo', type=str, metavar='',
                    help='String identifying MEG fidinfo files')
parser.add_argument('--meg_headshape', type=str, metavar='',
                    help='String identifying MEG headshape files')


# EEG
parser.add_argument('--eeg', type=str, metavar='',
                    help='String identifying EEG data files')
parser.add_argument('--eeg_channels', type=str, metavar='',
                    help='String identifying EEG channel files')
parser.add_argument('--eeg_events', type=str, metavar='',
                    help='String identifying EEG events files')
parser.add_argument('--eeg_electrodes', type=str, metavar='',
                    help='String identifying EEG electrodes files')
parser.add_argument('--eeg_coordsystem', type=str, metavar='',
                    help='String identifying EEG coordsystem files')
parser.add_argument('--eeg_photo', type=str, metavar='',
                    help='String identifying EEG photo files')

# IEEG
parser.add_argument('--ieeg', type=str, metavar='',
                    help='String identifying IEEG data files')
parser.add_argument('--ieeg_channels', type=str, metavar='',
                    help='String identifying IEEG channel files')
parser.add_argument('--ieeg_events', type=str, metavar='',
                    help='String identifying IEEG events files')
parser.add_argument('--ieeg_electrodes', type=str, metavar='',
                    help='String identifying IEEG electrodes files')
parser.add_argument('--ieeg_coordsystem', type=str, metavar='',
                    help='String identifying IEEG coordsystem files')
parser.add_argument('--ieeg_photo', type=str, metavar='',
                    help='String identifying IEEG photo files')

# PET
parser.add_argument('--pet', type=str, metavar='',
                    help='String identifying PET images')
parser.add_argument('--pet_blood', type=str, metavar='',
                    help='String identifying PET blood files')

# BEH
parser.add_argument('--beh', type=str, metavar='',
                    help='String identifying BEH images')
parser.add_argument('--beh_events', type=str, metavar='',
                    help='String identifying BEH events files')


parser.add_argument('--nocompress', default=False,
                    action='store_true', help='Turn off gzip compression, saves time while testing')
parser.add_argument('--nosidecars', default=False,
                    action='store_true', help='Do not create empty JSON sidecar templates')
parser.add_argument('--descriptor', default = False,
                    action='store_true', help='Create a boutiques descriptor when running the program (does not execute BIDSifiation).')
parser.add_argument('--local', default = False,
                    action='store_true', help='Do not use Docker filepaths [/app/] for supporting data files.')


args = parser.parse_args()

#print(args)

print('Done.')


# Declare global vars

entity_dict = {}  # Stores input strings as keys and BIDS entities as values
subject_folder = ''
session_folders = []

# Define helper functions


def create_datatype_dir(subject_folder, session_folders, datatype_exists, folder_name):
    """
    Creates folder for specified datatype. If there are sessions, nests within session folders.

        INPUT:
            datatype_exists = input argument for modality under datatype. If empty, is NULL/false.
            folder_name = name of datatype folder to be created
    """

    if not datatype_exists:
        return

    if session_folders:
        for folder in session_folders:
            path = os.path.join(folder, folder_name)
            if os.path.isdir(path):
                return
            os.mkdir(path)
    else:
        path = os.path.join(subject_folder, folder_name)
        if os.path.isdir(path):
            return
        os.mkdir(path)


def compress_nii(file_path):
    """
    Compresses uncompressed NIfTI files. Removed uncompressed file from BIDS output directory.

        INPUT:
            file_path = uncompressed NIfTI file in output directory (not original file).
    """

    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path + '.gz', 'wb', compresslevel=3) as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)


def populate_dict(entity_dict_local, entity_prefix, entity_identifier, entity_suffix, use_index):
    """
    Populates the Entity key-value dictionary, where key is the input file substring and value is the BIDS-valid entity string.

        INPUT:
            entity_dict = entity dictionary
            entity_prefix = BIDS entity prefix (e.g. ses, run, acq)
            entity_identifier = Substring identifying entity in input filenames
            entity_suffix = label or value of entity (e.g. run-[1], ses-[2])
            use_index = boolean indicating whether to prefer index over label (for session entity)

        OUTPUT:
            entity_dict = entity dictionary
    """

    # If argument is blank, exit function
    if not entity_identifier:
        return entity_dict_local

    # loop through input sets separated by semicolons
    sets = entity_identifier.split(';')
    for set in sets:

        # Loop through keys within sets
        keys = set.split(',')

        index = 0
        for key in keys:
            # construct appropriate BIDS entity string
            if (use_index):
                entity_suffix_list = entity_suffix.split(',')
                entity_dict_local[key.casefold()] = entity_prefix + \
                    '-' + entity_suffix_list[index]
            else:
                entity_dict_local[key.casefold()] = entity_prefix + \
                    '-' + str((index + 1))

            index += 1

    return entity_dict_local


def copy_modality_files(subject_folder, entity_dict_local, identifier, modality, category):
    """
    Copies files from input directory to BIDS output directory with proper filenames.

        INPUT:
            identifier = Substring identifying modality
            modality = Modality string (e.g. t1w, bold)
            category = Datatype of modality (e.g. anat, func)
    """

    # if argument is empty, return
    if not identifier:
        return False, False

    # Find all files with identifier
    source_files = glob(args.input + '/**/*' +
                        identifier + '*', recursive=True)
    if not source_files:
        msg = "Error: No files found with identifier '" + identifier + "' for modality " + \
            modality + ".\nEnsure that the indentifier accurately describes source files."
        raise Exception(msg)

    src = []
    dest = []

    # For each file of modality
    for source_file in source_files:

        # Find which entities are present
        # This_entities stores values of present entities
        this_entities = {}
        entity_strings = ['ses', 'task', 'acq', 'run', 'ce', 'trc', 'rec', 'dir', 'mod', 'echo', 'flip', 'inv', 'mt', 'part', 'recording']

        for key in entity_dict_local:
            if key in source_file.casefold():
                value = entity_dict_local.get(key).split('-')[0]
                for entity_string in entity_strings:
                    if value == entity_string:
                        this_entities[entity_string] = entity_dict_local[key] + '_'

        # total_entity_string is the final string which will be included in the file name
        total_entity_string = ""

        for entity_string in entity_strings:
            total_entity_string += this_entities.get(entity_string, "")

        # Create file extension
        ext = os.path.splitext(source_file)[1]

        # Create final filename
        dest_filename = os.path.split(subject_folder)[1] + '_' + total_entity_string + modality + ext
        dest_filepath = os.path.join(subject_folder, this_entities.get(
            'ses', "").strip('_'), category, dest_filename)

        if not args.local:
            dest_filepath = '/' + dest_filepath

        if os.path.isfile(dest_filepath):
            msg = "Error when trying to write file: " + dest_filepath + \
                "\nFile with this name has already been written.\nMake sure that you include sufficient entities to differentiate files with similar properties."
            raise Exception(msg)


        # Copy file
        shutil.copy(source_file, dest_filepath)

        # Compress file if it is an uncompressed NIfTI
        if ('.nii' in dest_filepath) and (not '.gz' in dest_filepath) and not args.nocompress:
            compress_nii(dest_filepath)

        src.append(source_file)
        dest.append(dest_filepath)

    return src, dest


def create_descriptor():
    """Create a Boutiques descriptor rather than running the program."""
    import boutiques.creator as bc
    
    descriptor = bc.CreateDescriptor(parser, execname="python /app/bids-converter.py")
    descriptor.save("boutiques_descriptor/bids-converter2.json")

def create_json_sidecars(outdir, modalities):
    """
    Where a template exists, create an empty JSON sidecar in outout directory if sidecar is missing

        INPUT:
            modalities = total modalities data structure
            outdir = output directory
        OUTPUT:
            num = number of JSON sidecars created
            dest = names of JSON sidecars
    """

    num = 0
    dest = []

    for modality in modalities:
        # get all files in outdir

        out_files = glob(outdir + '/**/*' + modality[1] + '*', recursive=True)

        # for each file, check if it has JSON extension or if there is a file with the same name with JSON extension

        for file in out_files:
            if os.path.isdir(file):
                continue

            root, ext = os.path.splitext(file)

            if ext == '.json':
                continue
            if root + '.json' in out_files:
                continue
                
            # if not, get datatype and modality

            mod = modality[1]
            dtype = modality[2]

            # if template exists, create template with appropriate name
            dtype_path = os.path.join('bids_templates', dtype)
            if not os.path.isdir(dtype_path):
                continue

            if args.local:
                template_dir = 'bids_templates/'
            else:
                template_dir = '/app/bids_templates/'

            template_file = template_dir + dtype + '/' + mod + '.json'

            if os.path.isfile(template_file):
                dest_file = os.path.splitext(file)[0] + '.json'
                shutil.copy(template_file, dest_file)

                num += 1
                dest.append(dest_file)

    return num, dest



###########################################

############################## MAIN SCRIPT

if __name__ == '__main__':

    # If descriptor argument is checked, create a descriptor and quit the program
    if args.descriptor:
        create_descriptor()
        quit()


    outdir = ""
    if not args.output_prefix:
        outdir = "bids-converter-results_" + os.path.split(args.input)[1]
    else:
        outdir = args.output_prefix + "_" + os.path.split(args.input)[1]

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    ###################### SET UP SUBJECT FOLDER

    # Get subject number
    print('Creating subject folder...')
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
            msg = 'Error! Did not find subject number in folder name.'
            raise Exception(msg)
        subject_num = extracted_num.zfill(2)

    # Create top-level subject folder
    subject_folder = os.path.join(outdir, 'sub-' + subject_num)

    if os.path.isdir(subject_folder):
        shutil.rmtree(subject_folder)
    
    os.mkdir(subject_folder)

    print('Done.')

    #########################################

    ################## SET UP SESSION FOLDERS

    # If sessions were input, create a list of sessions and
    # a folder for each one.
    # Also create a dictionary mapping session strings to session directory names.
    session_folders = []

    if args.session:
        print('Creating session folders...')
        session_string_sets = args.session.split(';')
        if args.session_labels:
            session_labels = args.session_labels.split(';')

        # Loop through elements of one session key array
        index = 0
        for session in session_string_sets[0].split(','):

            if (args.session_use_index or not args.session_labels):
                subdir_name = 'ses-' + str(index + 1)
            else:
                subdir_name = 'ses-' + args.session_labels[index]

            session_folders.append(os.path.join(subject_folder, subdir_name))
            os.mkdir(session_folders[index])

            index += 1
        print('Done.')

    ###########################################

    ################### CREATE DATATYPE FOLDERS

    print('Creating datatype subfolders...')

    # modality parameters now stored in txt file
    if args.local:
        modality_file = open("modalities.txt")
    else:
        modality_file = open("/app/modalities.txt")

    read_modality_file = csv.reader(modality_file, delimiter='\t')

    # Create modality array (triple)
    modalities = []
    for row in read_modality_file:
        modalities.append(row)

    #print(modalities)

    # col 0 is argument name, col 1 is suffix string, and col 2 is datatype
    for modality in modalities:
        create_datatype_dir(subject_folder, session_folders, getattr(args, modality[0]), modality[2])

    print('Done.')

    ##############################################

    #################### CREATE ENTITY DICTIONARY

    print('Creating BIDS entity dictionary...')

    if args.local:
        entity_file = open("entities.txt")
    else:
        entity_file = open("/app/entities.txt")

    read_entity_file = csv.reader(entity_file, delimiter='\t')

    entities = []
    for row in read_entity_file:
        entities.append(row)

    # Populate entity dictionary using input strings
    # col 0 = string, col 1 = argname, col 2 = label, col 3 = use_index
    for entity in entities:
        # if entity is session, get use_index from argument
        if entity[0] == 'ses':
            entity[3] = getattr(args, entity[3])

        entity_dict = populate_dict(entity_dict, entity[0], getattr(args, entity[1]),
                        getattr(args, entity[2]), entity[3])

    print('Done.')
    print('Entity dictionary:')
    for key in entity_dict:
        print('Key: ' + key + '\t Value: ' +
              entity_dict.get(key, 'None').strip('_'))

    print('Modality identifiers:')
    for md in modalities:
        if getattr(args, md[0]):
            print('Modality: ' + md[1] +
                  '\tIdentifier: ' + getattr(args, md[0]))

    #######################################
    
    ############################ COPY FILES

    # Prepare logfile

    log = open(os.path.join(outdir, 'bids_converter.log'), 'w')
    log.write("## Log of BIDS Converter on CBRAIN\n")
    log.write("## Author: Darius Valevicius, McGill University, 2022\n")
    now = datetime.now()
    log.write('## Date and time: ' + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')

    print('NIFTI compression is set to ' + str(not args.nocompress) + '.')

    print('Copying files...')

    num_files = 0

    for modality in modalities:
        src, dest = copy_modality_files(subject_folder, entity_dict,
            getattr(args, modality[0]), modality[1], modality[2])

        if not src:
            continue

        for s, d in zip(src, dest):
            log.write('\n' + s)
            log.write(' => ')
            log.write(str.removeprefix(d, outdir + '\\') + '\n')

        num_files += len(src)


    log.write('\nCopied ' + str(num_files) + ' files from source to destination.\n')

    print('Done.')

    ########################################

    ###################### Create JSON sidecars

    if not args.nosidecars:
        print('Creating JSON sidecars...')
        num, dest = create_json_sidecars(outdir, modalities)

        log.write('\nCreated ' + str(num) + ' JSON sidecars from BIDS templates:\n')
        for d in dest:
            log.write('\n' + str.removeprefix(d, outdir + '\\'))

        print('Done.')


    log.close()
    

    ###########################################

    # print('Running BIDS validator...')
    # print(BIDSValidator().is_bids(subject_folder))
    # print('Done.')
