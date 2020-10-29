def openFile(filename):
	text = ""
	try:
		f = open(filename, 'r')
		text = f.readlines()
	except FileNotFoundError:
		print("No such file found")
		retype = input("Retype your file name or type in a number 0-2 to change mode")
		if retype in ['0', '1', '2']:
			return retype
		else:
			text = openFile(retype)

	return " ".join(text)


def getText():
	mode = input("\n\n\n\n\n\n\n\n\n\n\n\nEnter mode ID(0 to quit, 1 for input, 2 for file):")

	while mode not in ['0', '1', '2']:
		print("WRONG ID!")
		mode = input("Enter mode ID:(0 to quit, 1 for input, 2 for file):")

	text = ""
	while text == "":
		if mode == '0':
			return 0
		elif mode == '1':
			text = input("Enter a text to spellcheck:")
		elif mode == '2':
			filename = input("Enter a filename of txt file for spellchecking:")
			text = openFile(filename)
			if text in ['0', '1', '2']:
				mode = text
	return text

def formatText(text):
	formattedText = text
	# remove everything that is not a letter or whitespace
	for char in text:
		if char.isalpha() == False:
			if char != ' ':
				formattedText = formattedText.replace(char, '')
	print(formattedText)

	# turn the text into a list
	formattedText = formattedText.split(' ')

	# make everything lowercase
	for i in range(len(formattedText)):
		for char in formattedText[i]:
			formattedText[i] = formattedText[i].replace(char, char.lower())
	return formattedText

def main():
	text = getText()
	text = formatText(text)
	print(text)

	misspelled_count = 0
	added_to_dict = 0
	dictionary = open("EnglishWords.txt", 'r').read().split('\n')
	for word_to_check in text:
		for word_in_dict in dictionary:
			if word_in_dict == word_to_check.lower() or len(word_to_check) == 0:
				break;
		else:
			print(word_to_check + " not found")
			option = 0
			while option not in ['1', '2', '3', '4']:
				option = input("1 to ignore, 2 to mark, 3 to add to dictionary, 4 to get a suggestion:")

			if option == '1':
				misspelled_count += 1
			elif option == '3':
				added_to_dict += 1


	print("Misspelled words:" + str(misspelled_count))
		

main()