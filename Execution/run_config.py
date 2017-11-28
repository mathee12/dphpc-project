#############################################################################
#                                                                           #
#   JSON configuration file to do parameter grid scans.                     #
#                                                                           #
#############################################################################

run_config = {
    'run_name': 'test',

    'run_params':
        {
            'n_cores':              [1, 4, 8],
            'n_points':             [2000],
            'img_files':            ['homer.jpg'],
            'algorithms':           ['chan_normal'],
            'sub_size':             [None],
            'n_iterations':         5,
            'write_output_files':   True
        },

    'post_process_params':
        {
            'store_final_plots':    True,
            'store_movies':         False,
            'store_bm_plots':       True
        }
}


#############################################################################
#                                                                           #
#   Note:                                                                   #
#                                                                           #
#   1) Input images must be placed in the "Input" folder (.png or .jpg)     #
#                                                                           #
#   2) Output is stored in the "Output" folder in a directory called        #
#      <run_name>_MMDD_hhmmss                                               #
#                                                                           #
#   3) Possible inputs for "algorithms" list:                               #
#      'chan_normal', 'chan_merge_var', 'jarvis', 'graham'                  #
#                                                                           #
#############################################################################
