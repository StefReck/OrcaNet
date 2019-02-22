#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO
"""
import numpy as np
import toml

from orcanet_contrib.custom_objects import get_custom_objects


def update_orca_objects(orca, model_file):
    """
    Update the orca object for using the model.

    Look up and load in the respective sample-, label-, and dataset-
    modifiers, as well as the custom objects.
    Will assert that the respective objects have not already been set
    to a non-default value (nothing is overwritten).

    Parameters
    ----------
    orca : object OrcaHandler
        Contains all the configurable options in the OrcaNet scripts.
    model_file : str
        Path to a toml file which has the infos about which modifiers
        to use.

    """
    file_content = toml.load(model_file)
    orca_modifiers = file_content["orca_modifiers"]

    sample_modifier = orca_modifiers.get("sample_modifier")
    label_modifier = orca_modifiers.get("label_modifier")
    dataset_modifier = orca_modifiers.get("dataset_modifier")

    if sample_modifier is not None:
        assert orca.cfg.sample_modifier is None, \
            "Can not set sample modifier: Has already been set: " \
            "{}".format(orca.cfg.sample_modifier)
    if label_modifier is not None:
        assert orca.cfg.label_modifier is None, \
            "Can not set label modifier: Has already been set: " \
            "{}".format(orca.cfg.label_modifier)
    if dataset_modifier is not None:
        assert orca.cfg.dataset_modifier is None, \
            "Can not set dataset modifier: Has already been set: " \
            "{}".format(orca.cfg.dataset_modifier)
    assert orca.cfg.custom_objects is None, \
        "Can not set custom objects: Have already been set: " \
        "{}".format(orca.cfg.custom_objects)

    if sample_modifier is not None:
        print("Using orca sample modifier: ", sample_modifier)
        orca.cfg.sample_modifier = orca_sample_modifiers(sample_modifier)
    if label_modifier is not None:
        print("Using orca label modifier: ", label_modifier)
        orca.cfg.label_modifier = orca_label_modifiers(label_modifier)
    if dataset_modifier is not None:
        print("Using orca dataset modifier: ", dataset_modifier)
        orca.cfg.dataset_modifier = orca_dataset_modifiers(dataset_modifier)
    print("Using orca custom objects")
    orca.cfg.custom_objects = get_custom_objects()


def orca_sample_modifiers(name):
    """
    Returns one of the sample modifiers used for Orca networks.

    They will permute columns, and/or add permuted columns to xs.

    The input to the functions is:
        xs_files : dict
            Dict that contains the input samples from the file(s).
            The keys are the names of the inputs in the toml list file.
            The values are a single batch of data from each corresponding file.

    The output is:
        xs_layer : dict
            Dict that contains the input samples for a Keras NN.
            The keys are the names of the input layers of the network.
            The values are a single batch of data for each input layer.

    Parameters
    ----------
    name : None/str
        Name of the sample modifier to return.

    Returns
    -------
    sample_modifier : function
        The sample modifier function.

    """
    # assuming input is bxyzt
    xyzt_permute = {'yzt-x': (0, 2, 3, 4, 1),
                    'xyt-z': (0, 1, 2, 4, 3),
                    't-xyz': (0, 4, 1, 2, 3),
                    'tyz-x': (0, 4, 2, 3, 1)}

    if name in xyzt_permute:
        def swap_columns(xs_files):
            # Transpose dimensions
            xs_layer = dict()
            keys = list(xs_files.keys())
            xs_layer[keys[0]] = np.transpose(xs_files, xyzt_permute[name])
            return xs_layer
        sample_modifier = swap_columns

    elif name == 'xyz-t_and_yzt-x':
        def sample_modifier(xs_files):
            # Use xyz-t, and also transpose it to yzt-x and use that, too.
            xs_layer = dict()
            xs_layer['xyz-t'] = xs_files['xyz-t']
            xs_layer['yzt-x'] = np.transpose(xs_files['xyz-t'], xyzt_permute['yzt-x'])
            return xs_layer

    elif name == 'xyz-t_and_yzt-x_multi_input_single_train_tight-1_tight-2':
        def sample_modifier(xs_files):
            # Use xyz-t in two different time cuts, and also transpose them to yzt-x and use these, too.
            xs_layer = dict()
            xs_layer['xyz-t_tight-1'] = xs_files['xyz-t_tight-1']
            xs_layer['xyz-t_tight-2'] = xs_files['xyz-t_tight-2']
            xs_layer['yzt-x_tight-1'] = np.transpose(xs_files['xyz-t_tight-1'], xyzt_permute['yzt-x'])
            xs_layer['yzt-x_tight-2'] = np.transpose(xs_files['xyz-t_tight-2'], xyzt_permute['yzt-x'])
            return xs_layer

    elif name == 'xyz-t_and_xyz-c_single_input':
        def sample_modifier(xs_files):
            # Concatenate xyz-t and xyz-c to a single input
            xs_layer = dict()
            xs_layer['xyz-t_and_xyz-c_single_input'] = np.concatenate([xs_files['xyz-t'], xs_files['xyz-c']], axis=-1)
            return xs_layer

    else:
        raise ValueError('Unknown input_type: ' + str(name))

    return sample_modifier


def orca_label_modifiers(name):
    """
    Returns one of the label modifiers used for Orca networks.

    CAREFUL: y_values is a structured numpy array! if you use advanced numpy indexing, this may lead to errors.
    Let's suppose you want to assign a particular value to one or multiple elements of the y_values array.

    E.g.
    y_values[1]['bjorkeny'] = 5
    This works, since it is basic indexing.

    Likewise,
    y_values[1:3]['bjorkeny'] = 5
    works as well, because basic indexing gives you a view (!).

    Advanced indexing though, gives you a copy.
    So this
    y_values[[1,2,4]]['bjorkeny'] = 5
    will NOT work! Same with boolean indexing, like

    bool_idx = np.array([True,False,False,True,False]) # if len(y_values) = 5
    y_values[bool_idx]['bjorkeny'] = 10
    This will NOT work as well!!

    Instead, use
    np.place(y_values['bjorkeny'], bool_idx, 10)
    This works.

    Parameters
    ----------
    name : str
        Name of the label modifier that should be used.

    Returns
    -------
    label_modifier : function
        The label modifier function.

    """

    if name == 'energy_dir_bjorken-y_vtx_errors':
        def label_modifier(y_values):
            ys = dict()
            particle_type, is_cc = y_values['particle_type'], y_values['is_cc']
            elec_nc_bool_idx = np.logical_and(np.abs(particle_type) == 12, is_cc == 0)

            # correct energy to visible energy
            visible_energy = y_values[elec_nc_bool_idx]['energy'] * y_values[elec_nc_bool_idx]['bjorkeny']
            # fix energy to visible energy
            np.place(y_values['energy'], elec_nc_bool_idx, visible_energy)
            # set bjorkeny label of nc events to 1
            np.place(y_values['bjorkeny'], elec_nc_bool_idx, 1)

            ys['dx'], ys['dx_err'] = y_values['dir_x'], y_values['dir_x']
            ys['dy'], ys['dy_err'] = y_values['dir_y'], y_values['dir_y']
            ys['dz'], ys['dz_err'] = y_values['dir_z'], y_values['dir_z']
            ys['e'], ys['e_err'] = y_values['energy'], y_values['energy']
            ys['by'], ys['by_err'] = y_values['bjorkeny'], y_values['bjorkeny']

            ys['vx'], ys['vx_err'] = y_values['vertex_pos_x'], y_values['vertex_pos_x']
            ys['vy'], ys['vy_err'] = y_values['vertex_pos_y'], y_values['vertex_pos_y']
            ys['vz'], ys['vz_err'] = y_values['vertex_pos_z'], y_values['vertex_pos_z']
            ys['vt'], ys['vt_err'] = y_values['time_residual_vertex'], y_values['time_residual_vertex']

            for key_label in ys:
                ys[key_label] = ys[key_label].astype(np.float32)
            return ys

    elif name == 'ts_classifier':
        def label_modifier(y_values):
            # for every sample, [0,1] for shower, or [1,0] for track

            # {(12, 0): 0, (12, 1): 1, (14, 1): 2, (16, 1): 3}
            # 0: elec_NC, 1: elec_CC, 2: muon_CC, 3: tau_CC
            # label is always shower, except if muon-CC
            ys = dict()
            particle_type, is_cc = y_values['particle_type'], y_values['is_cc']
            is_muon_cc = np.logical_and(np.abs(particle_type) == 14, is_cc == 1)
            is_not_muon_cc = np.invert(is_muon_cc)

            batchsize = y_values.shape[0]
            # categorical [shower, track] -> [1,0] = shower, [0,1] = track
            categorical_ts = np.zeros((batchsize, 2), dtype='bool')

            categorical_ts[:, 0] = is_not_muon_cc
            categorical_ts[:, 1] = is_muon_cc

            ys['ts_output'] = categorical_ts.astype(np.float32)
            return ys

    elif name == 'bg_classifier':
        def label_modifier(y_values):
            # for every sample, [1,0,0] for neutrinos, [0,1,0] for mupage and [0,0,1] for random_noise
            # particle types: mupage: np.abs(13), random_noise = 0, neutrinos =
            ys = dict()
            particle_type = y_values['particle_type']
            is_mupage = np.abs(particle_type) == 13
            is_random_noise = np.abs(particle_type == 0)
            is_not_mupage_nor_rn = np.invert(np.logical_or(is_mupage, is_random_noise))

            batchsize = y_values.shape[0]
            categorical_bg = np.zeros((batchsize, 3), dtype='bool')

            categorical_bg[:, 0] = is_not_mupage_nor_rn
            categorical_bg[:, 1] = is_mupage
            categorical_bg[:, 2] = is_random_noise

            ys['bg_output'] = categorical_bg.astype(np.float32)
            return ys

    elif name == 'bg_classifier_2_class':
        def label_modifier(y_values):
            # for every sample, [1,0,0] for neutrinos, [0,1,0] for mupage and [0,0,1] for random_noise
            # particle types: mupage: np.abs(13), random_noise = 0, neutrinos =
            ys = dict()
            particle_type = y_values['particle_type']
            is_mupage = np.abs(particle_type) == 13
            is_random_noise = np.abs(particle_type == 0)
            is_not_mupage_nor_rn = np.invert(np.logical_or(is_mupage, is_random_noise))

            batchsize = y_values.shape[0]
            categorical_bg = np.zeros((batchsize, 2), dtype='bool')

            categorical_bg[:, 0] = is_not_mupage_nor_rn # neutrino
            categorical_bg[:, 1] = np.invert(is_not_mupage_nor_rn) # is not neutrino

            ys['bg_output'] = categorical_bg.astype(np.float32)
            return ys

    else:
        raise ValueError("Unknown output_type: " + str(name))

    return label_modifier


def orca_dataset_modifiers(name):
    """
    Returns one of the dataset modifiers used for predicting with OrcaNet.

    Parameters
    ----------
    name : str
        Name of the dataset modifier that should be used.

    """
    if name == 'bg_classifier':
        def dataset_modifier(mc_info, y_true, y_pred):

            # y_pred and y_true are dicts with keys for each output
            # we only have 1 output in case of the bg classifier
            y_pred = y_pred['bg_output']
            y_true = y_true['bg_output']

            datasets = dict()
            datasets['mc_info'] = mc_info  # is already a structured array

            # make pred dataset
            dtypes = np.dtype([('prob_neutrino', y_pred.dtype), ('prob_muon', y_pred.dtype), ('prob_random_noise', y_pred.dtype)])
            pred = np.empty(y_pred.shape[0], dtype=dtypes)
            pred['prob_neutrino'] = y_pred[:, 0]
            pred['prob_muon'] = y_pred[:, 1]
            pred['prob_random_noise'] = y_pred[:, 2]

            datasets['pred'] = pred

            # make true dataset
            dtypes = np.dtype([('cat_neutrino', y_true.dtype), ('cat_muon', y_true.dtype), ('cat_random_noise', y_true.dtype)])
            true = np.empty(y_true.shape[0], dtype=dtypes)
            true['cat_neutrino'] = y_true[:, 0]
            true['cat_muon'] = y_true[:, 1]
            true['cat_random_noise'] = y_true[:, 2]

            datasets['true'] = true

            return datasets

    elif name == 'bg_classifier_2_class':
        def dataset_modifier(mc_info, y_true, y_pred):

            # y_pred and y_true are dicts with keys for each output
            # we only have 1 output in case of the bg classifier
            y_pred = y_pred['bg_output']
            y_true = y_true['bg_output']

            datasets = dict() # y_pred is a list of arrays
            datasets['mc_info'] = mc_info # is already a structured array

            # make pred dataset
            dtypes = np.dtype([('prob_neutrino', y_pred.dtype), ('prob_not_neutrino', y_pred.dtype)])
            pred = np.empty(y_pred.shape[0], dtype=dtypes)
            pred['prob_neutrino'] = y_pred[:, 0]
            pred['prob_not_neutrino'] = y_pred[:, 1]

            datasets['pred'] = pred

            # make true dataset
            dtypes = np.dtype([('cat_neutrino', y_true.dtype), ('cat_not_neutrino', y_true.dtype)])
            true = np.empty(y_true.shape[0], dtype=dtypes)
            true['cat_neutrino'] = y_true[:, 0]
            true['cat_not_neutrino'] = y_true[:, 1]

            datasets['true'] = true

            return datasets

    elif name == 'ts_classifier':
        def dataset_modifier(mc_info, y_true, y_pred):

            # y_pred and y_true are dicts with keys for each output
            # we only have 1 output in case of the ts classifier
            y_pred = y_pred['ts_output']
            y_true = y_true['ts_output']

            datasets = dict()
            datasets['mc_info'] = mc_info  # is already a structured array

            # make pred dataset
            dtypes = np.dtype([('prob_shower', y_pred.dtype), ('prob_track', y_pred.dtype)])
            pred = np.empty(y_pred.shape[0], dtype=dtypes)
            pred['prob_shower'] = y_pred[:, 0]
            pred['prob_track'] = y_pred[:, 1]

            datasets['pred'] = pred

            # make true dataset
            dtypes = np.dtype([('cat_shower', y_true.dtype), ('cat_track', y_true.dtype)])
            true = np.empty(y_true.shape[0], dtype=dtypes)
            true['cat_shower'] = y_true[:, 0]
            true['cat_track'] = y_true[:, 1]

            datasets['true'] = true

            return datasets

    elif name == 'regression_energy_dir_bjorken-y_vtx_errors':
        def dataset_modifier(mc_info, y_true, y_pred):

            datasets = dict()
            datasets['mc_info'] = mc_info  # is already a structured array

            # make pred dataset
            """y_pred and y_true are dicts with keys for each output,
               here, we have 1 key for each regression variable"""

            pred_labels_and_nn_output_names = [('pred_energy', 'e'), ('pred_dir_x', 'dx'), ('pred_dir_y', 'dy'),
                                               ('pred_dir_z', 'dz'), ('pred_bjorkeny', 'by'), ('pred_vtx_x', 'vx'),
                                               ('pred_vtx_y', 'vy'), ('pred_vtx_z', 'vz'), ('pred_vtx_t', 'vt'),
                                               ('pred_err_energy', 'e_err'), ('pred_err_dir_x', 'dx_err'),
                                               ('pred_err_dir_y', 'dy_err'), ('pred_err_dir_z', 'dz_err'),
                                               ('pred_err_bjorkeny', 'by_err'), ('pred_err_vtx_x', 'vx_err'),
                                               ('pred_err_vtx_y', 'vy_err'), ('pred_err_vtx_z', 'vz_err'),
                                               ('pred_err_vtx_t', 'vt_err')]

            dtypes_pred = [(tpl[0], y_pred[tpl[1]].dtype) for tpl in pred_labels_and_nn_output_names]
            n_evts = y_pred['e'].shape[0]
            pred = np.empty((n_evts, len(dtypes_pred)), dtype=dtypes_pred)

            for tpl in pred_labels_and_nn_output_names:
                pred[tpl[0]] = y_pred[tpl[1]]

            datasets['pred'] = pred

            # make true dataset
            true_labels_and_nn_output_names = [('true_energy', 'e'), ('true_dir_x', 'dx'), ('true_dir_y', 'dy'),
                                               ('true_dir_z', 'dz'), ('true_bjorkeny', 'by'), ('true_vtx_x', 'vx'),
                                               ('true_vtx_y', 'vy'), ('true_vtx_z', 'vz'), ('true_vtx_t', 'vt'),
                                               ('true_err_energy', 'e_err'), ('true_err_dir_x', 'dx_err'),
                                               ('true_err_dir_y', 'dy_err'), ('true_err_dir_z', 'dz_err'),
                                               ('true_err_bjorkeny', 'by_err'), ('true_err_vtx_x', 'vx_err'),
                                               ('true_err_vtx_y', 'vy_err'), ('true_err_vtx_z', 'vz_err'),
                                               ('true_err_vtx_t', 'vt_err')]

            dtypes_true = [(tpl[0], y_true[tpl[1]].dtype) for tpl in true_labels_and_nn_output_names]
            true = np.empty((n_evts, len(dtypes_true)), dtype=dtypes_true)

            for tpl in true_labels_and_nn_output_names:
                true[tpl[0]] = y_true[tpl[1]]

            datasets['true'] = true

    else:
        raise ValueError('Unknown dataset modifier: ' + str(name))

    return dataset_modifier


def orca_learning_rates(name, total_file_no):
    """
    Returns one of the learning rate schedules used for Orca networks.

    Parameters
    ----------
    name : str
        Name of the schedule.
    total_file_no : int
        How many files there are to train on.

    Returns
    -------
    learning_rate : function
        The learning rate schedule.

    """
    if name == "triple_decay":
        def learning_rate(n_epoch, n_file):
            """
            Function that calculates the current learning rate based on the number of already trained epochs.

            Learning rate schedule is as follows: lr_decay = 7% for lr > 0.0003
                                                  lr_decay = 4% for 0.0003 >= lr > 0.0001
                                                  lr_decay = 2% for 0.0001 >= lr

            Parameters
            ----------
            n_epoch : int
                The number of the current epoch which is used to calculate the new learning rate.
            n_file : int
                The number of the current filenumber which is used to calculate the new learning rate.

            Returns
            -------
            lr_temp : float
                Calculated learning rate for this epoch.

            """
            n_lr_decays = (n_epoch - 1) * total_file_no + (n_file - 1)
            lr_temp = 0.005  # * n_gpu TODO think about multi gpu lr

            for i in range(n_lr_decays):
                if lr_temp > 0.0003:
                    lr_decay = 0.07  # standard for regression: 0.07, standard for PID: 0.02
                elif 0.0003 >= lr_temp > 0.0001:
                    lr_decay = 0.04  # standard for regression: 0.04, standard for PID: 0.01
                else:
                    lr_decay = 0.02  # standard for regression: 0.02, standard for PID: 0.005
                lr_temp = lr_temp * (1 - float(lr_decay))

            return lr_temp
    else:
        raise NameError("Unknown orca learning rate name", name)

    return learning_rate
