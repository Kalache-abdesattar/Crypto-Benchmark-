import argparse 
import os 


parser = argparse.ArgumentParser(description='++++++++++CPU ENCRYPTION BENCHMARK++++++++++')
parser.add_argument('-p', '--path', required=True, help='Text File Path')
args = vars(parser.parse_args())


def augment_file_size(filepath):
	size = 0

	while size < 1000:
		file = open(filepath, 'r+')
		size = os.path.getsize(filepath) / 1_000_000

		print('===================The size of lab-report.txt is {0}mb========================'.format(size))

		rl = file.readlines()

		for line in rl:
			file.write(line)

		file.close()

	file.close()
	print('File has been augmented successfully with {0}mb'.format(size))

	
augment_file_size(args['path'])