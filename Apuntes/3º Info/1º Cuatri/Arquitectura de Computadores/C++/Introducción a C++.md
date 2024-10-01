# Entrada Salida
**Hola mundo**
```Cpp
#include <iostream> 
int main() { 
	using namespace std; 
	cout << "Hello C++" << endl; 
	cerr << "Error message\n";
	return 0; 
}
```

- Cabecera: `<iostream>
- Espacio de nombres: `std` para no tener que especificarlo antes de los cout...
- Objetos globales: 
	- **`cin`**: Entrada estándar. 
	- **`cout`**: Salida estándar. 
	- **`cerr`**: Salida de errores. 
	- **`clog`**: Salida de log.
- Operadores
	- Volcado de un dato en un flujo: 
		- `std :: cout << "Valores: " << x << " , " << y << "\n";`
	- Lectura de valores: 
		- `std :: cin >> x >> y`

**Ejemplo entrada y salida**

```cpp
#include <iostream> 
#include <string> 
int main() { 
	std :: cout << "Enter your name: \n"; 
	std :: string name; 
	std :: cin >> name; 
	std :: cout << "Hello, " << name << "!\n"; 
}
```
# Vectores
vector permite almacenar y procesar un conjunto de valores de un mismo tipo. 
Un vector: 
- Tiene una secuencia de elementos. 
- Se puede acceder a los elementos por su índice. 
- Incluye información de su tamaño.
![[Pasted image 20230905153100.png]]
- Alternativa a usar arrays directamente.
**Uso básico**
```cpp
#include <vector> 
#include <iostream> 
int main() { 
	using namespace std; 
	vector<int> v(4); 
	v[0] = 1; 
	v[1] = 2; 
	v[2] = 4; 
	v[3] = 8; 
	cout << v[2] << "\n"; 
}
```

- Se debe indicar el tipo del elemento entre <>
- Parámetro del constructor: Tamaño inicial.
- No se puede acceder a indices más allá del tamaño (inclusive)

**Otro ejemplo**
```cpp
#include <vector>
#include <string>
#include <iostream>
int main() {
	using namespace std;
	vector<string> v(2) ;
	v[0] = "Daniel";
	v[1] = "Carlos";
	vector<int> w(2);
	w[0] = 1969;
	w[1] = 2003;
	cout << v[0] << " : " << w[0] << "\n";
	cout << v[1] << " : " << w[1] << "\n";
}
```
## Iniciación de vectores
- Un vector con tamaño inicia todos sus valores al valor por defecto del tipo.
	- Valores numéricos: 0
	- Valores de cadena: “”
- Si no se indica tamaño inicial, el vector tiene tamaño 0.
	- ``vector<double> v; // Vector con 0 elementos``
- **Se puede suministrar un valor inicial distinto.
	- ``vector<double> v(100, 0.5); // 100 posiciones iniciadas a 0.5**``
**Ejemplo iniciación en declaración**
```cpp
#include <vector>
#include <string>
#include <iostream>
int main() {
	using namespace std;
	vector<string> v { "Daniel", "Carlos" };
	vector<int> w { 1969, 2003 };
	cout << v[0] << " : " << w[0] << "\n";
	cout << v[1] << " : " << w[1] << "\n";
}
```

## Modificar Vectores:
- Un vector puede crecer cuando se añaden elementos.
	- Operación push_back(): Añade un elemento al final del vector.
![[Pasted image 20230907104544.png]]
- Se puede consultar el tamaño de un vector mediante la función miembro size.
	- ``cout << v.size () ;``
- size() permite definir un bucle para recorrer los elementos de un vector.
```cpp
for ( int i =0; i <v.size() ; ++i) {
	cout << "v[ " << i << "] = " << v[ i ] << "\n";
}
```
- Se puede usar un recorrido basado en rango para un vector.
```cpp
vector<int> v1 { 1, 2, 3, 4 };
for (auto x : v1) {
	cout << x << "\n";
}

