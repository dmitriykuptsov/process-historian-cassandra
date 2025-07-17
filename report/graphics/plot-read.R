data<-read.csv("read.txt", header=T)
require(ggplot2)

pdf("read.pdf")
options(repr.plot.width = 5, repr.plot.height = 2)
ggplot(data, aes(x = Size, y = Mean)) +
  geom_line(lwd=1.5) + 
  geom_errorbar(aes(ymax = CIP, ymin = CIN)) +
  xlab("Number of tags") +
  ylab("Samples/s") +
  theme_minimal()
dev.off()
