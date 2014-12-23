Description
=============



This script is a handy utility that generates bitmap font sheets from TrueType fonts. The script makes use of imagemagick,
so you need to have imagemagick installed in order to use it.

Usage
=============

Given the following command("/Library/Fonts/Comic\ Sans\ MS.ttf" is where the font Comic Sans can be located on my system):

```
python font_sheet.py /Library/Fonts/Comic\ Sans\ MS.ttf out.png
```

the script produces a font sheet named out.png: 

![text](/images/out.png)


As can be seen, the sheet has been properly padded so that its sizes are powers of two, so that it can efficiently be used in for example games(in this case, a 1024x1024 texture is created). Also, the characters are ordered after ASCII. 

