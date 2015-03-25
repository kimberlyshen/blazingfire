import sys

import java.io.FileReader as FileReader
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.io.FileOutputStream as FileOutputStream
import java.io.PrintStream as PrintStream

import weka.core.Instances as Instances
import weka.classifiers.trees.J48 as J48
import weka.classifiers.Evaluation as Evaluation
import weka.core.Range as Range

"""

    The following code uses the machine learing algorithm (J48) in Weka
    
    to predict if the home is occupied or not based on the data provided 
    
    in the input ARFF file.
    
    Input Parameter in commandline: home.arff

    Note: needs Weka 3.6.x to run (due to changes in the 
      weka.classifiers.Evaluation class)

"""

# check commandline parameters
if (not (len(sys.argv) == 2)):
    print "Usage: homeMachineLearning.py home.arff"
    sys.exit()

# load data file
print "Loading home.arff..."
file = FileReader(sys.argv[1])
data = Instances(file)

# set the class Index - the index of the dependent variable
#data.setClassIndex(data.numAttributes() - 2)
data.setClassIndex(0)


# create the model
evaluation = Evaluation(data)
buffer = StringBuffer()  # buffer for the predictions
attRange = Range()  # no additional attributes output
outputDistribution = Boolean(False)  # we don't want distribution
print "Training J48 with the home occupancy data...\n"
j48 = J48()
j48.buildClassifier(data)  # only a trained classifier can be evaluated

#Creating a small 'instances' with just 1 'instance' (using first instance as dummy)
smallerData = Instances(data, 0, 1)
#Getting the last instance from the ARFF file
#Most recent output of the home occupancy detection algorithm
lastInst = data.lastInstance()
#Adding the second instance to the instances
smallerData.add(lastInst)
print smallerData

#Making the prediction on the instaces
evaluation.evaluateModel(j48, smallerData, [buffer, attRange, outputDistribution])

#Uncomment the below line to do the prediction on all attributes (might take longer)
#evaluation.evaluateModel(j48, data, [buffer, attRange, outputDistribution])


# print out the built model
print "Generated model for home occupancy:\n"
print j48

print "--> Evaluation for home occupancy:\n"
print evaluation.toSummaryString()

print "--> Predictions for home occupancy:\n"
print buffer

fout = FileOutputStream("machineLearningPrediction.txt")
pout = PrintStream(fout)
pout.print(buffer.toString())
