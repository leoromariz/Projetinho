document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('socialMediaForm');
    const outputDiv = document.getElementById('output');

    if (form) {
        form.addEventListener('submit', async (event) => { // Tornar a função async para usar await
            event.preventDefault(); // Impede o envio padrão do formulário

            // 1. Coletar dados do formulário usando FormData
            // Isso já lida com todos os campos input, select, radio pelo atributo 'name'
            const rawFormData = new FormData(form);
            
            // 2. Criar um objeto URLSearchParams para formatar como x-www-form-urlencoded
            // e RENOMEAR as chaves para snake_case, conforme o backend espera
            const urlSearchParams = new URLSearchParams();

            // Mapeamento de nomes do HTML (CamelCase) para o backend (snake_case)
            const fieldMapping = {
                'age': 'age',
                'gender': 'gender',
                'academicLevel': 'academic_level', // HTML: academicLevel, Python: academic_level
                'country': 'country',
                'avgDailyUsageHours': 'avg_daily_usage_hours', // HTML: avgDailyUsageHours, Python: avg_daily_usage_hours
                'mostUsedPlatform': 'most_used_platform', // HTML: mostUsedPlatform, Python: most_used_platform
                'affectsAcademicPerformance': 'affects_academic_performance', // HTML: affectsAcademicPerformance, Python: affects_academic_performance
                'sleepHours': 'sleep_hours_per_night', // HTML: sleepHours, Python: sleep_hours_per_night (note a diferença de nome)
                'mentalHealthScore': 'mental_health_score', // HTML: mentalHealthScore, Python: mental_health_score
                'relationshipStatus': 'relationship_status', // HTML: relationshipStatus, Python: relationship_status
                'socialMediaConflicts': 'conflicts_over_social_media' // HTML: socialMediaConflicts, Python: conflicts_over_social_media
            };

            for (const [htmlName, backendName] of Object.entries(fieldMapping)) {
                let value = rawFormData.get(htmlName);
                
                // Converter para números quando apropriado, pois FormData pega tudo como string
                if (backendName === 'age' || backendName === 'gender' || 
                    backendName === 'academic_level' || backendName === 'country' ||
                    backendName === 'most_used_platform' || backendName === 'affects_academic_performance' ||
                    backendName === 'mental_health_score' || backendName === 'relationship_status' ||
                    backendName === 'conflicts_over_social_media') {
                    value = parseInt(value);
                } else if (backendName === 'avg_daily_usage_hours' || backendName === 'sleep_hours_per_night') {
                    value = parseFloat(value);
                }

                // Adicionar ao URLSearchParams. Ele vai converter números de volta para string para o envio.
                urlSearchParams.append(backendName, value);
            }
            
            const urlEncodedData = urlSearchParams.toString();

            // Exibe os dados que serão enviados no console (para depuração)
            console.log("Dados a serem enviados (URL-encoded):", urlEncodedData);

            try {
                // Envia a requisição para a API
                const response = await fetch('http://127.0.0.1:5000/aluno', { // Verifique a URL da sua API
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: urlEncodedData,
                });

                const result = await response.json(); // Assume que a API sempre retorna JSON

                outputDiv.classList.remove('hidden'); // Mostra a div de saída
                outputDiv.innerHTML = ''; // Limpa o conteúdo anterior

                if (response.ok) { // Se a resposta da API for 2xx (sucesso)
                    const outcomeText = result.outcome === 1 ?
                        "Você se enquadra no grupo de viciados em Mídias Sociais." :
                        "Você não se enquadra no grupo de viciados em Mídias Sociais.";

                    outputDiv.innerHTML = `
                        <p class="success-message"><strong>Sucesso!</strong> Aluno adicionado e predição realizada.</p>
                        <p><strong>Resultado da Predição:</strong> ${outcomeText}</p>
                        <p>Detalhes do Aluno:</p>
                        <ul>
                            <li>Idade: ${result.age}</li>
                            <li>Gênero: ${result.gender}</li>
                            <li>Nível Acadêmico: ${result.academic_level}</li>
                            <li>País: ${result.country}</li>
                            <li>Horas de Uso Diário: ${result.avg_daily_usage_hours}</li>
                            <li>Plataforma Mais Usada: ${result.most_used_platform}</li>
                            <li>Afeta Desempenho Acadêmico: ${result.affects_academic_performance === 1 ? 'Sim' : 'Não'}</li>
                            <li>Horas de Sono: ${result.sleep_hours_per_night}</li>
                            <li>Pontuação de Saúde Mental: ${result.mental_health_score}</li>
                            <li>Status de Relacionamento: ${result.relationship_status}</li>
                            <li>Conflitos sobre Redes Sociais: ${result.conflicts_over_social_media}</li>
                        </ul>
                    `;
                } else { // Se a resposta da API for um erro (4xx, 5xx)
                    const errorMessage = result.message || "Ocorreu um erro desconhecido na API.";
                    outputDiv.innerHTML = `<p class="error-message"><strong>Erro:</strong> ${errorMessage}</p>`;
                    console.error('Erro da API:', result);
                }
            } catch (error) {
                outputDiv.classList.remove('hidden');
                outputDiv.innerHTML = `<p class="error-message">Erro ao conectar com a API: ${error.message}. Verifique se o backend está rodando.</p>`;
                console.error('Erro na requisição Fetch:', error);
            }
        });
    }
});