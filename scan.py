import easyocr
reader = easyocr.Reader(['en','th'])
result = reader.readtext('1.jpg' , detail = 0)
print(result)