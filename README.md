# Sublime Skim

* Version: 1.0.1
* Date: January 30, 2014

This package provides helper functions for cleaning PDF notes exported from [Skim](http://skim-app.sourceforge.net/). It comes with the following commands:

* Clean page numbers: Select all the text in the file and run the command to replace all ``
* Renumber single pages
* Renumber spreads

None of these commands are attached to keyboard shortcuts (since I don't use them that often), but it's easy to do so.


## Details

### Clean page numbers

Select all the text in the file and run the command to clean up the exported Skim notes. Cleaning does three things:

1. Removes all extra note metadata (e.g. `* Text Note, page 1` and `* Highlight, page 4`) and replace with simple page numbers (e.g. `1 - Lorem ipsum dolor sit amet` and `4 - consectetur adipisicing elit`)  
2. Removes stacked page numbers (e.g. `1 - Lorem ipsum...` and `1 - dolor sit amet` becomes `1 - Lorem ipsum` and `dolor sit amet`)
3. Wraps highlighted notes in quotes

For example, it will transform 

	* Text Note, page 1
	Alice was beginning to get very tired of sitting by her sister on the bank

	* Highlight, page 1
	and of having nothing to do: once or twice she had peeped into the book her sister was reading

	* Text Note, page 1
	but it had no pictures or conversations in it

	* Text Note, page 2
	'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	* Text Note, page 2
	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	* Text Note, page 3
	when suddenly a White Rabbit with pink eyes ran close by her.

into

	1 - Alice was beginning to get very tired of sitting by her sister on the bank

	"and of having nothing to do: once or twice she had peeped into the book her sister was reading"

	but it had no pictures or conversations in it

	2 - 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	3 - when suddenly a White Rabbit with pink eyes ran close by her.


## Renumber single pages

After cleaning the page numbers, you can renumber the pages so that the notes correspond to the actual pagination of the PDF and not however the PDF is numbered. If the PDF actually starts on page 56, but Skim exported the notes starting with page 1, select the text and run the "Renumber single pages command." Input the realy number of the first page in the PDF and all notes will be renumbered. 

It will transform 

	1 - Alice was beginning to get very tired of sitting by her sister on the bank

	"and of having nothing to do: once or twice she had peeped into the book her sister was reading"

	but it had no pictures or conversations in it

	2 - 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	3 - when suddenly a White Rabbit with pink eyes ran close by her.

into

	56 - Alice was beginning to get very tired of sitting by her sister on the bank

	"and of having nothing to do: once or twice she had peeped into the book her sister was reading"

	but it had no pictures or conversations in it

	57 - 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	58 - when suddenly a White Rabbit with pink eyes ran close by her.


### Renumber spreads

Sometimes PDFs come as spreads instead of individual pages. Similar to the "Renumber single pages" command, this will renumber pages to correspond to a two-page range. 

It transforms this

	1 - Alice was beginning to get very tired of sitting by her sister on the bank

	"and of having nothing to do: once or twice she had peeped into the book her sister was reading"

	but it had no pictures or conversations in it

	2 - 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	3 - when suddenly a White Rabbit with pink eyes ran close by her.

into

	102-103 - Alice was beginning to get very tired of sitting by her sister on the bank

	"and of having nothing to do: once or twice she had peeped into the book her sister was reading"

	but it had no pictures or conversations in it

	104-105 - 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

	So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies

	106-107 - when suddenly a White Rabbit with pink eyes ran close by her.


## Known issues

* "Clean page numbers" will choke on articles from JSTOR, since they number their pages with a `p.` prefix, making note headers like `* Text Note, page p. 1`. Find all ` p. `s and replace with nothing before cleaning the page numbers. 
* "Clean page numbers" only takes care of a subset of potential PDF annotations: Text Note, Anchored Note, and Highlight.
* "Renumber single pages" isn't necessary if the PDF is numbered correctly internally (like with Acrobat).
* "Renumber spreads" is experimental and totally confusing and needs negative numbers (for now) to work right. It takes a lot of unnecessary trial and error to make it work right. It needs significant improvements.
