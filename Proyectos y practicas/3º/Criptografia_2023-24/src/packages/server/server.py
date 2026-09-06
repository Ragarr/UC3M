from .user import User
from PIL import Image, PngImagePlugin
from .storage_manager import StorageManager
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.scrypt  import Scrypt
import re
import uuid
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from packages.authorities.ursula import Ursula
from packages.authorities.certificate import Certificate
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import logging
import datetime

class Server():
    def __init__(self) -> None:
        # logging
        # Configura el logger para la clase Server
        self.logger = logging.getLogger('Server')
        self.logger.setLevel(logging.DEBUG)

        # Crea un controlador para guardar logs en un archivo llamado server.log
        file_handler = logging.FileHandler('SYSTEM.log')
        file_handler.setLevel(logging.INFO)

        # Crea un formateador para los logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Agrega el controlador al logger de la clase Server
        self.logger.addHandler(file_handler)

        self.__sm = StorageManager()
        self.__sm.create_directories()
        self.__subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "AL"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Germany"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Munich"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "bmw"),
            x509.NameAttribute(NameOID.COMMON_NAME, "bmwaitzniert.com"),
        ])
        self.__private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        csr = x509.CertificateSigningRequestBuilder().subject_name(
            self.__subject
        ).sign(self.__private_key, hashes.SHA256())
        ursula = Ursula()
        self.__certificate = ursula.issueCertificate(csr)

        self.__trusted_certs = [self.__certificate] + ursula.trusted_certs


    @property
    def trusted_certs(self):
        return self.__trusted_certs


    @property
    def certificate(self):
        return self.__certificate     
        
    def __get_users(self) -> list:
        """Returns the list of users
        Returns:
            list: list of users
        """
        return self.__sm.get_users()
    
    def __remove_user(self, user: User) -> None:
        """Removes the given user
        Args:
            user (User): user to be removed
        """
        users = self.__get_users()
        for usr in users:
            if user == usr.name:
                users.remove(usr)
        self.__sm.remove_images(user)
        self.__sm.update_users_json(users)

    def create_user(self, name, password) -> None:
        """Creates a new user with the given name and password
        Args:
            name (str): name of the user
            password (str): password of the user (hashed)
        """
        # check if name is unique
        self.logger.info(" Creating user...")
        self.logger.info("   Checking if name is unique...")
        users = self.__get_users()
        for user in users:
            if user.name == name:
                raise ValueError("Name is already taken")
        self.logger.info("     Name is unique")
        self.logger.info("   Decrypting password...")
       # decrypt password
        password = self.__private_key.decrypt(
            bytes.fromhex(password),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        self.logger.info("     Password decrypted")
        self.logger.info("   Checking password...")
       
        # comprobar que la contraseña cumple los requisitos 
        # 12 caracteres, 1 mayuscula, 1 minuscula, 1 numero, 1 caracter especial
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters long")
        elif not re.search("[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        elif not re.search("[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        elif not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one number")
        elif not re.search("[!@#$%^&*()_+-={};':\"\\|,.<>/?]", password):
            raise ValueError("Password must contain at least one special character")
        
        self.logger.info("     Password is valid")
        self.logger.info("   Generating passwords KDF...")
        # KDF de la contraseña
        salt_p = uuid.uuid4().hex # son 16 bytes = 198 bits
        kdf = Scrypt(
            salt = bytes.fromhex(salt_p),
            length = 32, # 256 bits
            n = 2**14,
            r = 8,
            p = 1
        )
        password = kdf.derive(bytes(password, "utf-8")).hex()  
        self.logger.info("     Password KDF generated")
        self.logger.info("   Generating user...")
        # create user
        users = self.__get_users()
        users.append(User(name, password, salt_p))
        self.__sm.update_users_json(users)
        self.logger.info(" User created")
        

    def remove_user(self, name: str, password: str):
        """Removes the user with the given name
        Args:
            name (str): name of the user
            password (str): password of the user (hashed)
        """
        if name == "":
            raise ValueError("Name cannot be empty")
        elif password == "":
            raise ValueError("Password cannot be empty")
        
        # check if user exists and if password is correct
        if self.__authenticate(name=name, password=password):
            self.__remove_user(name)
        else:
            raise ValueError("User not found")

    def store_image(self, image: Image, user_name, password, certificate: Certificate):
        """ Stores the image in the server, IMAGE FORMAT: PNG
        Args:
            image_path (str): path to the image 
            camera_name (str): name of the camera
            user_name (str): name of the owner
        """
        self.logger.info(" received image")
        
        if user_name == "" or user_name is None:
            raise ValueError("User cannot be empty")
        if image is None:
            raise ValueError("Image cannot be empty")
        

        # check if owner is valid and if password is correct
        self.logger.info(" Checking users credentials...")
        if not self.__authenticate(user_name, password):
            raise ValueError("User or password incorrect")
        self.logger.info("   Users credentials are valid")
        
        self.logger.info(" Checking image integrity")
        image_metadata = image.info
        hash = image_metadata["hash"]
        key = bytes.fromhex(image_metadata["key"]) 
        # desencriptar la clave con la clave privada del servidor
        self.logger.info("   Checking image hash...")
        self.logger.info("     Decrypting hash key...")
        key = self.__private_key.decrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # regenerate hash
        self.logger.info("     Regenerating hash...")
        img_bytes = image.tobytes()
        iv = bytes.fromhex(image_metadata["iv"])
        salt = bytes.fromhex(image_metadata["salt"])

        h = hmac.HMAC(key, hashes.SHA256())
        h.update(img_bytes + iv + salt + key)
        img_hash = h.finalize()
        if hash != img_hash.hex():
            raise ValueError("Hashes do not match")
        self.logger.info("     Hashes match")
        
        # check certificate
        self.logger.info("   Checking client certificate...")
        certificate_pk = certificate.certificate.public_key()
        
        self.__verify_certificate(certificate)
        
        # check sign with public key
        self.logger.info("   Checking signature...")
        signature = bytes.fromhex(image_metadata["signature"])
        try:
            certificate_pk.verify(
                signature,
                img_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            raise ValueError("Signature not valid")
        self.logger.info("     Signature is valid")
        
        image.load()

        self.logger.info("   Image integrity is valid")
        self.logger.info(" Storing image...")
        # META DATA
        # copy metadata from original image to new image
        info = PngImagePlugin.PngInfo()
        for key, value in image.info.items():
            info.add_text(str(key), str(value))
        
        # store image
        self.__sm.storage_img(image, user_name, info)
        self.logger.info(" Image stored")
    
    def get_images(self, num: int, username: str | None = None, date: str | None =None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            author (str, optional): name of the  owner. Defaults to None.
            date (str, optional): date of the images. Defaults to None.
                format: "%Y/%m/%d"
            time (str, optional): time of the images. Defaults to None.
                format: HH_MM_SS
        Returns:
            list: list of images
        """
        # CHECKS #TODO

        # get images
        return self.__sm.get_images(num, username, date, time)

    def login(self, name: str, password: str) -> bool:
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """
        self.logger.info(" Logging in user...")
        # update users
        users = self.__get_users()
        self.logger.info("   Checking if user exists...")
        # check if user exists
        usernames = [ user.name for user in users ]
        if name not in usernames:
            return False
        self.logger.info("     User exists")

        self.logger.info("   Checking password...")
        
        # check if password is correct
        return self.__authenticate(name, password)
    
    def remove_image(self, username: str, password:str, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            username (str): name of the user
            date (str): date of the image
            time (str): time of the image
        """
        self.logger.info(" Removing image...")
        # check if user exists and if password is correct

        self.logger.info("   Checking users credentials...")
        if username == "" or username is None:
            raise ValueError("Username cannot be empty")
        elif date == "":
            raise ValueError("Date cannot be empty")
        elif time == "":
            raise ValueError("Time cannot be empty")
        
        if not self.__authenticate(username, password):
            raise ValueError("User or password incorrect")
        self.logger.info("     Users credentials are valid")
        self.__sm.remove_image(username, date, time)
        self.logger.info(" Image removed")

    
    def __authenticate(self, name: str, password: str) -> bool:
        # get users salt and password
        auth = False
        users = self.__get_users()

        # decrypt password
        self.logger.info("     Decrypting password...")
        password = self.__private_key.decrypt(
            bytes.fromhex(password),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        self.logger.info("       Password decrypted")

        for user in users:
            if user.name == name:
                # generate kdf with salt
                kdf = Scrypt(
                    salt = bytes.fromhex(user.salt_p),
                    length = 32,
                    n = 2**14,
                    r = 8,
                    p = 1
                )
                derivated_pass = kdf.derive(bytes(password, "utf-8")).hex()

                if user.password == derivated_pass:
                    auth = True
                    self.logger.info("     Password is correct")
                    # update salt and password
                    user.salt_p = uuid.uuid4().hex
                    kdf = Scrypt(
                        salt = bytes.fromhex(user.salt_p),
                        length = 32,
                        n = 2**14,
                        r = 8,
                        p = 1
                    )
                    user.password = kdf.derive(bytes(password, "utf-8")).hex()
                    self.__sm.update_users_json(users)
                    break
        
        return auth
    
    def clear_server(self):
        """Clears the server
        """
        # REMOVE AFTER TESTING
        self.__sm.delete_all_images()
        self.__sm.delete_all_users()
        self.__sm.create_directories()
        self.logger.info("Server cleared")

    def __verify_certificate(self, cert:Certificate):
        """Verifies the given certificate
        Args:
            cert (Certificate): certificate to be verified
        """

        trusted = False
        while not trusted:
            if isinstance(cert, Certificate):
                # check validity
                x509cert = cert.certificate
                issuerCert = cert.issuer_certificate

                # check if is expired
                if x509cert.not_valid_after < datetime.datetime.now():
                    raise ValueError("Certificate is expired")
                if x509cert.not_valid_before > datetime.datetime.now():
                    raise ValueError("Certificate is not valid yet")
                if isinstance(issuerCert, Certificate):
                    issuerCert = issuerCert.certificate
                
                # check if is revoked
                if cert.issuer.isRevoked(x509cert):
                    raise ValueError("Certificate is revoked")
                    
                issuerCert.public_key().verify(
                    x509cert.signature,
                    x509cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    x509cert.signature_hash_algorithm,
                )
                # check if trusted
                trusted = cert in self.__trusted_certs
                cert = cert.issuer_certificate
            elif isinstance(cert, x509.Certificate):
                trusted = cert in self.__trusted_certs
                break
            else:
                raise ValueError("Certificate not valid")

        if not trusted:
            raise ValueError("Certificate not trusted")