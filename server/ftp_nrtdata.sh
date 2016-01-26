#!/bin/sh
export PATH=$PATH:/usr/local/netcdf/bin
export PATH=$PATH:/usr/lib/gmt/bin
export PATH=$PATH:/home/aditya/GAMIT10_6/gamit/bin
export PATH=$PATH:/home/aditya/GAMIT10_6/kf/bin
export PATH=$PATH:/home/aditya/GAMIT10_6/com
export HELP_DIR=/home/aditya/GAMIT10_6/help/
export INSTITUTE=UMA

python /home/aditya/UMASS/Python_Scripts/DownloadCnvlV2.py
python /home/aditya/UMASS/Python_Scripts/Download_nwsd.py
python /home/aditya/UMASS/Python_Scripts/nrt_common_files.py
mv -f ~/UMASS/DFWnet/net1/2015/temp_rinex/obs/*0.15o ~/UMASS/DFWnet/net1/2015/rinex/
python /home/aditya/UMASS/Python_Scripts/run_gamit_nrt.py net1
python /home/aditya/UMASS/Python_Scripts/plot_WV.py
mv -f ~/UMASS/DFWnet/net1/2015/rinex/cnvl* /var/www/html/gpsmet/CASA/Rinex/2015/cnvl/obs/day_files/
mv -f ~/UMASS/DFWnet/net1/2015/rinex/nwsd* /var/www/html/gpsmet/CASA/Rinex/2015/nwsd/obs/day_files/
rm ~/UMASS/DFWnet/net1/2015/rinex/*
 
