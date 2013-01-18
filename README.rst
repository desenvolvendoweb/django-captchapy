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

5º urlpatterns  = patterns('',
    url(r'^captcha/'  , include('captchapy.urls')),
    ...
)

Fim. Fácil né?

Modo avançado

6º settings.py:
    CAPTCHA_CONF = {
        Tempo para limpar o cache

	'time_cache'   : 60),
        Tipo de imagem gerada, gif, jpeg, png

        'format_image' : 'gif'),

        'font'         : 'ChildsPlay.ttf'), # Tipo de fonte, se precisar de outras fontes é só mudar o dir_font e adicionar a fonte desejada

        'dir_font'     : "/media/fonts/"), # Diretorio das fontes

        Tamanho da fonte

        'text_size'    : 45),

        Diretorio onde se encontra as images de fundo

        'dir_image_bg' : "/media/images/"),

        Nome da imagem de fundo em seu diretorio personalizado

        'image_bg'     : "bg.png"),

        Linhas que desfocam o texto sobre o imagem de fundo

        'noiselines'   : False),

        Linhas que desfocam a imagem de fundo

        'squiggly'     : False),

        Botão de ok ao lado o campo input de texto

        'btn_ok'       : False),

        Caracteres disponiveis para sorteio

        'allowed'      : "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),

        Numero de letras dentro da imagem

        'text_length'  : 4),

        Mensagem amigavel para digitar a palavra

        'message_dig'  : u'Digite a palavra'),

        Mensagem amigavel para informar que a palavra está incorreta

        'message_erro' : u'Palavra íncorreta'),
    }

Bom pessoal, é isso.
