document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.poll-tab');
    const infoSection = document.querySelector('.info-section');
    const loadSection = document.querySelector('.load-section');
    const studentsTable = document.getElementById("studentsTable");
    const groupTagSelect = document.getElementById("GroupTag");
    const editTableButton = document.createElement('button');
    editTableButton.textContent = 'Редактировать таблицу';
    editTableButton.classList.add('edit-table-btn');
    const groupSelect = document.getElementById('GroupTag');
    const currentUserId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    

    
    // Parse group list from meta tag
    const groupListContent = document.querySelector('meta[name="group_list"]').getAttribute('content');
    const groupList = JSON.parse(groupListContent);
    const STUDENT_COUNT = groupList.length;
    
    // URL handling for group selection
    const urlParams = new URLSearchParams(window.location.search);
    const groupParam = urlParams.get('group');
    if (groupParam) {
        groupSelect.value = groupParam;
    }
    

    groupSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('group', selectedValue);
        window.location.href = currentUrl.toString();
    });

    let isEditMode = false;
    

    studentsTable.parentNode.insertBefore(editTableButton, studentsTable.nextSibling);

    function updateRowNumbers() {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        const rows = tbody.rows;
        for (let i = 0; i < rows.length; i++) {
            rows[i].cells[0].textContent = i + 1;
        }
    }

    function addRow(studentName = '') {
        const table = studentsTable.getElementsByTagName("tbody")[0];
        const newRow = table.insertRow();
    
        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);
    
        cell1.textContent = table.rows.length;
        cell2.textContent = studentName;
        cell2.setAttribute('contenteditable', 'false');
        
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '✖';
        deleteBtn.classList.add('delete-row-btn');
        deleteBtn.style.display = 'none';
        
        deleteBtn.addEventListener('click', async function() {
            const studentName = cell2.textContent;
            try {
                const response = await fetch(`/admin/account_main/${currentUserId}/group/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        studentName: studentName,
                        groupId: groupSelect.value
                    })
                });
                
                if (response.ok) {
                    table.deleteRow(newRow.rowIndex - 1);
                    updateRowNumbers();
                } else {
                    alert('Ошибка при удалении студента');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Ошибка при удалении студента');
            }
        });
        
        cell3.appendChild(deleteBtn);
    }

    function populateTable() {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        tbody.innerHTML = '';

        groupList.forEach((student, index) => {
            addRow(student.student_fio);
        });
        
        studentsTable.style.display = 'table';
        loadSection.classList.add('active');
    }
    
    const addRowBtn = document.createElement('button');
    addRowBtn.textContent = 'Добавить студента';
    addRowBtn.classList.add('add-row-btn');
    addRowBtn.style.display = 'none';
    addRowBtn.addEventListener('click', async function() {
        const newStudentName = prompt('Введите ФИО студента:');
        if (newStudentName) {
            try {
                const response = await fetch(`/admin/account_main/${currentUserId}/group/add`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        studentName: newStudentName,
                        groupId: groupSelect.value
                    })
                });
                
                if (response.ok) {
                    addRow(newStudentName);
                    editTable();

                } else {
                    alert('Ошибка при добавлении студента');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Ошибка при добавлении студента');
            }
        }
    });
    studentsTable.parentNode.insertBefore(addRowBtn, studentsTable.nextSibling);

    function removeEmptyRows() {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        const rows = tbody.rows;
        
        for (let i = rows.length - 1; i >= 0; i--) {
            const studentCell = rows[i].cells[1];
            const studentText = studentCell.textContent.trim();
            if (studentText === '') {
                tbody.deleteRow(i);
            }
        }
        updateRowNumbers();
    }

    function editTable() {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        const rows = tbody.rows;
        
        if (!isEditMode) {
            removeEmptyRows();
            if (rows.length < 1) {
                addRow();
            }
        }
        
        const deleteButtons = studentsTable.querySelectorAll('.delete-row-btn');
        deleteButtons.forEach(btn => {
            btn.style.display = isEditMode ? 'inline-block' : 'none';
        });
        
        for (let i = 0; i < rows.length; i++) {
            const studentCell = rows[i].cells[1];
            studentCell.setAttribute('contenteditable', isEditMode);
            studentCell.style.backgroundColor = isEditMode ? '#f0f0f0' : 'transparent';
        }
        
        addRowBtn.style.display = isEditMode ? 'inline-block' : 'none';
        editTableButton.textContent = isEditMode ? 'Завершить редактирование' : 'Редактировать таблицу';
    }

    editTableButton.addEventListener('click', function() {
        if (isEditMode)[location.reload()]
        isEditMode = !isEditMode;
        editTable();
        
    });
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            if (this.getAttribute('data-tab') === 'info') {
                infoSection.classList.add('active');
                studentsTable.style.display = 'none';
                loadSection.classList.remove('active');
            } else {
                infoSection.classList.remove('active');
            }

            if (this.getAttribute('data-tab') === 'load') {
                populateTable();
            } else {
                loadSection.classList.remove('active');
                studentsTable.style.display = 'none';
            }
        });
    });

    const initialActiveTab = document.querySelector('.poll-tab.active');
    if (initialActiveTab && initialActiveTab.getAttribute('data-tab') === 'load') {
        populateTable();
    }

    document.addEventListener('DOMContentLoaded', function() {
        
        const editInfoButton = document.getElementById('editInfoButton');
        const saveInfoButton = document.getElementById('saveInfoButton');
        const cancelEditButton = document.getElementById('cancelEditButton');
        
        const curatorName = document.getElementById('curatorName');
        const curatorNameEdit = document.getElementById('curatorNameEdit');
        
        const headmanName = document.getElementById('headmanName');
        const headmanNameEdit = document.getElementById('headmanNameEdit');
        
        const editControls = document.querySelector('.edit-controls');
        const from = document.getElementById('form2')
        

        editInfoButton.addEventListener('click', function(event) {
            event.preventDefault();
            curatorNameEdit.value = curatorName.textContent;
            headmanNameEdit.value = headmanName.textContent;

            curatorName.style.display = 'none';
            headmanName.style.display = 'none';
            curatorNameEdit.style.display = 'inline-block';
            headmanNameEdit.style.display = 'inline-block';

            editInfoButton.style.display = 'none';
            editControls.style.display = 'block';

            from.removeAttribute('onsubmit')

        });

        saveInfoButton.addEventListener('click', function() {
            curatorName.textContent = curatorNameEdit.value;
            headmanName.textContent = headmanNameEdit.value;

            curatorName.style.display = 'inline-block';
            headmanName.style.display = 'inline-block';
            curatorNameEdit.style.display = 'none';
            headmanNameEdit.style.display = 'none';

            editInfoButton.style.display = 'block';
            editControls.style.display = 'none';


        });

        cancelEditButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            curatorName.style.display = 'inline-block';
            headmanName.style.display = 'inline-block';
            curatorNameEdit.style.display = 'none';
            headmanNameEdit.style.display = 'none';

            editInfoButton.style.display = 'block';
            editControls.style.display = 'none';
        });
    });

    const editInfoButton = document.getElementById('editInfoButton');
    const saveInfoButton = document.getElementById('saveInfoButton');
    const cancelEditButton = document.getElementById('cancelEditButton');
    
    const curatorName = document.getElementById('curatorName');
    const curatorNameEdit = document.getElementById('curatorNameEdit');
    
    const headmanName = document.getElementById('headmanName');
    const headmanNameEdit = document.getElementById('headmanNameEdit');
    
    const editControls = document.querySelector('.edit-controls');

    editInfoButton.addEventListener('click', function() {
        curatorNameEdit.value = curatorName.textContent;
        headmanNameEdit.value = headmanName.textContent;

        curatorName.style.display = 'none';
        headmanName.style.display = 'none';
        curatorNameEdit.style.display = 'inline-block';
        headmanNameEdit.style.display = 'inline-block';

        editInfoButton.style.display = 'none';
        editControls.style.display = 'block';
    });

    saveInfoButton.addEventListener('click', function() {
        curatorName.textContent = curatorNameEdit.value;
        headmanName.textContent = headmanNameEdit.value;

        curatorName.style.display = 'inline-block';
        headmanName.style.display = 'inline-block';
        curatorNameEdit.style.display = 'none';
        headmanNameEdit.style.display = 'none';

        editInfoButton.style.display = 'block';
        editControls.style.display = 'none';

    });

    cancelEditButton.addEventListener('click', function() {
        curatorName.style.display = 'inline-block';
        headmanName.style.display = 'inline-block';
        curatorNameEdit.style.display = 'none';
        headmanNameEdit.style.display = 'none';

        editInfoButton.style.display = 'block';
        editControls.style.display = 'none';
    });
});