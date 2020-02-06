#https://www.qbit.it/lab/bintext.php
bins = []

file = open('./water_message.txt')
bins = [*file]
bins = [byte.strip() for byte in bins]
print(bins)
file.close()

message = '�MH�iH�nH�eH� H�yH�oH�uH�rH� H�cH�oH�iH�nH� H�iH�nH� H�rH�oH�oH�mH� H�2H�0H�7H'
message = message.replace('�','').replace('H','')
print(message)


