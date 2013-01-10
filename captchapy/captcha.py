# -*- coding: utf-8 -*-
#!/usr/bin/env python

__version__="1.2"

from subprocess import Popen, PIPE
from django.conf import settings

import Image
import ImageDraw
import ImageFont
import ImageFilter
import ImageColor
import random
import time
import hashlib
import os

MODPATH = os.path.abspath(os.path.dirname(__file__))

if not getattr(settings, 'CAPTCHA_CONF', False):
    settings.CAPTCHA_CONF = {}

CAPTCHA_CONF = {
                    'time_cache'   : settings.CAPTCHA_CONF.get('time_cache'    , 60),
                    'format_image' : settings.CAPTCHA_CONF.get('format_image'  , 'gif'),
                    'font'         : settings.CAPTCHA_CONF.get('font'          , 'ChildsPlay.ttf'),
                    'dir_font'     : settings.CAPTCHA_CONF.get('dir_font'      , MODPATH + "/media/fonts/"),
                    'text_size'    : settings.CAPTCHA_CONF.get('text_size'     , 45),
                    'dir_image_bg' : settings.CAPTCHA_CONF.get('dir_image_bg'  , MODPATH + "/media/images/"),
                    'image_bg'     : settings.CAPTCHA_CONF.get('image_bg'      , "bg.png"),
                    'noiselines'   : settings.CAPTCHA_CONF.get('noiselines'    , False),
                    'squiggly'     : settings.CAPTCHA_CONF.get('squiggly'      , False),
                    'btn_ok'       : settings.CAPTCHA_CONF.get('btn_ok'        , False),
                    'allowed'      : settings.CAPTCHA_CONF.get('allowed'       , "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                    'text_length'  : settings.CAPTCHA_CONF.get('text_length'   , 4),
                    'message_dig'  : settings.CAPTCHA_CONF.get('message_dig'   , u'Digite a palavra'),
                    'message_erro' : settings.CAPTCHA_CONF.get('message_erro'  , u'Palavra íncorreta'),
                }

class Captcha(object):
    def __init__(self, word, image):
        self.timestamp=time.time()
        self.word=word
        self.image=image
    def writeImage(self, local, outputstream, word):
        key   = hashlib.sha224(word.lower()).hexdigest()
        image = outputstream + key + '.' + CAPTCHA_CONF['format_image']
        self.urlimage = image
        self.image.save(local + image, format=CAPTCHA_CONF['format_image'])
        p = Popen( ('%s/daemon.sh' % MODPATH, '%s' % (local + image), '%s' % CAPTCHA_CONF['time_cache']), shell=True, stdout=PIPE, stderr=PIPE )
        p.communicate()
        return key
    def show(self):
        self.image.show()
    def age(self):
        return time.time()-self.timestamp
    def is_captcha(self, word, key):
        key2 = hashlib.sha224(word.lower()).hexdigest()
        if key == key2:
            return True
        return False

class CaptchaGen(object):
    
    def __init__(self, fontname, textcol_bright, textcol_dark, textsize=40, noiselines=False, bgpicture=None, squiggly=False):
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
        assert 4<=len(text)<=8
        letters=self.makeTextImage(text, self.squiggly)
        w,h=letters.size
        captchaw=w+self.lettersize[0]
        captchah=h+self.lettersize[1]/2
        if self.bgpicture:
            bg=self.bgpicture.copy()
            cx=random.randint(0,bg.size[0]-captchaw)
            cy=random.randint(0,bg.size[1]-captchah)
            bg=bg.crop((cx,cy,cx+captchaw,cy+captchah))
        else:
            bg=self.createBackground((captchaw, captchah))
        if self.noiselines:
            self.drawNoiseLines(bg)
        bg.paste(letters,(0+self.lettersize[0]/2,self.lettersize[1]/4),letters)
        bg=bg.convert("RGB")
        return Captcha(text, bg)

    def _makeTextImage(self, text, angle):
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
        splitpos=random.randint(2, len(text)-2)
        return text[0:splitpos], text[splitpos:]
    
    def createWord(self, length=6, allowed="cfkmpqrstvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"): 
        return "".join( [random.choice(allowed) for i in xrange(length)] )
    
    
class CaptchaForm(object):
    
    def __init__(self, p=None):
        cg   = CaptchaGen(CAPTCHA_CONF['dir_font'] + CAPTCHA_CONF['font'], (100,80,60), (60,40,30), textsize=CAPTCHA_CONF['text_size'], bgpicture=CAPTCHA_CONF['dir_image_bg'] + CAPTCHA_CONF['image_bg'], noiselines=CAPTCHA_CONF['noiselines'], squiggly=CAPTCHA_CONF['squiggly'])
        word = cg.createWord(length=CAPTCHA_CONF['text_length'], allowed=CAPTCHA_CONF['allowed'])
        c    = cg.generateCaptcha(word)
        
        self.c      = c
        self.key    = c.writeImage(MODPATH, '/media/tmp/', word)
        self.image  = c.urlimage
        self.hidden = '1'
        self.field  = '2'
        
        if p and p.get('hidden_captcha_1', False):
            self.hidden = p.get('hidden_captcha_1' , '')
            self.field  = p.get('field_captcha_1'  , '')
    
    def is_valid(self, verific=False):
        r = self.c.is_captcha(self.field, self.hidden)
        if not verific:
            try:
                os.remove(MODPATH + '/media/tmp/' + self.hidden + '.gif')
            except:
                return False
        return r
    
    def message(self):
        if self.field == '2':
            return u''
        elif not len(self.field) > 0:
            return CAPTCHA_CONF['message_dig']
        elif not self.is_valid(True):
            return CAPTCHA_CONF['message_erro']
        return u''
    
    def get_field(self):
        str      = u'<img class="image_captcha" src="/captcha%s" border="0" />' % (self.image,)
        str     += u'<input type="hidden" name="%s" value="%s" />' % ('hidden_captcha_1', self.key,)
        str     += u'<input class="field_captcha" type="text" name="%s" value="" size="10" />' % ('field_captcha_1',)
        if CAPTCHA_CONF['btn_ok']:
            str += u'<input class="btn_captcha" type="submit" name="OK" value="OK" />'
        
        return str
