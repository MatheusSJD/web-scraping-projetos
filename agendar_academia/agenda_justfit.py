from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import os


class Agendar_academia:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--lang=pt-BR')
        chrome_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            executable_path=os.getcwd() + os.sep + 'chromedriver.exe')

        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException]
        )

    def _iniciar(self):
        self.driver.get(
            f'https://fale.justfit.com.br/agenda/login')
        self.login('SEU CPF', 'SUA DATA DE NASCIMENTO')
        self.aceitar_termos()
        self.questionario_sobre_sintomas_do_covid()
        self.agendamento()

    def login(self, cpf, data_nascimento):
        try:
            # Pegando o campo de cpf
            campo_cpf = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//form/input[@placeholder="Digite seu CPF"]')
                )
            )
            # Pegando o campo de data de nascimento
            campo_data_nascimento = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '//form/input[@placeholder="Sua data de nascimento"]')
                )
            )
            # Preencher CPF
            campo_cpf.click()
            campo_cpf.send_keys(cpf)
            # Preencher data de nascimento
            campo_data_nascimento.click()
            campo_data_nascimento.send_keys(data_nascimento, Keys.ENTER)
        except Exception as erro:
            print(
                '\nCampo de preenchimento não encontrado!\nTente novamente mais tarde!\n')
            self.driver.quit()

    def aceitar_termos(self):
        try:
            botao_de_termos_de_condicao = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@type="button"]')
                )
            )
            botao_de_termos_de_condicao.click()
        except Exception as erro:
            print('\nTermos não encontrado!\n')
            self.driver.quit()

    def questionario_sobre_sintomas_do_covid(self):
        try:
            selecionando_radios = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="vx-radio-con undefined vx-radio-success"]/input')
                )
            )

            for radio in selecionando_radios:
                radio.click()

            time.sleep(2)

            botao_continuar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@type="button"]')
                )
            )

            botao_continuar.click()

        except Exception as erro:
            print('\nCampos não encontrando!\n')
            self.driver.quit()

    def agendamento(self):
        botao_horario = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@title="20:30 – 22:00: AGENDA DO DIA"]')
            )
        )
        botao_horario.click()

        marcar = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@class="btn btn-warning"]')
            )
        )
        fechar_modal = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="close-icon cursor-pointer"]')
            )
        )
        
        time.sleep(2)
        try:
            # btn btn-warning - desmarcar
            if marcar.get_attribute("class") == "btn btn-warning":
                fechar_modal.click()
                self.driver.quit()
                pyautogui.alert(text="Seu horário já esta marcado!", title="Agenda Academia", button="Ok")

            # btn btn-#c9d200 - Marcar
            else:
                botao_horario.click()
                marcar.click()
                fechar_modal.click()
                self.driver.quit()
                pyautogui.alert(text="Agendamento feito com sucesso!", title="Agenda Academia", button="Ok")

        except Exception as erro:
            print('Falha ao encotrar o elemento')
            self.driver.quit()
        
        


site = Agendar_academia()
site._iniciar()
