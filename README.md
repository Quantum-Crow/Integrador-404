Primero que nada hay que añadir la api key al codigo

Segundo, abrimos el cmd en la carpeta en la que se encuentra el dockerfile y la app y, siempre que docker este abierto, vamos a iniciar nuestra build con "docker build -t app ." y esperamos que se instale la build.

Tercero, para iniciar el container vas a usar el comando "docker run -it --rm --name 404 -p 5000:5000 app". en caso de que el container 404 ya exista vamos a usar el comando "docker start 404". (Otra opcion es usar "docker run -p 5000:5000 clima-app")

Cuarto, ahora nos vamos a dirigir al navegador y en la url colocamos "localhost:5000" o "http://127.0.0.1:5000" para iniciar.

Quinto, compruebe que la "app" funciona correctamente.