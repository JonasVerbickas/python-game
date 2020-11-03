from difflib import SequenceMatcher
from datetime import datetime

def openFile(filename):
	text = ""
	try:
		f = open(filename, 'r')
		text = f.readlines()
		f.close()
	except FileNotFoundError:
		print("No such file found")
		retype = input("Retype your file name OR type in a number 0-2 to change mode: ")
		if retype in ['0', '1', '2']:
			return retype
		else:
			text = openFile(retype)

	return " ".join(text)


def getText():
	mode = input("\n\nEnter mode ID (0 to quit, 1 for input, 2 for file): ")

	while mode not in ['0', '1', '2']:
		print("WRONG ID!")
		mode = input("Enter mode ID (0 to quit, 1 for input, 2 for file): ")

	print()
	text = ""
	while text == "":
		if mode == '0':
			return 0
		elif mode == '1':
			text = input("Enter text to spellcheck: ")
		elif mode == '2':
			filename = input("Enter a filename of the file for spellchecking (or to change mode type in one of the IDs): ")
			text = openFile(filename)
			if text in ['0', '1', '2']:
				mode = text
		text = formatText(text)
	return text

def formatText(text):
	formattedText = text
	# remove everything that is not a letter or whitespace
	for char in text:
		if char.isalpha() == False:
			if char != ' ':
				formattedText = formattedText.replace(char, '')
		else:
			formattedText = formattedText.replace(char, char.lower())
	return formattedText

def printDashes():
	print("-----------------------------------------------------")

def main():
	text = getText()
	if text == 0:
		return 0
	# turn the text string into a list of words
	text = text.split(' ')
	
	misspelled_count = 0
	added_to_dict = 0
	accepted_suggestions = 0
	dictionary = open("EnglishWords.txt", 'r').read().split('\n')
	add_to_dict = []
	total_number_of_words = len(text)

	starting_time = datetime.now()
	printDashes()
	print("CURRENT WORD")
	for index in range(total_number_of_words):
		word_to_check = text[index].lower()
		print(word_to_check, end="")

		# used if is this way to make it more easily readable
		word_is_correct = word_to_check in dictionary or word_to_check in add_to_dict
		if word_is_correct:
			print()
		else:
			print(" - NOT FOUND")
			option = 0
			while option not in ['1', '2', '3', '4']:
				option = input("1 to ignore, 2 to mark, 3 to add to dictionary, 4 to get a suggestion: ")

			if option == '1':
				misspelled_count += 1
			elif option == '2':
				text[index] = "?" + text[index] + "?"
				misspelled_count += 1
			elif option == '3':
				added_to_dict += 1
				add_to_dict.append(word_to_check)
			elif option == '4':
				closest_word = "";
				for word_in_dict in dictionary:
					if SequenceMatcher(None, word_in_dict, word_to_check).ratio() > SequenceMatcher(None, closest_word, word_to_check).ratio():
							closest_word = word_in_dict
				print("Suggestion: " + closest_word)
				decision_on_suggestion = ''
				while decision_on_suggestion not in ['1', '2']:
					decision_on_suggestion = input("Use the suggested word? (1 use, 2 reject): ")
				if decision_on_suggestion == '1':
					text[index] = closest_word
					accepted_suggestions += 1
				else:
					misspelled_count += 1


	total_time_needed = datetime.now() - starting_time
	# STATISTICS
	# to terminal
	printDashes()
	print("STATISTICS")
	print("Total number of words: " + str(total_number_of_words))
	print("Words spelled correctly: " + str(total_number_of_words - misspelled_count))
	print("Misspelled words: " + str(misspelled_count))
	print("Added to the dictionary: " + str(added_to_dict))
	print("Accepted suggestions: " + str(accepted_suggestions))
	print("Spellcheck was done on: " + str(starting_time))
	print("The program took " + str(round(total_time_needed.total_seconds(), 2)) + " seconds")
	printDashes()
	# to file
	filename = ""
	while len(filename) == 0:
		filename = input("\nEnter the name of the output file: ")
	print()

	output = open(filename, 'w')
	output.write("Total number of words: " + str(total_number_of_words) + '\n')
	output.write("Words spelled correctly: " + str(total_number_of_words - misspelled_count) + '\n')
	output.write("Misspelled words: " + str(misspelled_count) + '\n')
	output.write("Added to the dictionary: " + str(added_to_dict) + '\n')
	output.write("Accepted suggestions: " + str(accepted_suggestions) + '\n')
	output.write("Date: " + str(starting_time) + '\n')
	output.write("The program took " + str(round(total_time_needed.total_seconds(), 2)) + " seconds\n")
	output.write("\n")
	output.write(' '.join(text))
	output.close()
	# add new words to dictionary
	dict_file = open("EnglishWords.txt", 'a')
	for word_to_add in add_to_dict:
		dict_file.write('\n' + word_to_add)
	dict_file.close()

	printDashes()
	if input("\nInput (1) to go back to main manu or anything else to quit:") == '1':
		main()


main()
