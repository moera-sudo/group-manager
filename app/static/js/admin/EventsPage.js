document.addEventListener('DOMContentLoaded', function() {
    const eventsSection = document.querySelector('.events-section');
    const addEventBtn = document.getElementById('addEventBtn');
    const eventModal = document.getElementById('eventModal');
    const eventForm = document.getElementById('eventForm');
    const cancelBtn = document.getElementById('cancelBtn');
    const currentUserId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    const eventDateInput = document.getElementById('eventDate');
    const groupSelect = document.getElementById('GroupTag');
    
    
    // Установить начальное значение из URL при загрузке страницы
    const urlParams = new URLSearchParams(window.location.search);
    const groupParam = urlParams.get('group');
    if (groupParam) {
        groupSelect.value = groupParam;
    }
    
    // Обработчик изменения значения в select
    groupSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        const currentUrl = new URL(window.location.href);
        
        // Обновляем параметр group в URL
        currentUrl.searchParams.set('group', selectedValue);
        
        // Перенаправляем на новый URL с выбранным параметром
        window.location.href = currentUrl.toString();
    });

    

    
    // Управление модальным окном
    function openModal(mode = 'create', eventCard = null) {
        eventModal.style.display = 'block';
        document.getElementById('modalTitle').textContent = 
            mode === 'create' ? 'Добавить событие' : 'Изменить событие';
        
        document.getElementById('eventId').value = mode === 'edit' ? eventCard.dataset.eventId : '';
        document.getElementById('action').value = mode;
        
        if (mode === 'edit' && eventCard) {
            const eventTitle = eventCard.querySelector('.event-title').textContent;
            const eventDate = formatDateForInput(eventCard.querySelector('.event-date').textContent);
            const eventIcon = eventCard.querySelector('.event-icon i').textContent;

            document.getElementById('eventTitle').value = eventTitle;
            document.getElementById('eventDate').value = eventDate;
            document.getElementById('eventIcon').value = eventIcon;
        }
    }

    function closeModal() {
        eventModal.style.display = 'none';
        eventForm.reset();
        document.getElementById('action').value = 'create';
    }

    function formatDateForInput(dateString) {
        const months = {
            'января': '01', 'февраля': '02', 'марта': '03', 
            'апреля': '04', 'мая': '05', 'июня': '06',
            'июля': '07', 'августа': '08', 'сентября': '09', 
            'октября': '10', 'ноября': '11', 'декабря': '12'
        };

        const [day, month, year] = dateString.split(' ');
        return `${year}-${months[month]}-${day.padStart(2, '0')}`;
    }

    // Обработчики событий
    addEventBtn.addEventListener('click', () => openModal('create'));
    cancelBtn.addEventListener('click', closeModal);

    // Удаление события
    eventsSection.addEventListener('click', async function(e) {
        const deleteButton = e.target.closest('.delete-event');
        if (!deleteButton) return;

        const eventCard = deleteButton.closest('.event-card');
        const eventId = eventCard.dataset.eventId;

        if (confirm('Вы уверены, что хотите удалить это событие?')) {
            try {
                const response = await fetch(`/admin/account_main/${currentUserId}/events/${eventId}/delete`, {
                    method: 'POST'
                });

                if (response.ok) {
                    eventCard.remove();
                } else {
                    alert('Ошибка при удалении события');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка');
            }
        }
    });

    // Редактирование события
    eventsSection.addEventListener('click', function(e) {
        const editButton = e.target.closest('.edit-event');
        if (!editButton) return;

        const eventCard = editButton.closest('.event-card');
        openModal('edit', eventCard);
    });

    // Обработка формы редактирования/создания события
    eventForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch(`/admin/account_main/${currentUserId}/events`, {
                method: 'POST',
                body: formData
            });
    
            // Выведем полный ответ для диагностики
            const responseText = await response.text();
            console.log('URL запроса:', e.target.action);
            console.log('Ответ сервера:', responseText);
    
            if (response.ok) {
                window.location.reload();
            } else {
                // Попробуем распарсить ответ как JSON
                try {
                    const errorData = JSON.parse(responseText);
                    alert(errorData.error || 'Произошла неизвестная ошибка');
                } catch {
                    // Если не JSON, выведем сам текст ответа
                    alert(responseText || 'Не удалось сохранить событие. Попробуйте еще раз.');
                }
            }
        } catch (error) {
            console.error('Полная ошибка:', error);
            alert('Техническая ошибка при сохранении события');
        }
    });
    eventDateInput.addEventListener('input', function(e) {
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