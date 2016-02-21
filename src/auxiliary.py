#!/bin/python
import sys, fileinput, os, threading, subprocess, shlex, shutil, pipes

clean_list=[]

# delete all contents of a directory (not the directory itself) : " rm -rf dir/* "
def cleanDirectory(dir_path):
	if not os.path.exists(dir_path):
		return
	for root, dirs, files in os.walk(dir_path):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))

#extract compressed file to folder
#handles tar, rar, zip, tar.gz
def extract(compressedFile, destinationFolder):
	print "extracting..."
	compressedFile = normalizePathAndCheckExistence(compressedFile)
	destinationFolder = normalizePathAndCheckExistence(destinationFolder)

	output = subprocess.Popen(["file", compressedFile], stdout=subprocess.PIPE).communicate()[0]

	isTar = "false"
	isRar = "false"
	isZip = "false"
	if "tar archive" in output:
		isTar = "true"
	#if "RAR archive" in output:
	#	isRar = "true"
	if "Zip archive" in output:
		isZip = "true"

	cwd = os.getcwd()
	os.chdir(destinationFolder)

	if isTar == "true":
		subprocess.call(["tar","xf",compressedFile])
	elif isRar == "true":
		subprocess.call(["rar","e",compressedFile])
	elif isZip == "true":
		subprocess.call(["unzip","j",compressedFile])
	else:
		subprocess.call(["tar","xfz",compressedFile])

	print "DONE"

	os.chdir(cwd)

# specify a path "a/b/c/d" to create directories a,b,c,d
# the case where part or whole of the path already exists is gracefully handled
def mkdirIfDirectoryDoesntExist(pathToDir):
	try: 
		os.makedirs(pathToDir)
	except OSError:
		if not os.path.isdir(pathToDir):
			raise


# search for one of given list of files in the sub-tree rooted at given directory
# if found, return absolute path
def findFileInSubTree(fileNameLists, directory):
	for dirf in os.listdir(directory):
		for srchf in fileNameLists:
			if dirf == srchf:
				return os.path.abspath(os.path.join(directory,dirf))
		if os.path.isdir(dirf):
			return findFileInSubTree(fileNameLists, os.path.join(directory,dirf))
	return None


def cleanExit(returnCode):
	for f in clean_list:
		cleanDirectory(f)
	exit(returnCode)	

# delete all contents of a directory (not the directory itself) : " rm -rf dir/* "
def cleanDirectory(dir_path):
	if not os.path.exists(dir_path):
		return
	for root, dirs, files in os.walk(dir_path):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))

# used to run test cases
# a thread is spawned, and the new thread spawns a subprocess running the given command
# the original thread waits for the new one to join for a stipulated period of time
#	if thread hasn't joined within time limit, the executed process is terminated
# the STDOUT and STDERR of the process are redirected to specified files
class RunTestcase(object):
	def __init__(self, **args):
		self.process = None
		self.commands = args["commands"]	# a list of commands may be specified - they are tried in order until
							# one of them works
		self.working_directory = args["working_directory"]
		self.stdoutFilename = args["stdoutFilename"]
		self.stderrFilename = args["stderrFilename"]
		self.timeout_limit = args["timeout_limit"]

	def run(self):
		def target():
			for cmd in self.commands:
				try:
					self.process = subprocess.Popen(cmd, stdout=open(self.stdoutFilename,"w"), stderr=open(self.stderrFilename,"w"), cwd=self.working_directory)
					break
				except Exception as e:
					#print "exception " + str(e) + " while running " + str(cmd)
					pass
			if self.process == None:
				raise Exception('process creation error')
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(self.timeout_limit)
		if thread.is_alive():
			self.process.terminate()
			thread.join()
			raise Exception('timeout')
		return self.process.returncode

# run specified program using a RunTestCase object
def runProgram(command, working_directory, stdoutFilename, stderrFilename, timeout_limit):
	cmds = []
	cmds.append(shlex.split(command))
	threadInstance = RunTestcase(commands = cmds, working_directory = working_directory, stdoutFilename = stdoutFilename, stderrFilename = stderrFilename, timeout_limit = timeout_limit)
	try:
		ret = threadInstance.run()
	except Exception as e:
		print e
		with open(stderrFilename,"a+") as ferr:
			ferr.write(str(e))
		return -9999
	return ret

#normalizing path
def normalizePathAndCheckExistence(path):
	toReturn = os.path.abspath(path)
	if not os.path.isfile(toReturn) and not os.path.isdir(toReturn):
		print path + " does not exist\n"
		cleanExit(0)
	return toReturn


def cleanExit(returnCode):
	for f in clean_list:
		cleanDirectory(f)
	exit(returnCode)

def deleteDirectoryIfItExists(path):
	if os.path.isdir(os.path.abspath(path)):
		shutil.rmtree(os.path.abspath(path))
