from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import os
import random

class Telegram_bot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--lang=pt-BR')
        chrome_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            executable_path=os.getcwd() + os.sep + 'chromedriver.exe')
        
        TOKEN = "" #Token
        self.url_base = f'https://api.telegram.org/bot{TOKEN}/'

    def iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            print(atualizacao)
            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    print(update_id)
                    chat_id = mensagem['message']['from']['id']
                    print(chat_id)
                    primeira_mensagem = mensagem['message']['message_id'] == 1
                    print(primeira_mensagem)
                    resposta = self.criar_resposta(mensagem, primeira_mensagem)

                    self.responder(resposta, chat_id)
    
    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def criar_resposta(self, mensagem, primeira_mensagem):
        try:
            mensagem = mensagem['message']['text']
            self.driver.get(
                f'https://www.google.com/search?q={mensagem}')
            if primeira_mensagem == True or mensagem:
                try:
                    nome_acao = self.driver.find_element_by_xpath('//div[@class="E65Bx"]')
                    preco = self.driver.find_element_by_xpath('//span[@jscontroller="q6ctOd"]')
                    return f"Empresa: {nome_acao.text}\nPreço: {preco.text}"
                except:
                    aleatorio = self.driver.find_element_by_xpath('//h3[@class="LC20lb DKV0Md"]')
                    return f"Não encontrei essa ação. :/\nSó achei isso: {aleatorio.text}"
                else:
                    return f"Não encontrei essa ação. :/"
        except:
            numero = random.randint(0, 4)
            respostas = ['Mas rapaz que isso eim', 'Pesquisa por ações', 
                        'HAHA o que você mandou ai eim ? ', 'Me tira daqui. Estou preso aquiiiiii',
                        'Investir é bom né']
            return f"{respostas[numero]} "
        
    def responder(self, resposta, chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)
        
bot = Telegram_bot()
bot.iniciar()