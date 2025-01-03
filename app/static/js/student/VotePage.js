document.addEventListener('DOMContentLoaded', () => {
    const addVotetBtn = document.getElementById('addVoteBtn');
    const pollModal = document.getElementById('pollModal');
    const closeModal = document.getElementById('closeModal');
    const cancelModal = document.getElementById('cancelModal');
    const pollForm = document.getElementById('pollForm');
    const optionsContainer = document.getElementById('optionsContainer');
    const addOptionBtn = document.getElementById('addOptionBtn');
    const pollAnalytModal = document.getElementById('pollAnalytModal');
    const closeAnalytModal = document.getElementById('closeAnalytModal');
    const currentUserId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    const voteSection = document.querySelector('.poll-section');
    const pollDeadlineInput = document.getElementById('pollDeadline');


    // Переключение вкладок
    const pollTabs = document.querySelectorAll('.poll-tab');
    pollTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            pollTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const tabType = tab.getAttribute('data-tab');
            
            document.getElementById('all-polls').style.display = 
                tabType === 'all' ? 'block' : 'none';
            document.getElementById('open-polls').style.display = 
                tabType === 'open' ? 'block' : 'none';
            document.getElementById('closed-polls').style.display = 
                tabType === 'closed' ? 'block' : 'none';
        });
    });




    //кнопки добавления опроса)
    addVotetBtn.style.transition = 'opacity 0.3s';
    addVotetBtn.addEventListener('mouseenter', () => {
        addVotetBtn.style.opacity = '0.6';
    });
    addVotetBtn.addEventListener('mouseleave', () => {
        addVotetBtn.style.opacity = '1';
    });

    


    //Открытие модального окна создания опроса
    addVotetBtn.addEventListener('click', () => {
        document.getElementById('modalTitle').textContent = 'Создание опроса';
        pollModal.style.display = 'block';
        pollForm.reset();
        optionsContainer.innerHTML = `
            <input 
                type="text" 
                class="form-input option-input" 
                placeholder="Введите вариант ответа"
                name = "pollVar"
            >
        `;
    });

    // открытие окна аналитики
    function AnalyticPoll() {
        document.getElementById('pollAnalytModal').style.display = 'block';
    }
    

    // Добавление варианта ответа
    addOptionBtn.addEventListener('click', () => {
        const newOptionInput = document.createElement('input');
        newOptionInput.type = 'text';
        newOptionInput.className = 'form-input option-input';
        newOptionInput.placeholder = 'Введите вариант ответа';
        newOptionInput.name = "pollVar"
        
        const deleteButton = document.createElement('button');
        deleteButton.textContent = '×';
        deleteButton.className = 'btn btn-cancel';
        deleteButton.type = 'button';
        deleteButton.style.marginLeft = '10px';
        
        deleteButton.addEventListener('click', () => {
            optionsContainer.removeChild(newOptionInput);
            optionsContainer.removeChild(deleteButton);
        });
        
        optionsContainer.appendChild(newOptionInput);
        optionsContainer.appendChild(deleteButton);
    });

    // Закрытие модального окна
    function closeModalWindow() {
        pollModal.style.display = 'none';
        pollForm.reset();
    }

    closeModal.addEventListener('click', closeModalWindow);
    cancelModal.addEventListener('click', closeModalWindow);


    //закрытие окна аналитики при нажатии на кнопку либо при нажатии вне окна
    function closeAnalyticsModal() {
        pollAnalytModal.style.display = 'none';
    }

    closeAnalytModal.addEventListener('click', closeAnalyticsModal);

    window.addEventListener('click', (event) => {
        if (event.target === pollAnalytModal) {
            closeAnalyticsModal();
        }
    });    

    //Обработчик изменения опроса
    voteSection.addEventListener('click', function(e) {
        const editButton = e.target.closest('[data-action="edit"]');
        if (!editButton) return;

        const pollCard = editButton.closest('.poll-card');
        const voteId = pollCard.dataset.voteId;
        const voteTitle = pollCard.querySelector('.poll-title').textContent;

        // Populate modal with existing vote details
        document.getElementById('modalTitle').textContent = 'Редактирование опроса';
        document.getElementById('action').value = 'edit';
        document.getElementById('pollTitle').value = voteTitle;
        
        // Добавляем скрытое поле для ID опроса
        let voteIdInput = document.getElementById('voteIdEdit');
        if (!voteIdInput) {
            voteIdInput = document.createElement('input');
            voteIdInput.type = 'hidden';
            voteIdInput.id = 'voteIdEdit';
            voteIdInput.name = 'voteId';
            document.getElementById('pollForm').appendChild(voteIdInput);
        }
        voteIdInput.value = voteId;

        // Очищаем существующие варианты ответов
        const optionsContainer = document.getElementById('optionsContainer');
        optionsContainer.innerHTML = '';

        const optionInput = document.createElement('input');
        optionInput.type = 'text';
        optionInput.name = 'pollVar';
        optionInput.className = 'form-input option-input';
        optionInput.placeholder = 'Введите вариант ответа';
        optionsContainer.appendChild(optionInput);

        // Открываем модальное окно
        document.getElementById('pollModal').style.display = 'block';
    });

    // Обработчик удаления опроса
    voteSection.addEventListener('click', async function(e){
        const deleteButton = e.target.closest('.delete-vote')
        if (!deleteButton) return;

        const voteCard = deleteButton.closest('.poll-card');
        const voteId = voteCard.dataset.voteId;

        if (confirm('Вы уверены, что хотите удалить этот опрос?')){
            try {
                const response = await fetch(`/headman/account_main/${currentUserId}/votes/${voteId}/delete`, {
                    method: 'POST'
                });

                if (response.ok) {
                    console.log(voteId)
                    voteCard.remove();
                } else {
                    alert('Ошибка при удалении события');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка');
            }
        }
    })

    // Обработчик закрытия/открытия опроса
    voteSection.addEventListener('click', async function (e){
        const changeButton = e.target.closest('.change-vote')
        if (!changeButton) return;

        const voteCard = changeButton.closest('.poll-card');
        const voteId = voteCard.dataset.voteId;
        const currentIcon = changeButton;



        const confirmMessage = currentIcon.textContent.trim() === 'lock' 
        ? 'Вы уверены, что хотите закрыть этот опрос?' 
        : 'Вы уверены, что хотите открыть этот опрос?';

        if (confirm(confirmMessage)){
            try {
                const response = await fetch(`/headman/account_main/${currentUserId}/votes/${voteId}/change`,{
                    method: 'POST'
                });
                console.log(response)
                if (response.ok){
                    console.log(voteId)
                    location.reload();
                } else {
                    alert('Ошибка при изменении статуса')
                }
            } catch(error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка')
            }
        } 
    })
    pollDeadlineInput.addEventListener('input', function(e) {
        // Заменяем любые символы, кроме цифр
        this.value = this.value.replace(/[^0-9-]/g, '');

        // Проверяем длину года
        const parts = this.value.split('-');
        if (parts.length > 1 && parts[0].length > 4) {
            // Если год больше 4 цифр, обрезаем
            parts[0] = parts[0].slice(0, 4);
            this.value = parts.join('-');
        }
    });
});