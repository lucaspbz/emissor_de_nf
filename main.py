import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from captcha_decoder import decode_image

load_dotenv()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# Abrir o navegador e preencher dados para login
browser = webdriver.Chrome(executable_path='./bin/chromedriver', chrome_options=chrome_options)

cpf = os.getenv("CPF")
senha = os.getenv("PASS")
cnpj = os.getenv("CNPJ")
descricao = os.getenv("SERVICE_DESCRIPTION")
valor_da_nota = os.getenv("VALOR_DA_NOTA")

browser.get("https://iss.fortaleza.ce.gov.br/")

while True:
    try:
        cpfField = browser.find_element_by_xpath('//*[@id="login:username"]')
        cpfField.send_keys(cpf)
        browser.find_element_by_xpath(
            '//*[@id="login:password"]').send_keys(senha)

        with open('captcha.png', 'wb') as file:
            img = browser.find_element_by_xpath(
                '//*[@id="login:captchaDecor"]/img')

            src = img.get_attribute('src')
            file.write(img.screenshot_as_png)

        decoded_image = decode_image('captcha.png')

        browser.find_element_by_xpath(
            '//*[@id="login:captchaDecor:captchaLogin"]'
        ).send_keys(decoded_image)

        browser.find_element_by_xpath(
            '//*[@id="login:botaoEntrar"]'
        ).click()
        break
    except Exception as ex:
        print(str(ex))
        continue


# Navegar para emissão de nota

while True:
    try:
        browser.find_element_by_xpath(
            "/html/body/div[1]/div[2]/form/div/div[2]/div[1]/a/i"
        ).click()
        break
    except Exception:
        continue


# Altera o tipo do tomador para buscar por CNPJ
while True:
    try:
        browser.find_element_by_xpath(
            '//*[@id="emitirnfseForm:tipoPesquisaTomadorRb:1"]'
        ).click()
        break
    except Exception:
        continue

while True:
    try:
        # Busca pelo CNPJ
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]'
        ).clear()
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/form/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td/div[1]/div[3]/span/div/input[1]').send_keys(
            cnpj
        )
        break

    except Exception:
        continue

while True:
    try:
        # Aguarda aparecer a empresa e clicca
        browser.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr[1]/td[2]"
        ).click()
        break

    except Exception:
        continue

while True:
    try:
         element = browser.find_element_by_xpath('//*[@id="emitirnfseForm:idNome"]')
         if element.get_attribute("value") != "":
             break
    except Exception:
        continue

# Muda para aba de Serviço
browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:abaServico_lbl"]').click()

while True:
    try:
        # Seleciona a descrição CNAE
        browser.find_element_by_xpath(
            "/html/body/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/div[5]/div[1]/select/option[2]"
        ).click()
        break
    except Exception:
        continue


browser.find_element_by_xpath('//*[@id="emitirnfseForm:idDescricaoServico"]').send_keys(
    descricao
)

browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:idValorServicoPrestado"]'
).send_keys(valor_da_nota)

browser.find_element_by_xpath('//*[@id="emitirnfseForm:btnCalcular"]').click()
