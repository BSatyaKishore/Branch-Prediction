#!/bin/python

import auxiliary, sys, os, shutil

try:
	
	working_dir = os.getcwd() + "/working_directory/"
	auxiliary.mkdirIfDirectoryDoesntExist(working_dir)
	auxiliary.cleanDirectory(working_dir)

	if len(sys.argv) > 0:
		if sys.argv[1] == "clean":
			auxiliary.deleteDirectoryIfItExists(working_dir)# + "bin")
			"""
			auxiliary.deleteDirectoryIfItExists(working_dir + "jar")
			auxiliary.deleteDirectoryIfItExists(working_dir + "logs")
			if os.path.isfile(working_dir + "auxiliary.pyc"):
				os.remove(working_dir + "auxiliary.pyc")
			"""
			sys.exit(0)


#	golden_files_dir = os.getcwd() + "/golden_files/"
	trace_dir = os.getcwd() + "/traces/"

	submission = sys.argv[1]
	auxiliary.extract(submission, working_dir)
#	for f in os.listdir(working_dir):
#		os.rename(working_dir + f, working_dir + f + ".tmp")

	shutil.copyfile("Main.java", working_dir + "Main.java")
	shutil.copyfile("Predictor.java", working_dir + "Predictor.java")
	shutil.copyfile("Register.java", working_dir + "Register.java")
	shutil.copyfile("Table.java", working_dir + "Table.java")
	shutil.copyfile("build.xml", working_dir + "build.xml")

	os.chdir(working_dir)

	"""
	#test for tampered framework
	fileMismatch = False
	for f in os.listdir(golden_files_dir):
		if f == "Predictor.java":
			continue
		gf = open(golden_files_dir + f, "r")
		sf = open(working_dir + f, "r")
		while True:
			gb = gf.read(1)
			sb = sf.read(1)
			if not gb:
				if not sb:
					break
				else:
					fileMismatch = True
					break
			if gb != sb:
				fileMismatch = True
				break
		if fileMismatch == True:
			break

	if fileMismatch == True:
		print "file " + f + " mismatch!!"
		sys.exit(0)
	"""

	#compile and run
	log_dir = working_dir + "logs/"
	auxiliary.mkdirIfDirectoryDoesntExist(log_dir)
	auxiliary.cleanDirectory(log_dir)

	stdoutFilename = log_dir + "compile.stdout"
	stderrFilename = log_dir + "compile.stderr"
	ret1 = auxiliary.runProgram("ant clean", working_dir, stdoutFilename, stderrFilename, 60)
	ret2 = auxiliary.runProgram("ant", working_dir, stdoutFilename, stderrFilename, 60)
	ret3 = auxiliary.runProgram("ant make-jar", working_dir, stdoutFilename, stderrFilename, 60)
	if ret1 < 0 or ret2 < 0 or ret3 < 0:
		print "compilation error"
		sys.exit(0)


	#test that only Tables and Registers are used
	max_size = -1
	averageAccuracy = [0, 0, 0]
	expectedAccuracy = {"1200": 0.9484, "2400": 0.9513, "4800": 0.9531}
	failedTests = []
	sizeIndex = -1
	for jf in os.listdir(working_dir):
		if len(jf) <= 14:
			continue
		sizeIndex = sizeIndex + 1

		max_size = jf[9:13]
		print "\n\n-------------------------\nMAX SIZE = " + str(max_size) + "\n-------------------------\n"
		print "file = " + jf.split(".")[0] + "\n"

		illegalStructure = False
		illegalLine = ""
		"""
		f = open(jf, "r")
		for l in f:
			line = l
			if "[]" in line.replace(" ",""):
				if "Register" not in line and "Table" not in line:
					illegalStructure = True
					illegalLine = l
					break
			if "new" in line:
				line = line.replace("(", " ")
				line = line.replace(')', ' ')
				line = line.replace(',', ' ')
				line = line.split()
				for i in range(0, len(line)-1):
					if(line[i] == "new"):
						if line[i+1] != "Register" and line[i+1] != "Table":
							illegalStructure = True
							illegalLine = l
							break
		"""
		f = open(jf, "r")
		file_contents = f.read().replace('\n','')
		program_lines = file_contents.split(';')
		for l in program_lines:
			line = l
			if "[]" in l:
				line = line.replace("(", " ")
				line = line.replace(')', ' ')
				line = line.replace(',', ' ')
				line = line.replace("[", " [")
				line = line.split()
				for i in range(0, len(line)-1):
					if(line[i] == "[]"):
						if line[i-1] != "Register" and line[i-1] != "Table" and line[i-2] != "Register" and line[i-2] != "Table":
							print "1"
							print line[i-2]
							illegalStructure = True
							illegalLine = l
							break
			line = l
			if "new" in l:
				line = line.replace("(", " ")
				line = line.replace(')', ' ')
				line = line.replace(',', ' ')
				line = line.replace("[", " [")
				line = line.split()
				for i in range(0, len(line)-1):
					if(line[i] == "new"):
						if line[i+1] != "Register" and line[i+1] != "Table":
							print "2"
							print line[i+1]
							illegalStructure = True
							illegalLine = l
							break
				
		f.close()
		if illegalStructure == True:
			print "illegal structure used. culprit line:"
			print illegalLine
			sys.exit(0)


		anyFailureInThisSize = False
		numTests = 0
		for trace in os.listdir(trace_dir):
			print "\nTRACE: " + trace
			numTests = numTests + 1

			stdoutFilename = log_dir + trace + "_" + str(max_size) + ".stdout"
			stderrFilename = log_dir + trace + "_" + str(max_size) + ".stderr"

			ret = auxiliary.runProgram("java -jar jar/BranchPredictor.jar " + trace_dir + trace + " " + str(max_size), working_dir, stdoutFilename, stderrFilename, 300)
			error = False
			if (ret < 0):
				error = True
				continue

			size = -1
			accuracy = -1
			of = open(stdoutFilename, "r")
			for line in of:
				if "Size" in line:
					size = int(line.split()[3])
				if "Accuracy" in line:
					accuracy = float(line.split()[2])
			of.close()
			if size == -1 or accuracy == -1:
				error = True

			if error == True:
				print "runtime error!"
			else:
				print "size = " + str(size)
				if size <= max_size:
					print "accuracy = " + str(accuracy)
					averageAccuracy[sizeIndex] = averageAccuracy[sizeIndex] + accuracy
				else:
					print "predictor size too large!"
					error = True

			if error == True:
				failedTests.append(trace + "_" + str(max_size))
				anyFailureInThisSize = True

		if anyFailureInThisSize == False:
			averageAccuracy[sizeIndex] = averageAccuracy[sizeIndex] / numTests
			print "\n\naverage predictor accuracy = " + str(averageAccuracy[sizeIndex])
			print "expected average accuracy  = " + str(expectedAccuracy[max_size])

	if len(failedTests) != 0:
		print "\n\nfailed tests:"
		print failedTests


except Exception as e:
	print e
	sys.exit(1)

