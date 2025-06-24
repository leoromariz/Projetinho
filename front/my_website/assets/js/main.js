document.addEventListener('DOMContentLoaded', () => {
    // Adicionar a classe 'active' ao link de navegação da página atual
    const navLinks = document.querySelectorAll('.nav-links a');
    const currentPath = window.location.pathname.split('/').pop(); // Obtém o nome do arquivo (ex: index.html)

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Animação para scroll suave (exemplo, se você tiver âncoras internas)
    // document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    //     anchor.addEventListener('click', function (e) {
    //         e.preventDefault();
    //         document.querySelector(this.getAttribute('href')).scrollIntoView({
    //             behavior: 'smooth'
    //         });
    //     });
    // });
});