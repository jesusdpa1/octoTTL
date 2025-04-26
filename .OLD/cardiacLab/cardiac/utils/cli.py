import cardiac.utils.auxiliaryfunctions as cardiac_aux
import datetime

# TODO add description to each function, do this sooner than later...


class subjectDataDict():
    # REVIEW maybe updating is better than init
    def __init__(self):
        self.subjectId = None
        self.threshold = cardiac_aux.ThresholdLimits()
        self.data = None

    def update(self, metadata):
        self.subjectId = metadata['subjectId']

        self.datamap = list(zip([metadata['subjectId']]*metadata['var_list_loc'].__len__(),
                                metadata['var_list_loc']))

        self.threshold.update_threshold(threshold_val=dict(day=metadata['thresholds']['day'],
                                                           night=metadata['thresholds']['day']),
                                        parameter=metadata['thresholds']['parameter'],
                                        laser_trigger=metadata['thresholds']['laser_trigger'],
                                        window=metadata['thresholds']['window'])

        self.data = cardiac_aux.get_data_dict(metadata['var_list'],
                                              metadata['var_list_loc'])

        self.laser = metadata['laser']


def buildExperiment(subject_metadata):
    subject_names = list(subject_metadata.keys())
    whole_data = list()

    for name in subject_names:
        partial = subjectDataDict()
        partial.update(subject_metadata[name])
        whole_data.append(partial)

    print(f'number of subject to record from {subject_names.__len__()}')
    print(f'subjects = {subject_names}')
    return dict(zip(subject_names, whole_data))


def startExperiment(globalMetadata):
    experiment_time = cardiac_aux.DateTime()
    experiment_time.update_rectime(globalMetadata['duration'])
    # REVIEW this, it might be confusing in the future / check creating dicts instead of list for this! CLI
    experiment_time.update_datetime(globalMetadata['day'], 'day')
    experiment_time.update_datetime(globalMetadata['night'], 'night')
    experiment_time.print_intervals()
    experiment_time.get_remainingtime()
    return experiment_time


def turnOFF(time=[0, 0, 10]):
    # NOTE finish later
    clock = cardiac_aux.Timer()
    clock.update(time)
    clock.startTimer()
    clock.get_remainingtime()

    while clock.timeRemaining > datetime.timedelta(hours=0, minutes=0, seconds=0):
        clock.get_remainingtime()
    print('Program Turned OFF')
