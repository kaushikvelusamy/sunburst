conda module on Polaris:

module load conda

------------------------------------------------------------------------------
Create a virtual environment and install packages:
------------------------------------------------------------------------------

conda create -n my-demo-env python=3.9.12
conda activate my-demo-env
pip install --pre balsam
pip install parsl
pip install matplotlib
