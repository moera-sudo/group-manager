//headman
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.poll-tab');
    const infoSection = document.querySelector('.info-section');
    const loadSection = document.querySelector('.load-section');
    const studentsTable = document.getElementById("studentsTable");

    // Получаем JSON из метатега
    const groupListContent = document.querySelector('meta[name="group_list"]').getAttribute('content');

    // Парсим JSON в массив объектов
    const groupList = JSON.parse(groupListContent);
    const STUDENT_COUNT = groupList.length;

    
    function addStudent(index, name) {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        const row = tbody.insertRow();
        
        const cellNumber = row.insertCell(0);
        const cellName = row.insertCell(1);
        
        cellNumber.textContent = index;
        cellName.textContent = name;
    }
    
    function loadStudents() {
        const tbody = studentsTable.getElementsByTagName("tbody")[0];
        tbody.innerHTML = '';
        
        for(let i = 1; i <= STUDENT_COUNT; i++) {
            addStudent(i, groupList[i-1].student_fio)
        }
    }
    
    loadStudents();
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            
            this.classList.add('active');
            
            if (this.getAttribute('data-tab') === 'info') {
                infoSection.classList.add('active');
                loadSection.classList.remove('active');
            } else {
                infoSection.classList.remove('active');
                loadSection.classList.add('active');
            }
        });
    });

    document.querySelector('.custom-button').addEventListener('click', function() {
        alert('Экспорт данных...');
    });
});
