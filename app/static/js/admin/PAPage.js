document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.poll-tab');
    const studSection = document.getElementById('student-section');
    const familySection = document.querySelector('.family-section');
    const familySectionMum = document.querySelector('.mum-section');
    const familySectionDad = document.querySelector('.dad-section');
    const familySectionGuardian = document.querySelector('.guardian-section');
    const adressSection = document.querySelector('.adress-section');
    const adressSectionCameFrom = document.querySelector('.cameFrom-section');
    const adressSectionRegPlace = document.querySelector('.regPlace-section');
    const adressSectionLivPLace = document.querySelector('.livPlace-section');
    const currentUserId = document.querySelector('meta[name="user-id"]').getAttribute('content');
    let isEditModeStud = false;
    let isEditModeFamilyMum = false;
    let isEditModeFamilyDad = false;
    let isEditModeFamilyGuardian = false;
    let isEditModeAdressCameFrom = false;
    let isEditModeAdressRegPlace = false;
    let isEditModeAdressLivPlace = false;

    function setupCitizenshipRealTimeCheck() {
        const hiddenFields = document.querySelectorAll(" #studentcategory");
        const nationalityElement = document.getElementById('citizenchip');
        const FamilyStat = document.querySelectorAll(" #familystatus");
        
        if (nationalityElement) {
            nationalityElement.addEventListener('input', function() {
                const registrationBlock = document.querySelectorAll('.profile-detail-reg');
                if (registrationBlock) {
                    const citizenshipValue = nationalityElement.value.trim().toLowerCase();
                    
                    if (citizenshipValue !== 'казахстан') {
                        registrationBlock.forEach(value => {
                            value.style.display = 'flex';
                        });
                    } else {
                        registrationBlock.forEach(value => {
                            value.style.display = 'none';
                        });
                    }
                }
            });
        }
        
        const studentRequireSelect = document.getElementById("studentrequire");
        studentRequireSelect.addEventListener('change', function() {
            if (hiddenFields) {
                if (this.value === 'Присутствуют') {
                    hiddenFields.forEach(field => {
                        field.style.display = 'flex';
                    });
                } else {
                    hiddenFields.forEach(field => {
                        field.style.display = 'none';
                    });
                }
            }
        });
        
        const StatFamilySelect = document.getElementById("selectfamilystat");
        StatFamilySelect.addEventListener('change', function() {
            if (FamilyStat) {
                if (this.value === 'Неполная семья') {
                    FamilyStat.forEach(field => {
                        field.style.display = 'flex';
                    });
                } else {
                    FamilyStat.forEach(field => {
                        field.style.display = 'none';
                    });
                }
            }
        });
    }
    function validateIntegerField(input, fieldName) {
        const value = input.value.trim();
        if (!Number.isInteger(Number(value)) || value.includes('.') || value.includes(',')) {
            alert(`${fieldName} должно быть целым числом`);
            input.value = '';
            return false;
        }
        const numValue = parseInt(value);
        if (numValue < 0) {
            alert(`${fieldName} не может быть отрицательным`);
            input.value = '';
            return false;
        }
        input.value = numValue;
        return true;
    }

    function setupAddressValidations(section) {
        const integerInputs = {
            'flat': 'Номер квартиры',
            'floor': 'Этаж',
            'entrance': 'Подъезд'
        };

        Object.entries(integerInputs).forEach(([field, label]) => {
            const inputs = section.querySelectorAll(`input[name$="-${field}"]`);
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    this.value = this.value.replace(/[^\d]/g, '');
                });

                input.addEventListener('blur', function() {
                    if (this.value) {
                        validateIntegerField(this, label);
                    }
                });
            });
        });
    }
    
    function validateChildCount(input) {
        const value = input.value.trim();
        if (!Number.isInteger(Number(value)) || value.includes('.') || value.includes(',')) {
            alert('Количество детей должно быть целым числом');
            input.value = '';
            return false;
        }
        const numValue = parseInt(value);
        if (numValue < 0) {
            alert('Количество детей не может быть отрицательным');
            input.value = '';
            return false;
        }
        input.value = numValue;
        return true;
    }
    function validatePhoneNumber(input) {
        const phoneRegex = /^\+77\d{9}$/;
        if (!phoneRegex.test(input.value)) {
            alert('Номер телефона должен начинаться с +77 и содержать 11 цифр');
            input.value = '';
            return false;
        }
        return true;
    }

    function validateIIN(input) {
        if (input.value.length !== 12) {
            alert('ИИН должен состоять из 12 символов');
            input.value = '';
            return false;
        }
        return true;
    }

    function validateBirthdate(input) {
        const selectedDate = new Date(input.value);
        const maxDate = new Date('2024-01-01');
        const minDate = new Date('1924-01-01');

        if (selectedDate > maxDate) {
            alert('Дата рождения не может быть позже 01.01.2024');
            input.value = '';
            return false;
        }
        if (selectedDate < minDate) {
            alert('Дата рождения не может быть раньше 01.01.1924');
            input.value = '';
            return false;
        }
        return true;
    }

    function setupValidations(section) {
        const phoneInputs = section.querySelectorAll('input[name$="phone_number"], input[name="phonenumber"]');
        phoneInputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value) {
                    validatePhoneNumber(this);
                }
            });
        });

        const iinInput = section.querySelector('input[name="iin"]');
        if (iinInput) {
            iinInput.addEventListener('blur', function() {
                validateIIN(this);
            });
        }

        const birthdayInputs = section.querySelectorAll('input[name$="birthday"]');
        birthdayInputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value) {
                    validateBirthdate(this);
                }
            });
        });

        const childCountInput = section.querySelector('input[name="childs_count"]');
        if (childCountInput) {
            childCountInput.addEventListener('blur', function() {
                if (this.value) {
                    validateChildCount(this);
                }
            });
            childCountInput.addEventListener('input', function() {
                this.value = this.value.replace(/[^\d]/g, '');
            });
        }
        setupAddressValidations(section);
    }

    document.querySelector('form').addEventListener('submit', function(event) {
        const formData = new FormData(event.target);
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }
    });

    function toggleEditMode(section, isEditMode) {
        const detailValues = section.querySelectorAll('.edit-input');
        const editButton = section.querySelector('.custom-button');
        const form = section.querySelector('form');
        const select = section.querySelectorAll('select');
        const selection = section.querySelector('.type-selection')
        
        

        if (!isEditMode) {
            select.forEach(sel=>{
                sel.className = 'type-select'
            })
            detailValues.forEach(value => {
                value.disabled = false;
            });
            if (section.classList.contains('mum-section') || section.classList.contains('dad-section') || section.classList.contains('guardian-section')) {
                const parentTypeSelect = selection.querySelector('select')
                if (parentTypeSelect) {
                    parentTypeSelect.addEventListener('change', handleParentTypeChange);
                }
            }
            
            setupValidations(section);
            setupCitizenshipRealTimeCheck(); 
            editButton.textContent = 'Сохранить';
            editButton.type = 'submit';

            return true;
        } else {

            editButton.textContent = 'Редактировать';
            editButton.removeAttribute('type');
            form.onsubmit = 'event.preventDefault();'
            return false;
        }
    }
    function handleParentTypeChange(event) {
        const parentDetails = event.target.closest('.type-selection').nextElementSibling;
        if (event.target.value === 'Нету') {
            parentDetails.style.display = 'none';
        } else {
            parentDetails.style.display = 'block';
        }
    }
    
    const editButtons = document.querySelectorAll('.custom-button');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.closest('section');
            
            if (section.classList.contains('stud-section')) {
                isEditModeStud = toggleEditMode(section, isEditModeStud);
            } else if (section.classList.contains('mum-section')) {
                isEditModeFamilyMum = toggleEditMode(section, isEditModeFamilyMum);
            } else if (section.classList.contains('dad-section')) {
                isEditModeFamilyDad = toggleEditMode(section, isEditModeFamilyDad);
            } else if (section.classList.contains('guardian-section')) {
                isEditModeFamilyGuardian = toggleEditMode(section, isEditModeFamilyGuardian);
            } else if (section.classList.contains('cameFrom-section')) {
                isEditModeAdressCameFrom = toggleEditMode(section, isEditModeAdressCameFrom);
            } else if (section.classList.contains('regPlace-section')) {
                isEditModeAdressRegPlace = toggleEditMode(section, isEditModeAdressRegPlace);
            } else if (section.classList.contains('livPlace-section')) {
                isEditModeAdressLivPlace = toggleEditMode(section, isEditModeAdressLivPlace);
            } 
        });
    });

    document.querySelectorAll('.type-select').forEach(select => {        
        const parentDetails = select.closest('.type-selection').nextElementSibling;
        if (select.value === 'Нету') {
            parentDetails.style.display = 'none';
        } else {
            parentDetails.style.display = 'block';
        }
    });
});