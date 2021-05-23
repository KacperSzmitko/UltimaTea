from enum import Enum

class Error(Enum):
    WEAK_PASSWORD = "1000",
    PASSWORDS_NOT_MATCH = "1001",
    USER_EXISTS = "1002",
    SHORT_USERNAME = "1003",
    EMAIL_EXISTS = "1004",
    WRONG_LOGIN = "1005",
    WRONG_PASSWORD = "1006",
    EMAIL_NOT_EXISTS = "1007",


class ErrorMessages():

    languages = {
    'pl' : {
        Error.WEAK_PASSWORD: "Hasło powinno składać się conajmniej z 8 znaków oraz posiadać min.1 znak specjalny,1 liczbę oraz 1 wielką lietrę",
        Error.PASSWORDS_NOT_MATCH: "Hasła nie są takie same",
        Error.USER_EXISTS: "Istnieje już użytkownik o takiej nazwie",
        Error.SHORT_USERNAME: "Nazwa użytkownika powinna mieć długość conajmniej 3 znaków",
        Error.EMAIL_EXISTS: "Podany adres Email jest już przypisany do istniejącego konta",
        Error.WRONG_LOGIN: "Nieprawidłowa nazwa użytkownika/adres Email",
        Error.WRONG_PASSWORD: "Hasło nieprawidłowe",
        Error.EMAIL_NOT_EXISTS: "Podany adres email nie jest przypisany do żadnego użytkownika",
    },
    'en':{},
    }
    
        
