import os
import datetime
from datetime import date
import yaml
import numpy as np
from pathlib import Path


# TODO read from subject metadata, join list and use this to run the for loop, \

# METADATA
# Mergin functions --------------------------------------


def mergeMetadataDict(experiment_metadata, subject_metadata):
    experiment_metadata['subjects'] = subject_metadata
    return experiment_metadata


def mergeSubjectMetadata(metadata: list):
    mMetadata = dict()
    for value in metadata:
        mMetadata[value['subjectId']] = value
    return mMetadata
# End Merging functions ----------------------------------

# Metadata creation functions ---------------------------


def experimentMetadata(experiment_name=date.today().strftime("%b-%d-%Y"), save=False, experimenter=None, experiment_path=None, duration=list(), day=list(), night=list()):
    eMetadata = dict(experiment_name=experiment_name,
                     save=save,
                     experimenter=experimenter,
                     experiment_path=experiment_path,
                     experiment_day=datetime.datetime.now().ctime(),
                     duration=duration,
                     day=day,
                     night=night,

                     )
    return eMetadata


def subjectMetadata(subjectId=None, var_list=list(), var_pressure_loc=0,
                    thresholds=dict(day=dict(min=0, max=0),
                                    night=dict(min=0, max=0)),
                    parameter=None,
                    laser_trigger=None,
                    window=0,
                    laser=dict(stim=False, id=0, sync=False, syncTo=None)):

    varlist_flag = False
    varpressure_flag = False

    if var_list:
        varlist_flag = True
    if str(var_pressure_loc):
        varpressure_flag = True

    if varlist_flag & varpressure_flag:
        org_length = np.arange(var_pressure_loc,
                               var_pressure_loc + var_list.__len__())
        pre_res = list(map(lambda sub: ''.join(
            [';', sub]), org_length.astype('str').tolist()))
        suf_res = list(map(lambda sub: ''.join([sub, ';0']), pre_res))
        suf_res.append('laser')
        var_list.append('laser')
    elif not varlist_flag | varpressure_flag:
        suf_res = None
        print('var_list or var_pressue not set, var_list_loc set to None')

    sMetadata = dict(subjectId=subjectId,
                     var_list=var_list,
                     var_pressure_loc=var_pressure_loc,
                     var_list_loc=suf_res,
                     laser=laser,
                     thresholds=dict(thresholds,
                                     parameter=parameter,
                                     laser_trigger=laser_trigger,
                                     window=window,))

    return sMetadata
# END Metadata creation functions ---------------------------


def metadataToYaml(metadata, path_to_save=[]):

    if path_to_save:
        file_path = path_to_save.joinpath('metadata.yaml')
        if not file_path.exists():
            with open(file_path, 'w') as file:
                metadata_yaml = yaml.dump(metadata, file, sort_keys=False)
                return metadata_yaml
    elif not path_to_save:
        metadata_yaml = yaml.dump(metadata, sort_keys=False)
        return metadata_yaml
    # return metadata_yaml
