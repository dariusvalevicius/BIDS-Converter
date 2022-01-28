from bz2 import compress
import os
import argparse
import shutil
import gzip
import fnmatch
from glob import glob
from braceexpand import braceexpand

# Argument parser

parser = argparse.ArgumentParser(
    description='Convert an arbitrarily structured brain imaging dataset to BIDS format')
parser.add_argument('-i', '--input', type=str, metavar='',
                    help='Input folder containing data')
parser.add_argument('-s', '--subject', type=str,
                    metavar='', help='Subject number')
parser.add_argument('--sessions', type=str, metavar='',
                    help='Strings identifying sessions')
parser.add_argument('-t', '--tasks', type=str, metavar='',
                    help='Strings identifying tasks')

parser.add_argument('-a', '--anat', default=False,
                    action='store_true', help='Presence of anatomical data')
parser.add_argument('--t1w', type=str, metavar='',
                    help='Shell-type expression identifying T1 weighted images')

parser.add_argument('-f', '--func', default=False,
                    action='store_true', help='Presence of functional data')
parser.add_argument('-b', '--bold', type=str, metavar='',
                    help='Shell-type expression describing BOLD data files')
parser.add_argument('-p', '--physio', type=str, metavar='',
                    help='Shell-type expression describing physiological data files')

parser.add_argument('--nocompress', default=False,
                    action='store_true', help='Turn off gzip compression, saves time while testing')


args = parser.parse_args()

# Define helper functions

# Create modality folder
# If there are sessions, nest within sessions


def create_modality_dir(session_folders, folder_name):

    if session_folders:
        for folder in session_folders:
            os.mkdir(os.path.join(folder, folder_name))
    else:
        os.mkdir(os.path.join(subject_folder, folder_name))


def get_session_substr(session_strings, file, this_session):
    # If sessions and tasks are input,
    # get the session and task for this file
    for session in (session_string.casefold() for session_string in session_strings):
        if session in file.casefold():
            this_session = session_dict[session] + '_'
    
    return this_session

def get_task_substr(task_strings, file, this_task):
    # Gets task for this file
    for task in (task_string.casefold() for task_string in task_strings):
        if task in file.casefold():
            this_task = 'task-' + task + '_'

    return this_task


def get_session_task(session_strings, task_strings, file):
    # As in, "get session and task" for a single file
    # Calls individual session and task functions dependent on arguments
    this_session = ''
    if args.sessions:
        this_session = get_session_substr(session_strings, file, this_session)

    this_task = ''
    if args.tasks:
        this_task = get_task_substr(task_strings, file, this_task)

    return this_session, this_task


def compress_nii(file_path):
    # If .nii is uncompressed, compress
    if (not '.gz' in file_path) and (not args.nocompress):
        with open(file_path, 'rb') as f_in:
            with gzip.open(file_path + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file_path)

def get_modality_files(identifier):
    # Glob files in input directory matching identifier
    files = glob(args.input + '/**/' + identifier, recursive=True)
    return files


# Main
if __name__ == '__main__':

    for arg in vars(args):
        print(arg, getattr(args, arg))

    # Get subject number
    subject_num = ''

    if args.subject:
        # If explicitly declared, get from argument
        subject_num = args.subject.zfill(2)
    else:
        # Else, try to extract from input foldername
        extracted_num = ''
        for m in args.input:
            if m.isdigit():
                extracted_num += m
        if not extracted_num:
            print('Error! Did not find subject number in folder name.')
            # throw error
        subject_num = extracted_num.zfill(2)
        print('subject num:')
        print(subject_num)

    # Create top-level subject folder
    subject_folder = 'sub-' + subject_num

    # If folder exists, remove
    if os.path.isdir(subject_folder):
        shutil.rmtree(subject_folder)

    os.mkdir(subject_folder)

    # If sessions were input, create a list of sessions and
    # a folder for each one.
    # Also create a dictionary mapping session strings to session directory names.
    session_strings = []
    session_folders = []

    if args.sessions:
        session_dict = {}
        session_string_sets = args.sessions.split(';')
        print(session_string_sets)

        set = 0
        for session_string_set in session_string_sets:
            this_session_strings = list(braceexpand(session_string_set))
            session_strings += this_session_strings
            print('session strings:')
            print(session_strings)
            index = 0
            # create dictionary
            # print(session_strings)
            # print(len(session_strings))
            for session in this_session_strings:
                # add folder name to dictionary
                subdir_name = 'ses-' + str(index + 1)
                session_dict[this_session_strings[index].casefold()] = subdir_name.casefold()

                if set == 0:
                    session_folders.append(os.path.join(subject_folder, subdir_name))
                    os.mkdir(session_folders[index])

                index += 1
            set += 1

        print(session_dict)

    # If tasks were input,
    # get list of tasks
    task_strings = ''
    if args.tasks:
        task_strings = list(braceexpand(args.tasks))

    # If func is true...
    if args.func:

        # Create func directory
        # If sessions is true, nest within session folders
        create_modality_dir(session_folders, 'func')

        # If bold identifier was input, copy bold files
        if args.bold:
            bold_files = get_modality_files(args.bold)
            print(bold_files)
            for bold_file in bold_files:
                # Get .nii file extension
                ext = os.path.splitext(bold_file)[1]

                # Get session and task
                this_session, this_task = get_session_task(session_strings, task_strings, bold_file)

                # Copy file
                file_name = subject_folder + '_' + this_session + this_task + 'bold' + ext
                file_path = os.path.join(
                    subject_folder, this_session[:-1], 'func', file_name)

                shutil.copy(bold_file, file_path)
                compress_nii(file_path)


        if args.physio:
            physio_files = get_modality_files(args.physio)
            print(physio_files)
            for physio_file in physio_files:
                
                ext = os.path.splitext(physio_file)[1]

                this_session, this_task = get_session_task(session_strings, task_strings, physio_file)

                # Copy file
                file_name = subject_folder + '_' + this_session + this_task + 'physio' + ext
                file_path = os.path.join(
                    subject_folder, this_session[:-1], 'func', file_name)

                print(file_path)

                shutil.copy(physio_file, file_path)
                

    if args.anat:

        create_modality_dir(session_folders, 'anat')

        if args.t1w:
            t1w_strings = list(braceexpand(args.t1w))
            print('t1w_strings:')
            print(t1w_strings)
            for t1w_string in t1w_strings:
                print(t1w_string)
                t1w_files = get_modality_files(t1w_string)
                print('t1w_files:')
                print(t1w_files)

                for t1w_file in t1w_files:
                    ext = os.path.splitext(t1w_file)[1]

                    this_session, this_task = get_session_task(session_strings, task_strings, t1w_file)

                    # Copy file
                    file_name = subject_folder + '_' + this_session + this_task + 'acq-' + t1w_string.split('.')[0].strip('*').strip('_').casefold() + '_' + 't1w' + ext

                    file_path = os.path.join(
                        subject_folder, this_session[:-1], 'anat', file_name)
                    print(file_path)

                    shutil.copy(t1w_file, file_path)

                    compress_nii(file_path)

                    