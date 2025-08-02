// Main JavaScript for Project Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-refresh data every 30 seconds if on project detail page
    if (window.location.pathname.includes('/project/')) {
        setInterval(function() {
            // Only refresh if no modals are open
            if (!document.querySelector('.modal.show')) {
                refreshProjectData();
            }
        }, 30000);
    }
});

// Utility functions
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
    }
}

function hideLoading(element) {
    if (element) {
        element.classList.remove('loading');
    }
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// API helper functions
async function apiCall(url, options = {}) {
    try {
        showLoading(document.body);
        
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    } finally {
        hideLoading(document.body);
    }
}

// Project management functions
async function createProject(name, description) {
    try {
        const result = await apiCall('/api/create_project', {
            method: 'POST',
            body: JSON.stringify({
                name: name,
                description: description
            })
        });
        
        showAlert(`Project "${name}" created successfully!`, 'success');
        return result;
    } catch (error) {
        showAlert(`Error creating project: ${error.message}`, 'danger');
        throw error;
    }
}

async function addTask(projectId, name, description, assignee) {
    try {
        const result = await apiCall(`/api/project/${projectId}/add_task`, {
            method: 'POST',
            body: JSON.stringify({
                name: name,
                description: description,
                assignee: assignee
            })
        });
        
        showAlert(`Task "${name}" added successfully!`, 'success');
        return result;
    } catch (error) {
        showAlert(`Error adding task: ${error.message}`, 'danger');
        throw error;
    }
}

async function completeTask(taskId) {
    try {
        const result = await apiCall(`/api/task/${taskId}/complete`, {
            method: 'POST'
        });
        
        showAlert(`Task completed successfully!`, 'success');
        return result;
    } catch (error) {
        showAlert(`Error completing task: ${error.message}`, 'danger');
        throw error;
    }
}

async function advanceStage(projectId) {
    try {
        const result = await apiCall(`/api/project/${projectId}/next_stage`, {
            method: 'POST'
        });
        
        if (result.success) {
            showAlert(result.message, 'success');
        } else {
            showAlert(result.message, 'warning');
        }
        
        return result;
    } catch (error) {
        showAlert(`Error advancing stage: ${error.message}`, 'danger');
        throw error;
    }
}

// Auto-refresh functionality
async function refreshProjectData() {
    try {
        // Get current project ID from URL
        const pathParts = window.location.pathname.split('/');
        const projectId = pathParts[pathParts.length - 1];
        
        if (!projectId || projectId === 'project') return;
        
        const projectData = await apiCall(`/api/project/${projectId}`);
        
        // Update progress bars
        updateProgressBars(projectData);
        
        // Update stage information
        updateStageInfo(projectData);
        
    } catch (error) {
        console.warn('Failed to refresh project data:', error);
    }
}

function updateProgressBars(projectData) {
    // Update overall progress
    const overallProgress = document.querySelector('.progress-bar');
    if (overallProgress) {
        const percentage = (projectData.progress * 100).toFixed(1);
        overallProgress.style.width = `${percentage}%`;
        overallProgress.setAttribute('aria-valuenow', percentage);
        overallProgress.textContent = `${percentage}%`;
    }
    
    // Update stage progress bars
    projectData.stages.forEach((stage, index) => {
        const stageProgress = document.querySelectorAll('.stage-card .progress-bar')[index];
        if (stageProgress) {
            const percentage = (stage.progress * 100).toFixed(1);
            stageProgress.style.width = `${percentage}%`;
        }
    });
}

function updateStageInfo(projectData) {
    // Update completed stages count
    const completedStagesEl = document.querySelector('h4.text-success');
    if (completedStagesEl) {
        const completedCount = projectData.stages.filter(s => s.status === 'completed').length;
        completedStagesEl.textContent = completedCount;
    }
    
    // Update total tasks count
    const totalTasksEl = completedStagesEl?.parentNode?.nextElementSibling?.querySelector('h4');
    if (totalTasksEl) {
        const totalTasks = projectData.stages.reduce((sum, stage) => sum + stage.task_count, 0);
        totalTasksEl.textContent = totalTasks;
    }
}

// Form validation helpers
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit forms in modals
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeModal = document.querySelector('.modal.show');
        if (activeModal) {
            const submitBtn = activeModal.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.click();
            }
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.show');
        if (activeModal) {
            const modal = bootstrap.Modal.getInstance(activeModal);
            if (modal) {
                modal.hide();
            }
        }
    }
});

// Export functions for global use
window.ProjectManager = {
    createProject,
    addTask,
    completeTask,
    advanceStage,
    refreshProjectData,
    showAlert,
    validateForm
};