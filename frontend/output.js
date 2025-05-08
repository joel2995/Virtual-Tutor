document.addEventListener('DOMContentLoaded', function() {
    // Get measurements data from localStorage
    const measurementsData = JSON.parse(localStorage.getItem('measurementsData') || '{}');
    
    // Display measurements
    displayMeasurements(measurementsData);
    
    // Handle customization form submission
    const customizationForm = document.getElementById('customizationForm');
    const promptInput = document.getElementById('promptInput');
    const customizeBtn = document.getElementById('customizeBtn');
    const customizationLoading = document.getElementById('customizationLoading');
    
    // Add back to home button functionality
    const backToHomeLink = document.getElementById('backToHome');
    if (backToHomeLink) {
        backToHomeLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'index.html';
        });
    }
    
    customizationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a description of the dress you want');
            return;
        }
        
        // Show loading indicator
        customizationLoading.style.display = 'flex';
        customizeBtn.disabled = true;
        
        try {
            // Send customization request to backend
            const response = await fetch('http://localhost:5000/api/customize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    measurements: measurementsData,
                    prompt: prompt
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to process customization');
            }
            
            const data = await response.json();
            
            // Display fabric requirements
            displayFabricRequirements(data.stitchingInfo.fabricRequirements);
            
            // Display custom pattern measurements
            displayCustomPatternMeasurements(data.stitchingInfo.customMeasurements);
            
            // Display stitching process
            displayStitchingProcess(data.stitchingInfo.steps);
            
            // Display reference images if available
            if (data.relevantImages && data.relevantImages.length > 0) {
                displayReferenceImages(data.relevantImages);
                document.getElementById('imageResultsSection').style.display = 'block';
            }
            
            // Show all sections
            document.getElementById('fabricRequirementsSection').style.display = 'block';
            document.getElementById('customPatternSection').style.display = 'block';
            document.getElementById('stitchingProcessSection').style.display = 'block';
            
            // Scroll to fabric requirements section
            document.getElementById('fabricRequirementsSection').scrollIntoView({
                behavior: 'smooth'
            });
            
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to process customization. Please try again.');
        } finally {
            // Hide loading indicator
            customizationLoading.style.display = 'none';
            customizeBtn.disabled = false;
        }
    });
    
    // Helper functions for displaying data
    function displayMeasurements(measurements) {
        const measurementsContainer = document.getElementById('bodyMeasurements');
        if (!measurementsContainer) return;
        
        measurementsContainer.innerHTML = '';
        
        // Create a table for measurements
        const table = document.createElement('table');
        table.className = 'measurements-table';
        
        // Add table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const headerCell1 = document.createElement('th');
        headerCell1.textContent = 'Measurement';
        const headerCell2 = document.createElement('th');
        headerCell2.textContent = 'Value';
        headerRow.appendChild(headerCell1);
        headerRow.appendChild(headerCell2);
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Add table body
        const tbody = document.createElement('tbody');
        
        for (const [key, value] of Object.entries(measurements)) {
            const formattedKey = key
                .split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
                
            const row = document.createElement('tr');
            const keyCell = document.createElement('td');
            keyCell.textContent = formattedKey;
            const valueCell = document.createElement('td');
            valueCell.textContent = `${value} cm`;
            
            row.appendChild(keyCell);
            row.appendChild(valueCell);
            tbody.appendChild(row);
        }
        
        table.appendChild(tbody);
        measurementsContainer.appendChild(table);
    }
    
    function displayFabricRequirements(requirements) {
        const fabricRequirementsContainer = document.getElementById('fabricRequirements');
        if (!fabricRequirementsContainer) return;
        
        fabricRequirementsContainer.innerHTML = '';
        
        const requirementsP = document.createElement('p');
        requirementsP.textContent = requirements;
        fabricRequirementsContainer.appendChild(requirementsP);
    }
    
    function displayCustomPatternMeasurements(customMeasurements) {
        const customPatternContainer = document.getElementById('customPatternMeasurements');
        if (!customPatternContainer) return;
        
        customPatternContainer.innerHTML = '';
        
        const list = document.createElement('ul');
        list.className = 'custom-measurements-list';
        
        customMeasurements.forEach(measurement => {
            const item = document.createElement('li');
            item.textContent = measurement;
            list.appendChild(item);
        });
        
        customPatternContainer.appendChild(list);
    }
    
    function displayStitchingProcess(steps) {
        const stitchingProcessContainer = document.getElementById('stitchingProcess');
        if (!stitchingProcessContainer) return;
        
        stitchingProcessContainer.innerHTML = '';
        
        const list = document.createElement('ol');
        list.className = 'stitching-steps-list';
        
        steps.forEach(step => {
            const item = document.createElement('li');
            item.textContent = step;
            list.appendChild(item);
        });
        
        stitchingProcessContainer.appendChild(list);
    }
    
    function displayReferenceImages(images) {
        const imageResultsContainer = document.getElementById('imageResults');
        if (!imageResultsContainer) return;
        
        imageResultsContainer.innerHTML = '';
        
        // Use placeholder images for demonstration
        const placeholderImages = [
            'https://via.placeholder.com/300x400?text=Dress+Front+View',
            'https://via.placeholder.com/300x400?text=Dress+Back+View',
            'https://via.placeholder.com/300x400?text=Dress+Detail+View'
        ];
        
        images.forEach((image, index) => {
            // Create image card container
            const imageCard = document.createElement('div');
            imageCard.className = 'image-card';
            
            // Create image element with placeholder
            const imageElement = document.createElement('img');
            imageElement.className = 'reference-image';
            imageElement.src = placeholderImages[index % placeholderImages.length]; // Use placeholder images
            imageElement.alt = image.title || 'Reference Image';
            
            // Create image info section
            const imageInfo = document.createElement('div');
            imageInfo.className = 'image-info';
            
            // Add title
            const titleElement = document.createElement('h3');
            titleElement.className = 'image-title';
            titleElement.textContent = image.title || 'Reference Image';
            imageInfo.appendChild(titleElement);
            
            // Add source link if available
            if (image.sourceUrl) {
                const sourceLink = document.createElement('a');
                sourceLink.href = image.sourceUrl;
                sourceLink.className = 'image-source';
                sourceLink.textContent = 'View Source';
                sourceLink.target = '_blank';
                imageInfo.appendChild(sourceLink);
            }
            
            // Assemble the card
            imageCard.appendChild(imageElement);
            imageCard.appendChild(imageInfo);
            
            // Add to container
            imageResultsContainer.appendChild(imageCard);
        });
    }
});
