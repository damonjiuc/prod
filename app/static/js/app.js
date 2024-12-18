document.querySelector('#hamburger-btn').addEventListener('click', () => {
    document.querySelector('#hamburger-menu').classList.add('active');
});


document.querySelector('#close-menu').addEventListener('click', () => {
    document.querySelector('#hamburger-menu').classList.remove('active');
});