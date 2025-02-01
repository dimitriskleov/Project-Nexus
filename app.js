import { fetchPredefinedAPIs } from './apiService.js';
import { analyzeAPI } from './apiAnalyzer.js';
import { getFullAPIURL } from './apiService.js';

document.addEventListener('DOMContentLoaded', async () => {
    const apiUrlInput = document.getElementById('apiUrlInput');
    const apiSearchInput = document.getElementById('apiSearchInput');
    const exploreBtn = document.getElementById('exploreBtn');
    const apiResults = document.getElementById('apiResults');
    const apiList = document.getElementById('apiList');
    const warningModal = document.getElementById('warningModal');
    const warningText = document.getElementById('warningText');
    const closeBtn = document.querySelector('.close-btn');

    // Banned words list
    const bannedWords = ['pr0ject-nexus', 'pr0jectnexus', 'project-n3xus', 'project-nexus'];

    // Function to show warning modal
    function showWarning(message) {
        warningText.textContent = message;
        warningModal.style.display = 'block';
    }

    // Close modal when close button is clicked
    closeBtn.onclick = () => {
        warningModal.style.display = 'none';
    }

    // Close modal when clicking outside
    window.onclick = (event) => {
        if (event.target === warningModal) {
            warningModal.style.display = 'none';
        }
    }

    // Prevent typing banned words
    function preventBannedWords(input) {
        input.addEventListener('input', (e) => {
            const value = e.target.value.toLowerCase();
            if (bannedWords.some(word => value.includes(word))) {
                showWarning('Prohibited text detected!');
                e.target.value = '';
            }
        });
    }

    preventBannedWords(apiUrlInput);
    preventBannedWords(apiSearchInput);

    // Fetch and display predefined APIs
    let allApis = [];
    try {
        allApis = await fetchPredefinedAPIs();
        renderApiList(allApis);
    } catch (error) {
        console.error('Error fetching APIs:', error);
    }

    // Render API list with extended details
    async function renderApiList(apis) {
        apiList.innerHTML = '';
        for (const api of apis) {
            try {
                const apiAnalysis = await analyzeAPI(api.url);
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="api-details">
                        <span class="api-name">${api.name}</span>
                        <span class="api-status ${apiAnalysis.isFree ? 'free' : 'paid'}">
                            ${apiAnalysis.isFree ? 'Free' : 'Paid'}
                        </span>
                    </div>
                    <div class="api-url">${api.url}</div>
                    <div class="api-description">${apiAnalysis.description}</div>
                `;
                li.addEventListener('click', () => {
                    apiUrlInput.value = api.url;
                });
                apiList.appendChild(li);
            } catch (error) {
                console.error('Error analyzing API:', error);
            }
        }
    }

    // Search functionality
    apiSearchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredApis = allApis.filter(api => 
            api.name.toLowerCase().includes(searchTerm) || 
            api.url.toLowerCase().includes(searchTerm)
        );
        renderApiList(filteredApis);
    });

    // API Exploration Handler
    exploreBtn.addEventListener('click', async () => {
        const apiUrl = apiUrlInput.value.trim();
        if (!apiUrl) {
            apiResults.innerHTML = '<p>Please enter an API URL</p>';
            return;
        }

        try {
            // Get the full API URL
            const fullApiUrl = await getFullAPIURL(apiUrl);
            
            const apiAnalysis = await analyzeAPI(fullApiUrl);
            
            apiResults.innerHTML = `
                <h3>API Analysis</h3>
                <p><strong>Full URL:</strong> ${fullApiUrl}</p>
                <p><strong>Is Free:</strong> ${apiAnalysis.isFree ? 'Yes' : 'No'}</p>
                <p><strong>Description:</strong> ${apiAnalysis.description}</p>
            `;
        } catch (error) {
            apiResults.innerHTML = `<p>Error analyzing API: ${error.message}</p>`;
        }
    });
});