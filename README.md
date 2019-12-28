# StegoPdf
Hide anything inside any PDF-file! (work in progress)

To be honest, your files will be not really "hidden". The script appends files as raw bytes at the end of any PDF. PDF-Readers ignore these part and dont "see" them.

## Usage
Hiding files inside a PDF:
```
stego.py --put <PDF-File> <file to hide> [<file to hide>, ...]

Example:
stego.py --put Serious_Research_Paper.pdf Super_Secret_Zip.zip Super_Dangerous_Trojan.exe
```

Getting files back:
```
stego.py --get <PDF-File>

Example:
stego.py --get Serious_Research_Paper.pdf
```

## What i want to add
- encryption
- really hiding files into pdf structure ( need to do tons of research about pdf standards )
