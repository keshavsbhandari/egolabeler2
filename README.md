# egolabeler2
EgoK360 Dataset Labeler


DataSet Source
https://egok360.github.io/

1. Download Dataset Sub-Folder wise and put sub-folder(or action folder) inside data folder in this project
2. Create a conda environment [Assumption latest anaconda/miniconda is installed, linux or mac]
    conda create -n egolabeler python=3.7
    conda activate egolabeler
    pip install -r requirements.txt
3. Now run following to start flask server and start labeling dataset one by one
    python app.py
    
4. If you want to run some background process to convert video into readable format ahead or while doing labeling run runinbg.py

    [OPEN NEW TERMINAL]
    conda activate egolabeler
    
    [FOR HELP]
    python runinbg.py --help
    
    [EXAMPLE convert n numbers of video while you work on labelling task]
    python runinbg.py --data folderinsidedatafolder --n numberofvideoyouwanttotransform
    
    [OR Convert all video inside folderinsidedatafolder]
    python runinbg.py --data folderinsidedatafolder --all
