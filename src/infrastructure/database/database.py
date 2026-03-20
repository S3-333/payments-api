#sqlalchemy es una biblioteca de Python que proporciona un conjunto de herramientas 
# para trabajar con bases de datos. 

#create_engine = Crea el motor de conexion (No conecta directamente todavía, solo lo prepara)
#text = Permite escribir SQL crudo dentro de SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker #sessionmaker es una función que crea una clase de sesión personalizada, 
# que se puede usar para crear instancias de conversacion que se conectan a la base de datos.


DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/payments" #URL de conexión a la base de datos, 
# en este caso se está utilizando MySQL con el conector pymysql

engine = create_engine(DATABASE_URL, echo=True) #echo=True es una opción que habilita el registro de todas 
# las consultas SQL que se ejecutan en la terminal.

#Una sesion es una conversación activa con la base de datos
SessionLocal = sessionmaker(
    autocommit=False, #Es falso, por lo que no se guardan cambios automaticamente
    autoflush=False, #Es falso, por lo que no se envian cambios a la base de datos hasta que se haga commit
    bind=engine #Indica que utilice este engine para conectarse a la base de datos
)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Resultado:", result.scalar())
            print("✅ Conexión exitosa")
    except Exception as e:
        print("❌ Error:", e)


if __name__ == "__main__":
    test_connection()