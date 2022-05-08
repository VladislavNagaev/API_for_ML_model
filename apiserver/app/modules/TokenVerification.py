import sqlalchemy


class TokenVerification:

    def __init__(
        self,
        postgres_user: str,
        postgres_password: str,
        postgres_host: str,
        postgres_port: str,
        postgres_db: str
    ) -> None:
        """Establishes a database connection for subsequent token verification.

        Args:
            postgres_user (str): database user
            postgres_password (str): user password
            postgres_host (str): host for database connectio
            postgres_port (str): port for database connectio
            postgres_db (str): database name

        Raises:
            TypeError: \
                <postgres_user> should be a non-empty \
                string variable without spaces!
            TypeError: \
                <postgres_password> should be a non-empty \
                string variable without spaces!
            TypeError: \
                <postgres_host> should be a non-empty \
                string variable without spaces!
            TypeError: \
                <postgres_port> should be a non-empty \
                string variable without spaces, containing only digits!
            TypeError: \
                <postgres_db> should be a non-empty \
                string variable without spaces!
        """

        if (
            (not isinstance(postgres_user, str)) or
            (postgres_user.isspace()) or
            (postgres_user == '')
        ):
            raise TypeError(
                '<postgres_user> should be a non-empty '
                'string variable without spaces!'
            )

        if (
            (not isinstance(postgres_password, str)) or
            (postgres_password.isspace()) or
            (postgres_password == '')
        ):
            raise TypeError(
                '<postgres_password> should be a non-empty '
                'string variable without spaces!'
            )

        if (
            (not isinstance(postgres_host, str)) or
            (postgres_host.isspace()) or
            (postgres_host == '')
        ):
            raise TypeError(
                '<postgres_host> should be a non-empty '
                'string variable without spaces!'
            )

        if (
            (not isinstance(postgres_port, str)) or
            (postgres_port.isspace()) or
            (postgres_port == '') or
            (not postgres_port.isdigit())
        ):
            raise TypeError(
                '<postgres_port> should be a non-empty '
                'string variable without spaces, containing only digits!'
            )

        if (
            (not isinstance(postgres_db, str)) or
            (postgres_db.isspace()) or
            (postgres_db == '')
        ):
            raise TypeError(
                '<postgres_db> should be a non-empty '
                'string variable without spaces!'
            )

        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_host = postgres_host
        self.postgres_port = postgres_port
        self.postgres_db = postgres_db
        self._connection = 'failure'

    def __connect_db(
        self,
        dialect: str,
        driver: str,
        user: str,
        passwor: str,
        host: str,
        port: str,
        db: str
    ) -> sqlalchemy.engine.base.Engine:
        """Returns database connection with sqlalchemy"""
        
        db_connection_url = \
            '%(dialect)s+%(driver)s://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s' % {
                'dialect': dialect,
                'driver': driver,
                'user': user,
                'pass': passwor,
                'host': host,
                'port': port,
                'db': db
            }
        db_connection = sqlalchemy.create_engine(db_connection_url)

        try:
            db_connection.connect()
        except sqlalchemy.exc.OperationalError:
            raise ConnectionError('Connection to {db_connection_url} refused!')

        return db_connection

    def verify_token(self, token: str) -> bool:
        """Performs token verification over an established database connection.

        Args:
            token (str): verification token

        Raises:
            TypeError: \
                '<token> should be a non-empty ' \
                'string variable without spaces!

        Returns:
            bool: token status: True - access allowed / False - access denied
        """

        if (not isinstance(token, str)) or (token.isspace()) or (token == ''):
            raise TypeError(
                '<token> should be a non-empty '
                'string variable without spaces!'
            )

        db_connection = self.__connect_db(
            dialect='postgresql',
            driver='psycopg2',
            user=self.postgres_user,
            passwor=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db
        )
        self._connection = 'seccess'

        answer = db_connection.execute((
            "SELECT access "
            "FROM public.users "
            f"WHERE token = '{token}'"
        ))

        received_data = answer.fetchall()

        if len(received_data) > 0:
            access = received_data[0][0]
            if access == True:
                valid = True
            else:
                valid = False
        else:
            valid = False

        return valid
