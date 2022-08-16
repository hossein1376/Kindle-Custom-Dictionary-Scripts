# This is an .opf file making script with input from the user

def opf_top(dic_name, author_name, in_lang, out_lang):
    infos = '''<?xml version="1.0"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">
  <metadata>
    <dc:title>''' + dic_name + '''</dc:title>
    <dc:creator opf:role="aut">''' + author_name + '''</dc:creator>
    <dc:language>''' + in_lang + '''</dc:language>
    <meta name="cover" content="my-cover-image"/>
    <x-metadata>
      <DictionaryInLanguage>''' + in_lang + '''</DictionaryInLanguage>
      <DictionaryOutLanguage>''' + out_lang + '''</DictionaryOutLanguage>
      <DefaultLookupIndex>default</DefaultLookupIndex>
    </x-metadata>
  </metadata>
  <manifest>'''
    return infos


def manifest(n):
    text = '     <item id="content' + str(n) + '" href="content' + str(n) + '.html" media-type="application/xhtml+xml"/>\n'
    return text


def spine(n):
    text = '    <itemref idref="content' + str(n) + '"/>\n'
    return text


def guide(n):
    text = '     <reference type="index" title="IndexName" href="content' + str(n) + '.html"/>\n'
    return text


print("Enter the number of created content.html files:")
page_count = int(input())
print('Enter the Dictinory name:')
dic_name = input()
print("Enter the Author's name:")
author_name = input()
print('Enter the input language code based on the ISO 639-1 codes (example en-US):')
in_lang = input()
print('Enter the output language code based on the ISO 639-1 codes (example en-US):')
out_lang = input()

opf = opf_top(dic_name, author_name, in_lang, out_lang) + '\n'

for i in range(page_count):
    opf += manifest(i+1)

opf += '''  </manifest>
  <spine>\n'''

for i in range(page_count):
    opf += spine(i+1)

opf += '''  </spine>
  <guide>\n'''

for i in range(page_count):
    opf += guide(i+1)

opf += '''  </guide>
</package>'''

with open(dic_name + '.opf', 'w', encoding="utf-8") as file:
    file.write(opf)
print(f'Successfully created the {dic_name}.opf file.')