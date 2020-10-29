def openFile(filename):
	sentance = ""
	try:
		f = open(filename, 'r')
		sentance = f.readlines()
	except FileNotFoundError:
		print("No such file found")
		retype = input("Retype your file name or type in a number 0-2 to change mode")
		if retype in ['0', '1', '2']:
			mode = retype
		else:
			sentance = openFile(retype)

	return sentance


def main():
	mode = input("\n\n\n\nEnter mode ID:(0 to quit, 1 for input, 2 for file):")

	while mode not in ['0', '1', '2']:
		print("WRONG ID!")
		mode = input("Enter mode ID:(0 to quit, 1 for input, 2 for file):")


	sentance = ""
	while sentance == "":
		if mode == '0':
			return 0
		elif mode == '1':
			sentance = input("Enter a sentance to spellcheck:")
		elif mode == '2':
			filename = input("Enter a filename of txt file for spellchecking:")
			sentance = openFile(filename)
		

main()