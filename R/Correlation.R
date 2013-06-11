#This R script analyse the correlation between different rankings
#The screen output of result should use print() function
#If you want to print like interactive mode, use source("file.R",print.eval=TRUE)

#set the current directory
setwd("/home/gzhu/gsiwork/semantic-matching/R")

#save result to file
sink("result", append=TRUE,split=TRUE)

#save graph to pdf file
#pdf("graph.pdf")

#print current derectory
#print(getwd())
#cat("Data set is below\n")

#read data from file and output to screen
result <- read.table("data.dat", header=TRUE, sep="")

#print("Numbers or records:")

# Count the rows in A
#print(nrow(result))   

#view the whole data set                            
#print(result)	

#view the summary of data set				
#print(summary(result))		

#cat("Correlation computing\n")
#print(cov(result))
print(cor(result,method="spearman"))


#sink()
#dev.off()
			



