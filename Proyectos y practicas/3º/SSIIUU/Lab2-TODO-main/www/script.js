// Autor: Raúl Aguilar Arroyo
let taskList = [];
let secondsToHold = 1;
let holdTimer;
let touchStartX = 0;
let deltaX = 0;
let isDragging = false;
let pixelThreshold = 100;

document.addEventListener('DOMContentLoaded', init);
document.addEventListener('selectstart', function(event) {
    event.preventDefault(); // Prevent text selection while holding the mouse button down
});
document.addEventListener('contextmenu', function(event) {
    event.preventDefault(); // Prevent the context menu from appearing on right-click
});

function init(){
    loadTasks().then(() => {
        updateTasksScreen();
    });
    const newTaskInput = document.getElementById('task-name');
    const addTaskButton = document.getElementById('add-task');
    addTaskButton.addEventListener('click', () => {
        if(newTaskInput.value !== ''){
            add(newTaskInput.value);
            newTaskInput.value = '';
        }
    });
    // enter key to add task
    newTaskInput.addEventListener('keypress', (event) => {
        if(event.key === 'Enter'){
            add(newTaskInput.value);
            newTaskInput.value = '';
        }
    });


}


async function loadTasks(){
    /*es la función que se llamará al entrar en la aplicación para inicializar 
    la lista de tareas según el contenido del fichero tasks.json 
    en el servidor. Será necesario utilizar el API Fetch para recuperar el 
    contenido del fichero de manera asíncrona. 
    Se puede utilizar la sintaxis async/await o la sintaxis con promesas. 
    El contenido del fichero se guardará en un Array de tareas en la aplicación.
    */
    try {
        const response = await fetch('http://localhost:80/tasks.json');
        const data = await response.json();
        taskList = data;
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function saveTasks(){
    fetch('http://localhost:80/tasks.json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskList)
    })
    .then(function(response){
        // console.log(response);
    });
} 

function add(taskTitle="New task", done=false){
    /*al hacer click en el boton + se añadirá una nueva tarea a la lista. 
    El nombre de la tarea será el nombre introducido en un campo de texto correspondiente. 
    No se añadirá nada si el campo de texto está vacío*/
    if (taskTitle.trim() === "" || taskTitle === null || taskTitle === undefined || taskTitle == '') {
        // Mostrar el popup de advertencia si el título está vacío
        const popup = document.createElement('div');
        popup.classList.add('popup');
        popup.textContent = "Debe introducir un título";
        document.body.appendChild(popup);

        // Mostrar el popup
        popup.style.display = 'block';

        // Desaparecer el popup después de 2 segundos
        setTimeout(() => {
            popup.style.display = 'none';
            document.body.removeChild(popup);
        }, 2000);
        return;
    }

    let newTask = {
        id: taskList.length + 1,
        title: taskTitle,
        done: done
    };
    taskList.push(newTask);
    saveTasks();
    console.log("added new task", taskTitle);
    updateTasksScreen();
}

function remove(id = 0){
    taskList = taskList.filter(task => task.id != id);
    taskList.forEach((task, index) => {
        task.id = index + 1;
    });

    saveTasks();
    console.log("removed task", id);
    updateTasksScreen();

    // Crear el elemento del popup
    const popup = document.createElement('div');
    popup.classList.add('popup');
    popup.textContent = `Se ha eliminado la tarea ${id}`;
    document.body.appendChild(popup);

    // Mostrar el popup
    popup.style.display = 'block';

    // Desaparecer el popup después de 2 segundos
    setTimeout(() => {
        popup.style.display = 'none';
        document.body.removeChild(popup);
    }, 5000);
}


function toggleDone(id = 0){
    /*es la función que se ejecutará al mantener el dedo en una tarea más de dos segundos. 
    Como resultado, se marcará la tarea como completada. 
    Si la tarea ya estaba marcada como completada, se desmarcará. */
    let task = taskList.find(task => task.id == id);
    task.done = !task.done;
    saveTasks();
    // console.log("toggleDone for task", id);
}

function pointerDownHandler(event){
    event.preventDefault();
    touchStartX = event.touches[0].screenX;
    console.log("touchStartX", touchStartX);

    console.log("pointer down");
    holdTimer = setTimeout(() => {
        console.log("holded");
        if (isDragging && deltaX > pixelThreshold) {console.log("returning"); return;};

        if(event.target.classList.contains('pending')){
            event.target.className = 'done';
            toggleDone(event.target.id); // Asegúrate de que toggleDone esté definido
        } else if(event.target.classList.contains('done')){
            event.target.className = 'pending';
            toggleDone(event.target.id); // Asegúrate de que toggleDone esté definido
        }
        updateTasksScreen();
    }, secondsToHold * 1000);
    isDragging = true;
    if (event.target.classList.contains('done') && deltaX < pixelThreshold){
        event.target.classList.add('to-complete');
        event.target.classList.remove("to-uncomplete");
    }
    else if (event.target.classList.contains('pending') && deltaX < pixelThreshold){
        event.target.classList.remove('to-complete');
        event.target.classList.add("to-uncomplete");
    }

}

function pointerMoveHandler(event){
    event.preventDefault();
    if(isDragging){
        console.log("touch moved to", event.targetTouches[0].screenX - touchStartX)
        deltaX = event.targetTouches[0].screenX - touchStartX;
        if (deltaX > pixelThreshold){
            event.target.classList.add('to-remove');
            event.target.classList.remove('to-complete');
            event.target.classList.remove('to-uncomplete');
        }
        else {event.target.classList.remove('to-remove');}

        deltaX = Math.min(pixelThreshold*2, deltaX); // Prevent from dragging too far left
        deltaX = Math.max(0, deltaX); // Prevent from dragging too far right
        event.target.style.left = `${deltaX}px`;
        console.log("pointer moved to", deltaX)
    }
}


function pointerUpHandler(event){
    event.preventDefault();
    console.log("pointer up");
    clearTimeout(holdTimer);
    let touchEndX = event.changedTouches[0].screenX;
    if(deltaX > pixelThreshold){
        remove(event.target.id); // Asegúrate de que remove esté definido
    }
    event.target.style.left = '0px';
    isDragging = false;
    event.target.classList.remove('to-remove');
    event.target.classList.remove('to-complete');
    event.target.classList.remove('to-uncomplete');
    deltaX = 0;
    touchStartX = 0;
}


function updateTasksScreen(){
    pendingContainer = document.getElementById('pending-container');
    doneContainer = document.getElementById('done-container');
    pendingContainer.innerHTML = '';
    doneContainer.innerHTML = '';
    taskList.forEach(task => {
        let taskDiv = document.createElement('div');
        taskDiv.id = task.id;
        taskDiv.className = task.done ? 'done' : 'pending';
        taskDiv.textContent = task.title;
        taskDiv.addEventListener('touchstart', pointerDownHandler);
        taskDiv.addEventListener('touchend', pointerUpHandler);
        taskDiv.addEventListener('touchleave', pointerUpHandler);
        taskDiv.addEventListener('touchcancel', pointerUpHandler);
        taskDiv.addEventListener('touchmove', pointerMoveHandler);
        if(task.done){
            doneContainer.appendChild(taskDiv);
        } else {
            pendingContainer.appendChild(taskDiv);
        }
    });
}

