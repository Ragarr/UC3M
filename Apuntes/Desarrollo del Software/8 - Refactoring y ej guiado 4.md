Realizar cambios en la estructura interna del software para que sea más fácil de entender y más barato de modificar sin cambiar su comportamiento observable.

# Proceso TDD en el refactoring

1. Rojo: añadir test → Agregar una prueba para una funcionalidad aún por construir
2. Verde: hazlo funcionar → Haz que el test pase la prueba mediante la implementación de la funcionalidad necesaria de forma sencilla, pero “cruda”
3. Refactoriza → Límpialo, asegúrate de que el código esté lo más limpio y bien diseñado posible para la funcionalidad implementada actualmente