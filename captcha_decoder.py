from anticaptchaofficial.imagecaptcha import *

class Captcha_decoder():
    _solver: imagecaptcha
    def __init__(self, api_key:str, debug=False) -> None:
        self._solver = imagecaptcha()
        self._solver.set_key(api_key)
        if debug:
            self._solver.set_verbose(1)
        pass

    def decode(self, image_path:str):
        captcha_text = self._solver.solve_and_return_solution(image_path)
        if captcha_text != 0:
            return captcha_text
        elif "ERROR_ZERO_BALANCE" in self._solver.err_string:
            return "ERROR_ZERO_BALANCE"
        else:
            raise Exception(self._solver.err_string)
            
