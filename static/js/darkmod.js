        const toggleButton = document.getElementById('toggleDarkMode');
        const darkModeIcon = document.getElementById('darkModeIcon');

        toggleButton.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // تغيير الأيقونة بين الشمس والقمر
            if (document.body.classList.contains('dark-mode')) {
                darkModeIcon.classList.remove('fa-moon');
                darkModeIcon.classList.add('fa-sun');
            } else {
                darkModeIcon.classList.remove('fa-sun');
                darkModeIcon.classList.add('fa-moon');
            }
        });

 