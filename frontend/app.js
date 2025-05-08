document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const photoInput = document.getElementById('photo');
    const filePreview = document.getElementById('filePreview');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    // Handle file preview
    photoInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                filePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <p>Click to change image</p>
                `;
            };
            
            reader.readAsDataURL(file);
        }
    });
    
    // Make the preview div clickable to trigger file input
    filePreview.addEventListener('click', function() {
        photoInput.click();
    });
    
    // Handle drag and drop
    filePreview.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.add('highlight');
    });
    
    filePreview.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.remove('highlight');
    });
    
    filePreview.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.remove('highlight');
        
        const dt = e.dataTransfer;
        const file = dt.files[0];
        
        if (file && file.type.match('image.*')) {
            photoInput.files = dt.files;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                filePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <p>Click to change image</p>
                `;
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!photoInput.files[0]) {
            alert('Please select an image first');
            return;
        }
        
        // Show loading indicator
        loadingIndicator.style.display = 'flex';
        submitBtn.disabled = true;
        
        const formData = new FormData();
        formData.append('image', photoInput.files[0]);
        
        try {
            // Send image to backend for processing
            const response = await fetch('http://localhost:5000/api/process-image', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to process image');
            }
            
            const data = await response.json();
            
            // Store measurements in localStorage for access on output.html
            localStorage.setItem('measurementsData', JSON.stringify(data.measurements));
            
            // Redirect to output.html
            window.location.href = 'output.html';
            
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to process image. Please try again.');
        } finally {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});
