from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import re
import os


class Buscar_cartaz:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--lang=pt-BR')
        chrome_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe', options=chrome_options)

        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException]
        )
        # Pode adicionar vários sites para fazer busca não só de cartazes de filme
        self.site = ['https://www.ingresso.com/home']

    def _iniciar(self):
        self.pegando_nome_dos_cartazes()
        self.buscando_por_cartaz(self.coletar_nome)

    def pegando_nome_dos_cartazes(self):
        # Nome dos filmes ou podemos fazer uma busca especifica em alguns sites
        self.coletar_nome = ['Viuva Negra', 'Homem de Ferro']
            

    def buscando_por_cartaz(self, nomes_imagens):
        self.driver.get(self.site[0])
        time.sleep(4)
        for nome_imagem in nomes_imagens:
            icon_busca = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="header"]/div[1]/div/div[2]/div[1]/a')
                )
            )
            icon_busca.click()
            campo_busca = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="hd-search-cont"]//input')
                )
            )
            campo_busca.click()            
            campo_busca.send_keys(nome_imagem)
            time.sleep(4)
            # Vai selecionar o primeiro elemento do input de busca
            campo_busca.send_keys(Keys.DOWN)
            # Depois vai dar enter
            campo_busca.send_keys(Keys.ENTER)
            
            # Pegando a classe onde contém a url da imagem
            cartaz_filme = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                    '//img[@class="pb-avatar-image akamai-img-manager"]')
                )
            )
            #localizando url da imagem
            print(cartaz_filme.get_attribute("src"))
            url_imagem = cartaz_filme.get_attribute("src")
            self.tratando_nome(nome_imagem)
            self.baixar_arquivo(url_imagem, self.nome_tratado)
        self.driver.quit()
    def tratando_nome(self, nome_sem_tratamento):
        tratando_nome = re.sub('[^a-zA-Z0-9 \n\.]', '', nome_sem_tratamento)
        tratando_nome = tratando_nome.split()
        tratando_nome = "-".join(tratando_nome).lower()
        self.nome_tratado = tratando_nome
        
        
    def baixar_arquivo(self, url, nome_imagem):
        with open(f'C:{os.sep}Workspace{os.sep}imagens{os.sep}cartazes/{nome_imagem+".jpg"}', 'wb') as imagem:
            resposta = requests.get(url, stream=True)

            if not resposta.ok:
                print("Ocorreu um erro, status:", resposta.status_code)
            else:
                for dado in resposta.iter_content(1024):
                    if not dado:
                        break

                    imagem.write(dado)

                print("Imagem salva! =)")


site = Buscar_cartaz()
site._iniciar()
