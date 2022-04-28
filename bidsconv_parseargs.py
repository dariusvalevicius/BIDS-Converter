import argparse

def bidsconv_parseargs(argv):

    # Argument parser
    print('Parsing arguments...')

    parser = argparse.ArgumentParser(
        description='Convert an arbitrarily structured brain imaging dataset to BIDS format')
    parser.add_argument('--input', type=str, metavar='',
                        help='Input folder containing data')
    parser.add_argument('--output_prefix', type=str, metavar='',
                        help='Top-level output folder prefix, to be combined with input foldername')
    parser.add_argument('--subject', type=str,
                        metavar='', help='Strings identifying subject numbers. Use wildcards (*) to represent number locations in relation to the string.')


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
    parser.add_argument('--nojsons', default=False,
                        action='store_true', help='Do not create empty JSON sidecar templates')
    parser.add_argument('--descriptor', default = False,
                        action='store_true', help='Create a boutiques descriptor when running the program (does not execute BIDSifiation).')
    parser.add_argument('--local', default = False,
                        action='store_true', help='Do not use Docker filepaths [/app/] for supporting data files.')


    args = parser.parse_args(argv)

    print('Done.')

    return args