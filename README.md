django-captchapy
================

Aplicação captcha para django python

Uso extremamente simples:

1º comandos no console:

    pip install git+https://github.com/desenvolvendoweb/django-captchapy.git

2º settings.py:

    INSTALLED_APPS = (
    	...
    	'captchapy',
    )

3º views.py:

    from captchapy.captcha import CaptchaForm
    human = False
    if request.POST:
        form = CaptchaForm(request.POST)
        if form.is_valid():
            human = True
    else:
        form = CaptchaForm()
    p['captcha'] = form
    p['human']   = human

4º template.html:

    {% if captcha.message %}
    	<div class="captcha_message">{{ captcha.message }}</div>
    {% endif %}
    <div class="captcha">{{ captcha.get_field|safe }}</div>

5º urls.py:

    urlpatterns = patterns('',
        url(r'^captcha/'  , include('captchapy.urls')),
        ...
    )

Fim. Fácil né?

Caso estiver usando sistema operacional Ubuntu 32 bits, instalar os motores de requisitos minimos:

    sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
    sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib
    sudo ln -s /usr/lib/i386-linux-gnu/libfreetype.so /usr/lib
    sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib
    pip install Pillow

Caso estiver usando sistema operacional Ubuntu 64 bits, instalar os motores de requisitos minimos:

    sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
    pip install Pillow

Modo avançado

6º settings.py:

    CAPTCHA_CONF = {
    	('time_cache'   : 60), # Tempo para limpar o cache
        ('format_image' : 'gif'), # Tipo de imagem gerada, gif, jpeg, png
        ('font'         : 'ChildsPlay.ttf'), # Tipo de fonte, se precisar de outras fontes é só mudar o dir_font e adicionar a fonte desejada
        ('dir_font'     : "/media/fonts/"), # Diretorio das fontes
        ('text_size'    : 45), # Tamanho da fonte
        ('dir_image_bg' : "/media/images/"), # Diretorio onde se encontra as images de fundo
        ('image_bg'     : "bg.png"), # Nome da imagem de fundo em seu diretorio personalizado
        ('noiselines'   : False), # Linhas que desfocam o texto sobre o imagem de fundo
        ('squiggly'     : False), # Linhas que desfocam a imagem de fundo
        ('btn_ok'       : False), # Botão de ok ao lado o campo input de texto
        ('allowed'      : "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), # Caracteres disponiveis para sorteio
        ('text_length'  : 4), # Numero de letras dentro da imagem
        ('message_dig'  : u'Digite a palavra'), # Mensagem amigavel para digitar a palavra
        ('message_erro' : u'Palavra íncorreta'), # Mensagem amigavel para informar que a palavra está incorreta
    }

Bom pessoal, é isso.
