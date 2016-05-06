workDir=/Users/jing/Dropbox/scripts/networkCommunityDetection/aaMMSB/
edgefile=$workDir/dat/matrix.txt
xgaufile=$workDir/dat/attributes_gau.txt
xbinfile=$workDir/dat/attributes_bin.txt
n=10
k=3
dgau=2
dbin=0
svinet -file $edgefile -fileGau $xgaufile -fileBin $xbinfile -n $n -k $k -dgau $dgau -dbin $dbin  -stratified -rnode -batch 
