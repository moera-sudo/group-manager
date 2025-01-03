document.addEventListener('DOMContentLoaded', function() {
    const addAnnouncementBtn = document.getElementById('addAnnouncementBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const closeEditModalBtn = document.getElementById('closeEditModalBtn');
    const modal = document.getElementById('addAnnouncementModal');
    const editModal = document.getElementById('editAnnouncementModal');
    const announcementForm = document.getElementById('announcementForm');
    const editAnnouncementForm = document.getElementById('editAnnouncementForm');
    const announcementSection = document.querySelector('.announcement-section');
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

    addAnnouncementBtn.addEventListener('click', function() {
        modal.style.display = 'flex';
    });

    closeModalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    closeEditModalBtn.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    // Закрытие модальных окон при клике вне их
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });

    // Добавление нового объявления
    announcementForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        
        // Добавьте action='create' в FormData
        formData.append('action', 'create');
    
        fetch(event.target.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Всегда парсим ответ как JSON
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            // Перезагрузка страницы после успешного создания
            window.location.reload();
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(error.message || 'Не удалось создать объявление. Попробуйте еще раз.');
        });

        const title = document.getElementById('announcementTitle').value;
        const content = document.getElementById('announcementContent').value;
        const tag = document.getElementById('announcementCategory').value;

        const newAnnouncement = document.createElement('div');
        newAnnouncement.classList.add('announcement-card');
        
        const currentDate = new Date().toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });

        newAnnouncement.innerHTML = `
            <div class="announcement-actions">
                <i class="material-icons announcement-action-icon edit-announcement">edit</i>
                <i class="material-icons announcement-action-icon delete-announcement">delete</i>
            </div>
            <div class="announcement-date">${currentDate}</div>
            <h2 class="announcement-title">${title}</h2>
            <p class="announcement-content">${content}</p>
            <span class="announcement-tag">${tag}</span>
        `;

        announcementSection.insertBefore(newAnnouncement, announcementSection.firstChild);
        
        modal.style.display = 'none';
        announcementForm.reset();

        // Добавляем обработчики событий для новых кнопок редактирования/удаления
        setupAnnouncementActions(newAnnouncement);
    });

    // Функция для настройки обработчиков событий редактирования и удаления
    function setupAnnouncementActions(announcementCard) {
        const editBtn = announcementCard.querySelector('.edit-announcement');
        const deleteBtn = announcementCard.querySelector('.delete-announcement');
    
        editBtn.addEventListener('click', function() {
            const postId = announcementCard.dataset.postId;
            const userId = announcementCard.dataset.userId;
            const title = announcementCard.querySelector('.announcement-title').textContent;
            const content = announcementCard.querySelector('.announcement-content').textContent;
            const tag = announcementCard.querySelector('.announcement-tag').textContent;
        
            // Заполнение формы редактирования
            document.getElementById('editAnnouncementTitle').value = title;
            document.getElementById('editAnnouncementContent').value = content;
            document.getElementById('editAnnouncementCategory').value = tag;
        
            editModal.style.display = 'flex';
        
            editAnnouncementForm.onsubmit = function(event) {
                event.preventDefault();
        
                const newTitle = document.getElementById('editAnnouncementTitle').value;
                const newContent = document.getElementById('editAnnouncementContent').value;
                const newTag = document.getElementById('editAnnouncementCategory').value;
        
                const formData = new FormData();
                formData.append('action', 'edit');
                formData.append('post_id', postId);
                formData.append('editAnnouncementTitle', newTitle);
                formData.append('editAnnouncementContent', newContent);
                formData.append('editAnnouncementCategory', newTag);
        
                fetch(`/admin/account_main/${userId}/posts`, {  
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Ошибка при редактировании');
                        });
                    }
                })
                .then(data => {
                    // Обновление карточки объявления после успешного редактирования
                    announcementCard.querySelector('.announcement-title').textContent = newTitle;
                    announcementCard.querySelector('.announcement-content').textContent = newContent;
                    announcementCard.querySelector('.announcement-tag').textContent = newTag;
        
                    editModal.style.display = 'none';
                    // alert(data.message || 'Объявление успешно изменено');
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert(error.message || 'Не удалось изменить объявление. Попробуйте еще раз.');
                });
            };
        });
        deleteBtn.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите удалить это объявление?')) {
                const postId = announcementCard.dataset.postId; 
                const userId = announcementCard.dataset.userId; 
        
                fetch(`/admin/account_main/${userId}/posts/${postId}/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    // Сначала проверяем статус ответа
                    if (response.ok) {
                        return response.json(); // Получаем JSON, если ответ успешный
                    } else {
                        // Если ответ не успешный, возвращаем rejected промис
                        return response.json().then(data => {
                            throw new Error(data.error || 'Ошибка при удалении');
                        });
                    }
                })
                .then(data => {
                    // Успешное удаление
                    announcementCard.remove();
                    // alert(data.message || 'Объявление успешно удалено');
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert(error.message || 'Не удалось удалить объявление. Попробуйте еще раз.');
                });
            }
        });
    }
    document.querySelectorAll('.announcement-card').forEach(setupAnnouncementActions);
});