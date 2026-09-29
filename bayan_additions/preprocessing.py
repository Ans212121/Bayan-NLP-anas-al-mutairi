"""New explicit profiles. Rerun models before attributing old results to them."""
import html
import re
import unicodedata
VERSION = 'bayan-protected/1.1.0'
EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
PHONE = re.compile(r'(?<!\d)(?:\+?966|00966|0)?5\d{8}(?!\d)')
DIACRITICS = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]')
def prepare(text, profile='protected'):
    if not isinstance(text,str): raise TypeError('text must be a string')
    if profile not in {'protected','arabic-search','english-search'}: raise ValueError('unknown profile')
    clean=unicodedata.normalize('NFC',html.unescape(text))
    # Preserve redaction markers on repeated preprocessing.
    clean=re.sub(r'<(?!EMAIL>|PHONE>)[^>]+>',' ',clean)
    clean=EMAIL.sub('<EMAIL>',clean)
    clean=PHONE.sub('<PHONE>',clean).replace('\u0640','')
    if profile=='arabic-search':
        clean=DIACRITICS.sub('',clean)
        clean=re.sub('[إأآٱ]','ا',clean).replace('ى','ي')
    return ' '.join(clean.split())
