# Deployment

ansible-playbook -i tencent_cloud.ini -f 4 one_remote_playbook.yaml

ansible-playbook -i tencent_cloud.ini one_remote_playbook.yaml --ask-become-pass

# Requirement
ansible = 7.3.0
python >= 3.9

conda install ansible
or pip install ansible
