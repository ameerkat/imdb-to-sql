# Conversion functions from Roman Numeral to Integers
# Ameer Ayoub <ameer.ayoub@gmail.com>

def rntoi(numeral_string):
	"""roman numeral to decimal integer conversion function."""
	if not numeral_string:
		return None
	d = { "I" : 1, "V" : 5, "X" : 10, "L" : 50, "C" : 100, "D" : 500, "M" : 1000 }
	for ch in numeral_string:
		if ch not in d:
			return None
	sum = 0
	lower_sum = 0
	last = numeral_string[0]
	lower_sum += d[last]
	for ch in numeral_string[1:]:
		if d[ch] > d[last]:
			sum += d[ch]-lower_sum
			lower_sum = 0
		elif d[ch] < d[last]:
			sum += lower_sum
			lower_sum = d[ch]
		else:
			lower_sum += d[ch]
		last = ch
	return sum + lower_sum

if __name__ == "__main__":
	# run tests
	# numbers taken from http://www.list-of.org.uk/list-of-roman-numerals.htm
	# fixed some errors though
	numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
				"XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
				"XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
				"XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
				"XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII", "XLVIII", "XLIX", "L",
				"LI", "LII", "LIII", "LIV", "LV", "LVI", "LVII", "LVIII", "LIX", "LX", 
				"LXI", "LXII", "LXIII", "LXIV", "LXV", "LXVI", "LXVII", "LXVIII", "LXIX", "LXX",
				"LXXI", "LXXII", "LXXIII", "LXXIV", "LXXV", "LXXVI", "LXXVII", "LXXVIII", "LXXIX", "LXXX",
				"LXXXI", "LXXXII", "LXXXIII", "LXXXIV", "LXXXV", "LXXXVI", "LXXXVII", "LXXXVIII", "LXXXIX", "XC",
				"XCI", "XCII", "XCIII", "XCIV", "XCV", "XCVI", "XCVII", "XCVIII", "XCIX", "C"]
	nums = map(rntoi, numerals)
	failure = False
	for i in xrange(100):
		if i+1 != nums[i]:
			print "mismatch: ", numerals[i], "->", nums[i], "expected", i+1
			failure = True
	if failure:
		print "complete."
	else:
		print "complete with no errors."
