library(ggplot2)

counts <- read.csv("phrase_counts.csv")

phrase.counts <- data.frame(Phrase=counts[, 1], year=counts[, 2], 
  match.count=counts[, 3], page.count=counts[, 4], volume.count=counts[, 5])

phrase.counts <- phrase.counts[which(phrase.counts$year >= 1900), ]
phrase.counts <- phrase.counts[which(phrase.counts$year <= 1947), ]

q <- qplot(year, volume.count, data=phrase.counts, geom="line", colour=Phrase, ylab="Publication Count", xlab="Year")
q <- q + opts(axis.text.x=theme_text(angle=-90, hjust=0),
  legend.background=theme_rect(fill="white"),legend.position=c(0.2, 0.8),
  legend.title=theme_text(size=13, face="bold",hjust=0),legend.text=theme_text(size=11))
q <- q + scale_x_continuous(breaks = seq(min(phrase.counts$year), max(phrase.counts$year), 2), minor_breaks=seq(min(phrase.counts$year), max(phrase.counts$year), 1))
q + scale_colour_manual(values = c("black", "red"))