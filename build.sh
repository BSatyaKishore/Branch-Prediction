cd src
ant clean
ant
ant make-jar
java -jar jar/BranchPredictor.jar ../traces/trace1 $1
java -jar jar/BranchPredictor.jar ../traces/trace2 $1
java -jar jar/BranchPredictor.jar ../traces/trace3 $1
java -jar jar/BranchPredictor.jar ../traces/trace4 $1
java -jar jar/BranchPredictor.jar ../traces/trace5 $1
