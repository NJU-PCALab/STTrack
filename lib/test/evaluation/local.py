from lib.test.evaluation.environment import EnvSettings

def local_env_settings():
    settings = EnvSettings()

    # Set your local paths here.

    settings.davis_dir = ''
    settings.got10k_lmdb_path = '/nasdata/tracking/hxt/STTrack_pub/data/got10k_lmdb'
    settings.got10k_path = '/nasdata/tracking/hxt/STTrack_pub/data/got10k'
    settings.got_packed_results_path = ''
    settings.got_reports_path = ''
    settings.itb_path = '/nasdata/tracking/hxt/STTrack_pub/data/itb'
    settings.lasot_extension_subset_path_path = '/nasdata/tracking/hxt/STTrack_pub/data/lasot_extension_subset'
    settings.lasot_lmdb_path = '/nasdata/tracking/hxt/STTrack_pub/data/lasot_lmdb'
    settings.lasot_path = '/nasdata/tracking/hxt/STTrack_pub/data/lasot'
    settings.network_path = '/nasdata/tracking/hxt/STTrack_pub/output/test/networks'    # Where tracking networks are stored.
    settings.nfs_path = '/nasdata/tracking/hxt/STTrack_pub/data/nfs'
    settings.otb_path = '/nasdata/tracking/hxt/STTrack_pub/data/otb'
    settings.prj_dir = '/nasdata/tracking/hxt/STTrack_pub'
    settings.result_plot_path = '/nasdata/tracking/hxt/STTrack_pub/output/test/result_plots'
    settings.results_path = '/nasdata/tracking/hxt/STTrack_pub/output/test/tracking_results'    # Where to store tracking results
    settings.save_dir = '/nasdata/tracking/hxt/STTrack_pub/output'
    settings.segmentation_path = '/nasdata/tracking/hxt/STTrack_pub/output/test/segmentation_results'
    settings.tc128_path = '/nasdata/tracking/hxt/STTrack_pub/data/TC128'
    settings.tn_packed_results_path = ''
    settings.tnl2k_path = '/nasdata/tracking/hxt/STTrack_pub/data/tnl2k'
    settings.tpl_path = ''
    settings.trackingnet_path = '/nasdata/tracking/hxt/STTrack_pub/data/trackingnet'
    settings.uav_path = '/nasdata/tracking/hxt/STTrack_pub/data/uav'
    settings.vot18_path = '/nasdata/tracking/hxt/STTrack_pub/data/vot2018'
    settings.vot22_path = '/nasdata/tracking/hxt/STTrack_pub/data/vot2022'
    settings.vot_path = '/nasdata/tracking/hxt/STTrack_pub/data/VOT2019'
    settings.youtubevos_dir = ''
    settings.lasher_path ='/nasdata/tracking/data/LasHeR'

    return settings