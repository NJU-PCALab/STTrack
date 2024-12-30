for ((runid=15; runid>=10; runid--))
do
   python ./RGBT_workspace/test_rgbt_mgpus.py --script_name sttrack --yaml_name deep_rgbt_256 --dataset_name LasHeR --threads 16 --num_gpus 4 --epoch $runid  && echo "Command for runid $runid executed successfully"
done

for ((runid=15; runid>=10; runid--))
do
    python ./RGBT_workspace/test_rgbt_mgpus.py --script_name sttrack --yaml_name deep_rgbt_256 --dataset_name RGBT234 --threads 16 --num_gpus 4 --epoch $runid  && echo "Command for runid $runid executed successfully"
done
