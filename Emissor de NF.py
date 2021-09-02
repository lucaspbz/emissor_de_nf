#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
from dotenv import load_dotenv

from selenium import webdriver


load_dotenv()
# Abrir o navegador e preencher dados para login

browser = webdriver.Firefox()

cpf = os.getenv('CPF')
senha = os.getenv('PASS')
cnpj = os.getenv('CNPJ')
descricao = os.getenv('SERVICE_DESCRIPTION')
valor_da_nota = os.getenv('VALOR_DA_NOTA')


for x in range(0, 4):  # try 4 times
    try:
        browser.get("https://iss.fortaleza.ce.gov.br/")

        time.sleep(2)

        browser.find_element_by_xpath(
            '//*[@id="login:username"]').send_keys(cpf)
        browser.find_element_by_xpath(
            '//*[@id="login:password"]').send_keys(senha)
        str_error = None
        browser.find_element_by_xpath(
            '//*[@id="login:captchaDecor:captchaLogin"]').click()

    except Exception as str_error:
        pass

    if str_error:
        # wait for 2 seconds before trying to fetch the data again
        time.sleep(2)
    else:
        break


time.sleep(10)

# In[2]:

# Navegar para emissão de nota


browser.find_element_by_xpath(
    '/html/body/div[1]/div[2]/form/div/div[2]/div[1]/a/i').click()
time.sleep(2)

# Altera o tipo do tomador para buscar por CNPJ
browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:tipoPesquisaTomadorRb:1"]').click()
time.sleep(1)


for x in range(0, 4):  # try 4 times
    try:
        # Busca pelo CNPJ
        browser.find_element_by_xpath(
            '//*[@id="emitirnfseForm:cpfPesquisaTomador"]').clear()
        browser.find_element_by_xpath(
            '//*[@id="emitirnfseForm:cpfPesquisaTomador"]').send_keys(cnpj)

# Aguarda aparecer a aurea e clica
        time.sleep(1)
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr[1]/td[2]').click()
        str_error = None
    except Exception as str_error:
        pass

    if str_error:
        # wait for 2 seconds before trying to fetch the data again
        time.sleep(2)
    else:
        break


# Muda para aba de Serviço
browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:abaServico_lbl"]').click()
time.sleep(1)

# Seleciona a descrição CNAE
browser.find_element_by_xpath(
    '/html/body/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/div[5]/div[1]/select/option[2]').click()

browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:idDescricaoServico"]').send_keys(descricao)

browser.find_element_by_xpath(
    '//*[@id="emitirnfseForm:idValorServicoPrestado"]').send_keys(valor_da_nota)

browser.find_element_by_xpath('//*[@id="emitirnfseForm:btnCalcular"]').click()


# In[ ]:
