d<-scan("1tag.dist.txt")
pdf("1tag.dist.write.pdf")
hist(d, breaks=30, col="dark red", main="", xlab="Number of writes/s", ylab="Frequence")
grid()
dev.off()