vector<string> v2 { "Carlos", "Daniel", "José", "Manuel" };
for (auto x : v2) {
	cout << x << "\n";
}
```

**Ejemplo, estadísticas:**
- Objetivo: Leer de la entrada estándar una secuencia de calificaciones y volcar en la salida estándar la calificación mínima, la máxima y la calificación media.
	- Finalizar la lectura si se llega a fin de fichero.
	- Finalizar la lectura si no se lee un valor correctamente (p. ej. letras en lugar de números).
	- Se desconoce (y no se pregunta) el número de valores

```cpp
#include <vector>
#include <iostream>
int main() {
	using namespace std;
	vector<double> marks;
	double x;
	while (cin >> x) { // x OK?
		marks.push_back(x);
	}
	double average = 0.0;
	double max_val = marks[0];
	double min_val = marks[0];
	for (auto m: marks) {
		average += m;
		max_val = (m >max_val) ? m : max_val;
		min_val = (m <min_val) ? m : min_val;
	}
	average /= static_cast<double>(marks.size());
	cout << "Average: " << average << "\n";
	cout << "Max: " << max_val << "\n";
	cout << "Min: " << min_val << "\n";
}
```
**Ejemplo palabras unicas:**
- Objetivo: Volcar la lista ordenada de palabras únicas de un texto.
	- El texto se lee de la entrada estándar hasta fin de fichero.
	- La lista de palabras se imprime en la salida estándar
```cpp
#include <iostream>  

#include <vector>  

#include <string>  

#include <algorithm>  

