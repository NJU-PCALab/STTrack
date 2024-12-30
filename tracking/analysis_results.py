import _init_paths
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [8, 8]

from lib.test.analysis.plot_results import plot_results, print_results, print_per_sequence_results
from lib.test.evaluation import get_dataset, trackerlist
import argparse

parser = argparse.ArgumentParser(description='Run tracker on sequence or dataset.')
parser.add_argument('--tracker_name', default='sttrack')
parser.add_argument('--tracker_param', default='deep_rgbt_384',type=str, help='Name of config file.')
parser.add_argument('--dataset_name', default='lasher',type=str, help='Name of config file.')
parser.add_argument('--runid', type=int, default=None, help='The run id.')
# parser.add_argument('--run_ids', type=str, help='Name of config file.')
# parser.add_argument('--run_ids', nargs='+', help='<Required> Set flag', required=True)
args = parser.parse_args()
args.runid = [15,14,13,12,11]
# args.runid = []
# for i in range(18,20):
#     args.runid.append(i)
# for i in range(10,15):
#     args.runid.append(i)
trackers = []
dataset_name = args.dataset_name
"""tbsi_track"""
trackers.extend(trackerlist(name=args.tracker_name, parameter_name=args.tracker_param, dataset_name=dataset_name,
                            run_ids=args.runid, display_name=args.tracker_param))


dataset = get_dataset(dataset_name)
# dataset = get_dataset('otb', 'nfs', 'uav', 'tc128ce')
#plot_results(trackers, dataset, 'LasHeR', merge_results=True, plot_types=('success', 'prec'),
#             skip_missing_seq=False, force_evaluation=True, plot_bin_gap=0.05)
print_results(trackers, dataset, dataset_name, merge_results=False, plot_types=('success', 'norm_prec', 'prec'))
# print_results(trackers, dataset, 'UNO', merge_results=True, plot_types=('success', 'prec'))

