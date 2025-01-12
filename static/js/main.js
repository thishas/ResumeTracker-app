// Function to format contact information as clickable links
function formatContactInfo(contact) {
    if (!contact) return '';
    
    // Email
    contact = contact.replace(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi, '<a href="mailto:$1">$1</a>');
    
    // Phone numbers (various formats)
    contact = contact.replace(/(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}/g, function(match) {
        const cleanNumber = match.replace(/[^\d+]/g, '');
        return `<a href="tel:${cleanNumber}">${match}</a>`;
    });
    
    // URLs
    contact = contact.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    contact = contact.replace(/(?<!:\/\/)(www\.[^\s]+)/g, '<a href="http://$1" target="_blank">$1</a>');
    
    return contact;
}

let csrfToken = null;

// Function to get CSRF token
async function getCsrfToken() {
    try {
        const response = await fetch('/get_csrf_token');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        csrfToken = data.csrf_token;
        console.log('Got CSRF token:', csrfToken);
        return csrfToken;
    } catch (error) {
        console.error('Error getting CSRF token:', error);
        throw error;
    }
}

// Function to make a POST request with CSRF token
async function postWithCsrf(url, formData) {
    try {
        if (!csrfToken) {
            console.log('No CSRF token, getting one...');
            csrfToken = await getCsrfToken();
        }
        
        const headers = new Headers();
        headers.append('X-CSRF-Token', csrfToken);
        
        console.log('Making POST request to:', url);
        console.log('With CSRF token:', csrfToken);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    } catch (error) {
        console.error('Error in postWithCsrf:', error);
        throw error;
    }
}

// Function to refresh the submissions table
async function refreshTable() {
    try {
        console.log('Refreshing table...');
        const searchQuery = document.querySelector('input[type="text"]')?.value || '';
        const response = await fetch('/search?query=' + encodeURIComponent(searchQuery));
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Got submissions:', data);
        
        const tbody = document.querySelector('#submissionsTable');
        if (!tbody) {
            console.error('Submissions table not found');
            return;
        }
        
        tbody.innerHTML = '';
        data.forEach((submission, index) => {
            const tr = document.createElement('tr');
            tr.dataset.id = submission.id;
            
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${submission.submission_date}</td>
                <td>${submission.recruiter_firm}</td>
                <td>${submission.client_name}</td>
                <td>${submission.recruiter_name}</td>
                <td>${formatContactInfo(submission.recruiter_contact)}</td>
                <td>${submission.position}</td>
                <td>${submission.rate || ''}</td>
                <td>${submission.job_id}</td>
                <td>${submission.interview_date || ''}</td>
                <td>${submission.follow_up_date || ''}</td>
                <td>
                    <button class="btn btn-info btn-sm edit-btn" 
                            data-id="${submission.id}"
                            data-recruiter-firm="${submission.recruiter_firm}"
                            data-client-name="${submission.client_name}"
                            data-recruiter-name="${submission.recruiter_name}"
                            data-recruiter-contact="${submission.recruiter_contact}"
                            data-position="${submission.position}"
                            data-rate="${submission.rate || ''}"
                            data-job-id="${submission.job_id}"
                            data-submission-date="${submission.submission_date}"
                            data-interview-date="${submission.interview_date || ''}"
                            data-follow-up-date="${submission.follow_up_date || ''}"
                            data-notes="${submission.notes || ''}"
                            data-bs-toggle="modal" 
                            data-bs-target="#submissionModal">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-danger btn-sm delete-btn" data-id="${submission.id}">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            
            tbody.appendChild(tr);
        });
        
        // Reattach event listeners
        attachEventListeners();
        
    } catch (error) {
        console.error('Error refreshing table:', error);
    }
}

// Function to handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    try {
        console.log('Form submitted');
        const form = event.target;
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const modalElement = document.getElementById('submissionModal');
        
        submitButton.disabled = true;
        
        // Check if we're editing or adding
        const isEdit = form.getAttribute('data-editing') === 'true';
        const editId = form.getAttribute('data-edit-id');
        const url = isEdit ? `/edit/${editId}` : '/add';
        
        console.log('Submitting to:', url, 'isEdit:', isEdit, 'editId:', editId);
        const response = await postWithCsrf(url, formData);
        
        if (response.error) {
            throw new Error(response.error);
        }
        
        // Clear form and close modal
        form.reset();
        form.removeAttribute('data-editing');
        form.removeAttribute('data-edit-id');
        
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
        
        // Refresh the table
        await refreshTable();
        
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Error submitting form: ' + error.message);
    } finally {
        submitButton.disabled = false;
    }
}

