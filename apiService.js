export async function fetchPredefinedAPIs() {
    const API_LIST_URL = 'https://raw.githubusercontent.com/dimitriskleov/project-nexus-xi-apis/refs/heads/main/apis';
    
    try {
        const response = await fetch(API_LIST_URL);
        if (!response.ok) {
            throw new Error('Failed to fetch APIs');
        }
        const apiListText = await response.text();
        
        // Parse the text file into an array of API objects with improved name processing
        const apiEntries = apiListText.split('\n')
            .filter(line => line.trim() !== '') // Remove empty lines
            .map(line => {
                const [url, originalName = 'Unnamed API'] = line.split(',');
                
                // More robust name extraction
                const processedName = extractAPIName(url);
                
                return { 
                    url: url.trim(), 
                    name: processedName
                };
            });
        
        return apiEntries;
    } catch (error) {
        console.error('Error fetching APIs:', error);
        return [];
    }
}

function extractAPIName(url) {
    // Remove protocol (http:// or https://)
    let cleanUrl = url.replace(/^https?:\/\//, '');
    
    // Remove domain and path components
    const pathParts = cleanUrl.split('/').filter(part => part && part !== 'main' && part !== 'api');
    
    // Take the last meaningful part as the name
    return pathParts[pathParts.length - 1] || 'Unnamed API';
}

export async function getFullAPIURL(partialUrl) {
    const APIs = await fetchPredefinedAPIs();
    const matchedAPI = APIs.find(api => 
        api.url.includes(partialUrl) || partialUrl.includes(api.url)
    );
    return matchedAPI ? matchedAPI.url : partialUrl;
}