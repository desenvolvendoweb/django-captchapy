"""Captcha image generator.

Draws images of random words in such a way that efficient computer based
recognition is highly difficult. These images can be used for example to validate
if form-posts are done by a honest human being, or by a computerized spambot.

This generator can use a background picture or generate its own background.
The output is a JPG image. The dimensions vary a bit depending on what size is
needed to draw all the letters in the specified word.
You have to supply a Truetype font (.ttf) that it will use to draw the letters.
Don't use a regular font such as Courier. Use handwriting-style fonts or similar,
for example (freely available at http://www.fontgirl.com):
  FGJaynePrint, AnkeCalligraph, ChildsPlay, FontOnAStick.
Adding a squiggly is recommended as it makes segmentation much harder.
Adding noiselines may make automatic recognition harder too, but sometimes it
renders the image unreadable for humans as well (which is not really nice).
Requires PIL for image manipulations (http://www.pythonware.com/products/pil/)

(c) Irmen de Jong - irmen@razorvine.net
Software License: MIT (http://www.opensource.org/licenses/mit-license.php)
I.e. use it freely, but include the above copyright notice and this license text.
Supplied as-is. No warranties.
"""

__version__="1.2"

import Image
import ImageDraw
import ImageFont
import ImageFilter
import ImageColor
import random
import time
import hashlib

def createWord(length=6, allowed="cfkmpqrstvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"):
    """create a random 'word' from a set of letters with high visual distinction, or any given set""" 
    return "".join( [random.choice(allowed) for i in xrange(length)] )

class Captcha(object):
    """A generated captcha image and some extra properties."""
    def __init__(self, word, image):
        self.timestamp=time.time()
        self.word=word
        self.image=image
    def writeImage(self, outputstream, word):
	key = hashlib.sha224(word.lower()).hexdigest()
        self.image.save(outputstream + key + '.jpg', format="jpeg")
	return key
    def show(self):
        self.image.show()
    def age(self):
        """returns the 'age' of the generated captcha image in seconds"""
        return time.time()-self.timestamp
    def is_captcha(self, word, key):
	key2 = hashlib.sha224(word.lower()).hexdigest()
	if key == key2:
	    return True
	return False