int main() {  
    using namespace std;  
    vector<string> words;  
    string w;  
    while (cin >> w && w != "quit") {  
        words.push_back(w);
    }
    sort (words.begin(), words.end());
    cout << "\n";
    cout << words[0] << "\n";
    for (std :: size_t i =1; i <words.size(); ++i) {
        if (words[i - 1] != words[i ]) {
            cout << words[i] << "\n";
        }
    }
}
```
- en el while: cin se escribe en w

# Funciones
- Declaración: Incluye parámetros y tipo de retorno.
- Dos sintaxis alternativas.
	- ``double area(double ancho, double alto);
	- ``auto area(double ancho, double alto) −> double;
- Definición: Permite deducción automática de tipo de retorno
```cpp
auto area(double ancho, double alto) {
	return ancho * alto ;
}
```
## Paso de parametros
### Paso por Valor
- Único paso de parámetros válido en C. (no en cpp)
- Se pasa a la función una copia del argumento especificado en la llamada.
```cpp
int incrementa(int n) {
	++n;
	return n;
}
void f () {
	int x = 5;
	int a = incrementa(x);
	int b = incrementa(x);
	int c = incrementa(42);
}
```
### Paso por referencia
- Pasa la dirección del objeto
	- Conceptualmente equivale a paso por valor.
	- Físicamente equivalente a paso de un puntero
- Se tiene acceso al propio objeto

```cpp
void rellena (std :: vector <int> & v, int n) {
	for ( int i =0; i <n; ++i) {
		v.push_back(i);
	}
}
void f () {
	using namespace std;
	vector<int> v; // v.size () == 0
	rellena (v, 100); // v.size () == 100
}
```
### Paso por referencia constante
- Pasa la dirección del objeto pero impide su alteración dentro de la función
```cpp
double maxref(const std::vector<double> & v) {
	double res = std::numeric_limits<double>::min();
	for (auto x : v) {
		if (x>res) {
			res = x;
		}
	}
	return res;
}
void f () {
	vector<double> vec(1000000);
	// ...
	cout << "Max: " << maxref(vec) << "\n";
}
```

# Excepciones
- El modelo de excepciones de C++ presenta diferencias con otros lenguajes
- Una excepción puede ser cualquier tipo definido por el usuario.
	- class tiempo_negativo {};
- Cuando una función detecta una situación excepcional lanza (throw) una excepción.
```cpp
void imprime_velocidad(double s, double t) {
	if ( t > 0.0) {
		cout << s/t << "\n";
	}
	else {
		throw tiempo_negativo{};
	}
}
```
## Tratamiento de excepciones
- El llamante puede tratar una excepción con un bloque try-catch.
```cpp
void f () {
	double s = lee_espacio();
	double t = lee_tiempo();
	try {
		imprime_velocidad(s,t);
	}
	catch (tiempo_negativo) {
		cerr << "Error: Tiempo negativo\n";
	}
}
```
- Si no se trata una excepcion puesto que se propaga

### Excepciones estandar
- Varias excepciones predefinidas en la biblioteca estándar.
	- ``out_of_range``, ``invalid_argument``, . . .
	- Todos heredan de ``exception``
	- Todos tienen una función miembro ``what()``
```cpp
int main()
	try {
		f () ;
		return 0;
	}
	catch (out_of_range & e) {
		cerr << "Out of range:" << e.what() << "\n";
		return −1;
	}
	catch (exception & e) {
		cerr << "Excepción: " << e.what() << "\n";
		return −2;
	}
}
```

# Memoria Dinámica
## Almacén libre
- El almacén libre contiene la memoria que se puede adquirir y liberar
- IMPORTANTE: C++ no es un lenguaje con gestión automática de recursos.
	- Si se adquiere un recurso, se debe liberar.
	- La memoria adquirida hay que liberarla
- El operador ``new`` permite asignar memoria del almacén libre.
```cpp
int * p = new int; // Asigna memoria para un int sin iniciarlo
char * q = new char[10]; // Asigna memoria para 10 char
```
- Efecto:
	- El operador new devuelve un puntero al inicio de la memoria asignada.
	- Una expresión ``new T ``devuelve un valor de tipo ``T*``.
	- Una expresión new ``T[sz]`` devuelve un valor de tipo ``T*``.
- Una variable de tipo puntero no se inicia de forma automática a ningún valor.
	- Si se desreferencia un puntero no iniciado se tiene un comportamiento no definido.
```cpp
int * p;
*p = 42; // Comportamiento no definido.
p[0] = 42; // Comportamiento no definido.
```
- Una variable de tipo puntero iniciada a una secuencia solamente puede accederse dentro de sus límites establecidos.
```cpp
int * v = new int[10];
v[0] = 42; // OK
x = v [−1]; // No definido
x = v [15]; // No definido
v[10] = 0; // No definido
```
- Se puede iniciar un puntero al valor puntero-nulo para indicar que no apunta a ningún objeto.
	- Literal nullptr.
```cpp
int * p = nullptr ;
char * q = nullptr ;
if (p != nullptr) { /* ... */ }
if (q == nullptr) { /* ... */ }
```
- El operador new no inicia el objeto asignado.
	- ``int * p = new int;
	- ``x = *p; // x tiene un valor desconocido
- Si se reserva una secuencia con new no se inicia ninguno de los objetos.
	- ``int * v = new int[10];
- Se puede indicar los valores iniciales entre llaves.
```cpp
v = new int [4]{1,2,3,4}; // v[0] = 1, v[1] = 2, v[2] = 3, v[3] = 4
v = new int[4]{1, 2}; // v[0] = 1, v[1] = 2, v[2] = 0, v[3] = 0
v = new int [4]{}; // v[0] = 0, v[1] = 0, v[2] = 0, v[3] = 0
v = new int [4]{1,2,3,4,5}; // Error demasiados iniciadores
```
- El operador delete permite liberar memoria y marcarla como no asignada.
- Pude aplicarse solamente a:
	- Memoria devuelta por el operador new y actualmente asignada.
	- El puntero nulo
```cpp
nt * p = new int{10};
*p = 20;
delete p; // Libera p
```
- Existe una version diferente para liberar arrays
```cpp
int * p = new int{10};
int * v = new int[10];
delete p; // Libera p
delete [] v;
```
- Si se agota la memoria se lanza la excepción bad_alloc.

## Punteros inteligentes
- Un puntero inteligente encapsula un puntero y gestiona de forma automática la gestión de la memoria asociada
	- Su destructor libera automáticamente la memoria asociada
- Tipos de punteros inteligentes:
	- ``unique_ptr``: Puntero a un objeto que no admite copias.
	- ``shared_ptr``: Puntero con contador de referencias asociado.
	- ``weak_ptr``: Puntero auxiliar para shared_ptr.
### ``shared_ptr``
- Cuando se copia se incrementa el contador de referencias.
- Cuando se destruye se decrementa el contador.
- Si el contador llega a cero el objeto se destruye.
```cpp
void f () {
	shared_ptr<string> p1{new string{"Hola"}};
	shared_ptr<string> p2{p1}; // referencias −> 2
	auto n = p1−>size(); // string :: size () . p1 usado como ptr
	*p1 = "Adios";
	if (p2) { cerr << "Ocupado\n"; }
		p1 = nullptr ; // referencias −> 1
	// ...
} // referencias −> 0 ==> Destrucción
```
### ``unique_ptr
- Ofrece un puntero no compartido que no se puede copiar
```cpp
void f ( string & s, int n) {
	unique_ptr<int> p = new int{50};
	string tmp = s; // Podría lanzar excepción
	if (n<0) return;
	*p = 42;
} // Libera p
```
### ``weak_ptr
te lo imaginas o algo por que no esta en los apuntes

## Creación """""simplificada""""""
- Asigna el objeto y los meta-datos en una única operación
```cpp
auto p = std :: make_shared<registro>("Daniel", 42);
auto q = std :: make_unique<string>("Hola")
```
ESto es SIMPLIFICADO?????????

# Tipos definidos por el usuario aka clases
- Una clase se puede definir con struct o class.
	- La única diferencia es la visibilidad por defecto.
```cpp
struct fecha {
// Visibilidad pública por defecto
};
class fecha {
// Visibilidad privada por defecto
};
```
## Función miembro aka métodos
- Solamente se puede invocar para un objeto del tipo definido.
Punto
```cpp
struct punto {
	double x, y;
	double modulo();
	double mover_a(double cx, double cy);
};
```
Usando un punto
```cpp
void f () {
	punto p{2.5, 3.5};
	p.mover_a(5.0, 7.5);
	cout << p.modulo() << "\n";
}
```
### Visibilidad
- Niveles de visibilidad de los miembros de una clase:
	- ``public``: Cualquiera puede acceder.
	- ``private``: Solamente por miembros de la clase.
	- ``protected``: Miembros de clases derivadas pueden acceder.
```cpp
class fecha {
public:
// Miembros públicos
protected:
// Miembros protegidos
private:
// Miembros privados
};
```

### Constructor
- Un constructor es una función miembro especial.
	- Se usa para iniciar objetos del tipo definido por la clase.
	- La sintaxis obliga a invocar al constructor

```cpp
class punto {
	public:
		punto(double cx, double cy) :
			x{cx}, y{cy} {}
	// ...
	private:
		double x;
		double y;
};
// USO
void f () {
	punto p{1.5, 1.5}; // Construye punto
	punto q; // Error: faltan args
	punto r{p}; // OK. Copia
}
```
### Destructor
- Un destructor es una función miembro especialque se ejecuta de forma automática cuando un objeto sale de alcance.
	- No tiene tipo de retorno. 
	- No toma parámetros. 
	- Nombre de clase precedido de carácter
```cpp
class numvector {
	public:
		// ...
		numvector(int n) : size{n}, vec{new double[size]}
		{}
		~numvector() { delete [] vec; }
	private:
		int size ;
		double * vec;
};
```
- El destructor se invoca de forma automática
```cpp
void f () {
	numvector v(100);
	for ( int i =0; i <100; ++i) {
		v[ i ] = i ;
	}
	// ...
	for ( int i =0; i <100; ++i) {
		cout << v[ i ] << "\n";
	}
} // Invocación de destructor
```
