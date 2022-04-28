import os
import shutil
import gzip
import csv
from glob import glob

def splitext_recurse(p):
    """
    Splitext function that can handle multiple extensions
    """
    base, ext = os.path.splitext(p)
    if ext == '':
        return (base,)
    else:
        return splitext_recurse(base) + (ext,)


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


def create_dict_entry(entity_dict_local, args, entity):
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

    entity_prefix = entity[0]
    entity_identifier = getattr(args, entity[1])
    entity_suffix = getattr(args, entity[2])
    use_index = entity[3]

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
            if eval(str(use_index)) or not entity_suffix:
                entity_dict_local[key.casefold()] = entity_prefix + \
                '-' + str((index + 1))
            else:
                entity_suffix_list = entity_suffix.split(',')
                entity_dict_local[key.casefold()] = entity_prefix + \
                '-' + entity_suffix_list[index]

            index += 1

    return entity_dict_local



def populate_dict(args):
    entity_dict = {}

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

        entity_dict = create_dict_entry(entity_dict, args, entity)

    return entity_dict


def copy_modality_files(args, subject_folder, subject_id, entity_dict_local, modality_data):
    """
    Copies files from input directory to BIDS output directory with proper filenames.

        INPUT:
            identifier = Substring identifying modality
            modality = Modality string (e.g. t1w, bold)
            category = Datatype of modality (e.g. anat, func)
    """

    identifier = getattr(args, modality_data[0])
    modality = modality_data[1]
    category = modality_data[2]

    input_folder = args.input
    nocompress = args.nocompress


    # if argument is empty, return
    if not identifier:
        return False, False

    # Find all files with identifier
    source_files = glob(input_folder + '/**/*' + subject_id + '*' +
                        identifier + '*', recursive=True)
    if not source_files:
        # If glob failed, try putting subject identifier after modality identifier
        source_files = glob(input_folder + '/**/*' + identifier + '*' +
                        subject_id + '*', recursive=True)
    if not source_files:
        # msg = "Error: No files found with identifier '" + identifier + "' for modality " + \
        #     modality + ".\nEnsure that the indentifier accurately describes source files."
        # raise Exception(msg)
        return False, False

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
        ext = splitext_recurse(os.path.split(source_file)[1])[1:]
        #ext = os.path.splitext(source_file)[1]

        # Create final filename
        dest_filename = os.path.split(subject_folder)[1] + '_' + total_entity_string + modality + ''.join(ext)
        dest_filepath = os.path.join(subject_folder, this_entities.get(
            'ses', "").strip('_'), category, dest_filename)

        # if not args.local:
        #     dest_filepath = '/' + dest_filepath

        if os.path.isfile(dest_filepath):
            msg = "Error when trying to write file: " + dest_filepath + \
                "\nFile with this name has already been written.\nMake sure that you include sufficient entities to differentiate files with similar properties."
            raise Exception(msg)


        # Copy file
        shutil.copy(source_file, dest_filepath)

        # Compress file if it is an uncompressed NIfTI
        if ('.nii' in dest_filepath) and (not '.gz' in dest_filepath) and not nocompress:
            compress_nii(dest_filepath)

        src.append(source_file)
        dest.append((dest_filepath, modality, category))

    return src, dest


# def create_descriptor():
#     """Create a Boutiques descriptor rather than running the program."""
#     import boutiques.creator as bc
    
#     descriptor = bc.CreateDescriptor(parser, execname="python /app/bids-converter.py")
#     descriptor.save("boutiques_descriptor/bids-converter2.json")

def create_json_sidecars(dest):
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
    out = []


    for tuple in dest:

        file = tuple[0]        

        # Skip if directory and not file
        if os.path.isdir(file):
            continue

        path, filename = os.path.split(file)
        extsep = splitext_recurse(filename)

        # Skip if file is already a .JSON or if sister .JSON file already exists
        if '.json' in extsep:
            continue
        if path + extsep[0] + '.json' in [x[0] for x in dest]:
            continue
            
        # if not, get datatype and modality

        mod = tuple[1]
        dtype = tuple[2]

        # if template exists, create template with appropriate name
        dtype_path = os.path.join('/app/bids_templates', dtype)
        if not os.path.isdir(dtype_path):
            continue

        template_dir = '/app/bids_templates/'

        template_file = os.path.join(template_dir, dtype, mod) + '.json'

        if os.path.isfile(template_file):
            out_file = os.path.join(path, extsep[0]) + '.json'
            shutil.copy(template_file, out_file)

            num += 1
            out.append(out_file)

    return num, out

def create_subject_list(args):

    subject_id_list = []

    for subject_string in args.subject.split(','):

        if not '*' in subject_string:
            msg = 'Error with subject identifier "' + subject_string + '". Subject identifiers must have a * wildcard.'
            raise Exception(msg)

        before_num, after_num = subject_string.split('*')

        files = glob(args.input + '/**/*' + subject_string + '*', recursive=True)

        for file in files:
            filename = os.path.split(file)[1]

            start = filename.find(before_num) + len(before_num)
            end = filename.find(after_num)
            number = filename[start:end]

            if not str.isdigit(number):
                msg = 'Subject identifier "' + subject_string + '" returned non-numeric inner string.'
                raise Exception(msg)

            subject_id = before_num + number + after_num

            subject_tuple = (subject_id, number)

            if not subject_id in [x[0] for x in subject_id_list]:
                subject_id_list.append(subject_tuple)

    if not subject_id_list:
        msg = 'Error creating subject list. Check if subject identifier argument was entered correctly.'
        raise Exception(msg)

    return subject_id_list

def create_session_folders(args, subject_folder):
    session_folders = []

    if args.session:
        print('Creating session folders...')
        session_string_sets = args.session.split(';')
        if args.session_labels:
            session_labels = args.session_labels.split(',')

        # Loop through elements of one session key array
        index = 0
        for session in session_string_sets[0].split(','):

            if args.session_use_index or not args.session_labels:
                subdir_name = 'ses-' + str(index + 1)
            else:
                subdir_name = 'ses-' + session_labels[index]

            session_folders.append(os.path.join(subject_folder, subdir_name))
            if not os.path.isdir(session_folders[index]):
                os.mkdir(session_folders[index])

            index += 1
        print('Done.')
    
    return session_folders