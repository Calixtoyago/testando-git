const texto = document.querySelector('h1');
const botao = document.querySelector('button');

botao.addEventListener('click', function() {
    if (texto.style.color == 'red'){
        texto.style.color = 'black';
    } else {
        texto.style.color = 'red'
    }
});

