workdir = '/Users/Sky/Dropbox/Columbia/Spring 2016/'
setwd( workdir )
options(stringsAsFactors = T)

node.attr.exp = read.csv2("nodes_attributes_proteinExpression.txt",sep="\t",stringsAsFactors = F)

node.name =  node.attr.exp[,1]
node.attr.exp = node.attr.exp[,-1]
node.attr.exp = node.attr.exp[,1:108]

binAtrributes = function(x, nbin = 6){
  #nbin = 6
  x = as.numeric(x)
  y = rep(0, length(x))
  na.id = is.na(x)
  qntl = c(0,0.01,0.25,0.5,0.75,0.99,1)
  x.bin = cut(na.omit(x), nbin, labels = 1:nbin, include.lowest = T)
  y[!na.id] <- x.bin
  return(y)
}

node.attr.exp.bin = apply(node.attr.exp,2,function(x) binAtrributes(x,6))
rownames(node.attr.exp.bin) = node.name

outputfile = "nodes_attributes_proteinExpression_bin_6.txt"
write.table(node.attr.exp.bin,file = outputfile, col.names = F,row.names = T,sep="\t",quote=F)
