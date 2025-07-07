document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('socialMediaForm');
    // const outputDiv = document.getElementById('output'); // Não precisamos mais desta div para o sucesso

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault(); // Impede o envio padrão do formulário

            const rawFormData = new FormData(form);
            const urlSearchParams = new URLSearchParams();

            const fieldMapping = {
                'age': 'age',
                'gender': 'gender',
                'academicLevel': 'academic_level',
                'country': 'country',
                'avgDailyUsageHours': 'avg_daily_usage_hours',
                'mostUsedPlatform': 'most_used_platform',
                'affectsAcademicPerformance': 'affects_academic_performance',
                'sleepHours': 'sleep_hours_per_night',
                'mentalHealthScore': 'mental_health_score',
                'relationshipStatus': 'relationship_status',
                'socialMediaConflicts': 'conflicts_over_social_media'
            };

            for (const [htmlName, backendName] of Object.entries(fieldMapping)) {
                let value = rawFormData.get(htmlName);
                
                if (backendName === 'age' || backendName === 'gender' || 
                    backendName === 'academic_level' || backendName === 'country' ||
                    backendName === 'most_used_platform' || backendName === 'affects_academic_performance' ||
                    backendName === 'mental_health_score' || backendName === 'relationship_status' ||
                    backendName === 'conflicts_over_social_media') {
                    value = parseInt(value);
                } else if (backendName === 'avg_daily_usage_hours' || backendName === 'sleep_hours_per_night') {
                    value = parseFloat(value);
                }

                urlSearchParams.append(backendName, value);
            }
            
            const urlEncodedData = urlSearchParams.toString();

            console.log("Dados a serem enviados (URL-encoded):", urlEncodedData);

            try {
                const response = await fetch('http://127.0.0.1:5000/aluno', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: urlEncodedData,
                });

                const result = await response.json();

                // outputDiv.classList.remove('hidden'); // Não precisamos mais desta linha para o sucesso
                // outputDiv.innerHTML = ''; // Não precisamos mais desta linha para o sucesso

                if (response.ok) {
                    const outcomeText = result.outcome === 1 ?
                        "Viciado em Mídias Sociais" :
                        "Não Viciado em Mídias Sociais";

                    // Usando alert() para o feedback de sucesso
                    alert(`Aluno adicionado com sucesso!\nResultado da Predição: ${outcomeText}`);
                    
                    form.reset(); // Limpa o formulário após o sucesso
                    // Não precisamos mais do setTimeout para esconder a div, pois estamos usando alert
                } else {
                    // Mantemos a div para exibir mensagens de erro da API
                    outputDiv.classList.remove('hidden');
                    const errorMessage = result.message || "Ocorreu um erro desconhecido na API.";
                    outputDiv.innerHTML = `<p class="error-message"><strong>Erro:</strong> ${errorMessage}</p>`;
                    console.error('Erro da API:', result);
                }
            } catch (error) {
                // Mantemos a div para exibir erros de conexão
                outputDiv.classList.remove('hidden');
                outputDiv.innerHTML = `<p class="error-message">Erro ao conectar com a API: ${error.message}. Verifique se o backend está rodando.</p>`;
                console.error('Erro na requisição Fetch:', error);
            }
        });
    }
});
