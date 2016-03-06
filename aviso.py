# PyNorte - Gerador de Avisos
#
# Para mudar a data e o horário, modifique os valores da variável hangout.
# Você pode usar a seu fuso horário para escolher o horário e assim evitar erros.
#
# Autor: Nilo Menezes (2016)
# Dependências:
# Instalar Pillow e pytz
#

from PIL import Image, ImageDraw, ImageFont
import pytz
import datetime

castanhas = Image.open("fundo.jpg")
logo = Image.open("logo.png")

LOGO_PEQUENO = (150, 150)
AVISO_TAMANHO = (450, 500)
# Parte a retirar da imagem de fundo (castanhas)
TAMANHO_CROP = AVISO_TAMANHO
POSICAO_DO_CROP = (100, 100)
FONTE_LOGO = 'Pillow/Tests/fonts/FreeMono.ttf'
# Fonte do Ubuntu
FONTE_TEXTO = 'UbuntuMono-B.ttf'
TAMANHO_GRANDE = 40
TAMANHO_PEQUENO = 24

# Horários
bruxelas = pytz.timezone("Europe/Brussels")
manaus = pytz.timezone("America/Manaus")
belem = pytz.timezone("America/Belem")
rio_branco = pytz.timezone("America/Rio_Branco")
hangout = bruxelas.localize(datetime.datetime(day=2, month=4, year=2016,
                                              hour=19, minute=0))

# Posicoes relativas - calculadas
FUNDO_CROP = (POSICAO_DO_CROP[0], POSICAO_DO_CROP[1],
              POSICAO_DO_CROP[0] + TAMANHO_CROP[0], POSICAO_DO_CROP[1] + TAMANHO_CROP[1])
POSICAO_PASTE = (0, 0, AVISO_TAMANHO[0], AVISO_TAMANHO[1])
FUSAO_FUNDO_MASCARA = 0.8  # 50%
# Cores
BRANCO = (255, 255, 255, 0)
VERDE = (0, 100, 0, 255)
COR_DO_TEXTO = (255, 255, 255, 255)


def escreve_centralizado(texto, largura, linha, draw, fonte, cor=COR_DO_TEXTO):
    s = (largura - draw.textsize(texto, font=fonte)[0]) / 2
    draw.text((s, linha), texto, font=fonte, fill=cor)

# Cria nova imagem com fundo branco
aviso = Image.new("RGBA", AVISO_TAMANHO, BRANCO)
# Cria imagem verde para fazer fusao
fundo = Image.new("RGBA", AVISO_TAMANHO, VERDE)
# Recorta um pedaco da imagem de fundo (castanhas)
pc = castanhas.crop(FUNDO_CROP)
# Cola o pedacao do fundo no aviso
aviso.paste(pc, POSICAO_PASTE)
# Fusiona o fundo do aviso com a imagem verde a 50%
aviso = Image.blend(aviso, fundo, FUSAO_FUNDO_MASCARA)
# Prepara para escrever
lapis = ImageDraw.Draw(aviso, mode="RGBA")
fGrande = ImageFont.truetype(FONTE_LOGO, TAMANHO_GRANDE)
fPequena = ImageFont.truetype(FONTE_TEXTO, TAMANHO_PEQUENO)

escreve_centralizado("PyNorte", AVISO_TAMANHO[0], 160, lapis, fGrande)
lapis.text((20, 210), ">> Terceiro Hangout", font=fPequena, fill=COR_DO_TEXTO)
lapis.text((20, 250), ">> Data: {0.day:02d}/{0.month:02d}/{0.year}".format(
           hangout.astimezone(manaus)),
           font=fPequena, fill=COR_DO_TEXTO)
lapis.text((20, 290), ">> Horário:", font=fPequena, fill=COR_DO_TEXTO)
lapis.text((20, 330), "{0.hour:02d}h Rio Branco".format(
           hangout.astimezone(rio_branco)),
           font=fPequena, fill=COR_DO_TEXTO)
lapis.text((20, 360), "{0.hour:02d}h Manaus, Boa Vista, Porto Velho".format(hangout.astimezone(manaus)),
           font=fPequena, fill=COR_DO_TEXTO)
lapis.text((20, 390), "{0.hour:02d}h Belém, Palmas, Macapá".format(hangout.astimezone(belem)),
           font=fPequena, fill=COR_DO_TEXTO)

del lapis
# Cria mascara branca para inverter a cor do logo
branco = Image.new("RGBA", LOGO_PEQUENO, (255, 255, 255, 255))
minilogo = logo.resize(LOGO_PEQUENO, Image.LANCZOS)
aviso.paste(branco, ((AVISO_TAMANHO[0] - LOGO_PEQUENO[0])//2, 25), minilogo)

# Grava imagem final
aviso.save("aviso.png")

