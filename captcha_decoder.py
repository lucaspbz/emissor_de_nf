import os

from anticaptchaofficial.imagecaptcha import *

def decode_image(image_path):
    client_key = os.getenv("API_KEY")
    if client_key is None:
        raise Exception("APIKEY do serviço de captcha não encontrada.")
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(client_key)
    captcha_text = solver.solve_and_return_solution(image_path)
    return captcha_text
