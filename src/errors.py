from enum import Enum

class Error(Enum):
    WEAK_PASSWORD = "1000",
    PASSWORDS_NOT_MATCH = "1001",
    USER_EXISTS = "1002",
    SHORT_USERNAME = "1003",
    EMAIL_EXISTS = "1004",
    WRONG_LOGIN_OR_PASSWORD = "1005",


class ErrorMessages():

    languages = {
    'pl' : {
        Error.WEAK_PASSWORD: "Hasło powinno składać się conajmniej z 8 znaków oraz posiadać min.1 znak specjalny,1 liczbę oraz 1 wielką lietrę",
        Error.PASSWORDS_NOT_MATCH: "Hasła nie są takie same",
        Error.USER_EXISTS: "Istnieje już użytkownik o takiej nazwie",
        Error.SHORT_USERNAME: "Nazwa użytkownika powinna mieć długość conajmniej 3 znaków",
        Error.EMAIL_EXISTS: "Podany adres Email jest już przypisany do istniejącego konta",
        Error.WRONG_LOGIN_OR_PASSWORD: "Nieprawidłowa nazwa użytkownika/Email lub hasło",
    },
    'en':{},
    }
    
        
