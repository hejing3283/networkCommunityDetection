rm(list = ls())
# plot_hpARACNe_newworkProperty.r
# preliminary analsysi for hpARACNe signaling network

wd = "/Users/jing/Dropbox/scripts/pmdd/"
datadir = 'dat/'
plotdir = 'doc/report/plots/'

setwd( wd )
setwd(datadir)
options(stringsAsFactors = F)
f.hpnet = 'ppNetworks/RESULT_formatted.txt'
colClass = c("character","character",'numeric','numeric','numeric','numeric')
hpnet = read.csv(f.hpnet, header= T,sep="\t")
head(hpnet)


edges = hpnet[sample(1:nrow(hpnet),nrow(hpnet)),]
## add edge attributes
edges.color = sample(c('green','red'),size = NROW(edges), replace = T)
edges.anno = data.frame(cbind(edges, edges.color ))

# add node attributes 
nodes.name = unique(unlist(edges[,1:2]))
nodes.id = as.integer(factor(nodes.name))
nodes.anno = data.frame( cbind(nodes.name,nodes.id) )

# check
edges[!edges[,1] %in% nodes.name & edges[,2] %in% nodes.name, ]


# build up network
require(igraph) ; require(scales)

net = graph.data.frame( edges.anno, nodes.anno, directed = T) 
net = simplify(net, remove.multiple = T, remove.loops = T)

####

# visulization
setwd(wd)
setwd(plotdir)
# set viz attributes
g = net
V(g)$size <- 5
V(g)$label.cex <- .2
V(g)$label <- NA
V(g)$color <-'skyblue' #rgb(0.45, 0.4, .45, 0.5)
V(g)$frame.color <- NA
egam <- (-log10(max(as.numeric(E(g)$pvalue),1e-7))+.1) /( max(-log10(max(1e-7,as.numeric(E(g)$pvalue))))+.1)
E(g)$color <- 'gray'#rgb(.94, .93, 0.96, 0.5)
E(g)$width <- 0.2

### another way 
#E(net)$edge.width = rescale(as.numeric(gsub(Inf,6,-log10(as.numeric(get.edge.attribute(net)$pvalue)))), to = c(0.3, 1))
# E(net)$edge.color <- ifelse( get.edge.attribute(net)$isGSD, 'orange','green')
# E(net)$edge.arrow.size <- .05
# E(net)$arrow.mode <- 0 
# # V(net)$size  <- rescale(as.numeric(get.vertex.attribute(net)$hasSubsCnt) * 
# # as.numeric( get.vertex.attribute(net)$isKinase) + 1,
# # to = c(0.5, 6) )
# V(net)$color  <- ifelse(get.vertex.attribute(net)$isKinase == '1', makeTransparent('red'),makeTransparent('skyblue',alpha = 0.8))
# V(net)$frame.color  <- ifelse(get.vertex.attribute(net)$isKinase == '1', 'darkred',makeTransparent('skyblue', alpha =0.5))
# V(net)$size   <- ifelse(get.vertex.attribute(net)$name %in% kinase.plot, 7,1)
# V(net)$label <- ''


# plot the graph in layout1
g.layout <- layout.fruchterman.reingold(g)
pdf("global_network_2wedges.pdf")
plot(g, edge.arrow.size=.01)
dev.off()


install.packages("animation", repos = "http://cran.cnr.berkeley.edu/", dependencies = TRUE)
library('igraph')
library('cluster')
library('animation')

## set up plot aes 

# Create sub-graphs based on edge attributes
#net.sig <- delete.edges(net, E(net)[get.edge.attribute(net)$pvalue > 0.001])

# Look at the plots for each sub-graph
#layout.netsig <- layout.fruchterman.reingold(net.sig)
#plot(m182_friend, layout=net.sig, edge.arrow.size=.01)

# community discovery
net.community <- walktrap.community(net, steps=200,modularity=TRUE)
net.community
modularity(net.community)
membership(net.community)
net.community.dend <- as.dendrogram(net.community, use.modularity=TRUE)
pdf("global_network_community_walktrap.pdf")
plot(net.community.dend)
dev.off()

net.ebtwnes <- edge.betweenness.community(net)
pdf("global_network_community_edgeBetweeness.pdf")
plot(net.ebtwnes, net)
dev.off()




# The following function will find the betweenness for each
# vertex.
friend_comm_eb <- edge.betweenness.community(m182_friend_no_iso)
friend_comm_eb
plot(as.dendrogram(friend_comm_eb))



