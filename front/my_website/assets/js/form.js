document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('socialMediaForm');
    const outputDiv = document.getElementById('output');

    // Verifica se o formulário existe na página atual antes de adicionar o event listener
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário

            // Coleta os valores de cada campo do formulário
            const formData = {
                age: parseInt(document.getElementById('age').value),
                gender: document.getElementById('gender').value,
                academicLevel: document.getElementById('academicLevel').value,
                country: document.getElementById('country').value,
                avgDailyUsageHours: parseFloat(document.getElementById('avgDailyUsageHours').value),
                mostUsedPlatform: document.getElementById('mostUsedPlatform').value,
                affectsAcademicPerformance: document.querySelector('input[name="affectsAcademicPerformance"]:checked') ? document.querySelector('input[name="affectsAcademicPerformance"]:checked').value : 'N/A',
                sleepHoursPerNight: parseFloat(document.getElementById('sleepHours').value),
                mentalHealthScore: parseInt(document.getElementById('mentalHealthScore').value),
                relationshipStatus: document.getElementById('relationshipStatus').value,
                socialMediaConflicts: parseInt(document.getElementById('socialMediaConflicts').value)
            };

            // Exibe os dados coletados no console do navegador
            console.log("Dados do Formulário Coletados:", formData);

            // Exibe os dados coletados em uma div na página para feedback visual
            outputDiv.innerHTML = '<h3>Dados Enviados (simulação):</h3>' + JSON.stringify(formData, null, 2);
            outputDiv.classList.remove('hidden');
            outputDiv.classList.add('visible'); // Adiciona classe para transição

            // Você pode adicionar um pequeno atraso antes de resetar o formulário, se quiser
            // setTimeout(() => {
            //     form.reset(); // Limpa o formulário após a "simulação de envio"
            //     outputDiv.classList.remove('visible');
            //     outputDiv.classList.add('hidden');
            // }, 5000); // 5 segundos
        });
    }
});