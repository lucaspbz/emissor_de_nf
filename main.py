import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from captcha_decoder import decode_image


class Emissor():
    browser: webdriver.Chrome
    def __init__(self) -> None:
        load_dotenv()
        pass

    def find_element_by_xpath(self, xpath:str):
        return self.browser.find_element(By.XPATH ,xpath)

    def emit(self):
        cpf = os.getenv("CPF")
        if cpf is None:
            cpf = input("Digite o CPF sem pontos ou espaços: \n")

        senha = os.getenv("PASS")
        if senha is None:
            senha = input("Digite sua senha: \n")

        cnpj = os.getenv("CNPJ")
        if cnpj is None:
            cnpj = input("Digite o CNPJ do tomador de servico, sem espacos, pontos ou barra: \n")

        descricao = os.getenv("SERVICE_DESCRIPTION")
        if descricao is None:
            descricao = input("Digite a descricao do servico: \n")

        valor_da_nota = os.getenv("VALOR_DA_NOTA")
        if valor_da_nota is None:
            valor_da_nota = input("Digite o valor da nota. Digite '10000' para R$100,00: \n")

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        service = Service(executable_path='./bin/chromedriver')

        # Abrir o navegador
        self.browser = webdriver.Chrome(service=service, options=chrome_options)

        # Navegar para site correto
        self.browser.get("https://iss.fortaleza.ce.gov.br/")

        # Preencher campos e resolver captcha
        while True:
            try:
                cpfField = self.find_element_by_xpath('//*[@id="login:username"]')
                cpfField.send_keys(cpf)
                self.find_element_by_xpath(
                    '//*[@id="login:password"]').send_keys(senha)

                with open('captcha.png', 'wb') as file:
                    img = self.find_element_by_xpath(
                        '//*[@id="login:captchaDecor"]/img')
                    file.write(img.screenshot_as_png)

                decoded_image = decode_image('captcha.png')

                self.find_element_by_xpath(
                    '//*[@id="login:captchaDecor:captchaLogin"]'
                ).send_keys(decoded_image)

                self.find_element_by_xpath(
                    '//*[@id="login:botaoEntrar"]'
                ).click()
                break
            except Exception as ex:
                if "APIKEY do serviço de captcha não encontrada." in str(ex):
                    self.browser.close()
                    raise ex
                continue


        # Navegar para emissão de nota
        while True:
            try:
                self.find_element_by_xpath("/html/body/div[1]/div[2]/form/div/div[2]/div[1]/a/i").click()
                break
            except Exception:
                continue


        # Altera o tipo do tomador para buscar por CNPJ
        while True:
            try:
                self.find_element_by_xpath('//*[@id="emitirnfseForm:tipoPesquisaTomadorRb:1"]').click()
                break
            except Exception:
                continue

        while True:
            try:
                # Busca pelo CNPJ
                self.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]'
                ).clear()
                self.find_element_by_xpath('/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]').send_keys(
                    cnpj
                )
                break

            except Exception:
                continue

        while True:
            try:
                # Aguarda aparecer a empresa e clicca
                self.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr[1]/td[2]"
                ).click()
                break

            except Exception:
                continue

        while True:
            try:
                element = self.find_element_by_xpath('//*[@id="emitirnfseForm:idNome"]')
                if element.get_attribute("value") != "":
                    break
            except Exception:
                continue

        # Muda para aba de Serviço
        self.find_element_by_xpath(
            '//*[@id="emitirnfseForm:abaServico_lbl"]').click()

        while True:
            try:
                # Seleciona a descrição CNAE
                self.find_element_by_xpath(
                    "/html/body/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/div[5]/div[1]/select/option[2]"
                ).click()
                break
            except Exception:
                continue


        self.find_element_by_xpath('//*[@id="emitirnfseForm:idDescricaoServico"]').send_keys(
            descricao
        )

        self.find_element_by_xpath(
            '//*[@id="emitirnfseForm:idValorServicoPrestado"]'
        ).send_keys(valor_da_nota)

        self.find_element_by_xpath('//*[@id="emitirnfseForm:btnCalcular"]').click()

emissor = Emissor()
emissor.emit()
