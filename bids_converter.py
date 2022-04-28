from bidsconv_parseargs import bidsconv_parseargs
import bidsconv_functions as bcf
from glob import glob
import os
import sys
import shutil
import csv
from datetime import date, datetime
# from bids_validator import BIDSValidator

###########################################

############################## MAIN SCRIPT

if __name__ == '__main__':

    # parse args
    args = bidsconv_parseargs(sys.argv[1:])

    # If descriptor argument is checked, create a descriptor and quit the program
    # if args.descriptor:
    #     create_descriptor()
    #     quit()

    # Create output directory
    outdir = ""
    if not args.output_prefix:
        outdir = "bids-converter-results_" + os.path.split(args.input)[1]
    else:
        outdir = args.output_prefix + "_" + os.path.split(args.input)[1]

    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    
    os.mkdir(outdir)

    # Make dataset description JSON template

    dataset_json = glob(args.input + '/**/*' + 'dataset_description.json', recursive=True)
    if dataset_json:
        shutil.copy(dataset_json, outdir)
    elif not args.nojsons:
        shutil.copy('/app/bids_templates/dataset_description.json', os.path.join(outdir, 'dataset_description.json'))


    # Prepare logfile
    log = open(os.path.join(outdir, 'bids_converter.log'), 'w')
    log.write("## Log of BIDS Converter on CBRAIN\n")
    log.write("## Author: Darius Valevicius, McGill University, 2022\n")
    now = datetime.now()
    log.write('## Date and time: ' + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')


    ##############################################

    #################### CREATE ENTITY DICTIONARY

    print('Creating BIDS entity dictionary...')

    entity_dict = bcf.populate_dict(args)

    print('Done.')
    print('Entity dictionary:')
    for key in entity_dict:
        print('Key: ' + key + '\t Value: ' +
            entity_dict.get(key, 'None').strip('_'))


    ##############################################

    #################### CREATE MODALITY LIST

    # modality parameters now stored in txt file
    modality_file = open("/app/modalities.txt")

    read_modality_file = csv.reader(modality_file, delimiter='\t')

    # Create modality array (triple)
    modalities = []
    for row in read_modality_file:
        modalities.append(row)

    print('Modality identifiers:')
    for md in modalities:
        if getattr(args, md[0]):
            print('Modality: ' + md[1] +
                '\tIdentifier: ' + getattr(args, md[0]))


    ##############################################

    #################### CREATE SUBJECT LIST

    # Get all subjects

    # All files with sub identifier

    subject_id_list = bcf.create_subject_list(args)

    # print(subject_id_list)

    int_list = [int(x[1]) for x in subject_id_list]
    max_sub = max(int_list)
    # print(max_sub)

    if max_sub > 99:
        sub_padding = 3
    elif max_sub > 9:
        sub_padding = 2
    else:
        sub_padding = 1


    ################################################

    #################### RUN MAIN PROCESS ON EACH SUB

    # For each subject, run main process

    for subject_tuple in subject_id_list:
            
        # Declare global vars
        subject_identifier = subject_tuple[0]
        subject_num = subject_tuple[1]
        subject_folder = ''
        session_folders = []

        log.write('\n\n\nUsing subject identifier "' + subject_identifier + '"\n')
        print('Processing subject identifier: ' + subject_identifier)

        ###################### SET UP SUBJECT FOLDER

        print('Creating subject folder...')

        # set appropriate zero padding
        subject_padded = str(int(subject_num)).zfill(sub_padding)

        # Create top-level subject folder
        subject_folder = os.path.join(outdir, 'sub-' + subject_padded)

        if not os.path.isdir(subject_folder):
            os.mkdir(subject_folder)

        print('Done.')

        #########################################

        ################## SET UP SESSION FOLDERS

        # If sessions were input, create a list of sessions and
        # a folder for each one.
        # Also create a dictionary mapping session strings to session directory names.
        session_folders = bcf.create_session_folders(args, subject_folder)

        ###########################################

        ################### CREATE DATATYPE FOLDERS

        print('Creating datatype subfolders...')

        # col 0 is argument name, col 1 is suffix string, and col 2 is datatype
        for modality in modalities:
            bcf.create_datatype_dir(subject_folder, session_folders, getattr(args, modality[0]), modality[2])

        print('Done.')

        #######################################
        
        ############################ COPY FILES

        print('NIFTI compression is set to ' + str(not args.nocompress) + '.')

        print('Copying files...')

        num_files = 0
        src_tot = []
        dest_tot = []

        for modality in modalities:
            src, dest = bcf.copy_modality_files(args, subject_folder, subject_identifier, entity_dict, modality)

            if not src:
                continue

            for s, d in zip(src, dest):
                log.write('\n' + s)
                log.write(' => ')
                log.write(str.removeprefix(d[0], outdir)[1:])

            num_files += len(src)

            # Check if a source file has already been copied
            if any(file in src_tot for file in src):
                msg = "Error: Source file is being copied >1 times. Check for redundancy in modality identifiers."
                raise Exception(msg)
            else:
                src_tot.extend(src)
                dest_tot.extend(dest)

        # print(dest_tot) ############

        log.write('\n\nCopied ' + str(num_files) + ' files from source to destination.\n')

        print('Done.')

        ########################################

        ###################### Create JSON sidecars

        if not args.nojsons:
            print('Creating JSON sidecars...')
            num, out = bcf.create_json_sidecars(dest_tot)

            log.write('\nCreated ' + str(num) + ' JSON sidecars from BIDS templates:\n')
            for f in out:
                log.write('\n' + str.removeprefix(f, outdir)[1:])

            print('Done.')        

        ###########################################

        # print('Running BIDS validator...')
        # print(BIDSValidator().is_bids(subject_folder))
        # print('Done.')

    ##### END OF LOOP

    log.close()

