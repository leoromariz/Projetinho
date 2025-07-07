document.addEventListener('DOMContentLoaded', async () => {
    const tableContainer = document.getElementById('studentsTableContainer');
    const errorMessageDiv = document.getElementById('errorMessage');

    // Mapeamentos para converter códigos numéricos em strings legíveis
    const genderMap = {
        1: 'Masculino',
        2: 'Feminino'
    };

    const academicLevelMap = {
        2: 'Ensino médio',
        0: 'Graduação',
        1: 'Pós-graduação',
        3: 'Outro'
    };

    const countriesData = {
        'Bangladesh': 0, 'India': 1, 'USA': 2, 'UK': 3, 'Canada': 4, 'Australia': 5,
        'Germany': 6, 'Brazil': 7, 'Japan': 8, 'South Korea': 9, 'France': 10,
        'Spain': 11, 'Italy': 12, 'Mexico': 13, 'Russia': 14, 'China': 15,
        'Sweden': 16, 'Norway': 17, 'Denmark': 18, 'Netherlands': 19, 'Belgium': 20,
        'Switzerland': 21, 'Austria': 22, 'Portugal': 23, 'Greece': 24, 'Ireland': 25,
        'New Zealand': 26, 'Singapore': 27, 'Malaysia': 28, 'Thailand': 29,
        'Vietnam': 30, 'Philippines': 31, 'Indonesia': 32, 'Taiwan': 33,
        'Hong Kong': 34, 'Turkey': 35, 'Israel': 36, 'UAE': 37, 'Egypt': 38,
        'Morocco': 39, 'South Africa': 40, 'Nigeria': 41, 'Kenya': 42, 'Ghana': 43,
        'Argentina': 44, 'Chile': 45, 'Colombia': 46, 'Peru': 47, 'Venezuela': 48,
        'Ecuador': 49, 'Uruguay': 50, 'Paraguay': 51, 'Bolivia': 52, 'Costa Rica': 53,
        'Panama': 54, 'Jamaica': 55, 'Trinidad': 56, 'Bahamas': 57, 'Iceland': 58,
        'Finland': 59, 'Poland': 60, 'Romania': 61, 'Hungary': 62, 'Czech Republic': 63,
        'Slovakia': 64, 'Croatia': 65, 'Serbia': 66, 'Slovenia': 67, 'Bulgaria': 68,
        'Estonia': 69, 'Latvia': 70, 'Lithuania': 71, 'Ukraine': 72, 'Moldova': 73,
        'Belarus': 74, 'Kazakhstan': 75, 'Uzbekistan': 76, 'Kyrgyzstan': 77,
        'Tajikistan': 78, 'Armenia': 79, 'Georgia': 80, 'Azerbaijan': 81, 'Cyprus': 82,
        'Malta': 83, 'Luxembourg': 84, 'Monaco': 85, 'Andorra': 86, 'San Marino': 87,
        'Vatican City': 88, 'Liechtenstein': 89, 'Montenegro': 90, 'Albania': 91,
        'North Macedonia': 92, 'Kosovo': 93, 'Bosnia': 94, 'Qatar': 95, 'Kuwait': 96,
        'Bahrain': 97, 'Oman': 98, 'Jordan': 99, 'Lebanon': 100, 'Iraq': 101,
        'Yemen': 102, 'Syria': 103, 'Afghanistan': 104, 'Pakistan': 105, 'Nepal': 106,
        'Bhutan': 107, 'Sri Lanka': 108, 'Maldives': 109, 'Other': 110
    };
    const countryMap = Object.fromEntries(Object.entries(countriesData).map(([key, value]) => [value, key]));

    const platformData = {
        'Instagram': 0, 'Twitter': 1, 'TikTok': 2, 'YouTube': 3, 'Facebook': 4,
        'LinkedIn': 5, 'Snapchat': 6, 'LINE': 7, 'KakaoTalk': 8, 'VKontakte': 9,
        'WhatsApp': 10, 'WeChat': 11, 'Other': 12
    };
    const mostUsedPlatformMap = Object.fromEntries(Object.entries(platformData).map(([key, value]) => [value, key]));

    const affectsAcademicPerformanceMap = {
        0: 'Não',
        1: 'Sim'
    };

    const relationshipStatusMap = {
        0: 'Solteiro',
        1: 'Em um relacionamento',
        2: 'Complicado',
        3: 'Outro'
    };

    const outcomeMap = {
        0: 'Não Viciado',
        1: 'Viciado'
    };

    async function fetchStudents() {
        try {
            const response = await fetch('http://127.0.0.1:5000/alunos'); // Rota da sua API para listar alunos
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.alunos && data.alunos.length > 0) {
                renderTable(data.alunos);
            } else {
                tableContainer.innerHTML = '<p>Nenhum aluno cadastrado ainda.</p>';
            }
        } catch (error) {
            console.error('Erro ao buscar dados dos alunos:', error);
            tableContainer.innerHTML = '';
            errorMessageDiv.classList.remove('hidden');
        }
    }

    async function deleteStudent(studentId) {
        // Exibe um modal de confirmação (substituindo o alert/confirm)
        const confirmed = await showConfirmModal(`Tem certeza que deseja deletar o aluno com ID ${studentId}?`);
        if (!confirmed) {
            return; // Usuário cancelou a operação
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/aluno?id=${studentId}`, {
                method: 'DELETE',
            });

            const result = await response.json();

            if (response.ok) {
                alert(`Aluno ${studentId} deletado com sucesso!`); // Usando alert temporariamente para feedback
                fetchStudents(); // Recarrega a tabela após a deleção
            } else {
                alert(`Erro ao deletar aluno ${studentId}: ${result.message || 'Erro desconhecido'}`);
            }
        } catch (error) {
            console.error('Erro na requisição DELETE:', error);
            alert(`Erro ao conectar com a API para deletar aluno ${studentId}: ${error.message}`);
        }
    }

    // Função para exibir um modal de confirmação customizado
    function showConfirmModal(message) {
        return new Promise(resolve => {
            const modalHtml = `
                <div id="confirmModal" class="modal">
                    <div class="modal-content">
                        <p>${message}</p>
                        <div class="modal-buttons">
                            <button id="confirmYes" class="btn-confirm-yes">Sim</button>
                            <button id="confirmNo" class="btn-confirm-no">Não</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);

            const modal = document.getElementById('confirmModal');
            const confirmYes = document.getElementById('confirmYes');
            const confirmNo = document.getElementById('confirmNo');

            confirmYes.onclick = () => {
                modal.remove();
                resolve(true);
            };
            confirmNo.onclick = () => {
                modal.remove();
                resolve(false);
            };

            modal.style.display = 'block'; // Exibe o modal
        });
    }


    function renderTable(students) {
        const table = document.createElement('table');
        table.classList.add('students-table');

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const headers = [
            'ID', 'Idade', 'Gênero', 'Nível Acadêmico', 'País',
            'Horas de Uso Diário', 'Plataforma Mais Usada', 'Afeta Desempenho Acadêmico',
            'Horas de Sono', 'Pontuação de Saúde Mental', 'Status de Relacionamento',
            'Conflitos em Mídias Sociais', 'Resultado (Vício)', 'Ações' // Adicionada coluna de Ações
        ];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        students.forEach(student => {
            const row = document.createElement('tr');
            
            const displayData = {
                id: student.id,
                age: student.age,
                gender: genderMap[student.gender] || student.gender,
                academic_level: academicLevelMap[student.academic_level] || student.academic_level,
                country: countryMap[student.country] || student.country,
                avg_daily_usage_hours: student.avg_daily_usage_hours,
                most_used_platform: mostUsedPlatformMap[student.most_used_platform] || student.most_used_platform,
                affects_academic_performance: affectsAcademicPerformanceMap[student.affects_academic_performance] || student.affects_academic_performance,
                sleep_hours_per_night: student.sleep_hours_per_night,
                mental_health_score: student.mental_health_score,
                relationship_status: relationshipStatusMap[student.relationship_status] || student.relationship_status,
                conflicts_over_social_media: student.conflicts_over_social_media,
                outcome: outcomeMap[student.outcome] || student.outcome
            };

            Object.values(displayData).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                row.appendChild(td);
            });

            // Adiciona a célula de Ações com o ícone de lixeira
            const actionsTd = document.createElement('td');
            const deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-btn');
            deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>'; // Ícone de lixeira do Font Awesome
            deleteButton.title = `Deletar aluno ${student.id}`;
            deleteButton.addEventListener('click', () => deleteStudent(student.id)); // Passa o ID do aluno
            actionsTd.appendChild(deleteButton);
            row.appendChild(actionsTd);

            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        tableContainer.innerHTML = '';
        tableContainer.appendChild(table);
    }

    fetchStudents();
});
