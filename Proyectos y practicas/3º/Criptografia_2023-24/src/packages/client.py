from packages.server import Server, ImgPackage
from packages.imgproc import *
from PIL import Image
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from packages.imgproc.img_cripto_utils import ImageCryptoUtils
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from packages.authorities import PedroSanchez, Certificate
import logging




class Client:
    def __init__(self):
        # logging
        self.logger = logging.getLogger('Client')
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('SYSTEM.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.username = None
        self.password = None
        self.__plain_pass = None
        self.encryptor = None
        self.__server = Server()
        self.__private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.__subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Colmenarejo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UC3M"),
            x509.NameAttribute(NameOID.COMMON_NAME, "uc3m.com"),
        ])
        # para probar certificado auto firmado borrar desde aqui hasta el comentario
        csr = x509.CertificateSigningRequestBuilder().subject_name(
            self.__subject
        ).sign(self.__private_key, hashes.SHA256())
        pedroSanchez = PedroSanchez()
        self.__certificate = pedroSanchez.issueCertificate(csr)

        self.__trusted_certs = [self.__certificate] + pedroSanchez.trusted_certs

        """ # test certificado auto firmado
        self.__certificate = x509.CertificateBuilder().subject_name(
                self.__subject
            ).issuer_name(
                self.__subject
            ).public_key(
                self.__private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.now(datetime.timezone.utc)
            ).not_valid_after(
                # Our certificate will be valid for 10 days
                datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName("localhost")]),
                critical=False,
            # Sign our certificate with our private key
            ).sign(self.__private_key, hashes.SHA256())
        
        self.__certificate = Certificate(self.__certificate)

        self.__trusted_certs = [self.__certificate]
        """
    """    # FIXME remove this  
    @property
    def server(self):
        return self.__server"""
    
    

    def get_images(self, num: int | None = -1, username: str | None = None,
                   date: str | None = None, time: str | None = None) -> list:
        """Returns a list of images from the given camera
        Args:
            num (int): number of images to return
            username (str, optional): name of the camera owner.
                - None it will return all the images from the logged user.
                - "@all" it will return all the images from all the users.
            date (str, optional): date of the images. Defaults to None.ç
                format: "%Y/%m/%d"

            time (str, optional): time of the images. Defaults to None.
                format: HH_MM_SS
        Returns:
            list: list of images
        """
        # si no se espècifica usuario se coge al usuario logeado (si hay, si no sera None)
        if username is None:
            username = self.username
        # si se especifica @all se coge todas las imagenes idependientemente del usuario logeado
        if username == "@all":
            username = None

        if time is not None:
            if date is None:
                self.logger.error("Date must be specified if time is specified")
                raise Exception("Date must be specified if time is specified")

        if username is None:
            images = self.__server.get_images(num=num, username=username, date=date, time=time)
            progress = 0
            for i in images:
                yield round((progress / len(images)) * 100, 2), i
                progress += 1
            return

        # if the user is logged in, we will return de decrypted images
        images = self.__server.get_images(num=num, username=username, date=date, time=time)
        decrypted_images = []
        progress = 0
        for im in images:
            decrypted = ImageCryptoUtils.decrypt(im.image, self.__plain_pass)
            new = ImgPackage(im.author, im.date, im.time, im.path, decrypted)
            decrypted_images.append(new)
            yield round((progress / len(images)) * 100, 2), new
            progress += 1

        return

    def register(self, name: str, password: str) -> None:
        """Creates a new user
        Args:
            name (str): name of the user
            password (str): password of the user
        """
        self.logger.info(" Registering user...")
        self.logger.info("   Checking servers certificate...")
        if not self.__check_servers_certificate(self.__server.certificate):
            self.logger.error("Servers certificate not trusted")
            raise Exception("Servers certificate not trusted")
        self.logger.info("     Servers certificate is trusted")
        self.logger.info("   Obtaining servers public key...")
        
        servers_pk = self.__server.certificate.certificate.public_key()
        # encrypt password with public key
        
        self.logger.info("   Encrypting password...")
        password = password.encode()
        password = servers_pk.encrypt(
            password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).hex()
        self.logger.info("  Password encrypted and sended to server")
        return self.__server.create_user(name, password)

    def logout(self):
        """
        Logs out a user from the server
        :return:
        """
        self.username = None
        self.password = None

    def login(self, name: str, password: str):
        """Logs in a user
        Args:
            name (str): name of the user
            password (str): password of the user
        Returns:
            bool: True if the user was logged in, False otherwise
        """
        self.logger.info(" Logging in...")
        self.logger.info("   Checking servers certificate...")
        if not self.__check_servers_certificate(self.__server.certificate):
            self.logger.error("Servers certificate not ")
            raise Exception("Servers certificate not trusted")
        self.logger.info("     Servers certificate is trusted")
        # encrypt password with public key
        self.logger.info("   Encrypting password...")
        servers_pk = self.__server.certificate.certificate.public_key()
        # encrypt password with public key
        
        self.logger.info("   Encrypting password...")
        plain_pass = password
        password = password.encode()
        password = servers_pk.encrypt(
            password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).hex()
        
        self.logger.info("   Password encrypted and sended to server")
        if self.__server.login(name, password):
            self.__plain_pass = plain_pass
            self.username = name
            self.password = password
            self.logger.info(" Logged in")

        else:
            self.logger.error("User or password incorrect")
            raise ValueError("User or password incorrect")

    def remove_user(self) -> None:
        """Removes the user from the server"""
        if self.__server.login(self.username, self.password):
            self.__server.remove_user(self.username, self.password)

    def upload_photo(self, path: str, x: int = 0, y: int = 0, w: int = 200, h: int = 200) -> None:
        """Uploads a photo to the server
        Args:
            path (str): path to the image
            x (int, optional): x coordinate of the top left corner of the square to encrypt. Defaults to 0.
            y (int, optional): y coordinate of the top left corner of the square to encrypt. Defaults to 0.
            w (int, optional): width of the square to encrypt. Defaults to 200.
            h (int, optional): height of the square to encrypt. Defaults to 200.
        """
        self.logger.info(" Uploading image...")
        # check if image is png
        if not path.endswith(".png"):
            self.logger.error("Image must be a PNG")
            raise Exception("Image must be a PNG")
        # try to open image
        try:
            image = Image.open(path)
        except:
            self.logger.error("Image could not be opened check path and format")
            raise Exception("Image could not be opened check path and format")
        self.logger.info("   Image valid...")
        self.logger.info("   Encrypting image...")
        self.logger.info("     Checking servers certificate...")
        if not self.__check_servers_certificate(self.__server.certificate):
            self.logger.error("Servers certificate not trusted")
            raise Exception("Servers certificate not trusted")
        self.logger.info("       Servers certificate is trusted")
        
        self.logger.info("     obtaining servers public key...")
        servers_pk = self.__server.certificate.certificate.public_key()
        # encrypt image 
        self.logger.info("     Encrypting image...")
        image = ImageCryptoUtils.encrypt(image, self.__plain_pass, x, y, w, h)
        ImageCryptoUtils.generate_image_hash(image, self.__private_key, servers_pk)
        self.logger.info("       Image encrypted")
        self.logger.info("   Uploading image...")
        # upload image
        self.__server.store_image(image, self.username, self.password, self.__certificate)
        self.logger.info(" Image uploaded successfully")

    def remove_image(self, date: str, time: str) -> None:
        """Removes the image with the given name
        Args:
            date (str): date of the image
            time (str): time of the image
        """
        return self.__server.remove_image(self.username, self.password, date, time)

    def __check_servers_certificate(self, certificate: Certificate) -> bool:
        """
        Checks if the servers certificate is trusted
        :param certificate: certificate to check
        :return: True if the certificate is trusted, False otherwise
        """
        # is a trusted certificate?
        trusted = False
        while not trusted:
            if isinstance(certificate, Certificate):
                x509cert = certificate.certificate
                issuerCert = certificate.issuer_certificate
                if certificate.issuer.isRevoked(x509cert):
                    raise ValueError("Certificate is revoked")
                if isinstance(issuerCert, Certificate):
                    issuerCert = issuerCert.certificate
                issuerCert.public_key().verify(
                    x509cert.signature,
                    x509cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    x509cert.signature_hash_algorithm,
                )
                trusted = certificate in self.__trusted_certs
                certificate = certificate.issuer_certificate
            elif isinstance(certificate, x509.Certificate):
                trusted = certificate in self.__trusted_certs
                break
            else:
                self.logger.error("Servers certificate not valid")
                raise ValueError("Servers certificate not valid")
        return trusted