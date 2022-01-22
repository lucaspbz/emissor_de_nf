import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from captcha_decoder import Captcha_decoder


class Emissor():
    browser: webdriver.Chrome
    debug: bool

    cpf:str
    senha:str
    cnpj:str
    descricao:str
    valor_da_nota:str

    def __init__(self) -> None:
        load_dotenv()
        self.debug = os.getenv("DEBUG")=="true"
        self.cpf = os.getenv("CPF")
        if self.cpf is None:
            self.cpf = input("Digite o CPF sem pontos ou espaços: \n")

        self.senha = os.getenv("PASS")
        if self.senha is None:
            self.senha = input("Digite sua senha: \n")

        self.cnpj = os.getenv("CNPJ")
        if self.cnpj is None:
            self.cnpj = input("Digite o CNPJ do tomador de servico, sem espacos, pontos ou barra: \n")

        self.descricao = os.getenv("SERVICE_DESCRIPTION")
        if self.descricao is None:
            self.descricao = input("Digite a descricao do servico: \n")

        self.valor_da_nota = os.getenv("VALOR_DA_NOTA")
        if self.valor_da_nota is None:
            self.valor_da_nota = input("Digite o valor da nota. Digite '10000' para R$100,00: \n")
        pass


    def find_by_xpath(self, xpath:str):
        return self.browser.find_element(By.XPATH ,xpath)


    def emit(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        service = Service(executable_path='./bin/chromedriver')

        # Abrir o navegador
        self.browser = webdriver.Chrome(service=service, options=chrome_options)

        # Navegar para site correto
        self.browser.get("https://iss.fortaleza.ce.gov.br/")


        # Preencher campos e resolver captcha
        self._step(self._step_1)


        # Navegar para emissão de nota
        self._step(lambda: self.find_by_xpath("/html/body/div[1]/div[2]/form/div/div[2]/div[1]/a/i").click())


        # Altera o tipo do tomador para buscar por CNPJ
        self._step(lambda: self.find_by_xpath('//*[@id="emitirnfseForm:tipoPesquisaTomadorRb:1"]').click())


        # Busca pelo CNPJ
        self._step(self.step_4)


        # Aguarda aparecer a empresa e clicca
        self._step(lambda: self.find_by_xpath("/html/body/div[1]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr[1]/td[2]").click())


        self._step(self.step_6)


        # Muda para aba de Serviço
        self.find_by_xpath('//*[@id="emitirnfseForm:abaServico_lbl"]').click()


        # Seleciona a descrição CNAE
        self._step(lambda: self.find_by_xpath("/html/body/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/div[5]/div[1]/select/option[2]").click())


        self.find_by_xpath('//*[@id="emitirnfseForm:idDescricaoServico"]').send_keys(self.descricao)


        self.find_by_xpath('//*[@id="emitirnfseForm:idValorServicoPrestado"]').send_keys(self.valor_da_nota)


        self.find_by_xpath('//*[@id="emitirnfseForm:btnCalcular"]').click()


    def step_6(self):
        element = self.find_by_xpath('//*[@id="emitirnfseForm:idNome"]')
        if element.get_attribute("value") == "":
            raise Exception()


    def step_4(self):
        self.find_by_xpath(
                    '/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]'
                ).clear()
        self.find_by_xpath('/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]').send_keys(
                    self.cnpj
                )


    def _step_1(self):
        cpfField = self.find_by_xpath('//*[@id="login:username"]')
        cpfField.send_keys(self.cpf)
        self.find_by_xpath(
                    '//*[@id="login:password"]').send_keys(self.senha)

        with open('captcha.png', 'wb') as file:
            img = self.find_by_xpath(
                        '//*[@id="login:captchaDecor"]/img')
            file.write(img.screenshot_as_png)
        client_key = os.getenv("API_KEY")

        if client_key is not None:
            image_decoder = Captcha_decoder(client_key, self.debug)
            decoded_image = image_decoder.decode('captcha.png')
                    
            self.find_by_xpath('//*[@id="login:captchaDecor:captchaLogin"]').send_keys(decoded_image)

            self.find_by_xpath('//*[@id="login:botaoEntrar"]').click()
        else:
            print("APIKEY não encontrada. Preencha o captcha manualmente")


    def _step(self, cb):
        while True:
            try:
                cb()
                break
            except Exception as ex:
                if self.debug:
                    print(ex)
                continue

emissor = Emissor()
emissor.emit()
