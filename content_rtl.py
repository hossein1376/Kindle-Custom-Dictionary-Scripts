# This script prepares the source data for creating the kindle custom dictionaries.
# This script is intended for RTL languages.
import time


def content_top():  # Each html file header
    return ('''<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
      xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
      xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
      xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">
	  
  <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>

  <body> 
    <mbp:frameset>''')


def content_end():  # Each html file footer
    return ('''  </mbp:frameset>
  </body>
</html>''')


def data_preface():  # Marks the beginning of each entry
    return ('''     <idx:entry name="default" scriptable="yes" spell="yes">''')


def column_a(data):
    return (f'<idx:orth value="{data}">')


def column_b(data):
    return (f'<b>{data}</b>')


def column_inflections(data):
    return (f'<idx:iform value="{data}" />')


def column_definitions(data):
    return (f'</idx:orth><p>{data}</p></idx:entry>\n')


def find_nth(haystack, needle, n):  # Is used to find exact location of each inflections
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def rtl_reverse(entry, break_point):  # Reverse the words' order
    definition = entry[break_point+1:]
    definition = definition.split()
    definition = definition[::-1]
    definition = ' '.join(definition)
    return definition


start_time = time.time()
page_count = 1  # Starts with content1.html
counter = 0
with open('content1.html', 'a', encoding="utf-8") as file:
    file.write(content_top() + '\n')

with open('Data Source.txt', 'r', encoding="utf-8") as file:
    for line in file:
        entry = line.rstrip()

        if counter == 15000:  # Number of entries in each html file.
            with open('content' + str(page_count) + '.html', 'a', encoding="utf-8") as newfile:
                newfile.write(content_end())
            with open('content' + str(page_count+1) + '.html', 'a', encoding="utf-8") as newfile:
                newfile.write(content_top() + '\n')
            page_count += 1
            counter = 0

        first = find_nth(entry, '|', 1)
        break_point = find_nth(entry, '	', 1)
        if first == -1:  # A single word without Inflections
            definition = rtl_reverse(entry, break_point)
            target = data_preface() + column_a(entry[:break_point]) + column_b(
                entry[:break_point]) + column_definitions(definition)
            with open('content' + str(page_count) + '.html', 'a', encoding="utf-8") as newfile:
                newfile.write(target)
            counter += 1

        else:
            target = data_preface() + \
                column_a(entry[:first]) + \
                column_b(entry[:first]) + '<idx:infl>'
            i = 2
            while True:  # Handle the inflections
                previous_inflection = find_nth(entry, '|', i-1)
                next_inflection = find_nth(entry, '|', i)

                if next_inflection == -1:  # The last inflection + the definition
                    definition = rtl_reverse(entry, break_point)
                    target += column_inflections(entry[previous_inflection+1:break_point]) + \
                        '</idx:infl>' + column_definitions(definition)
                    with open(f'content{str(page_count)}.html', 'a', encoding="utf-8") as newfile:
                        newfile.write(target)
                    counter += 1
                    break

                elif find_nth(entry, '|', i) != -1:  # There are still inflections left
                    target += column_inflections(
                        entry[previous_inflection+1:next_inflection])
                    i += 1
    with open(f'content{str(page_count)}.html', 'a', encoding="utf-8") as newfile:
        newfile.write(content_end())

time_taken = str(time.time()-start_time)
print(f'Successfully created {page_count} files in {time_taken} seconds.')
