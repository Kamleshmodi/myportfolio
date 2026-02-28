(function () {
    const controlsBtn = document.querySelectorAll('.control');
    
    // 1. Navigation Logic (Page Switching)
    controlsBtn.forEach(button => {
        button.addEventListener('click', function() {
            // Pehle current active button se class hatao
            let currentBtn = document.querySelector('.active-btn');
            if (currentBtn) {
                currentBtn.classList.remove('active-btn');
            }
            
            // Jis button par click hua hai, usko active banao
            this.classList.add('active-btn');

            // Pehle current active section se class hatao
            let currentSection = document.querySelector('.container.active');
            if (currentSection) {
                currentSection.classList.remove('active');
            }

            // Target section ko data-id ke through dhoondo aur active banao
            const id = this.dataset.id;
            const targetSection = document.getElementById(id);
            
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // 2. Theme Toggle Logic (Dark / Light Mode)
    const themeBtn = document.querySelector('.theme-btn');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
        });
    }
})();