class CaptchaGen(object):
    """Generator of Captcha Images in JPG format.
    
    Can use any truetype font for the text, and can use a background picture or a self-generated background.
    This class is thread-safe."""
    
    def __init__(self, fontname, textcol_bright, textcol_dark, textsize=40, noiselines=False, bgpicture=None, squiggly=False):
        """create a captcha generator object.
        
        fontname - path to a .ttf font file
        textcol_bright - bright text color; (r,g,b) tuple or a PIL-compatible color string
        textcol_dark - dark text color; (r,g,b) tuple or a PIL-compatible color string
        textsize - font size 
        noiselines - wether to draw noise lines all over the image
        bgpicture - background picture to load. If not specified, a background is generated.
        squiggly - wether to draw a squiggly line through the text
        """
        self.font=ImageFont.truetype(fontname, textsize)
        self.lettersize=self.font.getsize('x')
        if type(textcol_bright)!=tuple:
            textcol_bright=ImageColor.getrgb(textcol_bright)
        if type(textcol_dark)!=tuple:
            textcol_dark=ImageColor.getrgb(textcol_dark)
        self.textcol_bright=textcol_bright
        self.textcol_dark=textcol_dark
        ar,ag,ab=self.textcol_bright
        self.textcol_avg=(ar+self.textcol_dark[0])/2, (ag+self.textcol_dark[1])/2, (ab+self.textcol_dark[2])/2
        self.noiselines=noiselines
        self.squiggly=squiggly
        if bgpicture:
            self.bgpicture=Image.open(bgpicture)
        else:
            self.bgpicture=None
            
    def generateCaptcha(self, text):
        """Generate a Captcha image with the given text drawn in it, in JPG format.
        Note that the text must be between 5 and 8 characters."""
        assert 4<=len(text)<=8
        letters=self.makeTextImage(text, self.squiggly)
        w,h=letters.size
        captchaw=w+self.lettersize[0]
        captchah=h+self.lettersize[1]/2
        if self.bgpicture:
            # crop a random area from the configured background picture
            bg=self.bgpicture.copy()
            cx=random.randint(0,bg.size[0]-captchaw)
            cy=random.randint(0,bg.size[1]-captchah)
            bg=bg.crop((cx,cy,cx+captchaw,cy+captchah))
        else:
            # generate a random background ourselves
            bg=self.createBackground((captchaw, captchah))
        if self.noiselines:
            self.drawNoiseLines(bg)
        bg.paste(letters,(0+self.lettersize[0]/2,self.lettersize[1]/4),letters)
        bg=bg.convert("RGB")
        return Captcha(text, bg)

    def _makeTextImage(self, text, angle):
        """create an image containing the given text tilted at the given angle"""
        (width,height)=self.font.getsize(text)
        width+=10
        height+=10
        letters=Image.new("RGBA",(width,height))
        draw=ImageDraw.Draw(letters)
        draw.text((5,5),text, font=self.font, fill=self.textcol_bright)
        draw.text((7,7),text, font=self.font, fill=self.textcol_bright)
        draw.text((6,6),text, font=self.font, fill=self.textcol_dark)
        letters=letters.rotate(angle, resample=Image.BILINEAR, expand=1)
        letters=letters.crop(letters.getbbox())
        return letters

    def makeTextImage(self, text, squiggly=False):
        """create an image containing the given text, slightly warped, with optional squiggly line"""
        text1, text2 = self.splitText(text)
        letters1=self._makeTextImage(text1, 20)
        letters2=self._makeTextImage(text2, -20)
        letters=Image.new("RGBA",(letters1.size[0]+letters2.size[0], max(letters1.size[1], letters2.size[1])))
        letters.paste(letters1,(0,0),letters1)
        letters.paste(letters2,(letters1.size[0],0),letters2)
        if squiggly:
            letters=self.drawSquiggly(letters)
        letters=letters.filter(ImageFilter.SMOOTH)
        return letters
    
    def drawSquiggly(self, image):
        target=Image.new("RGBA",(image.size[0]+self.lettersize[0],image.size[1]))
        target.paste(image,(self.lettersize[0]/2,0))
        draw=ImageDraw.Draw(target)
        linecoords=[]
        stepsize=10
        y=target.size[1]/2
        for i in xrange(0,target.size[0]+stepsize,stepsize):
            linecoords.append((i,y+random.randint(-8,8)))
        draw.line(linecoords, fill=self.textcol_dark, width=2)
        linecoords=[(x+1,y+1) for x,y in linecoords]
        draw.line(linecoords, fill=self.textcol_dark)
        return target

    def drawNoiseLines(self, image, count=10):
        """add random noise lines to the image"""
        draw=ImageDraw.Draw(image)
        iw,ih=image.size
        for i in xrange(count):
            x,y=random.randint(0,iw-30),random.randint(0,ih-4)
            w,h=random.randint(-40,40),random.randint(-40,40)
            if self.bgpicture:
                draw.line( (x,y,x+w,y+h), fill=self.textcol_avg, width=2)
            else:
                r,g,b=image.getpixel((x,y))
                draw.line( (x,y,x+w,y+h), fill=(255-r,255-g,255-b), width=2)

    def createBackground(self, size):
        """if no background picture is used, a random background is created.
        The colors used are based on the negatives of the text colors."""
        lr,lg,lb=self.textcol_bright
        lr,lg,lb=255-lr,255-lg,255-lb
        dr,dg,db=self.textcol_dark
        dr,dg,db=255-dr,255-dg,255-db
        bg=Image.new("RGB",size, color=(dr,dg,db))
        draw=ImageDraw.Draw(bg)
        def circles(minsize,maxsize):
            spread=50
            for i in xrange(60):
                f_r=lr+random.randint(-spread,spread)
                f_g=lg+random.randint(-spread,spread)
                f_b=lb+random.randint(-spread,spread)
                o_r=dr+random.randint(-spread,spread)
                o_g=dg+random.randint(-spread,spread)
                o_b=db+random.randint(-spread,spread)
                x,y=random.randint(-20,size[0]), random.randint(-20,size[1])
                w,h=random.randint(minsize,maxsize), random.randint(minsize,maxsize)
                draw.ellipse((x,y,x+w,y+h), fill=(f_r,f_g,f_b), outline=(o_r,o_g,o_b))
        circles(20,80)
        circles(3,16)
        bg=bg.filter(ImageFilter.BLUR)
        bg=bg.filter(ImageFilter.SHARPEN)
        if self.noiselines:
            self.drawNoiseLines(bg, count=50)
        bg=bg.filter(ImageFilter.SMOOTH)
        return bg
        
    def splitText(self, text):
        """split the text in two pieces that will be drawn separately"""
        splitpos=random.randint(2, len(text)-2)
        return text[0:splitpos], text[splitpos:]


if __name__=="__main__":
    cg = CaptchaGen("media/fonts/ChildsPlay.ttf", (100,80,60), (60,40,30), textsize=45, bgpicture="media/images/bg.png", noiselines=False, squiggly=False)
    word=createWord(length=4, allowed="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print word
    c=cg.generateCaptcha(word)
    print c.writeImage('media/tmp/', word)
    print c.is_captcha('ZHjm', '57d43494472b403520e62893dff463f517c18a1b3cf20b293f42e7f1')