// Function to handle deletion
async function handleDelete(id) {
    if (!confirm('Are you sure you want to delete this submission?')) {
        return;
    }
    
    try {
        console.log('Deleting submission:', id);
        const formData = new FormData();
        const response = await postWithCsrf(`/delete/${id}`, formData);
        
        if (response.status === 'success') {
            await refreshTable();
        } else {
            throw new Error(response.message || 'Error deleting submission');
        }
    } catch (error) {
        console.error('Error deleting submission:', error);
        alert('Error deleting submission: ' + error.message);
    }
}

// Function to attach event listeners
function attachEventListeners() {
    try {
        // Edit buttons
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Edit button clicked:', button.dataset);
                populateEditForm(button);
            });
        });
        
        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const id = button.closest('tr').dataset.id;
                handleDelete(id);
            });
        });
    } catch (error) {
        console.error('Error attaching event listeners:', error);
    }
}

// Function to populate the edit form
function populateEditForm(button) {
    try {
        const form = document.getElementById('submissionForm');
        if (!form) {
            console.error('Form not found');
            return;
        }
        
        // Get all data attributes from the button
        const data = {
            id: button.getAttribute('data-id'),
            recruiterFirm: button.getAttribute('data-recruiter-firm'),
            clientName: button.getAttribute('data-client-name'),
            recruiterName: button.getAttribute('data-recruiter-name'),
            recruiterContact: button.getAttribute('data-recruiter-contact'),
            submissionDate: button.getAttribute('data-submission-date'),
            position: button.getAttribute('data-position'),
            rate: button.getAttribute('data-rate'),
            jobId: button.getAttribute('data-job-id'),
            interviewDate: button.getAttribute('data-interview-date'),
            followUpDate: button.getAttribute('data-follow-up-date'),
            notes: button.getAttribute('data-notes')
        };
        
        console.log('Data from button:', data);
        
        // Set form to editing mode
        form.setAttribute('data-editing', 'true');
        form.setAttribute('data-edit-id', data.id);
        
        // Map form fields
        const fieldMap = {
            'recruiter_firm': data.recruiterFirm,
            'client_name': data.clientName,
            'recruiter_name': data.recruiterName,
            'recruiter_contact': data.recruiterContact,
            'submission_date': data.submissionDate,
            'position': data.position,
            'rate': data.rate,
            'job_id': data.jobId,
            'interview_date': data.interviewDate,
            'follow_up_date': data.followUpDate,
            'notes': data.notes
        };
        
        // Populate form fields
        Object.entries(fieldMap).forEach(([fieldName, value]) => {
            const field = form.elements[fieldName];
            if (field) {
                field.value = value || '';
                console.log(`Setting ${fieldName} to ${value || ''}`);
            }
        });
        
        // Update modal title
        const modalTitle = document.querySelector('#submissionModal .modal-title');
        if (modalTitle) {
            modalTitle.textContent = 'Edit Submission';
        }
        
    } catch (error) {
        console.error('Error populating form:', error);
        console.error('Button data attributes:', button.dataset);
        alert('An error occurred while loading the submission details');
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', async () => {
    try {
        console.log('Page loaded, initializing...');
        
        // Get initial CSRF token
        await getCsrfToken();
        
        // Initial table load
        await refreshTable();
        
        // Form submission handler
        const form = document.getElementById('submissionForm');
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
            console.log('Form handler attached');
        } else {
            console.error('Form not found');
        }
        
        // Search input handler
        const searchInput = document.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(searchInput.timer);
                searchInput.timer = setTimeout(refreshTable, 300);
            });
            console.log('Search handler attached');
        }
        
        // Modal reset handler
        const modal = document.getElementById('submissionModal');
        if (modal) {
            modal.addEventListener('hidden.bs.modal', () => {
                const form = document.getElementById('submissionForm');
                if (form) {
                    form.reset();
                    form.removeAttribute('data-editing');
                    form.removeAttribute('data-edit-id');
                    const modalTitle = modal.querySelector('.modal-title');
                    if (modalTitle) {
                        modalTitle.textContent = 'New Submission';
                    }
                }
            });
            console.log('Modal handler attached');
        }
        
    } catch (error) {
        console.error('Error initializing page:', error);
    }
});
